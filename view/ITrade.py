
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
        self.app_region.wait(Pattern(self._images.get_trade(type)).similar(0.9), FOREVER)
        return True
        
    def cancel_trade(self):
        #if trade has alreaady been canceled, then click ok, otherwise cancel the trade
        cancel_button = self.app_region.exists(self._images.get_trade("cancel_button"))
        if cancel_button:
            self._slow_click(loc=cancel_button.getTarget())
        else:
            cancel_button = self.app_region.exists(self._images.get_trade(subsection="confirm", filename="cancel_button"))
            if cancel_button:
                self._slow_click(loc=cancel_button.getTarget())
        yes_button = self.app_region.exists(self._images.get_trade("yes_button"), 5)
        if yes_button:
            self._slow_click(loc=yes_button.getTarget())
        ok_button = self.app_region.wait(self._images.get_ok_button(), 5)
        if ok_button:
            print("looking for ok")
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
        print("accept_trade")
        request_loc = self.app_region.exists(self._images.get_trade("yes_button"))
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
                doubleClick(product_loc)
                quantity_to_take -= 1
            else:
                self._slow_click(loc=product_loc, button="Right")
                if quantity_to_take >= 32:
                    self._slow_click(self._images.get_amount(32))
                    quantity_to_take -= 32
                elif quantity_to_take >= 10:
                    self._slow_click(self._images.get_amount(10))
                    quantity_to_take -= 10

    def filter_product_rarity(self, rarity):
        #filter product by rarity, only applies to cards
        #valid string values are: any, common, uncommon, rare, mythic
        confirm_button = self.app_region.exists(Pattern(self._images.trade["confirm_button"]).similar(0.9))
        rarity_menu_loc = Location(confirm_button.getX()+110, confirm_button.getY()-26)
        self._slow_click(loc=rarity_menu_loc)
        self._slow_click(target=self._images.trade["filters"]["rarity"][rarity])
        
    def filter_product_version(self, version):
        #go to the product filter options and filter all product searches
        #valid string values for filter argument: packs_tickets
        confirm_button = self.app_region.exists(Pattern(self._images.trade["confirm_button"]).similar(0.9))
        version_menu_loc = Location(confirm_button.getX()+210, confirm_button.getY()-26)
        self._slow_click(loc=version_menu_loc)
        self._slow_click(target=self._images.trade["filters"]["version"][version])
        
    def filter_product_set(self, set):
        #filter the search by the set the product was printed in
        confirm_button = self.app_region.exists(Pattern(self._images.trade["confirm_button"]).similar(0.9))
        set_menu_loc = Location(confirm_button.getX()+140, confirm_button.getY()-65)
        self._slow_click(loc=set_menu_loc)
        #if set isn't found, mouse wheel down the menu
        set_found = self.app_region.exists(self._images.trade["filters"]["set"][set])
        print("filter product set called with " + str(set))
        if not set_found:
            for i in range(39):
                click(self._images.trade["filters"]["set"]["scroll_down"])
            set_found = self.app_region.exists(self._images.trade["filters"]["set"][set])
            if not set_found:
                raise Exception("The filter option for set: " + str(set) + ", was not found")
                
        self._slow_click(target=self._images.trade["filters"]["set"][set])
        
    def go_to_confirmation(self):
        confirm_button = self._images.get_trade("confirm_button")
        self._slow_click(target=confirm_button)