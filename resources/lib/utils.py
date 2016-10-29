import xbmcaddon
import xbmc
import os
import platform
import ctypes
from datetime import datetime, timedelta


addonID = "script.copy2folder"
addon_work_folder = xbmc.translatePath("special://profile/addon_data/" + addonID)
settings = xbmcaddon.Addon(id=addonID)
addonname = settings.getAddonInfo('name')
myLastFileDate = settings.getSetting('last_file_date')
myLastFileTime = settings.getSetting('last_file_time')

# HOME_DIR = os.getcwd()[:-1] + os.sep
MOVIES_FILE = "list_movies"
MOVIES_PATH = addon_work_folder + os.sep + MOVIES_FILE

if not os.path.isdir(addon_work_folder):
    xbmc.log(addonname + ": Create " + MOVIES_PATH, level=xbmc.LOGNOTICE)
    os.mkdir(addon_work_folder)

def get_free_space_mb(dirname):
    """Return folder/drive free space (in megabytes)."""
    free_hd = 0

    if platform.system() == 'Windows':
        free_bytes = ctypes.c_ulonglong(0)
        ctypes.windll.kernel32.GetDiskFreeSpaceExW(ctypes.c_wchar_p(dirname), None, None, ctypes.pointer(free_bytes))
        # return free_bytes.value / 1024 / 1024
        free_hd = free_bytes.value
    else:
        st = os.statvfs(dirname)
        # return st.f_bavail * st.f_frsize / 1024 / 1024
        free_hd = st.f_bavail * st.f_frsize

    return free_hd / 1024 / 1024


def init_app():
    myLastFileDateTime = datetime.strptime(myLastFileDate + " " + myLastFileTime, "%Y-%m-%d %H:%M")
    if myLastFileDate == "" or myLastFileTime == "" or datetime.now() - myLastFileDate > timedelta(hours=4):
        empty_list


def update_LastFileDateTime():
    myDateTime = datetime.now()
    settings.setSetting('last_file_date', myDateTime.strftime("%Y-%m-%d"))
    settings.setSetting('last_file_time', myDateTime.strftime("%H:%M"))


def empty_list():
    try:
        f = open(MOVIES_PATH, "w")
        f.write('')
        f.close()
        update_LastFileDateTime
    except Exception as e:
        xbmc.log(addonname + ": Can't empty the movies file " + MOVIES_PATH + "\n" + str(e), level=xbmc.LOGERROR)
