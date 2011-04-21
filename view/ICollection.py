#handles reading and writing to pricelist files

from sikuli.Sikuli import *
path_to_bot = getBundlePath().split("bot.sikuli")[0]

import sys, datetime
sys.path.append(path_to_bot + "view")

import Interface
import CSVAdapter

class ICollection(Interface.Interface):
    
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
        wait(0.5)
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
        wait(0.2)
        click(self._images.collection["explorer_file_path_bar"])
        wait(0.2)
        type(path_to_bot + "inventory")
        wait(0.2)
        doubleClick(self._images.collection["explorer_file_name_bar"])
        wait(0.2)
        wait(0.2)
        type(timestamp + ".csv")
        click(self._images.collection["explorer_save_button"])
        wait(0.5)
        return path_to_bot + "/" + timestamp + ".csv"
        
    def tradability_setup(self, packs_to_make_tradable, cards_to_make_tradable):
        """
        this will set all products in your collection to untradable, then individually
        set the tradability for all products passed as argument
        """
        click(self._images.menu["collection"])
        click(self._images.collection["sort_by_name"])
        rightClick(self._images.collection["sort_by_name"])
        click(self._images.collection["mark_all_untradable"])
        
        search_button = self.app_region.exists(self._images.collection["search_button"]).getTarget()
        search_bar = search_button
        search_bar.setX(search_bar.getX() + 30)
        
        for packname, amount in packs_to_make_tradable.items():
            click(search_bar)
            wait(0.2)
            type(packname + key.ENTER)
            
            product_location = self.app_region.exists(self._images.get_pack_text(phase="preconfirm", packname=packname))
            self.set_tradability(location=product_location, amount=amount)
        for cardname, amount in cards_to_make_tradable.items():
            click(search_bar)
            wait(0.2)
            type(cardname + key.ENTER)
            
            product_location = self.app_region.exists(self._images.get_card_text(phase="preconfirm", cardname=cardname))
            self.set_tradability(location=product_location, amount=amount)
            
    def set_tradability(self, location, amount):
        """
        Params is a location object of the product name, and amount to make tradable
        """
        amount_set = 0
        location_cache = {"mark_selected_tradable_to":False, "32": False, "10": False, "4": False, "3": False, "2": False, "1": False, "increase": False, "decrease": False}
        while amount_set > 0:
        
            rightClick(location)
            if location_cache["mark_selected_tradable_to"]:
                hover(location_cache["mark_selected_tradable_to"])
            else:
                location_cache["mark_selected_tradable_to"] = self.app_region.exists(self._images.collection["mark_selected_tradable_to"]).getTarget()
                hover(location_cache["mark_selected_tradable_to"])
                
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
                
            elif amount <= 3:
                if not location_cache["increase"]:
                    location_cache["increase"] = self.app_region.exists(Pattern(self._images.collection["increase_tradability"]).similar(0.9)).getTarget()
                click(location_cache["increase"])
                amount -= 1
                
    def create_inventory_file(self, inventory_info):
        inventory_info_formatted = []
        for productname, productinfo in inventory_info.items():
            tradable = productname["stock"] - productname["max"]
            single_line = productname + "," + productinfo["set"] + "," + productinfo["foil"] + "," + tradable
            inventory_info_formatted.append(single_line)
            
        self.CSVAdapter.generate_CSV_inventory(inventory_info_formatted)
    