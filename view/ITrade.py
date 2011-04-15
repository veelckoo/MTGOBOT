
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
        #for shifting products slots down
        self.how_many_pixels_to_move_down = 17
    
    def update_inventory(self, card_inventory, pack_inventory):
        self.card_inventory = card_inventory
        self.pack_inventory = pack_inventory
    
    def start_wait(self, type = "incoming_request"):
        #wait for whatever is passed in type parameter to show up
        #usually this will be used to wait for trade request
        self.app_region.wait(Pattern(self._images.get_trade(type)).similar(0.9), FOREVER)
        return True
    
    def next_row(self, *args):
        if self.how_many_pixels_to_move_down == 17:
            self.how_many_pixels_to_move_down = 18
        else:
            self.how_many_pixels_to_move_down = 17
        print("called next row")
        for slot_region in args:
            slot_region.setY(slot_region.getY()+self.how_many_pixels_to_move_down)
    
    def cancel_trade(self):
        #if trade has alreaady been canceled, then click ok, otherwise cancel the trade
        self._slow_click(target=self._images.trade["cancel_trade"])
        wait(2)
        yes_button = self.app_region.exists(self._images.trade["yes_button"], 1)
        if yes_button:
            self._slow_click(loc=yes_button.getTarget())
        wait(2)
        ok_button = self.app_region.exists(self._images.get_ok_button())
        if ok_button:
            self._slow_click(loc=ok_button.getTarget())
                
    def get_customer_name(self):
        #will get customer name by clicking on chat area, and copying message
        #then will edit string down
        confirm_button = self.app_region.exists(self._images.get_trade("confirm_button"), 120)
        click(Location(confirm_button.x+600, confirm_button.y+556))
        type("c", KEY_CTRL)
        #copy test to variable "msg"
        wait(0.5)
        try:
            clipboard = Env.getClipboard()
        except java.lang.IllegalStateException:
            clipboard = "Unknown"
        #smiley faces [sS] are appended to usernames who are on your buddy list, remove them
        if "[sS]" in clipboard:
            copied_wo_emote = clipboard.split("[sS]")[0]
            return copied_wo_emote.strip()
        else:
            return clipboard.strip()
        
    def accept_trade(self):
        #click on the accept button for a trade
        request_loc = self.app_region.exists(self._images.get_trade("yes_button"))
        if isinstance(request_loc, Match):
            self._slow_click(loc=request_loc.getTarget())
            return True
        else:
            return False

    def set_windows(self):
        #set the regions for the interactions
        #get match ogbject of giving window for use with making a region
        giving_window = exists(Pattern(self._images.get_trade("giving_window")).similar(0.9), 40)
        self.giving_window_region = Region(giving_window.getRect())
        taking_window = exists(Pattern(self._images.get_trade("taking_window")).similar(0.9))
        self.taking_window_region = Region(taking_window.getRect())

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

    def take_all_copies_of_product(self):
        #this will take all the packs from the given location
        #right click on the product to open context menu
        self._slow_click(loc=product_loc, button="Right")
        #take 32 at a time, until there are no more, Magic Online UI will give all if there are less than 32 left
        while quantity > 0:
            self._slow_click(self._images.get_amount(32))
            quantity -= 32

    def take_product(self, product_loc, quantity_to_take):
        #right click on the product to open context menu
        while quantity_to_take > 0:
            wait(0.2)
            if quantity_to_take < 10:
                try:
                    doubleClick(product_loc)
                except:
                    return False
                else:
                    quantity_to_take -= 1
            else:
                self._slow_click(loc=product_loc, button="Right")
                if quantity_to_take >= 32:
                    if not self._slow_click(self._images.get_amount(32)):
                        return False
                    quantity_to_take -= 32
                elif quantity_to_take >= 10:
                    if not self._slow_click(self._images.get_amount(10)):
                        return False
                    quantity_to_take -= 10
        return True

    
    def go_to_confirmation(self):
        confirm_button = self._images.get_trade("confirm_button")
        self._slow_click(target=confirm_button)