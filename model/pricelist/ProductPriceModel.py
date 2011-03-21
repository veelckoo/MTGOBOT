#handles reading and writing to pricelist files

from sikuli.Sikuli import *
path_to_bot = getBundlePath().split("bot.sikuli")[0]


class ProductPriceModel(object):
    
    def get_prices(self, product, list):
        """valid arguments for product are: "packs" or "cards", for list: "buy" or "sell" """
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
            single_product = newline.split("|")
            
            try:
                if list == "buy":
                    float(single_product[1].strip())
                elif list == "sell":
                    float(single_product[2].strip())
            except ValueError:
                sys.exit("A non-number found as a price for " + single_product[0] + " in in response to a " + list + " list request")
            product_name = str(single_product[0]).strip()
            
            #if there is no price next to the name of the product, then 
            try:
                if list == "buy":
                    product_price = float(single_product[2])
                elif list == "sell":
                    product_price = float(single_product[1])
            except IndexError:
                pass
            except ValueError:
                pass
            else:
                pricelist_dict[product_name.upper()] = product_price
        
        return pricelist_dict