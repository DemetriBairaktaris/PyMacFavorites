
import platform

if platform.system() == "Darwin":
    from .src import *
else:
    print("py_mac_favorite: Invalid Platform. This will only work on Macintosh")