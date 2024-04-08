import pyttsx3
import speech_recognition as sr
from datetime import date
import time
import webbrowser
import datetime
from pynput.keyboard import Key, Controller
import pyautogui
import sys
import os
from os import listdir
from os.path import isfile, join
import smtplib
import wikipedia
#import Gesture_Controller
#import Gesture_Controller_Gloved as Gesture_Controller
from logging import shutdown
import wikipedia
import random
import cv2
import requests
import app
from threading import Thread



# -------------Object Initialization---------------
today = date.today()
r = sr.Recognizer()
keyboard = Controller()
engine = pyttsx3.init('sapi5')
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[2].id)

# ----------------Variables------------------------
file_exp_status = False
files =[]
path = ''
is_awake = True  #Bot status

# ------------------Functions----------------------
def reply(audio):
    app.ChatBot.addAppMsg(audio)

    print(audio)
    engine.say(audio)
    engine.runAndWait()


def wish():
    hour = int(datetime.datetime.now().hour)

    if hour>=0 and hour<12:
        reply("Good Morning nikhil!")
    elif hour>=12 and hour<18:
        reply("Good Afternoon nikhil!")   
    else:
        reply("Good Evening nikhil!")  
        
    reply("I am Eva, your electronic virtual assistant, What can i do for you!")

# Set Microphone parameters
with sr.Microphone() as source:
        r.energy_threshold = 500 
        r.dynamic_energy_threshold = False

# Audio to String
def record_audio():
    with sr.Microphone() as source:
        r.pause_threshold = 1
        voice_data = ''
        audio = r.listen(source, phrase_time_limit=5)

        try:
            voice_data = r.recognize_google(audio)
        except sr.RequestError:
            reply('Sorry my Service is down. Plz check your Internet connection')
        except sr.UnknownValueError:
            print('cant recognize')
            pass
        return voice_data.lower()

