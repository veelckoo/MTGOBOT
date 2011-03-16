

from sikuli.Sikuli import *
path_to_bot = getBundlePath().split("bot.sikuli")[0]

import sys
sys.path.append(path_to_bot + "model/pricelist")
import PackPricesDAL
import CardPricesDAL

sys.path.append(path_to_bot + "model")
import Product

sys.path.append(path_to_bot + "view")
import ITrade

class ISell(ITrade.ITrade):
    #this class is used when the bot is put into temporary sell mode during a trade or perma sell mode prior to trade
    
    def __init__(self):
        super(ISell, self).__init__()
        self.__pack_prices = PackPricesDAL.PackPricesDAL()
        self.__card_prices = CardPricesDAL.CardPricesDAL()
        
    def tickets_to_take_for_cards(self):
        #scan which cards taken and how many and determine tickets to take ticket
        #found is a dictionary of all cards found, key is name of card, value is number taken
        found = []
        cards = self._image.get_cards()
        self.search_for_images_sale(region, cards)
        
    def tickets_to_take_for_packs(self):
        #scan the numbers of packs taken and determine number of tickets to take
        """
        returns the number of tickets to takes in the form of the Images.number[] format
        """
        
        #in case the user has canceled
        if not found:
            return False
            
        self.products_giving = found
        #calculate tickets to take
        total_tickets_to_take = self.calculate_products_to_tickets(found)
        
        #return the the number of packs that should be taken, number in image form
        return total_tickets_to_take
    
    def search_for_products(self):
        #searches a certain area for any image in a dictionary

        #combine all cards and packs for sale into a list
        pack_names_list = self._images.get_pack_keys()
        product_names_list = pack_names_list[:]
        product_names_list.extend(self._images.get_card_keys())
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
            for product_abbr in product_names_list:
                #if the product_abbr is not a pack name, it must be a card name, if not then skip the product
                try:
                    product = self._images.get_pack_text(phase="preconfirm", packname=product_abbr)
                except KeyError:
                    try:
                        product = self._images.get_card_text(phase="preconfirm", cardname=product_abbr)
                    except KeyError:
                        continue
                if scan_region.exists(Pattern(product).similar(0.9)):
                    found = True

                    for key in range(len(numbers_list)):
                        if key == 0:
                            continue
                        
                        searchPattern = Pattern(numbers_list[key]).similar(0.9)
                        if(scan_region.exists(searchPattern)):
                            amount = key
                            #for booster packs, there is a specific order in which they appear in the list,
                            #when a pack is found, remove all packs before and including that pack in the keys
                            #list as they will not appear any further below
                            pack_index = product_names_list.index(product_abbr)+1
                            product_names_list = product_names_list[pack_index:]
                            break

                    product = Product.Product(name = product_abbr, buy = self.__pack_prices.get_buy_price(product_abbr), sell = self.__pack_prices.get_sell_price(product_abbr), quantity = amount)
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

    def calculate_products_to_tickets(self, products_dict):
        #this takes all the products as a parameter and returns the number of tickets that should be taken
        running_total = 0
        for product in products_dict:
            running_total += (product["quantity"]) * (product["sell"])
        return running_total
    
    
    def take_ticket(self, number):
        #if loc cache is saved, then just click on saved locations, otherwise use image match
        #to find locations to click then save into cache then save into cache for next pass through loop
        location_cache = {}
        location_cache["ticket"] = None
        location_cache["take_10_tickets"] = None
        location_cache["take_4_tickets"] = None
        location_cache["take_1_tickets"] = None
        taken = 0
        while number - taken > 0:
            if number - taken >=10:
                click_result = self.click_tickets(take=10, taken=taken, cache=location_cache)
            elif number - taken < 10 and number - taken >= 4:
                click_result = self.click_tickets(take=4, taken=taken, cache=location_cache)
                
            #if less than 4 tickets, then take single tickets
            elif number - taken < 4:
                click_result = self.click_tickets(take=1, taken=taken, cache=location_cache)
            if not click_result:
                return False
            else:
                taken = click_result
        del(location_cache)
        return True
        
    def click_tickets(self, take, taken, cache):
        """this function is used in the take_ticket method, three required parameters are passed
        take=the number of tickets to take. taken=how many tickets have been taken, 
        this number will be returned after having added the numbers of tickets taken in this invocation.
        cache=the cached locations of the the buttons needed for this interaction
        click_check is used to see if the image could be found, if not this returns False,
        signifying that the trade was probably caneled"""
        
        #THIS METHOD IS IN NEED OF HEAVY OPTIMIZATION
        
        ticket_location = self.app_region.exists(self._images.get_ticket())
        if ticket_location:
            #first if else deals with caching ticket location if necessary
            if cache["ticket"] is None:
                if take == 1:
                    doubleClick(cache["ticket"])
                    taken += take
                    return taken
                else:
                    click_check = self._slow_click(loc=ticket_location.getTarget(), button="Right")
                    if not click_check:
                        return False
                cache["ticket"] = ticket_location.getTarget()
            else:
                if take == 1:
                    doubleClick(cache["ticket"])
                    taken += take
                    return taken
                click_check = self._slow_click(loc=cache["ticket"], button="Right")
                if not click_check:
                    return False
                    
            if cache["take_"+str(take)+"_tickets"] is None:
                self._slow_click(target=self._images.get_amount(take))
                cache["take_"+str(take)+"_tickets"] = Env.getMouseLocation()
                taken += take
            else:
                self._slow_click(loc=cache["take_"+str(take)+"_tickets"])
                taken += take
            return taken
        else:
            #no ticket found
            self.Ichat.type_msg("Not enough tickets available.")
            return False
    
    def return_ticket(self, number):
        #clicks on the decrease ticket to return one ticket
        pass
        
    def take_packs(self):
        #scans users collection for packs wanted
        pass

    def preconfirm_scan_sale(self, products_giving):
        """takes the total number of products taken by customer and checks to see if the correct amount of tickets are in the taking window"""
        numbers = self._images.get_all_numbers_as_dict(category="trade", phase="preconfirm")
        
        ticket = self._images.get_ticket_text()
        
        expected_total = 0
        for product in products_giving:
            expected_total += product["sell"]*product["quantity"]
        
        tickets_found = 0
        #product height = 17, width = 145, relative distance from upper left region corner, y = 46, x =35
        scan_region_product = Region(self.taking_window_region.getX()+34, self.taking_window_region.getY()+45, 145, 17)
        #product height = 17, width = 30, relative distance from upper left region corner, y = 46, x =1
        scan_region_number = Region(self.taking_window_region.getX(), self.taking_window_region.getY()+45, 30, 17)

        if scan_region_product.exists(ticket):
            #for performance, start the number scan with the expected number
            if scan_region_number.exists(self._images.get_number(number=expected_total, category="trade", phase="preconfirm")):
                tickets_found = expected_total
            #in case user canceled trade
            elif self.app_region.exists(self._images.get_trade("canceled_trade")):
                return False
            else:
                for number, number_image in numbers.items():
                    if scan_region_number.exists(number_image):
                        tickets_found = number
                        break
        print("Expected tickets: " + str(expected_total) + " and tickets found: " + str(tickets_found))
        if tickets_found >= expected_total:
            return True
        else:
            return False
  
    def confirmation_scan(self, type=None):
        #does a scan depending on which type is requested.  Each pass should scan the window differently
        #to confirm that the correct
        
        #verify confirm window by checking for confirm cancel buttons, then set regions relative to those buttons
        confirm_button = exists(self._images.get_trade(filename="confirm_button", subsection="confirm"), 1200)
        
        if isinstance(confirm_button, Match):
            #keeps record of products found and their amount so far
            giving_products_found = []
            pack_names_keys = self._images.get_pack_keys()
            product_names_list = pack_names_keys[:]
            product_names_list.extend(self._images.get_card_keys())
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
            found=True
            #scan the giving window
            hover(Location(receiving_number_region.getX(), receiving_number_region.getY()))
            wait(2)
            hover(Location(receiving_number_region.getX()+34, receiving_number_region.getY()+14))
            
            while found:
                hover(Location(giving_number_region.getX(), giving_number_region.getY()))
                found=False
                for product_abbr in pack_names_keys:
                    
                    try:
                        product = self._images.get_pack_text(phase="confirm", packname=product_abbr)
                    except KeyError:
                        try:
                            product = self._images.get_card_text(phase="confirm", cardname=product_abbr)
                        except KeyError:
                            continue
                        
                    if giving_name_region.exists(Pattern(product).similar(0.8)):
                        
                        #if still at 0 after for loop, error raised
                        amount = 0
                        for number in range(len(numbers)):
                            if number == 0:
                                continue
                            if giving_number_region.exists(Pattern(numbers[number]).similar(0.8)):
                                amount = number
                                
                                #packs are listed in Magic in the same sequence they are listed in the list of pack keys,
                                #if a pack is found, all packs including it and before, are removed from the list of packs
                                #to search
                                pack_index = pack_names_keys.index(product_abbr) + 1
                                pack_names_keys = pack_names_keys[pack_index:]
                                
                                break
                            
                        product_obj = Product.Product(name=product_abbr, buy = self.__pack_prices.get_buy_price(product_abbr), sell = self.__pack_prices.get_sell_price(product_abbr), quantity=amount)
                        giving_products_found.append(product_obj)
                                            
                        if amount == 0:
                            raise ErrorHandler("Could not find a number for product: " + str(product_abbr))
                        found=True
                        giving_number_region = Region(giving_number_region.getX(), giving_number_region.getY()+17, giving_number_region.getW(), giving_number_region.getH())
                        giving_name_region = Region(giving_name_region.getX(), giving_name_region.getY()+17, giving_name_region.getW(), giving_name_region.getH())
                        break
            
            #get image of number expected to scan for it first, to save time, else search through all other numbers
            expected_number = 0
            for product in giving_products_found:
                expected_number += product["quantity"] * product["sell"]
            
            if expected_number == 0:
                return False
            
            #in case the customer has canceled trade
            if self.app_region.exists(self._images.get_trade("canceled_trade")):
                return False

            hover(Location(receiving_number_region.getX(), receiving_number_region.getY()))
            ticket_text_image = Pattern(self._images.get_ticket_text()).similar(1)
            if receiving_name_region.exists(ticket_text_image):
                expected_number_image = Pattern(self._images.get_number(number=expected_number, category="trade", phase="confirm")).similar(0.7)
                if receiving_number_region.exists(expected_number_image):
                    
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
        
        number_of_tickets = self.calculate_products_to_tickets(products_giving)
        
        #if user has canceled or there was any other problem
        if not products_giving:
            self.cancel_trade()
            return False
        
        
        #if user has canceled or there was any other problem
        if not number_of_tickets:
            self.cancel_trade()
            return False
            
        self.filter_product_version(version="tickets_packs")
        
        take_result = self.take_ticket(number_of_tickets)
        
        #if trade was canceled or take tickets failed
        if not take_result:
            self.cancel_trade()
            return False
        
        
        preconfirm = self.preconfirm_scan_sale(products_giving=products_giving)
        
        #if trade was canceled or preconfirm failed
        if not preconfirm:
            self.cancel_trade()
            return False
        
        self.go_to_confirmation()
        #check to make sure correct number of tickets taken
        
        #INSERT PRE-FINAL TRANSACTION CHECK HERE#
        
        #scan confirmation screen multiple times in different ways before clicking final confirm
        
        #INSERT FINAL TRANSACTION CHECK HERE#
        
        #returns an object that holds all products sold if successful scan
        #otherwise returns False
        products_sold = self.confirmation_scan()
        
        self.Ichat.close_current_chat()
        
        if products_sold:
            self._slow_click(target=self._images.get_trade(subsection="confirm", filename="confirm_button"))
            wait(Pattern(self._images.get_ok_button()), 600)
            self._slow_click(target=self._images.get_ok_button(), button="LEFT")
            return products_sold
            
        else:
            #if false returned, either customer canceled trade in conformation screen, or product check failed
            cancel_button = self.app_region.exists(self._images.get_trade(subsection="confirm", filename="cancel_button"))
            if cancel_button:
                self.slow_click(cancel_button.getTarget())
            self._slow_click(target=self._images.get_ok_button())
            return False