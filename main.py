import ctypes, ctypes.wintypes
import win32gui
import pyautogui
import time
import os
import json

# TODO: add BFG mode (move mouse cursor between 2 points, also make it auto-set the zoom via scroll emulation)
# TODO: add keylogger-esque method to register killswitch key when console window not active
# TODO: try not to skid lel

macroActiveConsoleState = """         
       .-.,     ,.-.                ___  _       _           _  
  '-.  /:::\\   //:::\  .-'         / _ \| |     | |         | |  
 '-.\|':':' `"` ':':'|/.-'   _ __ | | | | |_   _| |__   ___ | |_ 
 `-./`. .-=-. .-=-. .`\.-`  | '_ \| | | | | | | | '_ \ / _ \| __|
   /=- /     |     \ -=\    | |_) | |_| | | |_| | |_) | (_) | |_         
  ;   |      |      |   ;   | .__/ \___/|_|\__, |_.__/ \___/ \__|
  |=-.|______|______|.-=|   | |             __/ |                
  |==  \  0 /_\ 0  /  ==|   |_|            |___/                 
  |=   /'---( )---'\   =|
   \   \:   .'.   :/   /         
    `\= '--`   `--' =/'           
      `-=._     _.=-'
           `\"\"\"`

    https://github.com/plexislucky/p0lybot
    https://twitter.com/plexalwayslucky
           """
def windowEnumerationHandler(hwnd, top_windows):
    top_windows.append((hwnd, win32gui.GetWindowText(hwnd)))


def windowName(name): # lazy
    os.system(f"title {name}")


clear = lambda: os.system('cls') # lazy again

user32 = ctypes.windll.user32

def growtopiaWindowMove (x, y):
    hwnd = user32.FindWindowW(None, u'Growtopia')
    rect = ctypes.wintypes.RECT()
    user32.GetWindowRect(hwnd, ctypes.pointer(rect))

    w = rect.right - rect.left
    h = rect.bottom - rect.top

    user32.MoveWindow(hwnd, x, y, w ,h)

def growtopiaWindowActivate(): # pasted function idc
    results = []
    top_windows = []
    win32gui.EnumWindows(windowEnumerationHandler, top_windows)
    for i in top_windows:
        if "growtopia" in i[1].lower():
            # print(i)
            win32gui.ShowWindow(i[0], 5)
            win32gui.SetForegroundWindow(i[0])
            break


def sendKey(key, length, repeat = 1):
    i = 0
    while i < repeat:
        pyautogui.keyDown(key)
        time.sleep(length)
        pyautogui.keyUp(key)
        i += 1 


def doFarmLoop(walkLength, punchCount):
    clear()
    windowName("p0lybot - Active")
    print(macroActiveConsoleState)
    growtopiaWindowActivate()
    growtopiaWindowMove(0, 0)
    time.sleep(0.5)
    while True:
        sendKey("space", 0, 3)
        sendKey("right", walkLength) # 0.04 with air robs
        time.sleep(0.5)   
    


configFile = open('config.json')
config = json.load(configFile)

windowName("p0lybot - Idle")

print("p0lybot v1\n")
print(f"Walk length: {config['walkKeystrokeLength']}\nPunch count: {config['punchCount']}\n")
print("These values can be changed within the config.json file\nPress enter to start botting...")

input()
doFarmLoop(config['walkKeystrokeLength'], config['punchCount'])






