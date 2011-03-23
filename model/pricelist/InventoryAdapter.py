#handles reading and writing to pricelist files

from sikuli.Sikuli import *
path_to_bot = getBundlePath().split("bot.sikuli")[0]

class InventoryAdapter(object):
    
    def get_inventory(self, product):
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
                    in_stock = int(single_product[3].strip())
                    desired_stock = int(single_product[4].strip())
                    sell_price = float(single_product[1].strip())
                    buy_price = float(single_product[2].strip())
                    
            except ValueError:
                sys.exit("A non-number found for " + single_product[0] + " in inventory information in response to an inventory request")
            except IndexError:
                sys.exit("A value is missing for " + single_product[0] + " in inventory information in response to am inventory request")
                
            else:
                pricelist_dict[product_name.upper()] = {"sell": sell_price, "buy": buy_price, "stock": in_stock, "max": desired_stock}
        
        return pricelist_dict