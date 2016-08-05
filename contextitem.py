import sys
import xbmc
import os
from resources.lib.utils import *


if __name__ == '__main__':
    # http://kodi.wiki/view/InfoLabels#ListItem
    # filepath = "File: %s" % sys.listitem.getVideoInfoTag().getPath()
    # filename = "File: %s" % sys.listitem.getfilename()
    filepathname = xbmc.getInfoLabel("ListItem.FileNameAndPath")
    if filepathname != "":
        try:
            f = open(MOVIES_PATH, 'a')
            f.write(filepathname + '\n')
            f.close()
            message = "Added to list '%s'" % sys.listitem.getLabel()
        except Exception as e:
            message = "ERROR added to list '%s'" % sys.listitem.getLabel()
    else:
        message = "ERROR added to list '%s'" % sys.listitem.getLabel()
        filepathname = "None"

    xbmc.executebuiltin("Notification(\"" + message + "\", \"File: %s\")" % filepathname)
