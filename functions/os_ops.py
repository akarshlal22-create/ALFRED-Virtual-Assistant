import os
import sys
import subprocess as sp

paths = {
    'notepad': "C:\\Program Files\\Notepad++\\notepad++.exe",
    'discord': "C:\\Users\\ashut\\AppData\\Local\\Discord\\app-1.0.9003\\Discord.exe",
    'calculator': "C:\\Windows\\System32\\calc.exe"
}


def open_notepad():
    if sys.platform == 'darwin':
        sp.Popen(['open', '-a', 'TextEdit'])
    elif sys.platform == 'win32':
        os.startfile(paths['notepad'])
    else:
        sp.Popen(['gedit'])


def open_discord():
    if sys.platform == 'darwin':
        sp.Popen(['open', '-a', 'Discord'])
    elif sys.platform == 'win32':
        os.startfile(paths['discord'])


def open_cmd():
    if sys.platform == 'darwin':
        sp.Popen(['open', '-a', 'Terminal'])
    elif sys.platform == 'win32':
        os.system('start cmd')
    else:
        sp.Popen(['x-terminal-emulator'])


def open_camera():
    if sys.platform == 'darwin':
        sp.Popen(['open', '-a', 'Photo Booth'])
    elif sys.platform == 'win32':
        sp.run('start microsoft.windows.camera:', shell=True)


def open_calculator():
    if sys.platform == 'darwin':
        # On macOS, Calculator is at /System/Applications/Calculator.app
        for target in ['/System/Applications/Calculator.app', 'Calculator']:
            try:
                res = sp.run(['open', target], capture_output=True)
                if res.returncode == 0:
                    break
            except Exception:
                pass
    elif sys.platform == 'win32':
        sp.Popen(paths['calculator'])
    else:
        sp.Popen(['gnome-calculator'])

