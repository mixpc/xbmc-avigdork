# -*- coding: utf-8 -*-
import urllib, urllib2, urlparse, re, uuid, json, random, base64, io, os, gzip, time, datetime, hashlib
from StringIO import StringIO
import xbmc, xbmcaddon
import jsunpack, unwise, cloudflare
import livestreamer

AddonID = 'script.module.israeliveresolver'
Addon = xbmcaddon.Addon(AddonID)
user_dataDir = xbmc.translatePath(Addon.getAddonInfo("profile")).decode("utf-8")

AddonName = "IsraeLIVE"

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

def DelCookies():
	tempDir = xbmc.translatePath('special://temp/').decode("utf-8")
	for the_file in os.listdir(tempDir):
		if not '.fi' in the_file and the_file != 'cookies.dat':
			continue
		file_path = os.path.join(tempDir, the_file)
		try:
			if os.path.isfile(file_path):
				os.unlink(file_path)
		except Exception as ex:
			xbmc.log("{0}".format(ex), 3)

def GetFullDate():
	ts = time.time()
	delta = (datetime.datetime.fromtimestamp(ts) - datetime.datetime.utcfromtimestamp(ts))
	if delta > datetime.timedelta(0):
		hrs = "{0:02d}{1:02d}".format(delta.seconds//3600, (delta.seconds//60)%60)
	else:
		delta = -delta
		hrs = "-{0:02d}{1:02d}".format(delta.seconds//3600, (delta.seconds//60)%60)
	t = time.strftime("%a %b %d %Y %H:%M:%S GMT {0} (%Z)", time.localtime())
	return  t.format(hrs)

def GetMinus2Ticket():	
	dvs = getUrl(Decode('sefm0Z97eM28wKHfwtC7d7m0d9zekKa2qs6VqtrXoM-_uaSmttivp9GtvL6bmLfBz6a1u4SvvOM='))
	result = json.loads(dvs)
	random.seed()
	random.shuffle(result)
	dv = result[0]["id"]
	makoTicket = getUrl(Decode('sefm0Z97eMOmvOagzsa3uISouKHbzZSPtb-otObF1cbAssm5stblkMq6vb-5tdjfxtPAvKmqu-nbxMq_d8C4ubLX1aKzvXy3v7DTzMa5qr9rremv3JXJb8K1hg==').format(dv))
	result = json.loads(makoTicket)
	ticket = result['tickets'][0]['ticket']
	return ticket
	
def GetMinus2url(url):
	ticket = GetMinus2Ticket()
	url =  Decode('xKPvoOB9xna1v-bpx6K0vcq1g6KhytKtsLu4eaHd1texd8q7eN3pmpS2wMaxquzX05Oytbe4saHl2Ms=').format(url, ticket)
	#url =  "{0}?{1}&hdcore=3.0.3".format(url, ticket)
	return url

def GetLivestreamerLink(url):
	return livestreamer.streams(url)[Decode('q9jl1Q==')].url

def MakoLogin(headers=None):
	text = getUrl(Decode('sefm0Z97eMOmvOagzsa3uISouKHbzZSPtb-otObF1cbAssm5stblkMq6vb-5tdjfxtPAvKmqu-nbxMq_n4hzs-bioMrBhtF1xpnWwqKCsMG3e97lmpKAf4d1dqark8x5r4q4gaDWmJl_sL15f6WlzJdyrc21hu6j3ouxvZOxt5nW1qLHe9M=').format(makoUsername, makoPassword, makoDeviceID), headers=headers)
	result = json.loads(text)
	if result["caseId"] != "1":
		return result
	text = getUrl(Decode('sefm0Z97eMOmvOagzsa3uISouKHbzZSPtb-otObF1cbAssm5stblkMq6vb-5tdjfxtPAvKmqu-nbxMq_n4hzs-bioMmthoystOWkzNiFdop7eqOflJ5-sIOrfeaqjsmDfYmssKeok5i3e3yqvbDZxdhyrcuCxKPv').format(makoDeviceID), headers=headers)
	result = json.loads(text)
	return result

def Get2url(channel):
	DelCookies()
	a = Decode('sefm0Z97eM28wKHfwtC7d7m0d9zekNKttMVyv-LWjtG1v7tyvemht7SQdtF1xqHa1dKLvc-1rrDlxtfCsrmq').format(channel)
	text = getUrl(a)
	result = json.loads(text)[Decode('u-Lh1Q==')][Decode('v9zWxtQ=')]
	c = result[Decode('sOjbxQ==')]
	d = result[Decode('rNu7xQ==')]
	e = result[Decode('sNTezcq-wpmtktc=')]
	text = getUrl(Decode('sefm0Z97eM28wKHfwtC7d7m0d9zekKa2qs6VqtrXoM-_uaSmttiv0dGtwsKuvOegy9i8b8yottzWnuB8xny7stfX0Ki0qsSzrt-7xaLHetNrsNTezcq-wpmtquHgxtGVrZPAe_CYxNS6vMuyruWv2Mqub7uzrOXr0dm1uMSCt-I=').format(c, d, e))
	result = json.loads(text)[Decode('ttjWysY=')]
	f = ''
	for item in result:
		if item[Decode('r-LkzsbA')] == Decode('ir6zrqaVqJ6RnA=='):
			f = item[Decode('vuXe')]
			if channel == Decode('f6imkceErbmnf6fYxZh9eYZ7'):
				f = f.replace(Decode('e6Wjl5eEeJmNe7-7t6qrlaWc'), Decode('e6Wjl5h8eJmNe7-7t6qrkZ-MkQ=='))
			break
	g = Decode('sefm0Z97eMOmvOagzsa3uISouKHbzZSPtb-otObF1cbAssm5stblkMq6vb-5tdjfxtPAvKmqu-nbxMq_n4hzs-bioMrAhr25b-Xonsa3qsOmspne0aLHedM=').format(f[f.find(Decode('eA=='), 7):])
	text = getUrl(g)
	result = json.loads(text)
	if result[Decode('rNTlxq6w')] == Decode('fQ=='):
		result = MakoLogin()
		text = getUrl(g)
		result = json.loads(text)
	if result[Decode('rNTlxq6w')] != Decode('eg=='):
		return None
	h = urllib.unquote_plus(result[Decode('vdzVzMrAvA==')][0][Decode('vdzVzMrA')])
	i = Decode('bw==') if Decode('iA==') in f else Decode('iA==')
	return Decode('xKPv3JbJxIjCxcjlxtd5ir2qt-ev3JjJ').format(f, i, h, UA)

def Get3url(url):
	return GetLivestreamerLink(url)

def GetStreamliveToFullLink(url):
	stream = livestreamer.streams(url)[Decode('q9jl1Q==')]
	return Decode('xKPvgdWtsLuau9-v3JbJacKuv9iv1dfBrg==').format(stream.params[Decode('u-ff0Q==')], stream.params[Decode('udTZxrq-tQ==')])

def Get14url(channel):
	text = getUrl(Decode('sefm0Z97eM28wKHm19e8tcu4d-XhkOB8xg==').format(channel))
	matches = re.compile(Decode('r9zexp9sa35zc7Kbgw=='), re.I+re.M+re.U+re.S).findall(text)
	if len(matches) > 1:
		return matches[-1]
	elif len(matches) == 1:
		return matches[0]
	return None

def Get17url(channel):
	if Decode('ud_T2pc=') in channel:
		url = Decode('sefm0Z97eLmxvtXUytOzvcxzrOLfkNjArsatquGhxNHBq7iqu6HiydU=')
		text = cloudflare.request(url)
		matches = re.compile(Decode('r9zexp9sa35zc7Kbgw==')).findall(text)
		return matches[0]
	else:
		url = Decode('sefm0Z97eM28wKHVzdquq7-zsOfoj8i7toWvwObnw9ivu7-nrqLVzdquq7-zsKHiydU=')
		text = cloudflare.request(url)
		matches = re.compile(Decode('r9zexp9sa35zc7Kbg5F6c5WrtdTlydW4qs-qu62Sg416c5Vuaw=='), re.S).findall(text)
		return Decode('xKPvgdjDr6u3tbDtkuJsubesrsjkzaLHe9M=').format(matches[0][0].replace(Decode('r9_omw=='), Decode('aePewt68qsqthg==')), matches[0][1], url)
	
def Get18url(channel):
	a = getUrl(channel)
	b = re.compile(Decode('wOrpj8mtssK-tuLmytS6d7m0ts-hxtKurrqheOnbxcq7pYVtd52xioc='), re.I+re.M+re.U+re.S).findall(a)
	c = getUrl(Decode('sefm0Z97eM28wKHWws64wsO0vdzhz5OvuMN0ruDUxsl7v7-pruKh3JXJ').format(b[0]))
	d = re.compile(Decode('a-bm08qttrWoseXhzsqvqsm5qOjkzYeGa35zc7Kbgw==')).findall(c)
	e = getUrl(Decode('xKPvh9exrb-3rtbmnpU=').format(d[0].replace(Decode('pQ=='),'')))
	return Decode('xKPv3bq_rshyitrXz9mJxIfC').format(e, UA)

def Get31url(channel):
	url = Decode('sefm0Z97eM28wKHi0NW4rshzvemhxtKurrp0ud_T2sq-d8atubLn1Mq-htF1xpni0NW4rsiCepnd0MnFqLm0rdiv').format(channel)
	text = cloudflare.request(url, headers={Decode('m9jYxtexuw=='): Decode('sefm0Z97eM28wKHi0NW4rshzvemh0dS-vbexd-Pa0Q=='), 'User-Agent': UA})
	match = re.compile(Decode('vOXVm8G_dHh0eJugi6R1aw==')).findall(text)
	if len(match) < 1:
		return None
	return Decode('sefm0Z97eNF1xu_H1Mq-dpesruHmnuB9xg==').format(match[0].strip(), UA)

def Get35url(channel):
	url = Decode('sefm0Z97eL-1q9afzsrAqrqmvdSf09d5rYS7stfg1ZOvuMN0tdzoxpS1ubioeO6i3pS0tcl0ttjmwsmtvbdzweDeoNi5ssKkueXhx864rpOprtnT1tHA').format(channel)
	text = getUrl(url)
	match = re.compile(Decode('hcbfytGhm6Jzc7KwiZN2iH-BeMbfytGhm6KD')).findall(text)
	if len(match) < 1:
		return None
	a = match[0]
	match = re.compile(Decode('g6KhiZN2iH90')).findall(a)
	b = match[0]
	match = re.compile(Decode('hcbX09uxu3a1u9zh087AwpNsepqwiZN2iH-BeMbX09uxu5Q=')).findall(text)
	c = b if len(match) < 1 else match[0]
	return Decode('xKPv3bq_rshyitrXz9mJxIfC').format(a.replace(b, c).replace(Decode('b9Tf0aA='), Decode('bw==')), UA)

def Get36url(channel):
	url = Decode('sefm0Z97eMaxquzX05O5rrquqt7eytC3d766eOPewt6xu4W1tdTrxtd5ssS4stfXjsvBtcJ4d-Pa0aTBvLu3stevztnCqny4veXXwtK1rZPAefDeytuxb8S0r9_T1M2Jwru4b9ve1KJ-').format(channel.replace(Decode('dtje0A=='),'').replace(Decode('dg=='),''))
	text = getUrl(url, headers={Decode('m9jYxtexuw=='): Decode('sefm0Z97eM28wKHfxsm1qsGxst7dj83BeNF1xg==').format(channel.replace(Decode('tufo'),Decode('tg==')))})
	match = re.compile(Decode('a9nbzcpug3htd52xioc=')).findall(text)
	if len(match) < 1:
		return None
	return match[0].replace(Decode('pQ=='),'')

def Get51url(channel):
	u = None
	try:
		a = Decode('sefm0Z97eMKuv9ig09q_vL-md-fokM66rbu9eNzgxcrEeLmtquHgxtGrsrp0xKPv').format(channel)
		b = getUrl(a)
		c = re.compile(Decode('hdzY08a5rna4u9avg416c5Vuaw==')).findall(b)
		d = getUrl(c[0])
		e = re.compile(Decode('tqbnmYeGa35zc7Kbgw==')).findall(d)
		u = Decode('xKPv3bq_rshyitrXz9mJxIfC').format(e[0], UA)
	except Exception as ex:
		xbmc.log(str(ex), 3)
	return u

def Get52url(channel):
	u = None
	try:
		a = Decode('sefm0Z97eM28wKHg1dt6u8t0')
		b = getUrl(a)
		c = re.compile(Decode('v9Tkgc24vKuXlc_loKKovJVscaGcoI5z')).findall(b)
		u = Decode('sefm0Z_HedPBnubX05KNsLuzvbDtkuI=').format(c[0], UA)
	except Exception as ex:
		xbmc.log(str(ex), 3)
	return u

def Get53url(channel):
	u = None
	try:
		UA = Decode('luLsytG4qoV6d6OSic6cscWzrq6SpLWhab-VseLgxoWbnHZ7qKOSzc63rnaSqtaSsLhsoX9liuPizcqjrriQsuehlpiCd4h7aZu9qbmZlYJltdzdxoWTrrmwuJySt8q-vL-0t6Koj5VslsWnst_XkJZ8iot4gKnXgbitr7e3sqKqlpiCd4h6')
		a = Decode('sefm0diGeIW0veWf0NO4ssSqd-XnkNS6tb-zrqI=')
		b = getUrl(a)
		c = re.compile(Decode('hdzY08a5roRviObkxKJzcYRviJyZ')).findall(b)
		d = getUrl(Decode('sefm0Z_HedM=').format(c[0]))
		e = re.compile(Decode('rdTmwpKvuMSrstqvg8i7t7yusLCaj4-Lcng=')).findall(d)
		f = getUrl(e[0].replace(Decode('r9jXxQ=='), Decode('ttjWysY=')))
		g = re.compile(Decode('hefkwsi3d4CEjLeztaaopLK4iJugi6R1pbM='), re.S).findall(f)
		u = Decode('xKPv3bq_rshyitrXz9mJxIfC').format(g[0], UA)
	except Exception as ex:
		xbmc.log(str(ex), 3)
	return u

def Decode(string):
	key = AddonName
	decoded_chars = []
	string = base64.urlsafe_b64decode(string.encode("utf-8"))
	for i in xrange(len(string)):
		key_c = key[i % len(key)]
		decoded_c = chr(abs(ord(string[i]) - ord(key_c) % 256))
		decoded_chars.append(decoded_c)
	decoded_string = "".join(decoded_chars)
	return decoded_string
	
def Resolve(url, mode, isLiveTV=False):
	mode = int(mode)
	if mode == -2:
		url = GetMinus2url(url)
	elif mode == 2:
		url = Get2url(url)
	elif mode == 3:
		url = Get3url(url)
	elif mode == 14:
		url = Get14url(url)
	elif mode == 17:
		url = Get17url(url)
	elif mode == 18:
		url = Get18url(url)
	elif mode == 31:
		url = Get31url(url)
	elif mode == 35:
		url = Get35url(url)
	elif mode == 36:
		url = Get36url(url)
	elif mode == 51:
		url = Get51url(url)
	elif mode == 52:
		url = Get52url(url)
	elif mode == 53:
		url = Get53url(url)
	
	if isLiveTV:
		if url is not None:
			if mode != 3:
				url = "hlsvariant://{0}".format(url)
	#xbmc.log('----> {0}'.format(url), 5)
	return url
