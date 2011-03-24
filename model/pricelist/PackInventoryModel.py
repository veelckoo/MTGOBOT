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
        all_packs = ["alara reborn", "shards of alara", "conflux", "eighth edition", "magic 2011", "magic 2010", "masters edition",
                               "masters edition 2", "masters edition 3", "masters edition 4", "mirrodin besieged", "ninth edition", "rise of the eldrazi",
                               "scars of mirrodin", "seventh edition", "tenth edition", "worldwake", "zendikar"]
        packs_to_buy_sell = [abbr for abbr in all_packs if abbr in self.inventory.keys()]
        packs_to_buy_sell.sort()
        print(all_packs)
        print(self.inventory.keys())
        
        return packs_to_buy_sell