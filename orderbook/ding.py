import os
import platform

def beep():
    system = platform.system()
    
    if system == "Darwin":  # macOS
        os.system("afplay /System/Library/Sounds/Glass.aiff")
    elif system == "Windows":
        os.system("echo ^G")
    elif system == "Linux":
        os.system("echo -e '\a'")
    else:
        print('\a')  # 回退到转义字符

beep()
