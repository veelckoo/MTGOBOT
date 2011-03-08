from sikuli.Sikuli import *

path_to_bot = getBundlePath().split("bot.sikuli")[0]

exec(open(path_to_bot + "ini.py", "rb").read())

class ErrorHandler(Exception):
    #custom Exception parent class to handle errors
    
    def __init__(self, message):
        ERRORHANDLERAPP = settings["ERRORHANDLERAPP"]
        self._errormsg = message
        print(self.__errormsg)
    def __openRecord(self):
        #this will be different depending on the application
        pass
    def __writeRecord(self):
        type(self._errormsg + "\n")