"""
Display the current platform
"""
import sys
import os

print("Platform:", sys.platform)
print("OS:", os.name)
#posix-only:
#print(os.uname())