

from sikuli.Sikuli import *
path_to_bot = getBundlePath().split("bot.sikuli")[0]

import sys, math
sys.path.append(path_to_bot + "model/pricelist")
import PackInventoryModel
import CardInventoryModel

sys.path.append(path_to_bot + "model")
import Product

sys.path.append(path_to_bot + "view")
import ITrade

class ISell(ITrade.ITrade):
    #this class is used when the bot is put into temporary sell mode during a trade or perma sell mode prior to trade
    
    def __init__(self):
        super(ISell, self).__init__()
        self.pack_inventory = PackInventoryModel.PackInventoryModel()
        self.card_inventory = CardInventoryModel.CardInventoryModel()
    
    def search_for_products(self):
        #searches a certain area for any image in a dictionary

        #combine all cards and packs for sale into a list
        product_names_list = self.pack_inventory.get_sorted_pack_list() + self.card_inventory.get_card_name_list()
        product_names_list.sort()
        numbers_list = self._images.get_all_numbers_as_dict(category="trade", phase="preconfirm")

        #if area searched contains a full sized scroll bar, then scroll down
        #variable to hold last mouse position for the scrollbar movement code
        self.last_mouse_position = False
        #list of all images found
        products = []

        #keep a record of product names found to prevent duplicates
        regular_scroll_bar = None
        mini_scroll_bar = None
        scroll_bar = self.giving_window_region.exists(self._images.get_trade(("scroll_bar_regular")))
        if not scroll_bar:
            scroll_bar = self.giving_window_region.exists(self._images.get_trade(("scroll_bar_mini")))
        #hover over scroll bar for mouse wheel manipulation
        scroll_bar_loc = scroll_bar.getTarget()
        #scan_region will be used as the region to scan for the packs and number of packs
        #using the giving window as region, each product row is scanned for a product name and quantity
        #NOTE: A single area reserved for the text of a single product is a 192px(width) by 16/17px(height) area, with a 1px buffer in between each string
        scan_region = Region(self.giving_window_region.getX()+2, self.giving_window_region.getY()+43, 196, 17)
        #keep while loop as long as there is still a pack to be scanned
        found = True
        while found:
            found = None
            for product_name in product_names_list:
                #if the product name to check is not a pack name, it must be a card name, if not then skip the product
                #because there is no png file for the product
                try:
                    product = self._images.get_pack_text(phase="preconfirm", packname=product_name)
                except KeyError:
                    try:
                        product = self._images.get_card_text(phase="preconfirm", cardname=product_name)
                    except KeyError:
                        continue
                    else:
                        product_type = "card"
                else:
                    product_type = "pack"
                if scan_region.exists(Pattern(product).exact()):
                    found = True

                    for key in range(len(numbers_list)):
                        if key == 0:
                            continue
                        
                        searchPattern = Pattern(numbers_list[key]).exact()
                        if(scan_region.exists(searchPattern)):
                            amount = key
                            #for booster packs, there is a specific order in which they appear in the list,
                            #when a pack is found, remove all packs before and including that pack in the keys
                            #list as they will not appear any further below
                            pack_index = product_names_list.index(product_name)+1
                            product_names_list = product_names_list[pack_index:]
                            break
                    if product_type == "pack":
                        product = Product.Product(name = product_name, buy = self.pack_inventory.get_buy_price(product_name), sell = self.pack_inventory.get_sell_price(product_name), quantity = amount)
                    elif product_type == "card":
                        product = Product.Product(name = product_name, buy = self.card_inventory.get_buy_price(product_name), sell = self.card_inventory.get_sell_price(product_name), quantity = amount)
                    else:
                        raise ErrorHandler("Product type has not been set, but product detected")
                    products.append(product)

                    wheel(scroll_bar_loc, WHEEL_DOWN, 2)

                if found == True:
                    break

            #if first scan area was already set, then relative distance from last region
            #scan area will be slightly larger than estimated height of product slot to compensate for any variances, to compensate for larger region, the Y coordinate -1
            scan_region = Region(scan_region.getX(), scan_region.getY()+17, scan_region.getW(), scan_region.getH())
    
        #in case the customer has canceled the trade
        if self.app_region.exists(self._images.get_trade("canceled_trade")):
            return False
        
        return products
            
    def confirmation_scan(self, type=None):
        #does a scan depending on which type is requested.  Each pass should scan the window differently
        #to confirm that the correct
        
        #verify confirm window by checking for confirm cancel buttons, then set regions relative to those buttons
        confirm_button = exists(self._images.get_trade("confirm_button", "confirm"), 1200)
        
        if isinstance(confirm_button, Match):
            #keeps record of products found and their amount so far
            giving_products_found = []
            
            product_names_list = self.card_inventory.get_card_name_list() + self.pack_inventory.get_sorted_pack_list()
            product_names_list.sort()
            
            numbers = self._images.get_all_numbers_as_dict(category="trade", phase="preconfirm")
            #confirm products receiving
            #set the regions of a single product and and the amount slow
            #number region is 20px down and 260px to the left, 13px height and 30px wide, 4px buffer vertically
            receiving_number_region = Region(confirm_button.getX()-289, confirm_button.getY()+42, 34, 14)
            #height for each product is 13px, and 4px buffer vertically between each product slot
            receiving_name_region = Region(confirm_button.getX()-254, confirm_button.getY()+42, 160, 14)
            #confirm products giving
            giving_number_region = Region(confirm_button.getX()-291, confirm_button.getY()+391, 34, 14)
            giving_name_region = Region(confirm_button.getX()-257, confirm_button.getY()+391, 160, 14)
            #this is a variable that will hold the number of pixels to move down after scanning each area
            #between some rows, theres a 4 pixel space buffer, between others there is 5, this variable will hold
            #alternating numbers 4 or 5
            how_many_pixels_to_move_down = 0
            
            found = True
            while found:
                print("scanning region: " + str(giving_name_region.x) + ", " + str(giving_name_region.y) + ", " + str(giving_name_region.w) + ", " + str(giving_name_region.h))
                hover(Location(giving_number_region.getX(), giving_number_region.getY()))
                found=False
                for product_name in product_names_list:
                    
                    try:
                        product_image_filepath = self._images.get_pack_text(phase="confirm", packname=product_name)
                    except KeyError:
                        try:
                            product_image_filepath = self._images.get_card_text(phase="confirm", cardname=product_name)
                        except KeyError:
                            continue
                        else:
                            product_type = "card"
                    else:
                        product_type = "pack"
                    if giving_name_region.exists(Pattern(product_image_filepath).similar(0.8)):
                        print("found " + str(product_name))
                        #if still at 0 after for loop, error raised
                        amount = 0
                        for number in range(len(numbers)):
                            if number == 0:
                                continue
                            if giving_number_region.exists(Pattern(numbers[number]).similar(0.8)):
                                amount = number
                                print("found " + str(amount) + " copies")
                                #packs are listed in Magic in the same sequence they are listed in the list of pack keys,
                                #if a pack is found, all packs including it and before, are removed from the list of packs
                                #to search
                                product_index = product_names_list.index(product_name) + 1
                                product_names_list = product_names_list[product_index:]
                                break
                        if product_type == "pack":
                            product_obj = Product.Product(name=product_name, buy = self.pack_inventory.get_buy_price(product_name), sell = self.pack_inventory.get_sell_price(product_name), quantity=amount)
                        elif product_type == "card":
                            product_obj = Product.Product(name=product_name, buy = self.card_inventory.get_buy_price(product_name), sell = self.card_inventory.get_sell_price(product_name), quantity=amount)
                        else:
                            raise Errorhandler("Product type has not been set, but product detected")
                        giving_products_found.append(product_obj)
                                            
                        if amount == 0:
                            raise ErrorHandler("Could not find a number for product: " + str(product_abbr))
                        found=True
                        
                        if how_many_pixels_to_move_down != 17:
                            how_many_pixels_to_move_down = 17
                        else:
                            how_many_pixels_to_move_down =  18
                        giving_number_region = Region(giving_number_region.getX(), giving_number_region.getY()+how_many_pixels_to_move_down, giving_number_region.getW(), giving_number_region.getH())
                        giving_name_region = Region(giving_name_region.getX(), giving_name_region.getY()+how_many_pixels_to_move_down, giving_name_region.getW(), giving_name_region.getH())
                        break
            
            #get image of number expected to scan for it first, to save time, else search through all other numbers
            expected_number = 0
            for product in giving_products_found:
                expected_number += math.ceil(product["quantity"] * product["sell"])
            print("expected tickets: " + str(expected_number))
            if expected_number == 0:
                return False
            
            #in case the customer has canceled trade
            if self.app_region.exists(self._images.get_trade("canceled_trade")):
                return False

            hover(Location(receiving_number_region.getX(), receiving_number_region.getY()))
            ticket_text_image = Pattern(self._images.get_ticket_text()).similar(1)
            if receiving_name_region.exists(ticket_text_image):
                print("ticket image found")
                expected_number_image = Pattern(self._images.get_number(number=int(expected_number), category="trade", phase="confirm")).similar(0.7)
                print(str(expected_number_image))
                if receiving_number_region.exists(expected_number_image):
                    print("ticket amount image found")
                    return giving_products_found
                else:
                    return False
            
    def complete_sale(self):
        #calls calculate_tickets_to_take to get the number of tickets to take and proceeds to take them, 
        #does a check to make sure correct ticket amount was taken
        
        message_found = self.Ichat.wait_for_message(string="done", duration=120)
        
        #if user has canceled or there was any other problem
        if not message_found:
            self.cancel_trade()
            return False
        
        self.Ichat.type_msg("Calculating tickets to take.  Please wait..")
        
        products_giving = self.search_for_products()
        
        #calculate the number of tickets to take according to products found
        number_of_tickets = 0
        for product in products_giving:
            number_of_tickets += (product["quantity"]) * (product["sell"])
            
            
        #if user has canceled or there was any other problem
        if not products_giving or not number_of_tickets > 0:
            self.cancel_trade()
            return False
        
            
        self.filter_product_version(version="packs_tickets")
        
        tickets = self.app_region.exists(self._images.get_ticket())
        
        self.take_product(product_loc=tickets.getTarget(), quantity_to_take=number_of_tickets)
        
        #if trade was canceled or take tickets failed
        if not self.app_region:
            self.cancel_trade()
            return False
        
        self.go_to_confirmation()
        
        #returns an object that holds all products sold if successful scan
        #otherwise returns False
        products_sold = self.confirmation_scan()
        
        self.Ichat.close_current_chat()
        
        if products_sold:
            self._slow_click(target=self._images.get_trade("confirm_button", "confirm"))
            wait(Pattern(self._images.get_ok_button()), 600)
            self._slow_click(target=self._images.get_ok_button(), button="LEFT")
            return products_sold
            
        else:
            #if false returned, either customer canceled trade in conformation screen, or product check failed
            self.cancel_trade()
            return False