import xbmc, xbmcaddon, os
import common

AddonID = "plugin.video.israelive"
Addon = xbmcaddon.Addon(AddonID)

user_dataDir = xbmc.translatePath(Addon.getAddonInfo("profile")).decode("utf-8")
fullGuideFile = os.path.join(user_dataDir, 'fullGuide.txt')
iptvChannelsFile = os.path.join(user_dataDir, "iptv.m3u")
iptvGuideFile = os.path.join(user_dataDir, "guide.xml")
iptvLogosDir = os.path.join(user_dataDir, "logos")

def Update():
	# Update channels-lists files
	common.UpdateChList(forceUpdate=False)

	# Update EPG files for selected LiveTV channels first
	isGuideUpdated = False
	if Addon.getSetting("useEPG") == "true":
		epg = common.ReadList(fullGuideFile)
		if len(epg) > 0:
			isGuideUpdated = True
			fullCategoriesList = []
			selectedCategoriesList = []
			categoriesList = []
			iptvList = Addon.getSetting("iptvList")
			if iptvList == "0": # Favourites
				categoriesList = [{"id": "Favourites"}]
			elif iptvList == "1": # No filter 
				categoriesList = fullCategoriesList = common.ReadList(os.path.join(user_dataDir, "lists", "categories.list"))
			elif iptvList == "2": # Selected categories
				categoriesList = selectedCategoriesList = common.ReadList(os.path.join(user_dataDir, "lists", "selectedCategories.list"))
			common.MakeCatGuides(categoriesList, epg)
			
	useIPTV = common.getUseIPTV()
	# Update LiveTV channels and EPG
	if useIPTV:
		import myIPTV
		myIPTV.makeIPTVlist(iptvChannelsFile)
		myIPTV.MakeChannelsGuide(fullGuideFile, iptvGuideFile)
		myIPTV.RefreshPVR(iptvChannelsFile, iptvGuideFile, iptvLogosDir)
	
	# Update EPG files for non-selected LiveTV channels
	if isGuideUpdated:
		if fullCategoriesList == []:
			fullCategoriesList =  common.ReadList(os.path.join(user_dataDir, "lists", "categories.list"))
		if iptvList == "0": # Favourites
			categoriesList = fullCategoriesList
		elif iptvList == "1": # No filter 
			categoriesList = [{"id": "Favourites"}]
		elif iptvList == "2": # Selected categories
			categoriesList = common.GetUnSelectedList(fullCategoriesList, selectedCategoriesList)
			categoriesList.append({"id": "Favourites"})
			
		common.MakeCatGuides(categoriesList, epg)
		
	# Update channels-logos files
	if useIPTV and myIPTV.GetIptvType() < 2:
		myIPTV.SaveChannelsLogos(iptvLogosDir)

	checkInterval = 720 # 12 hours = 720 minutes
	xbmc.executebuiltin("XBMC.AlarmClock({0},XBMC.RunPlugin(plugin://plugin.video.israelive/default.py?mode=100&url=checkUpdates),{1},silent)".format("IsraeLiveUpdates", checkInterval))
