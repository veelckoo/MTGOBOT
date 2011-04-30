#handles reading and writing to pricelist files

from sikuli.Sikuli import *
path_to_bot = getBundlePath().split("bot.sikuli")[0]

import sys, datetime
sys.path.append(path_to_bot + "view")

import Interface
import CSVAdapter

class ICollection(Interface.Interface):
    def __init__(self):
        super(ICollection, self).__init__()
        self.CSVAdapter = CSVAdapter.CSVAdapter()
    
    def export_inventory_file(self, set=None, rarity=None, version=None):
        """
        will export all products with given params to a csv file.
        if param is omitted, then that filter will not be set.
        e.g. if no filters set, the will export all products to csv file
        """
        #scan your collection and return a dict of all products with given parameters
        timestamp = str(datetime.datetime.now())
        timestamp = timestamp.replace(":", " ")
        click(self._images.menu["collection"])
        wait(1)
        if set:
            self.filter_product_set(set=set)
        if rarity:
            self.filter_product_rarity(rarity=rarity)
        if version:
            self.filter_product_version(version=version)
        rightClick(Region(App("Magic Online").window()))
        click(self._images.collection["select_all"])
        rightClick(Region(App("Magic Online").window()))
        click(self._images.collection["export_to_csv"])
        wait(1)
        click(Pattern(self._images.collection["explorer_file_path_bar"]).similar(0.5))
        wait(1)
        type(path_to_bot + "inventory" + Key.ENTER)
        wait(1)
        doubleClick(self._images.collection["explorer_file_name_bar"])
        wait(1)
        type(timestamp + ".csv")
        click(self._images.collection["explorer_save_button"])
        wait(1)
        return path_to_bot + "/" + timestamp + ".csv"
        
    def tradability_setup(self, packs_to_make_tradable, cards_to_make_tradable):
        """
        this will set all products in your collection to untradable, then individually
        set the tradability for all products passed as argument
        """
        click(self._images.menu["collection"])
        click(Region(App("Magic Online").window()))
        rightClick(self._images.collection["sort_by_name"])
        click(Pattern(self._images.collection["mark_all_untradable"]).similar(0.5))
        
        products_to_make_tradable = dict(packs_to_make_tradable.items() + cards_to_make_tradable.items())
        self.create_inventory_file(inventory_info=products_to_make_tradable);wait(1)
        rightClick(Region(App("Magic Online").window()));wait(1)
        click(Pattern(self._images.collection["import_trade_data"]).similar(0.5));wait(1)
        click(Pattern(self._images.collection["explorer_file_path_bar"]).similar(0.5));wait(1)
        type(path_to_bot + "inventory" + Key.ENTER);wait(1)
        doubleClick(self._images.collection["explorer_file_name_bar"])
        type("trade_data.csv" + Key.ENTER)
        
        
    def set_tradability(self, location, amount):
        """
        Params is a location object of the product name, and amount to make tradable
        """
        location_cache = {"mark_selected_tradable_to":False, "32": False, "10": False, "4": False, "3": False, "2": False, "1": False, "increase": False, "decrease": False}
        while amount > 0:
        
            rightClick(location)
            if amount <= 3:
                if location_cache["mark_selected_tradable_to"]:
                    hover(location_cache["mark_selected_tradable_to"].getTarget())
                else:
                    print(str(self._images.collection["mark_selected_tradable_to"]))
                    location_cache["mark_selected_tradable_to"] = self.app_region.exists(self._images.collection["mark_selected_tradable_to"])
                    hover(location_cache["mark_selected_tradable_to"].getTarget())
                    
                if amount >= 32:
                    if not location_cache["32"]:
                        location_cache["32"] = self.app_region.exists(Pattern(self._images.collection["32"]).similar(0.9)).getTarget()
                    click(location_cache["32"])
                    amount -= 32
                    
                elif amount >= 10:
                    if location_cache["10"]:
                        location_cache["32"] = self.app_region.exists(Pattern(self._images.collection["10"]).similar(0.9)).getTarget()
                    click(location_cache["10"])
                    amount -= 10
                    
                elif amount >= 4:
                    if not location_cache["4"]:
                        location_cache["4"] = self.app_region.exists(Pattern(self._images.collection["4"]).similar(0.9)).getTarget()
                    click(location_cache["4"])
                    amount -= 4
            else:
                if not location_cache["increase"]:
                    location_cache["increase"] = self.app_region.exists(Pattern(self._images.collection["increase_tradability"]).similar(0.9)).getTarget()
                click(location_cache["increase"])
                amount -= 1
                
    def create_inventory_file(self, inventory_info):
        inventory_info_formatted = []
        for productname, productinfo in inventory_info.items():
            tradable = productinfo["stock"] - productinfo["min"]
            if tradable < 0:
                tradable = 0
            single_line = productname + "," + productinfo["set"] + "," + productinfo["foil"] + "," + str(tradable)
            inventory_info_formatted.append(single_line)
            
        self.CSVAdapter.create_inventory_file(inventory_info_formatted)
    