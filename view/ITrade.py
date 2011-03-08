from sikuli.Sikuli import *

path_to_bot = getBundlePath().split("bot.sikuli")[0]

import sys
sys.path.append(path_to_bot + "view")

import Interface
import IChat

class ITrade(Interface.Interface):
    def __init__(self):
        super(ITrade, self).__init__()
        self.Ichat= IChat.IChat()

    def start_wait(self, type = "incoming_request"):
        #wait for whatever is passed in type parameter to show up
        #usually this will be used to wait for trade request
        self.app_region.wait(self._images.get_trade(type), FOREVER)
        return True
    def get_customer_name(self):
        #will get customer name by clicking on chat area, and copying message
        #then will edit string down
        confirm_button = self.app_region.exists(self._images.get_trade("confirm_button"))
        hover(Location(confirm_button.x+600, confirm_button.y))
        #copy test to variable "msg"
        msg = "9:56 PM placeholder accepts trade invitation"
        if " PM " in msg:
            msg_split = msg.split(" PM ", 1)
        else:
            msg_split = msg.split(" AM ", 1)
            
        customer_name = msg_split[1].split(" accepts trade invitation", 0)
        
        return customer_name
        
    def accept_trade(self):
        #click on the accept button for a trade
        print("accept_trade")
        request_loc = self.app_region.exists(self._images.get_trade("accept_request"))
        print("453")
        if isinstance(request_loc, Match):
            print("455")
            self._slow_click(loc=request_loc.getTarget())
            print("457")
            return True
        else:
            print("460")
            return False

    def set_windows(self):
        #set the regions for the interactions
        #get match ogbject of giving window for use with making a region
        giving_window = exists(self._images.get_trade("giving_window"), 40)
        self.giving_window_region = Region(giving_window.getRect())
        t_window = exists(self._images.get_trade("taking_window"))
        self.taking_window_region = Region(t_window.getRect())

    def turn_page(self, direction):
        #turns the page if no elements of interest found on current page
        """Returns true if string is left or right and successfully turns page, returns false otherwise"""
        if direction == "left":
            self._slow_click(target=self._images.get_trade("turn_left"))
            #insert an image into wait to use to confirm that the page has been turned
            wait()
            return True
        elif direction == "right":
            self._slow_click(target=self._images.get_trade("turn_right"))
            #insert an image into wait to use to confirm that the page has been turned
            wait()
            return True
        else:
            return False

    def go_to_tickets_packs(self):
        #go to the tickets section
        self._slow_click(target=self._images.get_trade("version_menu"))
        self._slow_click(target=self._images.get_trade("version_menu_packs_tickets"))

    def go_to_confirmation(self):
        confirm_button = self._images.get_trade(filename="confirm_button")
        self._slow_click(target=confirm_button)