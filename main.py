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
           """ # TODO: probably add some sort of config display to this, idk


def windowEnumerationHandler(hwnd, top_windows):
    top_windows.append((hwnd, win32gui.GetWindowText(hwnd)))


def windowName(name): # lazy
    os.system(f"title {name}")


clear = lambda: os.system('cls') # lazy again
user32 = ctypes.windll.user32

def bfgScrollAdjust(): # im not sure why, but inputting values like 25 and -7 into pyautogui.scroll
       i = 0           # just doesnt work and it behaves the same as 1 and -1, so this is a workaround
       while i < 25:
              pyautogui.scroll(1)
              i += 1

       j = 0
       while j < 4:
              pyautogui.scroll(-1)
              j += 1

def growtopiaWindowMove(x, y):
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
        time.sleep(0.1)   
    

def farmLoopConfirm(c1, c2):
    clear()
    confirm = input("Are you sure you would like to enable farm mode? [y/n] > ")
    match confirm:
        case "y":
            doFarmLoop(c1, c2)
        
        case other:
            return

def doBfgLoop(punchCount):
    clear()

    windowName("p0lybot - Active")
    print(macroActiveConsoleState)
    growtopiaWindowActivate()

    x, y = 0, 0
    growtopiaWindowMove(x, y)

    time.sleep(0.5)
    pyautogui.moveTo(x+400, y+400)
    bfgScrollAdjust()

    while True:
        pyautogui.moveTo(x+875, y+475) # 1st block coords: +875 +475
        pyautogui.click()
        pyautogui.moveTo(x+1075, y+475)
        pyautogui.click()
        sendKey("space", 0, punchCount*2)
        time.sleep(0.1)


def bfgLoopConfirm(c1):
    clear()
    print("WARNING: you must put your chat window all the way up for the macro to work, and you may not resize or move the Growtopia window!\n")
    confirm = input("Are you sure you would like to enable BFG mode? [y/n] > ")
    match confirm:
        case "y":
            doBfgLoop(c1)

        case other: 
            return

configFile = open('config.json')
config = json.load(configFile)

windowName("p0lybot - Idle")
name = os.getlogin()

selected = False
while selected == False:
    clear()
     
    print("p0lybot v1\n")
    mode = input(f"[1] - Farm mode \n[2] - BFG mode \n\n{name}@p0lybot > ")

    match mode:
        case "1":
            farmLoopConfirm(config['walkKeystrokeLength'], config['punchCount'])

        case "2":
            bfgLoopConfirm(config["punchCount"])
            input() 

        case other:
            clear()






