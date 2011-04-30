from sikuli.Sikuli import *
path_to_bot = getBundlePath().rsplit("\\", 1)[0] + "\\"

import sys, copy
sys.path.append(path_to_bot + "model/pricelist")
import InventoryAdapter


class PackInventoryModel(object):
    #DAL layer for pricelist for buying and selling packs
    def __init__(self):
        self.inventory_adapter = InventoryAdapter.InventoryAdapter()
        self.inventory = self.inventory_adapter.read_inventory_from_db(product="packs")
    
    
    #set prices is to be done in gui bot settings prior to transaction
    def set_buy_price(self, name, price):
        self.inventory[name]["buy"] = price
    def set_sell_price(self, name, price):
        self.inventory[name]["sell"] = price
    
    def get_buy_price(self, name):
        return self.inventory[name]["buy"]
    def get_sell_price(self, name):
        return self.inventory[name]["sell"]
    
    def get_stock(self, pack_abbr):
        return self.inventory[pack_abbr]["stock"]
    def update_stock(self, pack):
        self.inventory_adapter.set_stock(product=pack)
        self.inventory = self.inventory_adapter.read_inventory_from_db(product="packs")
    def get_max_stock(self, pack_abbr):
        return self.inventory[pack_abbr]["max"]
    def get_min_stock(self, pack_abbr):
        return self.inventory[pack_abbr]["min"]
    
    def get_sorted_pack_list(self):
        """this is a list of all packs found in pricelist text file"""
        packs_inventory = [pack for pack in self.inventory]
        packs_inventory.sort()
        return packs_inventory
        
    def generate_inventory_file_info(self):
        inventory_info = {}
        for productname, productinfo in self.inventory.items():
            inventory_info[productname] = {"max": productinfo["max"], "min": productinfo["min"], "stock": productinfo["stock"], "set": productinfo["set"], "foil": productinfo["foil"]}
            
        return inventory_info