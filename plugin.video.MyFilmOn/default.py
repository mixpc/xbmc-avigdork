import  xbmcgui, xbmcplugin, sys

liz = xbmcgui.ListItem("[COLOR red][B]The addon removed.[/B][/COLOR]", iconImage="DefaultFolder.png", thumbnailImage="DefaultFolder.png")
#liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description} )
xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=".",listitem=liz,isFolder=False)
xbmcplugin.endOfDirectory(int(sys.argv[1]))