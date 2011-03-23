from sikuli.Sikuli import *
path_to_bot = getBundlePath().split("bot.sikuli")[0]

exec(open(path_to_bot + "ini.py", "rb").read())

import sys
sys.path.append(path_to_bot + "model/pricelist")
import PackInventoryModel
import CardInventoryModel

sys.path.append(path_to_bot + "model")
import Product


sys.path.append(path_to_bot + "view")
import ITrade

class IBuy(ITrade.ITrade):
    #this class is used when the bot is put into buy mode during a trade
    
    def __init__(self):
        super(IBuy, self).__init__()
        self.pack_inventory = PackInventoryModel.PackInventoryModel()
        self.card_inventory = CardInventoryModel.CardInventoryModel()
    
    
    
    def search_for_packs(self, tickets_to_give=0):
        #will take all packs found in the customers collection and in buy list
        self.filter_product_version(version="packs_tickets")
        
        #we don't want to take tickets, just products
        if self.topmost_product_name_area.exists(self._images.get_ticket_text()):
            product_name_area = Region(self.topmost_product_name_area.getX(), self.topmost_product_name_area.getY()+16, self.topmost_product_name_area.getW(), self.topmost_product_name_area.getH())
            product_quantity_area = Region(self.topmost_product_quantity_area.getX(), self.topmost_product_quantity_area.getY()+16, self.topmost_product_name_area.getW(), self.topmost_product_name_area.getH())
        else:
            product_name_area = Region(self.topmost_product_name_area.getX(), self.topmost_product_name_area.getY(), self.topmost_product_name_area.getW(), self.topmost_product_name_area.getH())
            product_quantity_area = Region(self.topmost_product_quantity_area.getX(), self.topmost_product_quantity_area.getY(), self.topmost_product_name_area.getW(), self.topmost_product_name_area.getH())
            
        #holds the prices for all the packs
        prices = PackInventoryModel.PackInventoryModel()
        
        #a dict that holds images of the names of all packs
        pack_names_keys = self.pack_inventory.get_sorted_pack_list()
        #this will hold all the product objects that have been taken
        number_list = self._images.get_all_numbers_as_dict(category="trade", phase="preconfirm")
        
        
        #this variable is used as an indicator whether the while loop should keep iterating
        found = True
        
        while found:
            found = False
            #MTGO has a maximum of 75 products that can be given or taken in a single transaction
            if tickets_to_give  >= 75:
                break
            if self.number_of_products_taken >= 75:
                break
            
            for pack_abbr in pack_names_keys:
            
                max_buy = self.pack_inventory.get_max_stock(pack_abbr) - self.pack_inventory.get_stock(pack_abbr)
                if max_buy == 0:
                    continue
                    
                print("Looking for " + str(pack_abbr))
                try:
                    pack_text_filepath = self._images.get_pack_text(phase="preconfirm", packname=pack_abbr)
                except KeyError:
                    try:
                        pack_text_filepath = self._images.get_card_text(phase="preconfirm", cardname=pack_abbr)
                    except KeyError:
                        continue
                if product_name_area.exists(Pattern(pack_text_filepath).exact()):
                    print(pack_abbr + " found!")
                    
                    amount = 0
                    
                    print("Max amount to buy: " + str(max_buy))
                    
                    for num in range(len(number_list)):
                        if num == 0:
                            continue
                        print("checkiing for number " + str(number_list[num]))
                        if product_quantity_area.exists(Pattern(number_list[num]).similar(0.9)):
                            
                            
                            #make sure to buy only enough to fill up to maximum stock level
                            if num < max_buy:
                                #customer has less than your max buy, so take all that they have
                                amount = num
                            else:
                                #if customer has more packs then you want, only take however much you want
                                amount = max_buy if max_buy > 0 else 0
                            print("amount to take " + str(amount))
                            found = True
                            break
                            

                    if amount > 0:
                        #if the amount of products would push the ticket total or products total over 75, then take just enough to get to 75 or closest
                        if self.number_of_products_taken + amount > 75:
                            amount = 75 - self.number_of_products_taken
                        if tickets_to_give + (self.pack_inventory.get_buy_price(pack_abbr) * amount) > 75:
                            amount = int((75 - tickets_to_give) / self.pack_inventory.get_buy_price(pack_abbr))
                        print("amount = int((75 - " + str(tickets_to_give) + " / " + str(self.pack_inventory.get_buy_price(pack_abbr)) + ")")
                        print("amount = " + str(amount))
                        self.take_product(product_loc=product_name_area.getCenter(), quantity_to_take=amount)

                        pack_abbr_index = pack_names_keys.index(pack_abbr)+1
                        pack_names_keys = pack_names_keys[pack_abbr_index:]

                        pack_obj = Product.Product(name=pack_abbr, buy = self.pack_inventory.get_buy_price(pack_abbr), sell = self.pack_inventory.get_sell_price(pack_abbr), quantity=amount)
                        self.products_taken.append(pack_obj)
                        tickets_to_give += pack_obj["quantity"] * pack_obj["buy"]
                        print("running total for packs = " + str(tickets_to_give))
                        break
                    else:
                        break

        if self.app_region.exists(self._images.get_trade("canceled_trade")):
            return False
        else:
            return tickets_to_give

    def search_for_bulk_cards(self, tickets_to_give=0):
        #this will buy all rares, mythics, uncommons, and/or commons that the customer has available
        
        number_list = self._images.get_all_numbers_as_dict(category="trade", phase="preconfirm")
        
        self.filter_product_version("all_versions")
        
        #will iterate once for filtering by rarity then by set
        for filter, filter_settings in bulkcardbuying.iteritems():
            #MTGO has a maximum of 75 products that can be given or taken in a single transaction
            if tickets_to_give  >= 75:
                break
            if self.number_of_products_taken >= 75:
                break
                        
            if filter == "rarity":
                #will iterate once for each rarity that is set to "yes"
                for rarity, valid in filter_settings.iteritems():
                    if tickets_to_give >= 75:
                        break
                    if valid == "yes":
                        print("setting rarity to " + str(rarity))
                        self.filter_product_rarity(rarity=rarity)
                        #will iterate through all sets that are set to "yes"
                        for set in bulkcardbuying["set"]:
                            for setname, valid in set.iteritems():
                                if tickets_to_give >= 75:
                                    break
                                if valid == "yes":
                                    self.filter_product_set(set=setname)
                                    
                                    found = True
                                    while found:
                                        if tickets_to_give >= 75:
                                            break
                                        found = False
                                        for num in range(settings["BULK_BUY_OPTIONS"]["max_amount"]):
                                            print("checking number " + str(num))
                                            if num == 0:
                                                continue
                                            numbersearch = self.topmost_product_quantity_area.exists(Pattern(number_list[num]))
                                            
                                            if numbersearch:
                                                print(str(num) + " cards found, taking...")
                                                amount = num
                                                #if we've reached the maximum amount of products able to be traded at one time, then break
                                                if self.number_of_products_taken + amount > 75:
                                                        amount = 75 - self.number_of_products_taken
                                                if tickets_to_give + (settings["BULK_BUY_OPTIONS"]["prices"][rarity] * amount) > 75:
                                                    amount = int((75 - tickets_to_give) / settings["BULK_BUY_OPTIONS"]["prices"][rarity])
                                                print("amount = int((75 - " + str(tickets_to_give) + ") / " + str(settings["BULK_BUY_OPTIONS"]["prices"][rarity]))
                                                
                                                if amount <= 0:
                                                    break
                                                self.take_product(product_loc=self.topmost_product_name_area.getCenter(), quantity_to_take=num)
                                                tickets_to_give += settings["BULK_BUY_OPTIONS"]["prices"][rarity] * num
                                                card_obj = Product.Product(name=rarity + ", " + setname, buy=settings["BULK_BUY_OPTIONS"]["prices"][rarity], sell=0, quantity=amount)
                                                self.products_taken.append(card_obj)
                                                self.number_of_products_taken += num
                                                print("running total for bulk cards = " + str(tickets_to_give))
                                                found = True
                                                wait(0.5)
                                                break
        return tickets_to_give
    
    def search_for_specific_cards(self, tickets_to_give=0):
        #this will search for specific cards on the buy list to buy
        self.filter_product_version(version="all_versions")
        wait(1)
        searchfield = Location(self.confirm_button.x-220, self.confirm_button.y-28)
        searchbutton = Location(self.confirm_button.x-255, self.confirm_button.y-28)
        cards_taken = []
        number_list = self._images.get_all_numbers_as_dict(category="trade", phase="preconfirm")
        self.filter_product_version("all_versions")
        number_of_searches = 2 if settings["SEARCH_BUY_FOIL"] == "yes" else 1
        
        for cardname, inv in self.card_inventory.inventory.items():
            #MTGO has a maximum of 75 products that can be given or taken in a single transaction
            if tickets_to_give  >= 75:
                break
            if self.number_of_products_taken >= 75:
                break
            
            if tickets_to_give  >= 75:
                break
            if self.number_of_products_taken >= 75:
                break
                
            #check how many copies of the card to buy, if 0 cards are desired, skip to the next card on list
            max_buy = self.card_inventory.get_max_stock(cardname) - self.card_inventory.get_stock(cardname)
            if max_buy <= 0:
                continue

            print(str(cardname))
            click(searchfield)
            type(cardname + Key.ENTER)
            wait(2)
            cardsearch = self.topmost_product_name_area.exists(Pattern(self._images.get_card_text(cardname=cardname, phase="preconfirm")).similar(0.9))
            if cardsearch:
                #sweeps have to be done twice in case there is a foil version AND a regular version of card
                for x in range(number_of_searches):
                    print(cardname + " has been found!")
                    
                    print("Max amount to buy: " + str(max_buy))
                    
                    for num in range(len(number_list)):
                        if num == 0:
                            continue
                        
                        numbersearch = self.topmost_product_quantity_area.exists(Pattern(number_list[num]).similar(0.9))
                        
                        if numbersearch:
                            if num < max_buy:
                                    #customer has less than your max buy, so take all that they have
                                    amount = num
                            else:
                                #if customer has more packs then you want, only take however much you want
                                amount = max_buy if max_buy > 0 else 0
                            break
                    
                    if amount > 0:
                        if self.number_of_products_taken + amount > 75:
                            amount = 75 - self.number_of_products_taken
                        if tickets_to_give + (self.card_inventory.get_buy_price(cardname) * amount) > 75:
                            amount = int((75 - tickets_to_give) / self.card_inventory.get_buy_price(cardname))
                        
                        self.take_product(product_loc=self.topmost_product_name_area.getCenter(), quantity_to_take=amount)
                        wait(0.5)
                        card_obj = Product.Product(name=cardname, buy=self.card_inventory.get_buy_price(cardname), sell=self.card_inventory.get_sell_price(cardname), quantity=amount)
                        self.products_taken.append(card_obj)
                        self.number_of_products_taken += amount
                        tickets_to_give += amount * self.card_inventory.get_buy_price(cardname)
                        break
                    else:
                        break
                    
        if self.app_region.exists(self._images.get_trade("canceled_trade")):
            return False
        else:
            return tickets_to_give
    
    def search_for_products(self):
        #confirm button will be used for relative positioning the regions for products scanning in preconfirm stage
        self.confirm_button = self.app_region.exists(self._images.get_trade("confirm_button"), 30)
        #find the position in the window where the topmost product would be located
        
        self.topmost_product_name_area = Region(self.confirm_button.getX()-271, self.confirm_button.getY()+47, 159, 17)
        self.topmost_product_quantity_area = Region(self.confirm_button.getX()-113, self.confirm_button.getY()+47, 40, 17)
        self.top_most_product_set_area = Region(self.confirm_button.getX()+9, self.confirm_button.getY()+47, 63, 17)
        
        #sort button will be used for preconfirm stage
        self.name_sort_button_location = Location(self.confirm_button.getX()-231, self.confirm_button.getY()+23)
        self._slow_click(loc=self.name_sort_button_location)
        
        #variables to hold amount of tickets that should be given
        tickets_to_give = 0
        #list that holds all products that were taken, for post transaction recording purposes
        self.products_taken = []
        self.number_of_products_taken = 0
        
        #DEBUG
        tickets_to_give = self.search_for_packs(tickets_to_give=0)
        
        if settings["CARD_BUYING"] == "bulk":
            tickets_to_give = self.search_for_bulk_cards(tickets_to_give=tickets_to_give)
        elif settings["CARD_BUYING"] == "search":
            tickets_to_give = self.search_for_specific_cards(tickets_to_give=tickets_to_give)

        #if customer cancels trade
        if tickets_to_give is False:
            return False
        else:
            return tickets_to_give
        
    def preconfirm_scan_purchase(self, tickets_to_give):
        giving_name_region = Region(self.giving_window_region.getX()+35, self.giving_window_region.getY()+43, 197, 17)
        giving_number_region = Region(self.giving_window_region.getX()+3, self.giving_window_region.getY()+43, 30, 17)
        
        numbers_list = self._images.get_all_numbers_as_dict(category="trade", phase="preconfirm")
        
        if giving_name_region.exists(self._images.get_ticket_text(), 120):
            if giving_number_region.exists(numbers_list[int(tickets_to_give)], 180):
                return True
        
        return False
                
        
    def confirmation_scan(self, tickets_to_give):
        """will return number of tickets taken for transaction recording"""
        #verify confirm window by checking for confirm cancel buttons, then set regions relative to those buttons
        confirm_button = exists(self._images.get_trade("confirm_button", "confirm"), 1200)
        
        if not confirm_button:
            self._slow_click(loc=Pattern(self._images.get_trade["cancel_button"]))
        
        if isinstance(confirm_button, Match):
            print("confirmation scan, tickets_to_give = " + str(tickets_to_give))
            #keeps record of products found and their amount so far
            receiving_products_found = []
            
            card_names_list = self.card_inventory.get_card_name_list()
            product_names_list = card_names_list[:]
            product_names_list.extend(self.pack_inventory.get_sorted_pack_list())
            
            rarities_list = self._images.trade["confirm"]["rarity"]
            
            numbers = self._images.get_all_numbers_as_dict(category="trade", phase="preconfirm")
            #confirm products receiving
            #these regions correspond to a single row from each column
            #height for each product is 13px, and 4px buffer vertically between each product slot
            receiving_number_region = Region(confirm_button.getX()-289, confirm_button.getY()+41, 34, 17)
            receiving_name_region = Region(confirm_button.getX()-254, confirm_button.getY()+41, 160, 17)
            receiving_rarity_region = Region(confirm_button.getX()+340, confirm_button.getY()+41, 61, 17)
            receiving_set_region = Region(confirm_button.getX()+291, confirm_button.getY()+41, 45, 17)
            
            #confirm products giving
            giving_number_region = Region(confirm_button.getX()-291, confirm_button.getY()+391, 34, 17)
            giving_name_region = Region(confirm_button.getX()-257, confirm_button.getY()+391, 160, 17)
            #this is a variable that will hold the number of pixels to move down after scanning each area
            #between some rows, theres a 4 pixel space buffer, between others there is 5, this variable will hold
            #alternating numbers 4 or 5
            how_many_pixels_to_move_down = 0
            
            found=True
            if settings["CARD_BUYING"] == "search":
                while found:
                    found=False
                    #scan each product one by one for it's name and quantity
                    for product_abbr in product_names_list:
                        try:
                            product = self._images.get_pack_text(phase="confirm", packname=product_abbr)
                            current_product = "pack"
                        except KeyError:
                            try:
                                product = self._images.get_card_text(phase="confirm", cardname=product_abbr)
                            except KeyError:
                                continue
                            else:
                                current_product = "card"
                        print("searching for :" + str(product))
                        
                        if receiving_name_region.exists(Pattern(product).similar(0.8)):
                            print(product_abbr + " found!")
                            #if still at 0 after for loop, error raised
                            amount = 0
                            for number in range(len(numbers)):
                                if number == 0:
                                    continue
                                if receiving_number_region.exists(Pattern(numbers[number]).similar(0.8)):
                                    print(str(number) + " amount of " + product_abbr + " found!")
                                    amount = number
                                    
                                    #packs are listed in Magic in the same sequence they are listed in the list of pack keys,
                                    #if a pack is found, all packs including it and before, are removed from the list of packs
                                    #to search
                                    product_index = product_names_list.index(product_abbr) + 1
                                    product_names_list = product_names_list[product_index:]
                                    break
                            if current_product == "pack":
                                product_obj = Product.Product(name=product_abbr, buy=self.pack_inventory.get_buy_price(product_abbr), sell=self.pack_inventory.get_sell_price(product_abbr), quantity=amount)
                            elif current_product == "card":
                                product_obj = Product.Product(name=product_abbr, buy=self.card_inventory.get_buy_price(product_abbr), sell=self.card_inventory.get_sell_price(product_abbr), quantity=amount)
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
            else:
                #scan the rarity and the amount to calculate total price
                while found:
                    found = False
                    for rarity, file in rarities_list.iteritems():
                        print("Looking for " + str(file))
                        print("hovering at " + str(receiving_rarity_region.x) + ", " + str(receiving_rarity_region.y))
                        if receiving_rarity_region.exists(Pattern(file).similar(0.7)):
                            print("found a " + str(rarity))
                            
                            for number in range(len(numbers)):
                                if number == 0:
                                    continue
                                if receiving_number_region.exists(Pattern(numbers[number]).similar(0.8)):
                                    amount = number
                                    break

                            product_obj = Product.Product(name=str(rarity + "s"), buy=settings["BULK_BUY_OPTIONS"]["prices"][rarity], sell=0, quantity=amount)
                            receiving_products_found.append(product_obj)

                            if amount == 0:
                                raise ErrorHandler("Could not find a number for product: " + str(product_abbr))
                            found = True

                            if how_many_pixels_to_move_down != 17:
                                how_many_pixels_to_move_down = 17
                            else:
                                how_many_pixels_to_move_down = 18
                            receiving_number_region = Region(receiving_number_region.getX(), receiving_number_region.getY()+how_many_pixels_to_move_down, receiving_number_region.getW(), receiving_number_region.getH())
                            receiving_rarity_region = Region(receiving_rarity_region.getX(), receiving_rarity_region.getY()+how_many_pixels_to_move_down, receiving_rarity_region.getW(), receiving_rarity_region.getH())
                            
                            break
            
            
            #get image of number expected to scan for it first, to save time, else search through all other numbers
            expected_number = 0
            for product in receiving_products_found:
                expected_number += product["quantity"] * product["buy"]

            print("expected number of tickets " + str(expected_number))
            
            if expected_number == 0 or not expected_number == tickets_to_give:
                return False

            hover(Location(giving_number_region.getX(), giving_number_region.getY()))
            ticket_text_image = Pattern(self._images.get_ticket_text()).similar(1)
            if giving_name_region.exists(ticket_text_image):
                expected_number_image = Pattern(self._images.get_number(number=int(expected_number), category="trade", phase="confirm")).similar(0.7)
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
            self._slow_click(target=self._images.get_trade("list_view_collection_window"))
            
            running_total = self.search_for_products()
            
            if running_total == 0 or not running_total:
                cancel_button = self.app_region.exists(self._images.get_trade("cancel_button"))
                if cancel_button:
                    self.slow_click(loc=cancel_button.getTarget())
                self._slow_click(target=self._images.get_ok_button())
                return False
            
            total_tickets_notice = 'Please take %i tickets.' % running_total
            self.Ichat.type_msg(total_tickets_notice)
            
            #wait for the customer to get the tickets, then click confirm
            if not self.preconfirm_scan_purchase(running_total): 
                self._slow_click(loc=Pattern(self._images.get_trade["cancel_button"]))
            
            self.go_to_confirmation()
            
            #run a final confirmation scan to check the products and tickets taken
            products_bought = self.confirmation_scan(tickets_to_give=running_total)
            
            self.Ichat.close_current_chat()
        
            if products_bought:
                
                self._slow_click(target=self._images.get_trade("confirm_button", "confirm"))
                wait(Pattern(self._images.get_ok_button()), 600)
                self._slow_click(target=self._images.get_ok_button())
            
                return products_bought
                
            else:
                cancel_button = self.app_region.exists(self._images.get_trade("cancel_button", "confirm"))
                if cancel_button:
                    self._slow_click(loc=cancel_button.getTarget())
                self._slow_click(target=self._images.get_ok_button())
                return False
