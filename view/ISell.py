from sikuli.Sikuli import *
path_to_bot = getBundlePath().rsplit("\\", 1)[0] + "\\"

import sys, math

sys.path.append(path_to_bot + "model")
import Product

sys.path.append(path_to_bot + "view")
import ITrade
import FrameGrabTrade

class ISell(ITrade.ITrade):
    #this class is used when the bot is put into temporary sell mode during a trade or perma sell mode prior to trade
    
    def __init__(self):
        super(ISell, self).__init__()
        self.frame_grab = FrameGrabTrade.FrameGrabTrade()
        
    def search_for_products(self, credit=0):
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
        
        number_of_tickets_to_take = 0 - credit
        #keep a record of product names found to prevent duplicates
        
        #mouse will hover over scroll bar and wheel down after 
        scroll_bar_x_loc = self.giving_window_region.getX() + self.giving_window_region.getW() - 1
        scroll_bar_y_loc = self.giving_window_region.getY() + (self.giving_window_region.getH()/2)
        scroll_bar_loc= Location(scroll_bar_x_loc, scroll_bar_y_loc)
        
        #scan_region will be used as the region to scan for the packs and number of packs
        #using the giving window as region, each product row is scanned for a product name and quantity
        #NOTE: A single area reserved for the text of a single product is a 192px(width) by 16/17px(height) area, with a 1px buffer in between each string
        #scan_region = Region(self.giving_window_region.getX(), self.giving_window_region.getY()+43, 198, 17)
        
        giving_product_name_area = self.frame_grab.get_trade_frame(app_region=self.app_region, phase="preconfirm", frame_name="giving_window", subsection="product_name_area")
        giving_product_quantity_area = self.frame_grab.get_trade_frame(app_region=self.app_region, phase="preconfirm", frame_name="giving_window", subsection="product_quantity_area")
        
        #keep while loop as long as there is still a pack to be scanned
        found = True
        while found:
            found = False
            if giving_product_name_area.exists(self._images.trade["empty"]):
                print("blank line found")
                break
            print("scanning " + str(giving_product_name_area.x) + ", "  + str(giving_product_name_area.y) + ", "  + str(giving_product_name_area.w) + ", "  + str(giving_product_name_area.h))
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
                print("searching for " + str(product))
                if giving_product_name_area.exists(Pattern(product).exact()):
                    print("found " + str(product))
                    found = True

                    for key in range(len(numbers_list)):
                        if key == 0:
                            continue
                        
                        searchPattern = Pattern(numbers_list[key]).exact()
                        if(giving_product_quantity_area.exists(searchPattern)):
                            amount = key
                            #for booster packs, there is a specific order in which they appear in the list,
                            #when a pack is found, remove all packs before and including that pack in the keys
                            #list as they will not appear any further below
                            pack_index = product_names_list.index(product_name)
                            product_names_list = product_names_list[pack_index:]
                            break
                    
                    if product_type == "pack":
                        number_of_tickets_to_take += self.pack_inventory.get_sell_price(product_name) * amount
                    elif product_type == "card":
                        number_of_tickets_to_take += self.card_inventory.get_sell_price(product_name) * amount
                    else:
                        raise ErrorHandler("Product type has not been set, but product detected")
                    products.append(product)
                    if found:
                        break
                    else:
                        raise ErrorHandler("Unrecognized card found")
            wheel(scroll_bar_loc, WHEEL_DOWN, 2)
            
            #if after the mousewheel down action, the products have not moved, then move down a slot.
            #if the products have shifted up, that means the scroll bar moved and product scan slot should remain the same,
            #because there is a new product in the current product slot
            if giving_product_name_area.exists(self._images.get_pack_text(phase="preconfirm", packname=product_names_list[0])):
                #if first scan area was already set, then relative distance from last region
                #scan area will be slightly larger than estimated height of product slot to compensate for any variances, to compensate for larger region, the Y coordinate -1
                self.next_row(giving_product_name_area, giving_product_quantity_area)
            
        #in case the customer has canceled the trade
        if self.app_region.exists(self._images.get_trade("canceled_trade")):
            return False

        return number_of_tickets_to_take
            
    def confirmation_scan(self, tickets_to_take, credit=0):
        #does a scan depending on which type is requested.  Each pass should scan the window differently
        #to confirm that the correct
        
        #verify confirm window by checking for confirm cancel buttons, then set regions relative to those buttons
        confirm_button = exists(self._images.get_trade("confirm_button", "confirm"), 1200)
        
        if isinstance(confirm_button, Match):
            #keeps record of products found and their amount so far
            giving_products_found = {"packs":[], "cards":[]}
            
            product_names_list = self.card_inventory.get_card_name_list() + self.pack_inventory.get_sorted_pack_list()
            product_names_list.sort()
            
            numbers = self._images.get_all_numbers_as_dict(category="trade", phase="preconfirm")
            #confirm products receiving
            #set the regions of a single product and and the amount slow
            #number region is 20px down and 260px to the left, 13px height and 30px wide, 4px buffer vertically
            #receiving_number_region = Region(confirm_button.getX()-289, confirm_button.getY()+42, 34, 14)
            #height for each product is 13px, and 4px buffer vertically between each product slot
            #receiving_name_region = Region(confirm_button.getX()-257, confirm_button.getY()+42, 163, 14)
            receiving_number_region = self.frame_grab.get_trade_frame(app_region=self.app_region, phase="confirm", frame_name="taking_window", subsection="product_quantity_area")
            receiving_name_region = self.frame_grab.get_trade_frame(app_region=self.app_region, phase="confirm", frame_name="taking_window", subsection="product_name_area")
            
            
            giving_number_region = self.frame_grab.get_trade_frame(app_region=self.app_region, phase="confirm", frame_name="giving_window", subsection="product_quantity_area")
            giving_name_region = self.frame_grab.get_trade_frame(app_region=self.app_region, phase="confirm", frame_name="giving_window", subsection="product_name_area")
            
            #confirm products giving
            #giving_number_region = Region(confirm_button.getX()-291, confirm_button.getY()+391, 34, 14)
            #giving_name_region = Region(confirm_button.getX()-260, confirm_button.getY()+391, 163, 14)
            #this is a variable that will hold the number of pixels to move down after scanning each area
            #between some rows, theres a 4 pixel space buffer, between others there is 5, this variable will hold
            #alternating numbers 4 or 5
            
            found = True
            while found:
                if giving_name_region.exists(self._images.trade["empty"]):
                    break
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
                    print("searching for " + str(product_image_filepath))
                    if giving_name_region.exists(Pattern(product_image_filepath).exact()):
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
                            giving_products_found["packs"].append(product_obj)
                        elif product_type == "card":
                            product_obj = Product.Product(name=product_name, buy = self.card_inventory.get_buy_price(product_name), sell = self.card_inventory.get_sell_price(product_name), quantity=amount)
                            giving_products_found["cards"].append(product_obj)
                        else:
                            raise Errorhandler("Product type has not been set, but product detected")
                                            
                        if amount == 0:
                            raise ErrorHandler("Could not find a number for product: " + str(product_abbr))
                        found=True
                        if found:
                            break
                        else:
                            raise ErrorHandler("Unrecognized card found")
                self.next_row(giving_number_region, giving_name_region)
            
            #get image of number expected to scan for it first, to save time, else search through all other numbers
            expected_number = 0
            for product_type, products in giving_products_found.items():
                for product in products:
                    expected_number += product["quantity"] * product["sell"]
                    print(expected_number)
            expected_number -= credit
            print("expected tickets: " + str(expected_number))

            if not expected_number == tickets_to_take:
                return False

            #in case the customer has canceled trade
            if self.app_region.exists(self._images.get_trade("canceled_trade")):
                return False

            hover(Location(receiving_number_region.getX(), receiving_number_region.getY()))
            if expected_number > 0 and expected_number is not False:
                ticket_text_image = Pattern(self._images.get_ticket_text()).similar(1)
                if receiving_name_region.exists(ticket_text_image):
                    print("ticket image found")
                    expected_number_image = Pattern(self._images.get_number(number=int(math.ceil(expected_number)), category="trade", phase="confirm")).similar(0.9)
                    print(str(expected_number_image))
                    if receiving_number_region.exists(expected_number_image):
                        print("ticket amount image found")
                        return giving_products_found
                    else:
                        return False
            elif expected_number <= 0:
            
                return giving_products_found
            else:
                return False
    def complete_sale(self, customer_credit=0):
        #calls calculate_tickets_to_take to get the number of tickets to take and proceeds to take them, 
        #does a check to make sure correct ticket amount was taken
        
        message_found = self.Ichat.wait_for_message(string="done", duration=120)
        
        #if user has canceled or there was any other problem
        if not message_found:
            self.cancel_trade()
            return False
        
        self.Ichat.type_msg("Calculating tickets to take.  Please wait..")
        
        number_of_tickets = self.search_for_products() - customer_credit
        
        #if user has canceled or there was any other problem
        if number_of_tickets is False:
            self.cancel_trade()
            return False
        
        self.filter_product_version(version="packs_tickets")
        
        tickets = self.app_region.exists(self._images.get_ticket())
        
        if not tickets:
            self.cancel_trade()
            return False
        elif not self.take_product(product_loc=tickets.getTarget(), quantity_to_take=math.ceil(number_of_tickets)):
            self.cancel_trade()
            return False
        
        #if trade was canceled or take tickets failed
        if not self.app_region:
            self.cancel_trade()
            return False
        
        self.go_to_confirmation()
        
        #returns an object that holds all products sold if successful scan
        #otherwise returns False
        products_sold = self.confirmation_scan(tickets_to_take=number_of_tickets, credit=customer_credit)
        
        self.Ichat.close_current_chat()
        
        if products_sold:
            self._slow_click(target=self._images.get_trade("confirm_button", "confirm"))
            wait(Pattern(self._images.get_ok_button()), 600)
            self._slow_click(target=self._images.get_ok_button(), button="LEFT")
            products_sold["total_tickets"] = number_of_tickets
            print("total tickets = " + str(number_of_tickets))
            return products_sold
            
        else:
            #if false returned, either customer canceled trade in conformation screen, or product check failed
            self.cancel_trade()
            return False