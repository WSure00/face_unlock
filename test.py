import os
a=os.system('gnome-screensaver-command -q | grep in')
print(a)
if a:
    print("true")
else:
    print("false")