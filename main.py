import win32gui
import pyautogui
import time
import os
import json

# TODO: add BFG mode (move mouse cursor between 2 points, also make it auto-set the zoom via scroll emulation)
# TODO: add keylogger-esque method to register killswitch key when console window not active
# TODO: try not to skid lel

macroActiveConsoleState = """
       pika thanks u for using p0lybot
               ,___          .-;'
               `"-.`\_...._/`.`
            ,      \        /
         .-' ',    / ()   ()\\
        `'._   \  /()    .  (|       https://twitter.com/plexalwayslucky
            > .' ;,     -'-  /       
           / <   |;,     __.;
           '-.'-.|  , \    , \\
              `>.|;, \_)    \_)
               `-;     ,    /
                  \    /   <
                   '. <`'-,_)
                    '._)"""
def windowEnumerationHandler(hwnd, top_windows):
    top_windows.append((hwnd, win32gui.GetWindowText(hwnd)))


def windowName(name): # lazy
    os.system(f"title {name}")


clear = lambda: os.system('cls') # lazy again


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






