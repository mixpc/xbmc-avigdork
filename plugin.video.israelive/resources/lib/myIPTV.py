# -*- coding: utf-8 -*-
import urllib, re, os, shutil, threading, urllib2, gzip, json, time, datetime
from StringIO import StringIO
import xbmc, xbmcaddon
import common, UA
try:
	from dateutil import tz
	isDateutil = True
except:
	isDateutil = False

AddonID = "plugin.video.israelive"
Addon = xbmcaddon.Addon(AddonID)
AddonName = Addon.getAddonInfo("name")
localizedString = Addon.getLocalizedString
KodiPlayer = Addon.getSetting("dynamicPlayer") == "1"
if not KodiPlayer:
	try:
		import myResolver
	except:
		myResolver = None
user_dataDir = xbmc.translatePath(Addon.getAddonInfo("profile")).decode("utf-8")

def makeIPTVlist(iptvFile):
	iptvType = GetIptvType()
	iptvList = '#EXTM3U\n'
	
	channelsList = GetIptvChannels()
	portNum = common.GetLivestreamerPort()
	hostName = '127.0.0.1'
		
	for item in channelsList:
		try:
			tvg_id = item["tvg"]
			view_name = item['name']
			tvg_logo = item['image'] if iptvType > 1 else common.GetLogoFileName(item)
			if iptvType == 0:
				tvg_logo = tvg_logo[:tvg_logo.rfind('.')]
			radio = ' radio="true"' if item['type'].lower() == "audio" else ''
			group = ' group-title="{0}"'.format(item['group']) if item.has_key('group') else ''

			url = item['url']
			if "mode=" in url:
				if KodiPlayer:
					url = "http://{0}:{1}/?url=plugin://plugin.video.israelive/&channelid={2}".format(hostName, portNum, item['id'])
					if item.get('catid') == 'Favourites':
						url += '&mode=11'
					else:
						url += '&mode=10'
				else:
					regex = re.compile('[\?|&]mode=(\-?[0-9]+)', re.I+re.M+re.U+re.S)
					matches = regex.findall(url)
					if len(matches) > 0:
						url = regex.sub('', url).strip()
						mode = matches[0]
						if myResolver is not None and (mode == '-3' or mode == '0' or mode == '16' or mode == '34'):
							url = myResolver.Resolve(url, mode)
							if url is None:
								continue
						elif mode == '13':
							continue
						else:
							url = "http://{0}:{1}/?url={2}&mode={3}".format(hostName, portNum, urllib.quote(url.replace('?', '&')), mode)
			iptvList += '\n#EXTINF:-1 tvg-id="{0}"{1} tvg-logo="{2}"{3},{4}\n{5}\n'.format(tvg_id, group, tvg_logo, radio, view_name, url)
		except Exception as ex:
			xbmc.log("{0}".format(ex), 3)

	with open(iptvFile, 'w') as f:
		f.write(iptvList)
	
def EscapeXML(str):
	return str.replace('&', '&amp;').replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;").replace("'", "&#39;")
	
def UnEscapeXML(str):
	return str.replace('&amp;', '&').replace("&lt;", "<").replace("&gt;", ">").replace("&quot;", '"').replace("&#39;", "'")
	
