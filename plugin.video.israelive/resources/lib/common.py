# -*- coding: utf-8 -*-
import os, io, re, hashlib, urllib2, json, shutil
import xbmc, xbmcgui, xbmcaddon
import multiChoiceDialog

resolverAddonID = "script.module.israeliveresolver"
AddonID = "plugin.video.israelive"
Addon = xbmcaddon.Addon(AddonID)
AddonName = "IsraeLIVE"
localizedString = Addon.getLocalizedString
user_dataDir = xbmc.translatePath(Addon.getAddonInfo("profile")).decode("utf-8")
listsFile = os.path.join(user_dataDir, "israelive.list")
favoritesFile = os.path.join(user_dataDir, 'favorites.txt')
listsDir = os.path.join(user_dataDir, 'lists')
if not os.path.exists(listsDir):
	os.makedirs(listsDir)

def ReadList(fileName):
	content=[]
	try:
		with open(fileName, 'r') as handle:
			content = json.load(handle)
	except Exception as ex:
		xbmc.log("{0}".format(ex), 3)
	return content

def WriteList(filename, list, indent=True):
	try:
		with io.open(filename, 'w', encoding='utf-8') as handle:
			if indent:
				handle.write(unicode(json.dumps(list, indent=2, ensure_ascii=False)))
			else:
				handle.write(unicode(json.dumps(list, ensure_ascii=False)))
		success = True
	except Exception as ex:
		xbmc.log("{0}".format(ex), 3)
		success = False
		
	return success
	
def GetUnSelectedList(fullList, selectedList):
	unSelectedList = []
	for index, item in enumerate(fullList):
		if not any(selectedItem["id"] == item.get("id", "") for selectedItem in selectedList):
			unSelectedList.append(item)
	return unSelectedList
	
def GetEncodeString(str):
	try:
		import chardet
		str = str.decode(chardet.detect(str)["encoding"]).encode("utf-8")
	except:
		try:
			str = str.encode("utf-8")
		except:
			pass
	return str

def UpdateFavouritesFromRemote():
	remoteFavouritesType = Addon.getSetting("remoteFavouritesType")
	if remoteFavouritesType == "1" or remoteFavouritesType == "2":
		if remoteFavouritesType == "1":
			try:
				req = urllib2.Request(Addon.getSetting("remoteFavouritesUrl"))
				req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:11.0) Gecko/20100101 Firefox/11.0')
				responseData = urllib2.urlopen(req).read().replace('\r','')
				remoteFavouritesList = json.loads(responseData)
			except Exception as ex:
				xbmc.log("{0}".format(ex), 3)
				remoteFavouritesList = []
		elif remoteFavouritesType == "2":
			remoteFavouritesList = ReadList(Addon.getSetting("remoteFavouritesFile"))
			
		favoritesList = ReadList(favoritesFile)
		if remoteFavouritesList != [] and cmp(favoritesList, remoteFavouritesList) != 0:
			WriteList(favoritesFile, remoteFavouritesList)
			return True
	return False
	
def SearchByID(item, id):
	if item["id"] == id: 
		return item
	else:
		if item["type"] == "playlist":
			for item1 in item["list"]:
				item2 = SearchByID(item1, id)
				if item2 is not None:
					return item2
	return None
	
def FindByID(chanList, id):
	item1 = None
	for item in chanList:
		item1 = SearchByID(item, id)
		if item1 is not None:
			break
	return item1

def GetChannelByID(chID):
	chList = ReadList(listsFile)
	channel = FindByID(chList, chID)
	return channel

def GetChannels(categoryID):
	if categoryID == "Favourites":
		retList = ReadList(favoritesFile)
	elif categoryID == 'categories' or categoryID == 'selectedCategories':
		retList = ReadList(os.path.join(listsDir, "{0}.list".format(categoryID)))
	else:
		retList = ReadList(listsFile)
		if categoryID is not None and categoryID != '9999':
			listItem = FindByID(retList, categoryID)
			retList = [] if listItem is None or listItem["type"] != "playlist" else listItem["list"]
	return retList

global_catList = []
global_fullChList = []
def MakeFullLists(current_list):
	for item in current_list:
		if item["type"] == "playlist":
			global_catList.append({"image": item["image"], "group": item["group"], "name": item["name"], "id": item["id"]})
			MakeFullLists(item["list"])
		else:
			global_fullChList.append(item)

def GetChannelsFlat(categoryID):
	catList = GetChannels(categoryID)
	MakeFullLists(catList)
	return global_fullChList
		
def UpdateChList(forceUpdate=True):
	isListUpdated = False
	if UpdateFavouritesFromRemote():
		isListUpdated = True

	if isListUpdated or forceUpdate:
		fullList = ReadList(listsFile)
		if len(fullList) == 0:
			addonPath = xbmc.translatePath(Addon.getAddonInfo("path")).decode("utf-8")
			shutil.copyfile(os.path.join(addonPath, 'resources', 'lists', 'israelive.list'), listsFile)
			fullList = ReadList(listsFile)
		MakeFullLists(fullList)
		WriteList(os.path.join(listsDir, "categories.list"), global_catList)
		
		selectedCatList = ReadList(os.path.join(listsDir, "selectedCategories.list"))
		for index, cat in enumerate(selectedCatList):
			if any(f["id"] == cat.get("id", "") for f in global_catList):
				categoty = [f for f in global_catList if f["id"] == cat.get("id", "")]
				selectedCatList[index] = categoty[0]
			else:
				selectedCatList[index]["type"] = "ignore"
		WriteList(os.path.join(listsDir, "selectedCategories.list"), selectedCatList)
		
		favsList = ReadList(favoritesFile)
		for index, favourite in enumerate(favsList):
			if any(f["id"] == favourite.get("id", "") for f in global_fullChList):
				channel = [f for f in global_fullChList if f["id"] == favourite.get("id", "")]
				favsList[index] = {"url": channel[0]["url"], "image": channel[0]["image"], "name": channel[0]["name"], "type": channel[0]["type"], "group": channel[0]["group"], "id": channel[0]["id"]}
			else:
				if favsList[index].has_key("id"):
					favsList[index]["type"] = "ignore"
		WriteList(favoritesFile, favsList)
	return isListUpdated

