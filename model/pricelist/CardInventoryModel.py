from sikuli.Sikuli import *
path_to_bot = getBundlePath().split("bot.sikuli")[0]

import sys, copy
sys.path.append(path_to_bot + "model/pricelist")
import InventoryAdapter


class CardInventoryModel(object):
    #DAL layer for pricelist for buying and selling single cards
    def __init__(self):
        self.inventory_adapter = InventoryAdapter.InventoryAdapter()
        self.inventory = self.inventory_adapter.read_inventory_from_db(product="cards")
        
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
    def update_stock(self, card):
        self.inventory_adapter.set_stock(product=card)
        self.inventory = self.inventory_adapter.read_inventory_from_db(product="packs")
    def get_max_stock(self, pack_abbr):
        return self.inventory[pack_abbr]["max"]
    
    def get_card_name_list(self):
        return [cardname for cardname in self.inventory.keys()]
        
    def generate_inventory_file_info(self):
        inventory_info = {}
        for productname, productinfo in self.inventory:
            inventory[productname] = {"max": productinfo["max"], "stock": productinfo["stock"], "set": productinfo["set"], "foil": productinfo["foil"]}
            
        return inventory_info