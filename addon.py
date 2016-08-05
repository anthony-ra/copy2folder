import xbmcgui
import os
import sys
import shutil
import re
from resources.lib.utils import *

bDidit = False
myFolder = settings.getSetting('folder')
if myFolder == "":
    xbmcgui.Dialog().ok(addonname, "You must define a folder in settings")
    sys.exit(0)

try:
    f = open(MOVIES_PATH, "r")
    strMoviesList = f.read()
    f.close()
except Exception as e:
    strMoviesList = ""
    xbmc.log(addonname + ": Can't read the file " + MOVIES_PATH + " -> movies list = None.\n" + str(e), level=xbmc.LOGERROR)

# remove blank lines in moviesList
moviesList = filter(lambda x: not re.match(r'^\s*$', x), strMoviesList.split("\n"))
nbFiles = len(moviesList)
if nbFiles <= 0:
    xbmcgui.Dialog().ok(addonname, "List of movies is empty!")
    sys.exit(0)
xbmcgui.Dialog().textviewer(addonname, "List of movies:\n" + strMoviesList)

step = 100 / nbFiles
c = 0
i = 0
m = ""
ret = xbmcgui.Dialog().yesno(addonname, "Do you want to copy files in folder\n" + myFolder + "?")
if not ret:
    sys.exit(0)

try:
    pDialog = xbmcgui.DialogProgressBG()
    pDialog.create(addonname, 'Copying files ...')
    pDialog.update(0, 'Starting to copy files ...')

    try:
        for m in moviesList:
            if m != "":
                # check free space on disk before start
                free = get_free_space_mb(myFolder)
                fsize = os.stat(m).st_size / 1024 / 1024
                if free > fsize:
                    c += step
                    i += 1
                    # xbmc.log(addonname + ": Copy " + m + " --> " + myFolder + "\n c=" + str(c) + ", step=" + str(step) + ", nbfiles=" + str(nbFiles), level=xbmc.LOGNOTICE)
                    # pDialog.update(c, str(i) + '/' + str(nbFiles) + ': ' + m)
                    pDialog.update(c, m)
                    try:
                        if os.path.isdir(m):
                            xbmc.log(addonname + ": Copy directory " + m + " --> " + myFolder, level=xbmc.LOGNOTICE)
                            shutil.copytree(m, myFolder)
                        else:
                            dst = os.path.join(myFolder, os.path.basename(m))
                            xbmc.log(addonname + ": Copy file " + m + " --> " + dst, level=xbmc.LOGNOTICE)
                            shutil.copyfile(m, dst)
                    except Exception as e:
                        xbmc.log(addonname + ": Can't copy file " + m + ".\n" + str(e), level=xbmc.LOGERROR)
                else:
                    xbmc.log(addonname + ": No more space on " + myFolder + "(" + str(fsize) + " MB/" + str(free) + " MB)", level=xbmc.LOGNOTICE)
                    xbmcgui.Dialog().ok(addonname, "No more space on " + myFolder)
                    break
            xbmc.sleep(1000)
    except Exception as e:
        xbmc.log(addonname + ": Can't copy files.\n" + str(e), level=xbmc.LOGERROR)

except Exception as e:
    xbmc.log(addonname + ": Can't create dialog progress bar.\n" + str(e), level=xbmc.LOGERROR)
finally:
    try:
        # pDialog.update(100, str(nbFiles) + '/' + str(nbFiles) + ': ' + m)
        pDialog.update(100, m)
        xbmc.sleep(1000)
        pDialog.close()
    except Exception as e:
        xbmc.log(addonname + ": Can't close dialog progress bar.\n" + str(e), level=xbmc.LOGERROR)

try:
    if i >= nbFiles:
        os.remove(MOVIES_PATH)
except Exception as e:
    xbmc.log(addonname + ": Can't delete " + MOVIES_PATH + ".\n" + str(e), level=xbmc.LOGERROR)

# Sanitize
# settings.setSetting('folder', '')
