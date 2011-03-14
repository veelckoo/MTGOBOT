#handles reading and writing to pricelist files

from sikuli.Sikuli import *
path_to_bot = getBundlePath().split("bot.sikuli")[0]


class ProductPriceModel(object):
    
    def get_prices(self, pricelist):
        """valid arguments for pricelist are: "packs_buy", "packs_sell", "cards_buy", or "cards_sell" """
        #this will return a dictionary containg all the buy or sell prices for requested products
        try:
            raw_feed = open(path_to_bot + "pricelist/" + str(pricelist) + ".txt", "r")
        except IOError:
            print("file for " + str(pricelist) + " cannot be opened for reading")
            return False
        
        pricelist_dict = {}
        
        while True:
            newline = raw_feed.readline()
            if newline == "/n" or newline == "":
               break
            single_product = newline.split(" $")
            try:
                int(single_product[1])
            except ValueError:
                sys.exit("A non-number found as a price for " + single_product[0] + " in in response to a " + pricelist + " request")
            product_name = str(single_product[0])
            
            #if there is no price next to the name of the product, then 
            try:
                product_price = int(single_product[1])
            except IndexError:
                pass
            except ValueError:
                pass
            else:
                pricelist_dict[product_name.upper()] = product_price
        
        return pricelist_dict