from sikuli.Sikuli import *
path_to_bot = getBundlePath().split("bot.sikuli")[0]

import sys
sys.path.append(path_to_bot + "view")
import Interface

class ISignIn(Interface.Interface):
    #methods for interaction with login window

    def __init__(self):
        super(ISignIn, self).__init__()
        
    def log_in(self):
        log_on_button = self.app_region.find(self._images.get_login("login_button"))
        
        self._slow_click(loc=Location(log_on_button.x, log_on_button.y-70))
        type(settings("USERNAME"))
        
        self._slow_click(loc=Location(log_on_button.x, log_on_button.y-40))
        type(settings("PASSWORD"))
        
        self._slow_click(loc=log_on_button.getTarget())
        
        if exists(self._images.get_login("login_success"), BotSettings.getSetting("LOGIN_WAIT")):
            print("succeeded")
            return True
        elif(exists(self._images.get_login("login_fail"), 10)):
            print("login failed")
            return False