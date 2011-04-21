from sikuli.Sikuli import *
path_to_bot = getBundlePath().rsplit("\\", 1)[0] + "\\"

import sys
sys.path.append(path_to_bot + "view")
import Interface
import InventoryAdapter

sys.path.append(path_to_bot + "model/pricelist")
import CardInventoryModel, PackInventoryModel
import ICollection

class IMaintenance(Interface.Interface):
    
    def __init__(self):
        super(IChat, self).__init__()
        self.ICollection
        self.inventory_adapter = InventoryAdapter.InventoryAdapter()
        self.card_pricelist_adapter = CardInventoryModel.CardInventoryModel()
        self.pack_pricelist_adapter = PackInventoryModel.PackInventoryModel()
        
    def refresh_inventory(self, rarity=None, set=None, version=None):
        del(self.inventory)
        try:
            self.inventory = self.inventory_adapter.get_inventory(rarity=rarity, set=set, version=verion)
        except:
            return False
        else:
            return True
            
    def get_inventory(self, rarity=None, set=None, version=None):
        try:
            self.inventory = self.inventory_adapter.get_inventory(rarity=rarity, set=set, version=verion)
        except:
            return False
        else:
            return True
    
    def set_tradable(self):
        self.inventory_adapter.set_all_untradable()
        for cardname, cardstats in self.inventory.items():
            click()
            type(cardname)
    
    def transfer_inventory(self):
        pass
        
    def query_bot_network(self):
        pass
    