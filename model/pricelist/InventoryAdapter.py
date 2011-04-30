#handles reading and writing to pricelist files

from sikuli.Sikuli import *
path_to_bot = getBundlePath().split("bot.sikuli")[0]

import sys, datetime
sys.path.append(path_to_bot + "view")

import CSVAdapter

class InventoryAdapter(object):

    def read_inventory_from_db(self, product):
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
