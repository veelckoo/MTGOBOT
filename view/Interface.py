from sikuli.Sikuli import *
path_to_bot = getBundlePath().split("bot.sikuli")[0]

import sys
sys.path.append(path_to_bot + "model")
import ImagesModel

class Interface(object):
    #parent class for all Interface classes
    
    def __init__(self):
        self._images = ImagesModel.ImagesModel()
        
        magic_online = App("Magic Online")
        if not magic_online.window():
            raise ErrorHandler("Please open and log into Magic Online")
        else:
            self.app_region = magic_online.window()
            
    def _define_region(self, image=None):
        #defines the region of the screen where the Magic Online app is located
        #limiting the interaction to a region will help improve performance
        if not image:
            #if no image is supplied to search for the prompt user to define
            region = App.window("Magic Online")
            if(region):
                return region
            else:
                raise ErrorHandler("region variable still empty")
        else:
            #search for image and define it as region
            area = find(image)
            region = Region(area.getRect())
            return region

    def _slow_click(self, target = None, button = None, loc = None):
        #need to create parent class that has slow_click to pass on
        #will click on a target or location with designated mouse button
        wait(0.2)
        if loc == None:
            target_match = self.app_region.exists(target)
            
            #if click was called in middle of trade, check if it was cancelled
            if not target_match:
                if self.app_region.exists(self._images.get_trade("canceled_trade")):
                    return False
            loc = target_match.getTarget()
        if isinstance(loc, Location):
            hover(loc); wait(0.3)
        else:
            return False
        if(button == "Right"):
            mouseDown(Button.RIGHT); wait(0.3)
        else:
            mouseDown(Button.LEFT); wait(0.3)
        if(button == "Right"):
            mouseUp(Button.RIGHT)
        else:
            mouseUp(Button.LEFT)
        return True
        
    def filter_product_rarity(self, rarity):
        #filter product by rarity, only applies to cards
        #valid string values are: any, common, uncommon, rare, mythic
        confirm_button = self.app_region.exists(Pattern(self._images.trade["confirm_button"]).similar(0.9))
        rarity_menu_loc = Location(confirm_button.getX()+110, confirm_button.getY()-26)
        self._slow_click(loc=rarity_menu_loc)
        self._slow_click(target=self._images.filters["rarity"][rarity])
        
    def filter_product_version(self, version):
        #go to the product filter options and filter all product searches
        #valid string values for filter argument: packs_tickets
        confirm_button = self.app_region.exists(Pattern(self._images.trade["confirm_button"]).similar(0.9))
        version_menu_loc = Location(confirm_button.getX()+210, confirm_button.getY()-26)
        self._slow_click(loc=version_menu_loc)
        self._slow_click(target=self._images.filters["version"][version])
        
    def filter_product_set(self, set):
        #filter the search by the set the product was printed in
        confirm_button = self.app_region.exists(Pattern(self._images.trade["confirm_button"]).similar(0.9))
        set_menu_loc = Location(confirm_button.getX()+140, confirm_button.getY()-65)
        self._slow_click(loc=set_menu_loc)
        #if set isn't found, mouse wheel down the menu
        set_found = self.app_region.exists(self._images.filters["set"][set])
        if not set_found:
            for i in range(39):
                click(self._images.trade["filters"]["set"]["scroll_down"])
            set_found = self.app_region.exists(self._images.trade["filters"]["set"][set])
            if not set_found:
                raise Exception("The filter option for set: " + str(set) + ", was not found")
                
        self._slow_click(target=self._images.trade["filters"]["set"][set])
        