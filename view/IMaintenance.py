from sikuli.Sikuli import *
path_to_bot = getBundlePath().rsplit("\\", 1)[0] + "\\"

import sys
sys.path.append(path_to_bot + "view")
import Interface
import CSVAdapter


class IMaintenance(Interface.Interface):
    
    def __init__(self):
        super(IChat, self).__init__()
        self.inventory = []
        self.CSVAdapter = CSVAdapter.CSVAdapter()
        
    def refresh_inventory(self, *filter):
        self.inventory = self.scan_inventory()
        
    def scan_inventory(self set=None, rarity=None, version=None):
        #scan your collection and return a dict of all products with given parameters
        click(self._images.menu["collection"])
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
        click()
        type(path_to_bot)
        click()
        type("inventory")
        
        self.inventory = self.CSVAdapter.read_inventory_file(path_to_csv=path_to_bot+"inventory.csv"):
        
        if self.inventory:
            return True
        
    def get_inventory():
        return self.inventory
        
    def transfer_inventory(self):
        pass
        
    def query_bot_network(self):
        pass
    