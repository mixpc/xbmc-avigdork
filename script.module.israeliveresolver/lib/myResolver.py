# -*- coding: utf-8 -*-
import urllib2, re, uuid, json, random, base64, gzip
from StringIO import StringIO
import xbmc, xbmcaddon
import jsunpack, unwise, cloudflare
import livestreamer

AddonID = 'script.module.israeliveresolver'
Addon = xbmcaddon.Addon(AddonID)

UAs = [
	'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36',
	'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/600.8.9 (KHTML, like Gecko) Version/8.0.8 Safari/600.8.9',
	'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36',
	'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:40.0) Gecko/20100101 Firefox/40.0',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
	'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
	'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36',
	'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/600.7.12 (KHTML, like Gecko) Version/8.0.7 Safari/600.7.12',
	'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
	'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:40.0) Gecko/20100101 Firefox/40.0',
	'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0',
	'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0',
	'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36',
	'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36',
	'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36',
	'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36',
	'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36',
	'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36',
	'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.10240',
	'Mozilla/5.0 (Windows NT 6.1; rv:40.0) Gecko/20100101 Firefox/40.0',
	'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
	'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36',
	'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36',
	'Mozilla/5.0 (Windows NT 5.1; rv:40.0) Gecko/20100101 Firefox/40.0',
	'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:40.0) Gecko/20100101 Firefox/40.0',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/600.8.9 (KHTML, like Gecko) Version/7.1.8 Safari/537.85.17',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/600.5.17 (KHTML, like Gecko) Version/8.0.5 Safari/600.5.17',
	'Mozilla/5.0 (X11; Linux x86_64; rv:40.0) Gecko/20100101 Firefox/40.0',
	'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0',
	'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.130 Safari/537.36',
	'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:39.0) Gecko/20100101 Firefox/39.0',
	'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/600.6.3 (KHTML, like Gecko) Version/8.0.6 Safari/600.6.3',
	'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/44.0.2403.89 Chrome/44.0.2403.89 Safari/537.36',
	'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36',
	'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11) AppleWebKit/601.1.56 (KHTML, like Gecko) Version/9.0 Safari/601.1.56',
	'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11) AppleWebKit/601.1.50 (KHTML, like Gecko) Version/9.0 Safari/601.1.50',
	'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.125 Safari/537.36',
	'Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:40.0) Gecko/20100101 Firefox/40.0',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/600.3.18 (KHTML, like Gecko) Version/8.0.3 Safari/600.3.18',
	'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/43.0.2357.130 Chrome/43.0.2357.130 Safari/537.36',
	'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0;  Trident/5.0)',
	'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;  Trident/5.0)',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36',
	'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
	'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36',
	'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36 OPR/31.0.1889.174',
	'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:40.0) Gecko/20100101 Firefox/40.0',
	'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:40.0) Gecko/20100101 Firefox/40.0',
	'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; Touch; rv:11.0) like Gecko',
	'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
	'Mozilla/5.0 (Windows NT 6.1; rv:38.0) Gecko/20100101 Firefox/38.0',
	'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0',
	'Mozilla/5.0 (X11; Linux x86_64; rv:38.0) Gecko/20100101 Firefox/38.0',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_5) AppleWebKit/537.78.2 (KHTML, like Gecko) Version/6.1.6 Safari/537.78.2',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/600.7.12 (KHTML, like Gecko) Version/7.1.7 Safari/537.85.16',
	'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.130 Safari/537.36',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:38.0) Gecko/20100101 Firefox/38.0',
	'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
	'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36',
	'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.130 Safari/537.36'
]

UA = random.choice(UAs)
makoDeviceID = ''
makoUsername = ''
makoPassword = ''
try:
	makoDeviceID = Addon.getSetting("MakoDeviceID")
	if makoDeviceID.strip() == '':
		uuidStr = str(uuid.uuid4()).upper()
		makoDeviceID = "W{0}{1}".format(uuidStr[:8], uuidStr[9:])
		Addon.setSetting("MakoDeviceID", makoDeviceID)
	makoUsername = Addon.getSetting("MakoUsername")
	makoPassword = Addon.getSetting("MakoPassword")
except:
	pass
		
def getUrl(url, cookieJar=None, post=None, timeout=20, headers=None, getCookie=False):
	link = ""
	try:
		cookie_handler = urllib2.HTTPCookieProcessor(cookieJar)
		opener = urllib2.build_opener(cookie_handler, urllib2.HTTPBasicAuthHandler(), urllib2.HTTPHandler())
		req = urllib2.Request(url)
		req.add_header('Accept-encoding', 'gzip')
		if headers:
			for h, hv in headers.items():
				req.add_header(h,hv)
		if not req.headers.has_key('User-Agent') or req.headers['User-Agent'] == '':
			req.add_header('User-Agent', UA)
		response = opener.open(req, post, timeout=timeout)
		if getCookie == True and response.info().has_key("Set-Cookie"):
			return response.info()['Set-Cookie']
		if response.info().get('Content-Encoding') == 'gzip':
			buf = StringIO( response.read())
			f = gzip.GzipFile(fileobj=buf)
			link = f.read()
		else:
			link = response.read()
		response.close()
	except Exception as ex:
		xbmc.log(str(ex),3)
	return link