def OKmsg(title, line1, line2="", line3=""):
	dlg = xbmcgui.Dialog()
	dlg.ok(title, line1, line2, line3)
	
def GetKeyboardText(title = "", defaultText = ""):
	keyboard = xbmc.Keyboard(defaultText, title)
	keyboard.doModal()
	text = "" if not keyboard.isConfirmed() else keyboard.getText()
	return text
	
def YesNoDialog(title, line1, line2="", line3="", nolabel="No", yeslabel="Yes"):
	dialog = xbmcgui.Dialog()
	ok = dialog.yesno(title, line1=line1, line2=line2, line3=line3, nolabel=nolabel, yeslabel=yeslabel)
	return ok
	
def GetMenuSelected(title, list, autoclose=0):
	dialog = xbmcgui.Dialog()
	answer = dialog.select(title, list, autoclose=autoclose)
	return answer

def GetMultiChoiceSelected(title, list):
	dialog = multiChoiceDialog.MultiChoiceDialog(title, list)
	dialog.doModal()
	selected = dialog.selected[:]
	del dialog #You need to delete your instance when it is no longer needed because underlying xbmcgui classes are not grabage-collected. 
	return selected
	
def GetLogoFileName(item):
	if item.has_key('image') and item['image'] is not None and item['image'] != "":
		ext = item['image'][item['image'].rfind('.')+1:]
		i = ext.rfind('?')
		if i > 0: 
			ext = ext[:i]
		if len(ext) > 4:
			ext = "png"
		tvg_logo = hashlib.md5(item['image'].strip()).hexdigest()
		logoFile = "{0}.{1}".format(tvg_logo, ext)
	else:
		logoFile = ""
		
	return logoFile

def MakeCatGuides(categories, epg):
	for category in categories:
		MakeCatGuide(category["id"], epg)
	
def MakeCatGuide(categoryID, epg):
	filename = os.path.join(listsDir, "{0}.guide".format(categoryID))
	channels = GetChannels(categoryID)
	categoryEpg = []
	for channel in channels:
		if channel["type"] == 'video' or channel["type"] == 'audio':
			tvg_id = channel.get('tvg', channel['name'].replace("[COLOR yellow][B]", "").replace("[/B][/COLOR]", "")).encode("utf-8")
			try:
				ch = [x for x in epg if x["channel"].encode('utf-8') == tvg_id]
				if not any(d.get('channel', '').encode('utf-8') == tvg_id for d in categoryEpg):
					categoryEpg.append(ch[0])
			except Exception as ex:
				xbmc.log("{0}".format(ex), 3)
	WriteList(filename, categoryEpg, indent=False)
	
def MakeFavouritesGuide(fullGuideFile, epg=None):
	if epg is None:
		epg = ReadList(fullGuideFile)
	MakeCatGuide("Favourites", epg)
			
def GetGuide(categoryID):
	if categoryID == '9999':
		return []
	fileName = os.path.join(listsDir, "{0}.guide".format(categoryID))
	return ReadList(fileName)

def GetLivestreamerPort():
	portNum = 65007
	try:
		portNum = int(Addon.getSetting("LiveStreamerPort"))
	except:
		pass
	return portNum
	
def getUseIPTV():
	useIPTV = Addon.getSetting("useIPTV")
	if useIPTV == "":	#if useIPTV not set (first time or reset to default) ask the user his choice
		useIPTVval = YesNoDialog(Addon.getAddonInfo("name"), localizedString(30311).encode('utf-8'), localizedString(30312).encode('utf-8'), localizedString(30313).encode('utf-8'), nolabel=localizedString(30002).encode('utf-8'), yeslabel=localizedString(30001).encode('utf-8'))
		useIPTV = "true" if useIPTVval == 1 else "false"
		Addon.setSetting("useIPTV", useIPTV)
	return useIPTV == "true"
	
def getAutoIPTV():
	autoIPTV = Addon.getSetting("autoIPTV")
	# convert old versions values from int to bool.
	if autoIPTV == "0" or autoIPTV == "2":
		Addon.setSetting("autoIPTV", "true")
		autoIPTV = Addon.getSetting("autoIPTV")
	elif autoIPTV == "1" or autoIPTV == "3":
		Addon.setSetting("autoIPTV", "false")
		autoIPTV = Addon.getSetting("autoIPTV")
	return autoIPTV == "true"

def GetUnColor(name):
	regex = re.compile("(\[/?(?:COLOR|B).*?\])", re.IGNORECASE)
	return regex.sub('', name).strip()
	
def GetKodiVer():
	return float(re.split(' |\-',xbmc.getInfoLabel('System.BuildVersion'))[0])

	