def GetTZtime(timestamp):
	timeStr = ""
	if isDateutil:
		from_zone = tz.tzutc()
		to_zone = tz.tzlocal()
		utc = datetime.datetime.utcfromtimestamp(timestamp)
		utc = utc.replace(tzinfo=from_zone)
		local_time = utc.astimezone(to_zone)
		timeStr = local_time.strftime('%Y%m%d%H%M%S %z')
	else:
		ts = time.time()
		delta = (datetime.datetime.fromtimestamp(ts) - datetime.datetime.utcfromtimestamp(ts))
		hrs = "+0000"
		if delta > datetime.timedelta(0):
			hrs = "+{0:02d}{1:02d}".format(delta.seconds//3600, (delta.seconds//60)%60)
		else:
			delta = -delta
			hrs = "-{0:02d}{1:02d}".format(delta.seconds//3600, (delta.seconds//60)%60)
		timeStr = "{0} {1}".format(time.strftime('%Y%m%d%H%M%S', time.localtime(timestamp)), hrs)
	return timeStr
	
def MakeChannelsGuide(fullGuideFile, iptvGuideFile):
	FullGuideList = GetIptvGuide()
	#if len(FullGuideList) == 0:
	#	return

	channelsList = ""
	programmeList = ""
	for channel in FullGuideList:
		chName = channel["channel"].encode("utf-8")
		channelsList += "\t<channel id=\"{0}\">\n\t\t<display-name>{1}</display-name>\n\t</channel>\n".format(EscapeXML(chName), chName)
		for programme in channel["tvGuide"]:
			start = GetTZtime(programme["start"])
			end = GetTZtime(programme["end"])
			name = EscapeXML(programme["name"].encode("utf-8")) if programme["name"] != None else ""
			description = EscapeXML(programme["description"].encode("utf-8")) if programme["description"] != None else ""
			programmeList += "\t<programme start=\"{0}\" stop=\"{1}\" channel=\"{2}\">\n\t\t<title>{3}</title>\n\t\t<desc>{4}</desc>\n\t</programme>\n".format(start, end, EscapeXML(chName), name, description)
	xmlList = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<tv>\n{0}{1}</tv>".format(channelsList, programmeList)
	with open(iptvGuideFile, 'w') as f:
		f.write(xmlList)
	
def SaveChannelsLogos(logosDir):
	if not os.path.exists(logosDir):
		os.makedirs(logosDir)
	
	forcePng = GetIptvType() == 0
	ua = UA.GetUA()
	newFilesList = []
	channelsList = GetIptvChannels()
	
	for channel in channelsList:
		try:
			logoFile = common.GetLogoFileName(channel)
			if logoFile != "":
				if forcePng:
					logoFile = '{0}.png'.format(logoFile[:logoFile.rfind('.')])
				newFilesList.append(logoFile)
				logoFile = os.path.join(logosDir, logoFile)
				if not os.path.isfile(logoFile):
					logo = channel['image']
					if logo.startswith('http'):
						threading.Thread(target=SaveChannelBackground, args=(logo, logoFile, ua, )).start()
					else:
						shutil.copyfile(logo, logoFile)
		except Exception as ex:
			xbmc.log("{0}".format(ex), 3)
	
	for the_file in os.listdir(logosDir):
		file_path = os.path.join(logosDir, the_file)
		try:
			if os.path.isfile(file_path) and the_file not in newFilesList:
				os.unlink(file_path)
		except Exception as ex:
			xbmc.log("{0}".format(ex), 3)

def SaveChannelBackground(logoUrl, logoFile, ua):
	try:
		req = urllib2.Request(logoUrl)
		req.add_header('User-Agent', ua)
		req.add_header('Accept-encoding', 'gzip')
		response = urllib2.urlopen(req,timeout=100)
		if response.info().get('Content-Encoding') == 'gzip':
			buf = StringIO(response.read())
			f = gzip.GzipFile(fileobj=buf)
			data = f.read()
		else:
			data = response.read()
		response.close()
	except:
		return
	with open(logoFile, 'wb') as f:
		f.write(data)

def EnableIptvClient():
	try:
		if not json.loads(xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Addons.GetAddonDetails","params":{"addonid":"pvr.iptvsimple", "properties": ["enabled"]},"id":1}'))['result']['addon']['enabled']:
			xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","params":{"addonid":"pvr.iptvsimple","enabled":true},"id":1}')
			return True
	except:
		pass
	return False

def EnablePVR():
	try:
		if not json.loads(xbmc.executeJSONRPC('{"jsonrpc":"2.0", "method":"Settings.GetSettingValue", "params":{"setting":"pvrmanager.enabled"},"id":1}'))['result']['value']:
			xbmc.executeJSONRPC('{"jsonrpc":"2.0", "method":"Settings.SetSettingValue", "params":{"setting":"pvrmanager.enabled", "value":true},"id":1}')
			return True
	except:
		pass
	return False

def GetIptvAddon():
	iptvAddon = None
	if xbmc.getCondVisibility("System.HasAddon(pvr.iptvsimple)"):
		try:
			iptvAddon = xbmcaddon.Addon("pvr.iptvsimple")
		except:
			pass
	else:
		if EnableIptvClient():
			iptvAddon = xbmcaddon.Addon("pvr.iptvsimple")

	if iptvAddon is None:
		import platform
		xbmc.log("---- {0} ----\nIPTVSimple addon is disable.".format(AddonName), 2)
		xbmc.log("---- {0} ----\nosType: {1}\nosVer: {2}\nxbmcVer: {3}".format(AddonName, platform.system(), platform.release(), xbmc.getInfoLabel( "System.BuildVersion" )), 2)
	return iptvAddon

def GetIptvType():
	try:
		ver = xbmcaddon.Addon("pvr.iptvsimple").getAddonInfo('version').split('.')
		ver1 = int(ver[0])
		ver2 = int(ver[1])
		ver3 = int(ver[2])
		if ver1 < 1 or (ver1 == 1 and (ver2 < 9 or (ver2 == 9 and ver3 < 3))):
			v = 0
		elif ver1 == 1 and ver2 < 11:
			v = 1
		else:
			v = 2
		return v
	except:
		return 2

def UpdateIPTVSimpleSettings(m3uPath, epgPath, logoPath):
	iptvSettingsFile = os.path.join(xbmc.translatePath("special://profile").decode("utf-8"), "addon_data", "pvr.iptvsimple", "settings.xml")
	iptvAddon = GetIptvAddon()
	
	if not os.path.isfile(iptvSettingsFile):
		if iptvAddon is None:
			return False
		iptvAddon.setSetting("epgPathType", "0") # make 'settings.xml' in 'userdata/addon_data/pvr.iptvsimple' folder
	
	oldIptv = GetIptvType() < 2

	dict = {
		"m3uPathType": "0",
		"m3uPath": m3uPath,
		"epgPathType": "0",
		"epgPath": epgPath
	}
	if oldIptv:
		dict["logoPathType"] = "0"
		dict["logoPath"] = logoPath
	else:
		dict["logoPathType"] = "1"
		dict["logoBaseUrl"] = ""
	
	with open(iptvSettingsFile, 'r') as f:
		xml = f.read()
		
	isSettingsChanged = False
	# make changes
	for k, v in dict.iteritems():
		if common.GetKodiVer() >= 18:
			matches = re.compile('<(.*?)>(.*?)</{0}>'.format(k)).findall(xml)
			if len(matches) > 0 and matches[0][1] != v:
				xml = xml.replace('<{0}>{1}</{2}>'.format(matches[0][0], matches[0][1], k), '<{0}>{1}</{2}>'.format(matches[0][0], v, k))
				isSettingsChanged = True
		else:
			matches = re.compile('<setting\s*id="{0}"\s*value="(.*?)"\s*?/>'.format(k)).findall(xml)
			if len(matches) > 0 and matches[0] != v:
				xml = xml.replace('<setting id="{0}" value="{1}" />'.format(k, matches[0]), '<setting id="{0}" value="{1}" />'.format(k, v))
				isSettingsChanged = True
	if not isSettingsChanged:
		return True

	# write updates back to settings.xml
	with open(iptvSettingsFile, 'w') as f:
		f.write(xml)
	return True

def RefreshPVR(m3uPath, epgPath, logoPath, forceUpdate=False, forceUpdateIPTV=False):
	if forceUpdateIPTV or common.getAutoIPTV():
		UpdateIPTVSimpleSettings(m3uPath, epgPath, logoPath)
	kodi16 = True if common.GetKodiVer() < 17 else False
	if Addon.getSetting("autoPVR") == "true":
		if (not json.loads(xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Addons.GetAddonDetails","params":{"addonid":"pvr.iptvsimple", "properties": ["enabled"]},"id":1}'))['result']['addon']['enabled'] or (kodi16 and not json.loads(xbmc.executeJSONRPC('{"jsonrpc":"2.0", "method":"Settings.GetSettingValue", "params":{"setting":"pvrmanager.enabled"},"id":1}'))['result']['value'])):
			tvOption = common.GetMenuSelected(localizedString(30317).encode('utf-8'), [localizedString(30318).encode('utf-8'), localizedString(30319).encode('utf-8')])
			if tvOption != 0:
				if tvOption == 1:
					Addon.setSetting("useIPTV", "False")
				return False
		isIPTVnotRestarted = not EnableIptvClient() and not kodi16
		isPVRnotRestarted = kodi16 and not EnablePVR()
		if isIPTVnotRestarted and forceUpdate:
			xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","params":{"addonid":"pvr.iptvsimple","enabled":false},"id":1}')
			xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","params":{"addonid":"pvr.iptvsimple","enabled":true},"id":1}')
			#iptvAddon = GetIptvAddon()
			#if iptvAddon is None:
			#	return False
			#iptvAddon.setSetting("m3uPathType", iptvAddon.getSetting("m3uPathType"))
		if isPVRnotRestarted:
			xbmc.executebuiltin('StopPVRManager')
			xbmc.executebuiltin('StartPVRManager')
		return True
	else:
		return False
		
def GetCategories():
	iptvList = int(Addon.getSetting("iptvList"))
	if iptvList == 0:
		categories = [{"id": "Favourites"}]
	elif iptvList == 1:
		categories = common.GetChannels('categories')
	elif iptvList == 2:
		categories = common.GetChannels('selectedCategories')
	return categories
		
def GetIptvChannels():
	allCategories = common.GetChannels('categories')
	categories = GetCategories()
	channelsList = []
	for category in categories:
		if category.get('type', '') == "ignore":
			continue
		channels = common.GetChannels(category["id"]) if category["id"] != "Favourites" else common.ReadList(os.path.join(user_dataDir, 'favorites.txt'))
		ind = -1
		for channel in channels:
			ind += 1
			if channel["type"] == 'video' or channel["type"] == 'audio':
				try:
					channelName = common.GetUnColor(channel['name'].encode("utf-8"))
					tvg_id = common.GetUnColor(channel.get("tvg", channel["name"]).encode("utf-8"))
					
					if category["id"] == "Favourites":
						gp = [x["name"] for x in allCategories if x["id"] == channel.get("group", "")]
						groupName = gp[0] if len(gp) > 0 else 'Favourites'
						channelID = ind
					else:
						groupName = category['name']
						channelID = channel['id']
							
					data = {'name': channelName, 'tvg': tvg_id, 'url': channel['url'], 'image': channel['image'], 'type': channel['type'], 'group': groupName.encode("utf-8"), 'id': channelID, 'catid': category["id"]}
					channelsList.append(data)
				except Exception, e:
					pass
					
	return channelsList
	
def GetIptvGuide():
	categories = GetCategories()
	epg = []
	for category in categories:
		channels = common.GetGuide(category["id"])		
		for channel in channels:
			try:
				if not any(channel["channel"] == d.get('channel', '') for d in epg):
					epg.append(channel)
			except Exception, e:
				pass
					
	return epg
