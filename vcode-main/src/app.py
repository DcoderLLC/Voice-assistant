import eel
import os
from queue import Queue

#defining a class named ChatBot
class ChatBot:

    #created a class level variable 
    started = False          # boolean flag to check if the chatBot is started
    userinputQueue = Queue()        #it is a thread-safe queue to store user input msg

    # created a static method
    def isUserInput():
        return not ChatBot.userinputQueue.empty() #it returns true if user input is not empty otherwise false

    # another static method
    def popUserInput():
        return ChatBot.userinputQueue.get()   #it retrieves and remove the user input msg from the front of userInputQueue

    #it is a callback functions
    def close_callback(route, websockets):
        # if not websockets:
        #     print('Bye!')
        exit()     #this is called when the application is closed. It currently calls Exit() to terminate the program

    ##decorating the below finction
    @eel.expose
    def getUserInput(msg): #it is exposed to the JS code running in the web brower and recieves msg
        ChatBot.userinputQueue.put(msg)  #it puts the msg into the userInputQueue
        print(msg)
    
    # static method 
    def close():
        ChatBot.started = False #sets started  to False indicating that the chatbot should stop
    
    # a static method thst takes msgs
    def addUserMsg(msg):
        eel.addUserMsg(msg)   #it uses eel library to send msg to the web interface to display user msg
    
    # a static method that takes msg
    def addAppMsg(msg):
        eel.addAppMsg(msg)   # it also uses the eel library to send the msg to the web interface and display application msg

    # a atatic method the initalize the eel library 
    def start():
        path = os.path.dirname(os.path.abspath(__file__))  # provides the path to the web folder containg JS and HTML file
        eel.init(path + r'\web', allowed_extensions=['.js', '.html'])  # it also set the allowed extension for files in the web folder
        try:
            # calling the application  with its specific index.html file
            eel.start('index.html', mode='chrome',  # set the browser mode to chrome
                                    host='localhost', #setting the host to localhost
                                    port=27005, # setting the port to 27005
                                    block=False,
                                    size=(350, 480), #setting the window size
                                    position=(10,100), #setting the position of window
                                    disable_cache=True, # disabling the cache
                                    close_callback=ChatBot.close_callback)  # setting the close callback if called
            ChatBot.started = True  # set the boolean flag to true
            while ChatBot.started:  # entering the loop as long as the started flag is true
                try:
                    # it set loop to sleep for 10 sec to allow the web interface to handle events 
                    eel.sleep(10.0)  # it is necessary to prevent loop  for consuming excessive CPU resource
                except:
                    #main thread exited
                    break
        #This try-except block catches any exceptions that occur during the execution of the eel.start() function, allowing the program to continue without crashing.
        except:
            pass