def respond(voice_data):
    global file_exp_status, files, is_awake, path
    print(voice_data)
    voice_data.replace('eva',' ')
    app.eel.addUserMsg(voice_data)

    if is_awake==False:
        if 'wake up' in voice_data:
            is_awake = True
            wish()

    elif 'hello' in voice_data:
        wish()

    elif 'what is your name' in voice_data:
        reply('My name is Eva i am build by nikhil!')
    
    #Volume controls
    elif 'volume up' in voice_data:
        pyautogui.press("volumeup")
        reply("Volume Increased")

    elif 'volume down' in voice_data:
        pyautogui.press("volumedown")
        reply("Volume Decreased")

    elif 'mute' in voice_data:
        pyautogui.press("volumemute")
        reply("Muted")

    elif 'unmute' in voice_data:
        pyautogui.press("volumemute")
        reply("Unmuted")
    # Volume control ends

    #CAMERA OPEN CODE...
    elif 'open camera'in voice_data:
        reply("opening Camera, Press Escape to close ")
        cap = cv2.VideoCapture(0)
        while True:
           ret, img = cap.read()
           cv2.imshow('webcam', img)
           k = cv2.waitKey(50)
           if k ==27:
                break
        cap.release()
        cv2.destroyAllWindows()
    #OPEN CAMERA CODE ENDS HERE...

    #MY LOCATION CODE STARTS HERE...
    elif 'my location' in voice_data:
        ip_add = requests.get("https://api.ipify.org").text
        url = f'https://get.geojs.io/v1/ip/geo/{ip_add}.json'
        geo_m = requests.get(url)
        geo_q = geo_m.json()
        lon = geo_q['longitude']
        lat = geo_q['latitude']
        state = geo_q['region']
        cocode = geo_q['country_code']
        country = geo_q['country']
        print(lon, lat,state,country, cocode)
        reply(f"Sir, you're now in {state, country, cocode}")

    #SEARCH LOCATION CODE STARTS HERE...
    elif 'location' in voice_data:
        reply('Which place are you looking for?📍')
        temp_audio = record_audio()
        app.eel.addUserMsg(temp_audio)
        reply('Locating...')
        url = 'https://google.nl/maps/place/' + temp_audio + '/&amp;'
        try:
            webbrowser.get().open(url)
            reply('This is what I found nikhil')
        except:
            reply('Please check your Internet')

    #CREATE A FOLDER CODESTARTS HERE..
    elif 'create a folder' in voice_data:
        os.mkdir("new folder")
        reply("Creating New Folder")

    #MAXIMISE AND MINIMIZE SCREEN CODE STARTS HERE...
    elif 'maximize' in voice_data:
        reply("maximising")
        with pyautogui.hold("win"):
            pyautogui.press("pgup")
          
    elif 'minimie' in voice_data:
        reply("minimizing")
        with pyautogui.hold("win"):
            pyautogui.press("pgdn")
    #MAXIMISE AND MINIMIZE SCREEN CODE ENDS HERE...
    
    #DATE AND TIME CODE STARTS HERE...
    elif 'date' in voice_data:
        reply(today.strftime("%B %d, %Y"))

    elif 'time' in voice_data:
        reply(str(datetime.datetime.now()).split(" ")[1].split('.')[0])
    
    #DATE AND TIME CODE STARTS HERE...

    #SEARCH ANYTHING CODES STARTS...
    elif 'wikipedia' in voice_data:
        reply('Searching wikipedia...')
        voice_data = voice_data.replace("wikipedia", "")
        results = wikipedia.summary(voice_data, sentences=2)
        reply("according to wikipedia")
        print(results)
        reply(results)

    #GOOGLE SEARCH AUTOMATION CODE STARTS HERE...
    elif 'search' in voice_data:
        reply('Searching for ' + voice_data.split('search')[1])
        url = 'https://google.com/search?q=' + voice_data.split('search')[1]
        try:
            webbrowser.get().open(url)
            reply('This is what I found nikhil')
        except:
            reply('Please check your Internet')
    
    #GOOGLE SEARCH AUTOMATION CODE ENDS HERE...

    #SCROLL AUTOMATION CODE STARTS HERE....
    elif 'scroll down' in voice_data:
        pyautogui.hotkey("fn","pagedown")

    elif 'scroll up' in voice_data:
        pyautogui.hotkey("fn","pageup")
    
    #SCROLL AUTOMATION CODE ENDS HERE...

    #TAB CLOSING CODE STARTS HERE...
    elif 'close tab' in voice_data:
        pyautogui.hotkey("ctrl","w")  
        reply("closing one tab")

    #NOTEPAD AUTOMATION CODE STARTS....
    elif 'open notepad' in voice_data:
        notePath = "C:\\Program Files\\WindowsApps\\Microsoft.WindowsNotepad_11.2302.16.0_x64__8wekyb3d8bbwe\\Notepad\\Notepad.exe"
        reply("opening Notepad") 
        os.startfile(notePath)

    elif 'write a note' in voice_data:
        reply("Listening Sir")
        while True:
            q = record_audio().lower()
            if q == 'exit':
                reply("Written sir")
                break
            pyautogui.typewrite(record_audio())
                    
    elif 'erase' in voice_data:
        reply("Erasing sir")
        pyautogui.press("backspace")

    elif 'close notepad' in voice_data:
        pyautogui.hotkey("ctrl" ,"w")
        reply("notepad closed")

    #NOTEPAD AUTOMATION CODE ENDS HERE...
    # COMPUTER DRIVES AUTOMATION CODE STARTS HERE...
    elif 'open c drive' in voice_data:
        cpath = "C:\\"
        os.startfile(cpath)
        reply("opening C drive")

    elif "close c drive" in voice_data:
        pyautogui.hotkey("ctrl","w")

    elif 'open d drive' in voice_data:
        dpath = "D:\\"
        os.startfile(dpath)
        reply("opening D drive")

    elif 'close d drive' in voice_data:
        pyautogui.hotkey("ctrl" ,"w")

    elif 'open f drive' in voice_data:
        fpath = "F:\\"
        os.startfile(fpath)
        reply("Opening F drive")

    elif 'close f drive' in voice_data:
        pyautogui.hotkey("ctrl" ,"w")
    
    # COMPUTER DRIVES AUTOMATION CODE STARTS HERE...
    # CALCULATOR START CODE HERE..
    elif 'open calculator' in voice_data:
        calcPath = "C:\\Windows\\System32\\calc.exe"
        os.startfile(calcPath)
        reply("Opening Calculator")

    #EXCEL FILE AUTOMATION CODE 
    elif 'open excel' in voice_data:
        excelPath = "C:\\ProgramData\Microsoft\\Windows\\Start Menu\\Programs\\Excel.lnk"
        os.startfile(excelPath)
        reply("opening MS excel")

    elif 'open new xl file' in voice_data:
        pyautogui.hotkey("ctrl","n")
        pyautogui.press("tab")
        pyautogui.press("enter")

    elif 'change font size' in voice_data:
               pyautogui.hotkey("ctrl","shift","p")
               pyautogui.typewrite(record_audio())
               pyautogui.press("enter")
               reply("Font size is changed")

    elif 'change font type' in voice_data:
        pyautogui.hotkey("ctrl","shift","f")
        pyautogui.typewrite(record_audio())
        pyautogui.press("enter")
        reply("font type is changed")

    elif 'write a xl file' in voice_data:
        reply("Say what you want to write")
        while True:
            q = record_audio().lower()
            if q == 'exit':
                reply("Written sir")
                break
            pyautogui.typewrite(record_audio())

    elif 'erase' in voice_data:
        reply("Erasing sir")
        pyautogui.press("backspace")

    #WORD FILE AUTOMATION CODE
    elif 'open word' in voice_data:
        wordPath = "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Word.lnk"
        os.startfile(wordPath)
        reply("Opening MS Word")

    elif 'open new word file' in voice_data:
        reply("opening new word file")
        pyautogui.hotkey("ctrl","n")
        pyautogui.press("tab")
        pyautogui.press("enter")
               
    elif 'change font size' in voice_data:
        pyautogui.hotkey("ctrl","shift","p")
        pyautogui.typewrite(record_audio().tostring())
        pyautogui.press("enter")
        reply("Font size is changed")

    elif 'change font type' in voice_data:
        pyautogui.hotkey("ctrl","shift","f")
        pyautogui.typewrite(record_audio())
        pyautogui.press("enter")
        reply("font type is changed")

    elif 'write a word file' in voice_data:
        reply("Say what you want to write")
        while True:
            q = record_audio().lower()
            if q == 'exit':
                reply("Written sir")
                break
            pyautogui.typewrite(record_audio())

    elif 'erase' in voice_data:
        reply("Erasing sir")
        pyautogui.press("backspace")

    #POWERPNT FILE AUTOMATION CODE
    elif 'open powerpoint' in voice_data:        
        powerPath = "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\PowerPoint.lnk"
        os.startfile(powerPath)
        reply("Opening MS powerpoint")

    elif 'open new ppt file' in voice_data:
        pyautogui.hotkey("ctrl","n")
        pyautogui.press("tab")
        pyautogui.press("enter")
        pyautogui.press("tab" )

    elif 'change font size' in voice_data:
        pyautogui.hotkey("ctrl","shift","p")
        pyautogui.typewrite(record_audio().tostring())
        pyautogui.press("enter")
        reply("Font size is changed")

    elif 'change font type' in voice_data:
        pyautogui.hotkey("ctrl","shift","f")
        pyautogui.typewrite(record_audio())
        pyautogui.press("enter")
        reply("font type is changed")

    elif 'write a ppt file' in voice_data:
        reply("Say what you want to write")
        while True:
            q = record_audio().lower()
            if q == 'exit':
                reply("Written sir")
                break
            pyautogui.typewrite(record_audio())

    elif 'erase' in voice_data:
        reply("Erasing sir")
        pyautogui.press("backspace")

    #PAINT FILE AUTOMATION CODE
    elif 'open paint' in voice_data:
        paintPath = "C:\\Program Files\\WindowsApps\\Microsoft.Paint_11.2301.22.0_x64__8wekyb3d8bbwe\\PaintApp\\mspaint.exe"
        os.startfile(paintPath)
        reply("Opening MS paint")
        

    #SHUT DOWN PC CODE STARTS...
    elif 'shutdown' in voice_data:
        reply("Shutting Down")
        os.system("shutdown/s ")
    # SHUT DOWN PC CODE ENDS... 
    #LOCK SCREEN CODE STARTS.
    elif 'lock screen' in voice_data:
        reply("Locking Screen")
        pyautogui.hotkey("win","l")
    #LOG OFF CODE STARTS HERE..

    elif 'log' in voice_data:
        reply("Logging Off")
        os.system("shutdown/l")

    #RESTART PC CODE STARTS...
    elif 'restart pc' in voice_data:
        reply("Restarting PC")
        os.system(f"shutdown/r")

    #RESTART PC CODE ENDS...
    #ABORTING SHUTDOWN CODE..
    elif "don't " in voice_data:
        reply("Aborting Shutdown")
        os.system("shutdown /a")

    # HIBERNATE THE PC CODE STARTS

    elif 'hibernate pc' in voice_data:
        reply("Hibernating ")
        os.system("shutdown/h")

    elif ('bye' in voice_data) or ('by' in voice_data):
        reply("Good bye nikhil! Have a nice day.")
        is_awake = False

    
    elif 'copy' in voice_data:
        with keyboard.pressed(Key.ctrl):
            keyboard.press('c')
            keyboard.release('c')
        reply('Copied')
          
    elif 'page' in voice_data or 'pest'  in voice_data or 'paste' in voice_data:
        with keyboard.pressed(Key.ctrl):
            keyboard.press('v')
            keyboard.release('v')
        reply('Pasted')
        
    # File Navigation (Default Folder set to C://)
    elif 'list' in voice_data:
        counter = 0
        path = 'y://'
        files = listdir(path)
        filestr = ""
        for f in files:
            counter+=1
            print(str(counter) + ':  ' + f)
            filestr += str(counter) + ':  ' + f + '<br>'
        file_exp_status = True
        reply('These are the files in your root directory')
        app.ChatBot.addAppMsg(filestr)
        
    elif file_exp_status == True:
        counter = 0   
        if 'open' in voice_data:
            if isfile(join(path,files[int(voice_data.split(' ')[-1])-1])):
                os.startfile(path + files[int(voice_data.split(' ')[-1])-1])
                file_exp_status = False
            else:
                try:
                    path = path + files[int(voice_data.split(' ')[-1])-1] + '//'
                    files = listdir(path)
                    filestr = ""
                    for f in files:
                        counter+=1
                        filestr += str(counter) + ':  ' + f + '<br>'
                        print(str(counter) + ':  ' + f)
                    reply('Files are listed')
                    app.ChatBot.addAppMsg(filestr)
                    
                except:
                    reply('I do not have permission to access this folder')
                                    
        if 'back' in voice_data:
            filestr = ""
            if path == 'C://':
                reply('Sorry, this is the root directory')
            else:
                a = path.split('//')[:-2]
                path = '//'.join(a)
                path += '//'
                files = listdir(path)
                for f in files:
                    counter+=1
                    filestr += str(counter) + ':  ' + f + '<br>'
                    print(str(counter) + ':  ' + f)
                reply('ok')
                app.ChatBot.addAppMsg(filestr)
                   
    else: 
        reply('I am not functioned to do this !')

# ------------------Driver Code--------------------

t1 = Thread(target = app.ChatBot.start)
t1.start()

# Lock main thread until Chatbot has started
while not app.ChatBot.started:
    time.sleep(0.5)

wish()
voice_data = None
while True:
    if app.ChatBot.isUserInput():
        #take input from GUI
        voice_data = app.ChatBot.popUserInput()
    else:
        #take input from Voice
        voice_data = record_audio()

    #process voice_data
    if 'eva' in voice_data:
        try:
            #Handle sys.exit()
            respond(voice_data)
        except SystemExit:
            reply("Exit Successfull")
            break
        except:
            #some other exception got raised
            print("EXCEPTION raised while closing.") 
            break