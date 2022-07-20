from pypresence import Presence
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

configFile = open('config.json')
config = json.load(configFile)

clear = lambda: os.system('cls') # lazy again
user32 = ctypes.windll.user32
x, y = config['window']['x'], config['window']['y']

rpcid = config['rpc']
rpc = Presence(rpcid)
rpc.connect()

def sendKey(key:str, length:float):
    pyautogui.keyDown(key)
    time.sleep(length)
    pyautogui.keyUp(key)

def placeModeScrollAdjust():
    pyautogui.moveTo(x+400, y+400)
    i = 0
    while i < 25:
        pyautogui.scroll(1)
        i += 1

def bfgScrollAdjust(): # im not sure why, but inputting values like 25 and -7 into pyautogui.scroll
       i = 0           # just doesnt work and it behaves the same as 1 and -1, so this is a workaround
       while i < 25:
              pyautogui.scroll(1)
              i += 1

       j = 0
       while j < 6:
              pyautogui.scroll(-1)
              j += 1

def windowMove():
    hwnd = user32.FindWindowW(None, u'Growtopia')
    rect = ctypes.wintypes.RECT()
    user32.GetWindowRect(hwnd, ctypes.pointer(rect))

    w = rect.right - rect.left
    h = rect.bottom - rect.top

    user32.MoveWindow(hwnd, x, y, w ,h)

def windowActivate(): # pasted function idc
    results = []
    top_windows = []
    win32gui.EnumWindows(windowEnumerationHandler, top_windows)
    for i in top_windows:
        if "growtopia" in i[1].lower():
            # print(i)
            win32gui.ShowWindow(i[0], 5)
            win32gui.SetForegroundWindow(i[0])
            break


def respawn():
    pyautogui.press('esc')
    pyautogui.moveTo(x+600, y+300)
    pyautogui.click()

def takeBlocksFromRespawn(): # cant use sendKey here :(
    pyautogui.keyDown('up')
    pyautogui.keyDown('up') # hoping this fixes the void-input ffs
    time.sleep(0.3)
    pyautogui.keyDown('left')
    time.sleep(0.01)
    pyautogui.keyUp('left')
    time.sleep(0.1)
    pyautogui.keyUp('up')

def placeLoop(third):
    i = 0
    while i < 3:
        pyautogui.keyDown('right')
        pyautogui.mouseDown()
        time.sleep(third)
        pyautogui.keyUp('right')
        pyautogui.mouseUp()
        i += 1

def afterCollectAbove(plat:int): # plat = how many jumps from plat above ghost charm


    i = 25  #25
    while i > 0: 
        pyautogui.moveTo(x+600, x+500)   

        sendKey('right', 0.1)
        sendKey('up', 0.05)

        j = 0
        while j < i:
            sendKey('up', 0.08) # 0.08 min for next plat prolly
            time.sleep(0.1)
            j += 1

        placeLoop(4.4)

        respawn()
        time.sleep(4)
        takeBlocksFromRespawn()
        time.sleep(0.5)
        i -= 1
        
def doPlaceLoop():
    windowActivate()
    windowMove()

    placeModeScrollAdjust()

    respawn()
    time.sleep(3)
    takeBlocksFromRespawn()
    time.sleep(0.25)
    afterCollectAbove(1)
    sendKey('right', 0.52)
    sendKey('up', 0.2)
    placeLoop(4.33)
    time.sleep(0.2)
    placeLoop(4.1)

    time.sleep(1)
    respawn()
    exit()

def placeLoopConfirm():
    clear()
    confirm = input("Are you sure you would like to enable place mode? [y/n] > ")
    match confirm:
        case "y":
            doPlaceLoop()
        
        case other:
            return
def doFarmLoop(walkLength, punchCount):
    timeStarted = time.time()
    rpc.update(state="Active [Mode: Farm]",large_image="rpcimage",start=timeStarted)
    clear()

    windowName("p0lybot - Active")
    print(macroActiveConsoleState)
    windowActivate()

    windowMove()

    time.sleep(0.5)
    while True:
        i = 0
        while i < 3:
            pyautogui.keyDown('space')
            pyautogui.keyUp('space')
            i += 1

        pyautogui.keyDown('right')
        time.sleep(walkLength)
        pyautogui.keyUp('right')
    

def farmLoopConfirm(c1, c2):
    clear()
    confirm = input("Are you sure you would like to enable farm mode? [y/n] > ")
    match confirm:
        case "y":
            doFarmLoop(c1, c2)
        
        case other:
            return

def doBfgLoop(punchCount):
    timeStarted = time.time()
    rpc.update(state="Active [Mode: BFG]",large_image="rpcimage",start=timeStarted)
    clear()

    windowName("p0lybot - Active")
    print(macroActiveConsoleState)
    windowActivate()

    windowMove()

    time.sleep(0.5)
    pyautogui.moveTo(x+400, y+400)
    bfgScrollAdjust()

    while True:
        pyautogui.moveTo(x+875, y+475) # 1st block coords: +875 +475
        pyautogui.click()
        pyautogui.moveTo(x+1075, y+475)
        pyautogui.click()

        i = 0
        while i < punchCount*2:          # have to do this cuz pyautogui.press doesnt register
            pyautogui.keyDown('space')   # the punch, growtopia issue prob
            pyautogui.keyUp('space')
            i += 1

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

windowName("p0lybot - Idle")
rpc.update(state="Idle",large_image="rpcimage")

name = os.getlogin()

selected = False
while selected == False:
    clear()
     
    print("p0lybot v1\n")
    mode = input(f"[1] - Farm mode \n[2] - BFG mode \n[3] - Place mode \n\n{name}@p0lybot > ")

    match mode:
        case "1":
            farmLoopConfirm(config['farmMode']['walkKeystrokeLength'], config['farmMode']['punchCount'])

        case "2":
            bfgLoopConfirm(config['bfgMode']['punchCount'])

        case "3":
            placeLoopConfirm()

        case other:
            clear()






