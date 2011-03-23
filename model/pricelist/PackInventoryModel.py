from sikuli.Sikuli import *
path_to_bot = getBundlePath().split("bot.sikuli")[0]

import sys
sys.path.append(path_to_bot + "model/pricelist")
import InventoryAdapter


class PackInventoryModel(object):
    #DAL layer for pricelist for buying and selling packs
    def __init__(self):
        inventory_adapter = InventoryAdapter.InventoryAdapter()
        self.inventory = inventory_adapter.get_inventory(product="packs")
        
    #set prices is to be done in gui bot settings prior to transaction
    def set_buy_price(self, name, price):
        self.inventory[name.upper()]["buy"] = price
    def set_sell_price(self, name, price):
        self.inventiry[name.upper()]["sell"] = price
    
    def get_buy_price(self, name):
        return self.inventory[name]["buy"]
    def get_sell_price(self, name):
        return self.inventory[name]["sell"]
    
    def get_stock(self, pack_abbr):
        return self.inventory[pack_abbr]["stock"]
    def get_max_stock(self, pack_abbr):
        return self.inventory[pack_abbr]["max"]
        
    def get_sorted_pack_list(self):
        """this is a list of all pack to abbreviations in alphabetical order according to 
        their full names(which is how they are sorted by interface) which the bot should buy/sell"""
        all_packs = ["ALA", "ARB", "8ED", "M11", "M10", "MED", "ME2", "ME3", "ME4", "MBS", "9ED", "ROE", "SOM", "7ED", "10E", "WWK", "ZEN"]
        packs_to_buy_sell = [abbr for abbr in all_packs if abbr in self.inventory.keys()]
        return packs_to_buy_sell