import xbmcaddon
import xbmc
import os
import platform
import ctypes


addonID = "script.copy2folder"
addon_work_folder = xbmc.translatePath("special://profile/addon_data/" + addonID)
settings = xbmcaddon.Addon(id=addonID)
addonname = settings.getAddonInfo('name')

# HOME_DIR = os.getcwd()[:-1] + os.sep
MOVIES_FILE = "list_movies"
MOVIES_PATH = addon_work_folder + os.sep + MOVIES_FILE

if not os.path.isdir(addon_work_folder):
    xbmc.log(addonname + ": Create " + MOVIES_PATH, level=xbmc.LOGNOTICE)
    os.mkdir(addon_work_folder)


def get_free_space_mb(dirname):
    """Return folder/drive free space (in megabytes)."""
    if platform.system() == 'Windows':
        free_bytes = ctypes.c_ulonglong(0)
        ctypes.windll.kernel32.GetDiskFreeSpaceExW(ctypes.c_wchar_p(dirname), None, None, ctypes.pointer(free_bytes))
        return free_bytes.value / 1024 / 1024
    else:
        st = os.statvfs(dirname)
        return st.f_bavail * st.f_frsize / 1024 / 1024
