"""
Display the current platform
"""
import sys
import os

print("Platform:", sys.platform)    # win32
print("OS:", os.name)               # nt
#posix-only:
#print(os.uname())