def OpenURL(url, headers={}, user_data={}, getCookies=False):
	data = ""
	cookie = ""
	try:
		req = urllib2.Request(url)
		for k, v in headers.items():
			req.add_header(k, v)
		if user_data:
			req.add_data(user_data)
		response = urllib2.urlopen(req)
		if getCookies == True and response.info().has_key("Set-Cookie"):
			cookie = response.info()['Set-Cookie']
		if response.info().get('Content-Encoding') == 'gzip':
			buf = StringIO( response.read())
			f = gzip.GzipFile(fileobj=buf)
			data = f.read()
		else:
			data = response.read()
		response.close()
	except Exception as ex:
		data = str(ex)
	return data, cookie

def GetLivestreamerLink(url):
	return livestreamer.streams(url)['best'].url

def Get3url(url):
	return GetLivestreamerLink(url)

def GetStreamliveToFullLink(url):
	stream = livestreamer.streams(url)['best']
	return '{0} pageUrl={1} live=true'.format(stream.params['rtmp'], stream.params['pageUrl'])

def Get14url(channel):
	url = 'http://www.tvrplus.ro/{0}'.format(channel)
	text, c = OpenURL(url)
	matches = re.compile("sources:\s*\[.+?src:\s*'(.+?)'", re.S).findall(text)
	if len(matches) > 0:
		return '{0}|Referer={1}&User-Agent={2}'.format(matches[0], url, UA)
	return None

def Get31url(channel):
	url = 'http://www.popler.tv/embed/player.php?user={0}&popler=1&kody_code='.format(channel)
	text = cloudflare.request(url, headers={'Referer': 'http://www.popler.tv/portal.php', 'User-Agent': UA})
	match = re.compile('src:\s+"(.*?)"').findall(text)
	if len(match) < 1:
		return None
	return '{0}|User-Agent={1}'.format(match[0].strip(), UA)

def Get36url(channel):
	url = 'http://player.mediaklikk.hu/player/player-inside-full3.php?userid=mtva&streamid={0}live&noflash=yes&hls=2'.format(channel.replace('-elo','').replace('-',''))
	text = getUrl(url, headers={'Referer': 'http://www.mediaklikk.hu/{0}'.format(channel.replace('mtv','m'))})
	match = re.compile('"file":"(.*?)"').findall(text)
	if len(match) < 1:
		return None
	return match[0].replace('\\','')

def Get51url(channel):
	u = None
	try:
		a = 'http://live.russia.tv/index/index/channel_id/{0}'.format(channel)
		b, ck = OpenURL(a, getCookies=True)
		c = re.compile('<iframe src="(.*?)"').findall(b)
		d = getUrl(c[0])
		d1 = re.compile("dataUrl\s*=\s*'//(.+?)'").findall(d)
		d2 = getUrl('https://{0}'.format(d1[0]), headers={'Referer': c[0], 'Cookie': ck[:ck.find(';')]})
		e = json.loads(d2)
		u = '{0}|User-Agent={1}'.format(e['data']['playlist']['medialist'][0]['sources']['m3u8'], UA)
	except Exception as ex:
		xbmc.log(str(ex), 3)
	return u

def Get52url(channel):
	u = None
	try:
		a = 'https://www.ntv.ru/'
		b = getUrl(a)
		c = re.compile("var hlsURL\s*=\s*'(.*?)'").findall(b)
		u = '{0}|Referer={1}&User-Agent={2}'.format(c[0], a, UA)
	except Exception as ex:
		xbmc.log(str(ex), 3)
	return u

def Get53url(channel):
	u = None
	try:
		UA = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
		a = 'https://otr-online.ru/online/'
		b = getUrl(a)
		c = re.compile('<iframe.*?src="(.*?)"', re.S).findall(b)
		d = getUrl(c[0])
		e = re.compile('data-config="config=(.*?)"').findall(d)
		f, ck = OpenURL(e[0].replace('feed', 'media'), getCookies=True)
		g = re.compile('<track.*?CDATA\[\s?(.*?)\]', re.S).findall(f)
		sl_b = ck.find('start_live') 
		sl_e = ck.find(';', sl_b)
		gs_b = ck.find('gpmd_sex') 
		gs_e = ck.find(';', gs_b)
		ga_b = ck.find('gpmd_age') 
		ga_e = ck.find(';', ga_b)
		u = '{0}|User-Agent={1}&Cookie={2};{3};{4}'.format(g[0], UA, ck[gs_b:gs_e], ck[ga_b:ga_e], ck[sl_b:sl_e])
	except Exception as ex:
		xbmc.log(str(ex), 3)
	return u

def Get54url(channel):
	u = None
	try:
		a = 'https://{0}.euronews.com/api/watchlive.json'.format(channel)
		b = json.loads(getUrl(a))
		c = json.loads(getUrl('https:{0}'.format(b['url'])))
		u = '{0}|User-Agent={1}'.format(c['primary'], UA)
	except Exception as ex:
		xbmc.log(str(ex), 3)
	return u

def Resolve(url, mode, isLiveTV=False):
	mode = int(mode)
	if mode == 3:
		url = Get3url(url)
	elif mode == 14:
		url = Get14url(url)
	elif mode == 31:
		url = Get31url(url)
	elif mode == 36:
		url = Get36url(url)
	elif mode == 51:
		url = Get51url(url)
	elif mode == 52:
		url = Get52url(url)
	elif mode == 53:
		url = Get53url(url)
	elif mode == 54:
		url = Get54url(url)
	
	if isLiveTV:
		if url is not None:
			if mode != 3:
				url = "hlsvariant://{0}".format(url)
	#xbmc.log('----> {0}'.format(url), 5)
	return url
