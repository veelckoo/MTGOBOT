from sikuli.Sikuli import *
path_to_bot = getBundlePath().split("bot.sikuli")[0]

exec(open(path_to_bot + "ini.py", "rb").read())

import sys
sys.path.append(path_to_bot + "model/pricelist")
import PackPricesDAL
import CardPricesDAL

sys.path.append(path_to_bot + "model")
import Product


sys.path.append(path_to_bot + "view")
import ITrade

class IBuy(ITrade.ITrade):
    #this class is used when the bot is put into buy mode during a trade
    
    def __init__(self):
        super(IBuy, self).__init__()
        self.__pack_prices = PackPricesDAL.PackPricesDAL()
        self.__card_prices = CardPricesDAL.CardPricesDAL()
    
    def take_all_copies_of_product(self):
        #this will keep taking the product until there are no more of that product
        pass

    def take_product(self, product_loc, quantity):
        #this will take all the packs from the given location
        #right click on the product to open context menu
        self._slow_click(loc=product_loc, button="Right")
        #take 32 at a time, until there are no more, Magic Online UI will give all if there are less than 32 left
        while quantity > 0:
            self._slow_click(self._images.get_amount(32))
            quantity -= 32

    def take_packs(self):
        #will take all packs found in the customers collection and in buy list
        self.filter_product_version(version="tickets_packs")
        
        #we don't want to take tickets, just products
        hover(Location(self.topmost_product_name_area.getX(), self.topmost_product_name_area.getY()))
        if self.topmost_product_name_area.exists(self._images.get_ticket_text()):
            self.topmost_product_name_area = Region(self.topmost_product_name_area.getX(), self.topmost_product_name_area.getY()+16, 159, 15)
            self.topmost_product_quantity_area = Region(self.topmost_product_quantity_area.getX(), self.topmost_product_quantity_area.getY()+16, 40, 15)
        
        
        #declare variable to hold amount of tickets the customer should take
        tickets_to_give = 0
        #holds the prices for all the packs
        prices = PackPricesDAL.PackPricesDAL()
        
        #a dict that holds images of the names of all packs
        pack_names_keys = self._images.get_pack_keys()
        #this will hold all the product objects that have been taken
        packs_taken = []
        number_list = self._images.get_all_numbers_as_dict(category="trade", phase="preconfirm")
        
        #this variable is used as an indicator whether the while loop should keep iterating
        found = True
        
        while found:
            found = False
            for pack_abbr in pack_names_keys:
                try:
                    pack_text_filepath = self._images.get_pack_text(phase="preconfirm", packname=pack_abbr)
                except KeyError:
                    try:
                        pack_text_filepath = self._images.get_card_text(phase="preconfirm", cardname=pack_abbr)
                    except KeyError:
                        continue
                if self.topmost_product_name_area.exists(Pattern(pack_text_filepath).similar(0.8)):
                    found = True
                    amount = 0
                    for num in range(len(number_list)):
                        if num == 0:
                            continue
                        if self.topmost_product_quantity_area.exists(Pattern(number_list[num]).similar(0.9)):
                            amount = num
                            self.take_product(product_loc=self.topmost_product_name_area.getCenter(), quantity=amount)
                            break

                    pack_abbr_index = pack_names_keys.index(pack_abbr)+1
                    pack_names_keys = pack_names_keys[pack_abbr_index:]
                    
                    if amount == 0:
                        raise ErrorHandler("Found 0 of " + str(pack_abbr))
                    
                    pack_obj = Product.Product(name=pack_abbr, buy = self.__pack_prices.get_buy_price(pack_abbr), sell = self.__pack_prices.get_sell_price(pack_abbr), quantity=amount)
                    packs_taken.append(pack_obj)
                    break
        
        for pack in packs_taken:
            tickets_to_give += pack["quantity"] * pack["buy"]
        
        if self.app_region.exists(self._images.get_trade("canceled_trade")):
            return False
        else:
            return tickets_to_give
    
    def take_bulk_cards(self):
        #this will buy all rares, mythics, uncommons, and/or commons that the customer has available
        tickets_to_give = 0
        
        for filter, valid in bulkcardbuying.iteritems():
            if valid is "yes":
                self.filter_product_rarity(rarity=filter)
                for setname, valid in bulkcardbuying["set"].iteritems():
                    if valid is "yes":
                        self.filter_product_set(set=setname)
                        #sort cards alphabetically
                        click(self.name_sort_button_location)
                    product_name_region = Region(self.confirm_button.getX()-271, self.confirm_button.getY()+47, 159, 15)
                    product_quantity_region = Region(self.confirm_button.getX()-113, self.confirm_button.getY()+47, 40, 15)
                    
                    
        return tickets_to_give
    
    def take_specific_cards(self):
        #this will search for specific cards on the buy list to buy
        self.filter_product_version(version="all_versions")
        searchfield = Location(self.confirm_button.x-220, self.confirm_button.y-28)
        searchbutton = Location(self.confirm_button.x-255, self.confirm_button.y-28)
        cards_taken = []
        
        number_list = self._images.get_all_numbers_as_dict(category="trade", phase="preconfirm")
        
        for card in self.__card_prices.buy:
            print(str(card))
            click(searchfield)
            type(card + Key.ENTER)
            wait(2)
            cardsearch = self.topmost_product_name_area.exists(Pattern(self._images.get_card_text(phase="preconfirm", cardname=card)).similar(0.9))
            if cardsearch:
                print(card + " has been found!")
                for num in range(len(number_list)):
                    if num == 0:
                        continue
                    numbersearch = self.topmost_product_quantity_area.exists(Pattern(number_list[num]).similar(0.9))
                    if numbersearch:
                        print(str(num) + " = amount")
                        amount = num
                        self.take_product(product_loc=self.topmost_product_name_area.getCenter(), quantity=amount)
                        wait(1)
                        break
                card_obj = Product.Product(name=card, buy=self.__card_prices.get_buy_price(card), sell=self.__card_prices.get_sell_price(card), quantity=amount)
                cards_taken.append(card_obj)
        
        tickets_to_give = 0
        
        for card in cards_taken:
            tickets_to_give += card["quantity"] * card["buy"]
        
        if self.app_region.exists(self._images.get_trade("canceled_trade")):
            return False
        else:
            return tickets_to_give
    
    def take_products(self):
        #confirm button will be used for relative positioning the regions for products scanning in preconfirm stage
        self.confirm_button = self.app_region.exists(self._images.get_trade(filename="confirm_button"), 30)
        #find the position in the window where the topmost product would be located
        
        self.topmost_product_name_area = Region(self.confirm_button.getX()-271, self.confirm_button.getY()+47, 159, 15)
        self.topmost_product_quantity_area = Region(self.confirm_button.getX()-113, self.confirm_button.getY()+47, 40, 15)
        self.top_most_product_set_area = Region(self.confirm_button.getX()+9, self.confirm_button.getY()+47, 63, 15)
        
        #sort button will be used for preconfirm stage
        self.name_sort_button_location = Location(self.confirm_button.getX()-231, self.confirm_button.getY()+23)
        self._slow_click(loc=self.name_sort_button_location)
        
        tickets_to_give = 0
        #DEBUG
        #tickets_to_give += self.take_packs()

        if settings["CARD_BUYING"] == "all":
            tickets_for_cards = self.take_all_cards()
        elif settings["CARD_BUYING"] == "search":
            tickets_for_cards = self.take_specific_cards()

        #if customer cancels trade
        if tickets_for_cards is False:
            return False
        else:
            tickets_to_give += tickets_for_cards
        return tickets_to_give
        
    def preconfirm_scan_purchase(self):
        #will scan the giving and receiving window to see if items match
        taking_name_region = Region(self.taking_window_region.getX()+34, self.taking_window_region.getY()+45, 145, 17)
        taking_number_region = Region(self.taking_window_region.getX(), self.taking_window_region.getY()+45, 30, 17)
        
        giving_name_region = Region(self.giving_window_region.getX()+35, self.giving_window_region.getY()+43, 197, 17)
        giving_number_region = Region(self.giving_window_region.getX()+3, self.giving_window_region.getY()+43, 30, 17)
        
        pack_image_keys = self._images.get_pack_keys()
        
        numbers_list = self._images.get_all_numbers_as_dict(category="trade", phase="preconfirm")
        
        #will hold the name of all products found
        products_found = []
        
        #will hold all the Product objects of items found
        products_obj_found = []
        
        scroll_bar_loc = Location(self.giving_window_region.getX()+388, self.giving_window_region.getY()+80)
        found = True
        while True:
            found = False
            
            for pack_abbr in pack_image_keys:
                try:
                    product = self._images.get_pack_text(phase="preconfirm", packname=product_abbr)
                except KeyError:
                    try:
                        product = self._images.get_card_text(phase="preconfirm", cardname=product_abbr)
                    except KeyError:
                        continue
                
                if taking_name_region.exists(Pattern(product).similar(0.9)):
                    found = True
                    products_found.append(pack_abbr)
                    
                    
                    for number, number_img in range(len(Pattern(numbers_list).similar(0.8))):
                    
                        if taking_number_region.exists(number_img):
                            pack_obj = Product(name = pack_abbr, buy = self.__pack_prices.get_buy_price(pack_abbr), sell = self.__pack_prices.get_sell_price(pack_abbr), quantity = number)
                            products_obj_found.append(pack_obj)
                            break
                    break
            
            wheel(scroll_bar_loc, WHEEL_DOWN, 2)
        total_expected_tickets = 0
        for product in product_obj_found:
            total_expected_tickets += product["buy"] * product["quantity"]
        
        #wait 2 minutes for the customer to find event ticket, then 2 minutes to take the correct amount
        if giving_name_region.wait(Pattern(self._images.get_ticket_text()).similar(0.9), 120):
            giving_name_region.wait(Pattern(numbers_list[total_expected_tickets]).similar(0.9), 120)
            return True
        #if he still hasn't taken a ticket, then close the trade
        else:
            return False
        
    def confirmation_scan(self):
        """will return number of tickets taken for transaction recording"""
        #verify confirm window by checking for confirm cancel buttons, then set regions relative to those buttons
        confirm_button = exists(self._images.get_trade(filename="confirm_button", subsection="confirm"), 1200)
        
        if not confirm_button:
            self._slow_click(loc=Pattern(self._images.get_trade["cancel_button"]))
        
        if isinstance(confirm_button, Match):
            #keeps record of products found and their amount so far
            receiving_products_found = []
            pack_names_keys = self._images.get_pack_keys()
            product_names_list = pack_names_keys[:]
            product_names_list.extend(self._images.get_card_keys())
            
            numbers = self._images.get_all_numbers_as_dict(category="trade", phase="preconfirm")
            #confirm products receiving
            #set the regions of a single product and and the amount slow
            #number region is 20px down and 260px to the left, 13px height and 30px wide, 4px buffer vertically
            receiving_number_region = Region(confirm_button.getX()-289, confirm_button.getY()+41, 34, 14)
            #height for each product is 13px, and 4px buffer vertically between each product slot
            receiving_name_region = Region(confirm_button.getX()-254, confirm_button.getY()+41, 160, 14)
            #confirm products giving
            giving_number_region = Region(confirm_button.getX()-291, confirm_button.getY()+391, 34, 14)
            giving_name_region = Region(confirm_button.getX()-257, confirm_button.getY()+391, 160, 14)
            #this is a variable that will hold the number of pixels to move down after scanning each area
            how_many_pixels_to_move_down = 0
            
            found=True
            while found:
                hover(Location(receiving_number_region.getX(), receiving_number_region.getY()))
                found=False
                for product_abbr in product_names_list:
                    
                    try:
                        product = self._images.get_pack_text(phase="confirm", packname=product_abbr)
                    except KeyError:
                        try:
                            product = self._images.get_card_text(phase="confirm", packname=product_abbr)
                        except KeyError:
                            continue
                    
                    if receiving_name_region.exists(Pattern(product).similar(0.8)):
                        
                        #if still at 0 after for loop, error raised
                        amount = 0
                        for number in range(len(numbers)):
                            if number == 0:
                                continue
                            if receiving_number_region.exists(Pattern(numbers[number]).similar(0.8)):
                                amount = number
                                
                                #packs are listed in Magic in the same sequence they are listed in the list of pack keys,
                                #if a pack is found, all packs including it and before, are removed from the list of packs
                                #to search
                                product_index = product_names_list.index(product_abbr) + 1
                                product_names_list = product_names_list[product_index:]
                                break
                            
                        product_obj = Product.Product(name=product_abbr, buy = self.__pack_prices.get_buy_price(product_abbr), sell = self.__pack_prices.get_sell_price(product_abbr), quantity=amount)
                        receiving_products_found.append(product_obj)
                                            
                        if amount == 0:
                            raise ErrorHandler("Could not find a number for product: " + str(product_abbr))
                        found=True
                        
                        if how_many_pixels_to_move_down != 17:
                            how_many_pixels_to_move_down = 17
                        else:
                            how_many_pixels_to_move_down =  18
                        receiving_number_region = Region(receiving_number_region.getX(), receiving_number_region.getY()+how_many_pixels_to_move_down, receiving_number_region.getW(), receiving_number_region.getH())
                        receiving_name_region = Region(receiving_name_region.getX(), receiving_name_region.getY()+how_many_pixels_to_move_down, receiving_name_region.getW(), receiving_name_region.getH())
                        break
            
            #get image of number expected to scan for it first, to save time, else search through all other numbers
            expected_number = 0
            for product in receiving_products_found:
                expected_number += product["quantity"] * product["buy"]
            
            if expected_number == 0:
                return False
                
            hover(Location(giving_number_region.getX(), giving_number_region.getY()))
            ticket_text_image = Pattern(self._images.get_ticket_text()).similar(1)
            if giving_name_region.exists(ticket_text_image):
                expected_number_image = Pattern(self._images.get_number(number=expected_number, category="trade", phase="confirm")).similar(0.7)
                if giving_number_region.exists(expected_number_image):
                    
                    return receiving_products_found
                else:
                    return False
            
    def complete_purchase(self, method="A"):
        """Will return the transactions details to be recorded if successul
        else will return False"""
        
        if method == "A":
            #take the products first, then tell customer how many tickets to take
            #requires IChat interface to be passed to tell customers how many tickets to take
            
            #switch to list view in the collection window
            self._slow_click(target=self._images.get_trade(filename="list_view_collection_window"))
            
            running_total = self.take_products()
            
            if running_total == 0 or not running_total:
                cancel_button = self.app_region.exists(self._images.get_trade(filename="cancel_button"))
                if cancel_button:
                    self.slow_click(loc=cancel_button.getTarget())
                self._slow_click(target=self._images.get_ok_button())
                return False
            
            total_tickets_notice = 'Please take %i tickets.' % running_total
            self.Ichat.type_msg(total_tickets_notice)
            
            #scan the giving region area, if customer doesn't take ticket in time or scan files, cancel trade
            #if not self.preconfirm_scan_purchase(): 
            #    self._slow_click(loc=Pattern(self._images.get_trade["cancel_button"]))
            
            self.go_to_confirmation()
            
            #run a final confirmation scan to check the products and tickets taken
            products_bought = self.confirmation_scan()
            
            self.Ichat.close_current_chat()
        
            if products_bought:
                
                self._slow_click(target=self._images.get_trade(subsection="confirm", filename="confirm_button"))
                wait(Pattern(self._images.get_ok_button()), 600)
                self._slow_click(target=self._images.get_ok_button())
            
                return products_bought
                
            else:
                cancel_button = self.app_region.exists(self._images.get_trade(subsection="confirm", filename="cancel_button"))
                if cancel_button:
                    self.slow_click(loc=cancel_button.getTarget())
                self._slow_click(target=self._images.get_ok_button())
                return False
            
        elif method == "B":
            #let customer take tickets first, then take products totalling up to products taken
            #prompt users with IChat whether they want to sell cards, packs, or both
        
            #read the number of tickets taken
            number_of_tickets_taken = self.tickets_taken()
            
            self.Ichat.type_msg("Type \"packs\" to sell boosters, \"cards\" to sell singles")
            
            prompts = ["packs", "cards", "both"]
            
            response = self.Ichat.wait_for_message(prompts)
            
            if response == "packs":
                self.take_packs(number_of_tickets)
            elif response == "cards":
                self.take_cards(number_of_tickets)