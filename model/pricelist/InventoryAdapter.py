#handles reading and writing to pricelist files

from sikuli.Sikuli import *
path_to_bot = getBundlePath().split("bot.sikuli")[0]

#MySQL connection settings needed
exec(open(path_to_bot + "ini.py", "rb").read())

import sys, datetime
sys.path.append(path_to_bot + "model/pricelist")
sys.path.append(path_to_bot + "model/pricelist/db_adapter")

import Text
import Mysql
import CSVAdapter

class InventoryAdapter(object):
    def __init__(self, adapter):
        """
        @adapter: string
        sets and initiates functions for adapter
        """
        
        if adapter and isinstance(adapter, str):
            if adapter == "mysql":
                self.adapter = Mysql
            elif adapter == "txt":
                self.adapter = Text
            else:
                raise ErrorHandler("No adapter chosen.")
        else:
            raise ErrorHandler("Non-string value passed as adapter to InventoryAdapter.__init__")
    
    def read_inventory(self, product):
        """
        @product: string
        calls the read inventory method for previously specified adapter
        @return: dict
        """
        
        return self.adapter.get_product_info(product)