#handles reading and writing to pricelist files

from sikuli.Sikuli import *
path_to_bot = getBundlePath().split("bot.sikuli")[0]

#MySQL connection settings needed
exec(open(path_to_bot + "ini.py", "rb").read())

import sys, datetime
sys.path.append(path_to_bot + "model/pricelist")
sys.path.append(path_to_bot + "model/pricelist/db_adapter")

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
                if settings["mysql"]["use"] == True:
                    self.adapter = "mysql"
                else:
                    raise ErrorHandler("MySQL settings have not been set or are invalid")
            else:
                self.adapter = "txt"
        else:
            raise ErrorHandler("Non-string value passed as adapter to InventoryAdapter.__init__")
    
    def read_inventory(self, product):
        """
        @product: string
        calls the read inventory method for previously specified adapter
        @return: dict
        """
        adapter_funcs = {"txt": self.read_inventory_from_txt, 
                         "mysql": self.read_inventory_from_mysql}
        if product == "packs" or product == "cards":
            try:
                return adapter_funcs[self.adapter](product)
            except KeyError:
                raise ErrorHandler("No adapters found for InventoryAdapter")
        else:
            raise ErrorHandler("Must pass either 'packs' or 'cards' to read_inventory")
    
    def read_inventory_from_mysql(self, product):
        """
        @product string
        will query MySQL db for pricing information
        """
        try:
            Mysql.connect(settings["mysql"]["url"], settings["mysql"]["username"], settings["mysql"]["password"])
        except:
            pass
        query_results = Mysql.query()
        if query_results == None:
            raise ErrorHandler("MySQL DB query returned None or there was an error")
        
        #do something with query results
        
        Mysql.close()
        
    
    def read_inventory_from_txt(self, product):
        """valid arguments for product are: "packs" or "cards" """
        #this will return a dictionary containg all the buy or sell prices for requested products
        try:
            raw_feed = open(path_to_bot + "pricelist/" + str(product) + ".txt", "r")
        except IOError:
            print("file for " + str(product) + " prices cannot be opened for reading")
            return False
        
        pricelist_dict = {}
        
        while True:
            newline = raw_feed.readline()
            
            if newline == "/n" or newline == "":
               break
            if "#" in newline:
                continue

            single_product = newline.split("|")
            
            try:
                    product_name = str(single_product[0]).strip()
                    set = str(single_product[1]).strip()
                    foil = str(single_product[2]).strip()
                    in_stock = int(single_product[5].strip())
                    max_stock = int(single_product[6].strip())
                    min_stock = int(single_product[7].strip())
                    sell_price = float(single_product[3].strip())
                    buy_price = float(single_product[4].strip())
                    
            except ValueError:
                sys.exit("A non-number found for " + single_product[0] + " in inventory information in response to an inventory request")
            except IndexError:
                sys.exit("A value is missing for " + single_product[0] + " in inventory information in response to am inventory request")
                
            else:
                pricelist_dict[product_name] = {"sell": sell_price, "buy": buy_price, "stock": in_stock, "min": min_stock, "max": max_stock, "set": set, "foil": foil}
        
        return pricelist_dict
    
    def update_inventory(self, product, update_info):
        """
        @product: string, update_info: dict
        calls the update inventory method for previously specified adapter
        @return: boolean, or Exception if passed incorrect product var
        """
        adapter_funcs = {"txt": self.update_inventory_from_txt, 
                         "mysql": self.update_inventory_from_mysql,
                         "excel": self.update_inventory_from_excel}
        if product == "packs" or product == "cards":
            if adapter_funcs[self.adapter](product, update_info):
                return True
            else:
                return False
        else:
            raise ErrorHandler("Must pass either 'packs' or 'cards' to read_inventory")