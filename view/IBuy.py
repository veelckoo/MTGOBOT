from sikuli.Sikuli import *
path_to_bot = getBundlePath().rsplit("\\", 1)[0] + "\\"

exec(open(path_to_bot + "ini.py", "rb").read())

import sys, math

sys.path.append(path_to_bot + "model")
import Product


sys.path.append(path_to_bot + "view")
import ITrade
import FrameGrabTrade

class IBuy(ITrade.ITrade):
    #this class is used when the bot is put into buy mode during a trade
    
    def __init__(self):
        super(IBuy, self).__init__()
        self.frame_grab = FrameGrabTrade.FrameGrabTrade()
    
    def search_for_packs(self, tickets_to_give=0.0):
        #will take all packs found in the customers collection and in buy list
        self.filter_product_version(version="packs_tickets")
        
        product_name_area = self.frame_grab.get_trade_frame(app_region=self.app_region, phase="preconfirm", frame_name="collection", subsection="product_name_area")
        product_quantity_area = self.frame_grab.get_trade_frame(app_region=self.app_region, phase="preconfirm", frame_name="collection", subsection="product_quantity_area")
        
        if product_name_area.exists(self._images.get_ticket_text()):
            product_name_area.setY(product_name_area.getY()+16)
            product_quantity_area.setY(product_quantity_area.getY()+16)
        
        searchfield = self.frame_grab.searchfield(app_region=self.app_region)
        searchbutton = self.frame_grab.searchbutton(app_region=self.app_region)
        
        #a dict that holds images of the names of all packs
        pack_names_keys = self.pack_inventory.get_sorted_pack_list()
        #this will hold all the product objects that have been taken
        number_list = self._images.get_all_numbers_as_dict(category="trade", phase="collection")
        
        
        #this variable is used as an indicator whether the while loop should keep iterating
        found = True
        
        while found:
            if product_name_area.exists(self._images.trade["empty"]):
                break
            found = False
            #MTGO has a maximum of 75 products that can be given or taken in a single transaction
            if tickets_to_give  >= settings["MAX_PRODUCTS_PER_TRADE"]:
                break
            if self.number_of_products_taken >= settings["MAX_PRODUCTS_PER_TRADE"]:
                break
            
            for packname in pack_names_keys:
                try:
                    pack_text_filepath = self._images.get_pack_text(phase="preconfirm", packname=packname)
                except KeyError:
                    print(str(packname) + "not found")
                    continue
                
                print("searching for " + str(pack_text_filepath))
                print("at " + str(product_name_area.x) + " " + str(product_name_area.y) + " " + str(product_name_area.w) + " " + str(product_name_area.h))
                
                if product_name_area.exists(Pattern(pack_text_filepath).exact()):
                    print(pack_text_filepath + " found!")
                    found = True
                    
                    current_product_location = product_name_area.getCenter()
                    
                    max_buy = self.pack_inventory.get_max_stock(packname) - self.pack_inventory.get_stock(packname)
                    if max_buy <= 0:
                        self.next_row(product_name_area, product_quantity_area)
                        pack_abbr_index = pack_names_keys.index(packname)
                        pack_names_keys = pack_names_keys[pack_abbr_index:]
                        print("shifting down 1")
                        break
                        
                    
                    amount = 0
                    
                    print("Max amount to buy: " + str(max_buy))
                    
                    for num in range(len(number_list)):
                        if num == 0:
                            continue
                        print("checkiing for number " + str(number_list[num]))
                        print("scan region: " + str(product_quantity_area.x) + " " + str(product_quantity_area.y) + " " + str(product_quantity_area.w) + " " + str(product_quantity_area.h) + " ")
                        if product_quantity_area.exists(Pattern(number_list[num]).similar(0.9)):
                            #make sure to buy only enough to fill up to maximum stock level
                            if num <= max_buy:
                                #customer has less than your max buy, so take all that they have
                                amount = num
                            else:
                                #if customer has more packs then you want, only take however much you want
                                amount = max_buy if max_buy > 0 else 0
                                
                                #since there will be left over product in the current product slot, move the scan region
                                #down to move onto the next product
                                print(str(product_name_area.getY()))
                                print("calling next row")
                                self.next_row(product_name_area, product_quantity_area)
                                print("finished next row")
                                print(str(product_name_area.getY()))
                                print("shifting down 2")
                            print("amount to take " + str(amount))
                            break
                            

                    if amount > 0:
                        #if the amount of products would push the ticket total or products total over 75, then take just enough to get to 75 or closest
                        if self.number_of_products_taken + amount > settings["MAX_PRODUCTS_PER_TRADE"]:
                            amount = settings["MAX_PRODUCTS_PER_TRADE"] - self.number_of_products_taken
                        if tickets_to_give + (self.pack_inventory.get_buy_price(packname) * amount) > settings["MAX_PRODUCTS_PER_TRADE"]:
                            amount = int((settings["MAX_PRODUCTS_PER_TRADE"] - tickets_to_give) / self.pack_inventory.get_buy_price(packname))
                        self.take_product(product_loc=current_product_location, quantity_to_take=amount)
                        #move pointer away so that it doesn't bring up tooltip, blocking the next product slot below
                        hover(Location(self.app_region.getX(), self.app_region.getY()))

                        pack_abbr_index = pack_names_keys.index(packname)
                        pack_names_keys = pack_names_keys[pack_abbr_index:]

                        pack_obj = Product.Product(name=packname, buy = self.pack_inventory.get_buy_price(packname), sell = self.pack_inventory.get_sell_price(packname), quantity=amount)
                        self.products_taken["packs"].append(pack_obj)
                        tickets_to_give += pack_obj["quantity"] * pack_obj["buy"]
                    if not found:
                        raise ErrorHandler("Pack scanned, but no png for it")
                    else:
                        break

        if self.app_region.exists(self._images.get_trade("canceled_trade")):
            return False
        else:
            return float(tickets_to_give)

    def search_for_bulk_cards(self, tickets_to_give=0.0):
        #this will buy all rares, mythics, uncommons, and/or commons that the customer has available
        
        number_list = self._images.get_all_numbers_as_dict(category="trade", phase="collection")
        
        if settings["BUY_FOIL"] == "yes":
            self.filter_product_version("all_versions")
        else:
            self.filter_product_version("regular")
        
        #will iterate once for filtering by rarity then by set
        for rarity, valid in bulkcardbuying["rarity"].iteritems():
            #MTGO has a maximum of 75 products that can be given or taken in a single transaction
            if tickets_to_give  >= settings["MAX_PRODUCTS_PER_TRADE"]:
                break
            if self.number_of_products_taken >= settings["MAX_PRODUCTS_PER_TRADE"]:
                break
                    
            if tickets_to_give >= settings["MAX_PRODUCTS_PER_TRADE"]:
                break
            if valid == "yes":
                print("setting rarity to " + str(rarity))
                self.filter_product_rarity(rarity=rarity)
                #will iterate through all sets that are set to "yes"
                for set in bulkcardbuying["set"]:
                    for setname, valid in set.iteritems():
                        if tickets_to_give >= settings["MAX_PRODUCTS_PER_TRADE"]:
                            break
                        if valid == "yes":
                            self.filter_product_set(set=setname)
                            
                            found = True
                            while found:
                                if self.topmost_product_quantity_area.exists(self._images.trade["empty"]):
                                    break
                                if tickets_to_give >= settings["MAX_PRODUCTS_PER_TRADE"]:
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
                                        if self.number_of_products_taken + amount > settings["MAX_PRODUCTS_PER_TRADE"]:
                                                amount = settings["MAX_PRODUCTS_PER_TRADE"] - self.number_of_products_taken
                                        if tickets_to_give + (settings["BULK_BUY_OPTIONS"]["prices"][rarity] * amount) > settings["MAX_PRODUCTS_PER_TRADE"]:
                                            amount = int((settings["MAX_PRODUCTS_PER_TRADE"]- tickets_to_give) / settings["BULK_BUY_OPTIONS"]["prices"][rarity])
                                        
                                        if amount <= 0:
                                            break
                                        self.take_product(product_loc=self.topmost_product_name_area.getCenter(), quantity_to_take=num)
                                        tickets_to_give += settings["BULK_BUY_OPTIONS"]["prices"][rarity] * num
                                        card_obj = Product.Product(name=rarity + ", " + setname, buy=settings["BULK_BUY_OPTIONS"]["prices"][rarity], sell=0, quantity=amount)
                                        self.products_taken["cards"].append(card_obj)
                                        self.number_of_products_taken += num
                                        print("running total for bulk cards = " + str(tickets_to_give))
                                        found = True
                                        wait(0.5)
                                        break
        return float(tickets_to_give)
    
    def search_for_specific_cards(self, tickets_to_give=0.0):
        #this will search for specific cards on the buy list to buy
        if settings["BUY_FOIL"] == "yes":
            self.filter_product_version("all_versions")
        else:
            self.filter_product_version("regular")
        wait(1)
        searchfield = self.frame_grab.searchfield(app_region=self.app_region)
        searchbutton = self.frame_grab.searchbutton(app_region=self.app_region)
        cards_taken = []
        number_list = self._images.get_all_numbers_as_dict(category="trade", phase="collection")
        number_of_searches = 2 if settings["BUY_FOIL"] == "yes" else 1
        
        for cardname, inv in self.card_inventory.inventory.items():
            #MTGO has a maximum of 75 products that can be given or taken in a single transaction
            if tickets_to_give  >= settings["MAX_PRODUCTS_PER_TRADE"]:
                break
            if self.number_of_products_taken >= settings["MAX_PRODUCTS_PER_TRADE"]:
                break
            
            if tickets_to_give  >= settings["MAX_PRODUCTS_PER_TRADE"]:
                break
            if self.number_of_products_taken >= settings["MAX_PRODUCTS_PER_TRADE"]:
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
                        if self.number_of_products_taken + amount > settings["MAX_PRODUCTS_PER_TRADE"]:
                            amount = settings["MAX_PRODUCTS_PER_TRADE"] - self.number_of_products_taken
                        if tickets_to_give + (self.card_inventory.get_buy_price(cardname) * amount) > settings["MAX_PRODUCTS_PER_TRADE"]:
                            amount = int((settings["MAX_PRODUCTS_PER_TRADE"] - tickets_to_give) / self.card_inventory.get_buy_price(cardname))
                        
                        self.take_product(product_loc=self.topmost_product_name_area.getCenter(), quantity_to_take=amount)
                        wait(0.5)
                        card_obj = Product.Product(name=cardname, buy=self.card_inventory.get_buy_price(cardname), sell=self.card_inventory.get_sell_price(cardname), quantity=amount)
                        self.products_taken["cards"].append(card_obj)
                        self.number_of_products_taken += amount
                        tickets_to_give += amount * self.card_inventory.get_buy_price(cardname)
                        break
                    else:
                        break
                    
        if self.app_region.exists(self._images.get_trade("canceled_trade")):
            return False
        else:
            return float(tickets_to_give)
    
    def search_for_products(self):
        #confirm button will be used for relative positioning the regions for products scanning in preconfirm stage
        self.confirm_button = self.app_region.exists(self._images.get_trade("confirm_button"), 30)
        #find the position in the window where the topmost product would be located
        
        self.topmost_product_name_area = self.frame_grab.get_trade_frame(app_region=self.app_region, phase="preconfirm", frame_name="collection", subsection="product_name_area")
        self.topmost_product_quantity_area = self.frame_grab.get_trade_frame(app_region=self.app_region, phase="preconfirm", frame_name="collection", subsection="product_quantity_area")
        self.topmost_product_set_area = self.frame_grab.get_trade_frame(app_region=self.app_region, phase="preconfirm", frame_name="collection", subsection="product_set_area")
        
        #sort button will be used for preconfirm stage
        self.name_sort_button_location = Location(self.confirm_button.getX()-231, self.confirm_button.getY()+23)
        self._slow_click(loc=self.name_sort_button_location)
        
        #variables to hold amount of tickets that should be given
        tickets_to_give = 0.0
        #list that holds all products that were taken, for post transaction recording purposes
        self.products_taken = {"packs": [], "cards": []}
        self.number_of_products_taken = 0
        
        ## DEBUG ##
        tickets_to_give = self.search_for_packs(tickets_to_give=tickets_to_give)
        
        if settings["CARD_BUYING"] == "bulk":
            tickets_to_give = self.search_for_bulk_cards(tickets_to_give=tickets_to_give)
        elif settings["CARD_BUYING"] == "search":
            tickets_to_give = self.search_for_specific_cards(tickets_to_give=tickets_to_give)

        #if customer cancels trade
        print("finished search for products with " + str(tickets_to_give))
        if tickets_to_give is False:
            return False
        else:
            return tickets_to_give
        
    def preconfirm_scan_purchase(self, tickets_to_give):
        giving_name_region = Region(self.giving_window_region.getX()+35, self.giving_window_region.getY()+43, 197, 17)
        giving_number_region = Region(self.giving_window_region.getX()+3, self.giving_window_region.getY()+43, 30, 17)
        
        numbers_list = self._images.get_all_numbers_as_dict(category="trade", phase="preconfirm")
        
        if giving_name_region.exists(self._images.get_ticket_text(), 120):
            if giving_number_region.exists(self._images.get_number(number=int(tickets_to_give), category="trade", phase="preconfirm"), 180 ):
                return True
        
        return False

    def confirmation_scan(self, tickets_to_give, credit=0):
        """will return number of tickets taken for transaction recording"""
        #verify confirm window by checking for confirm cancel buttons, then set regions relative to those buttons
        confirm_button = exists(self._images.get_trade("confirm_button", "confirm"), 1200)
        
        if not confirm_button:
            return False
        
        if isinstance(confirm_button, Match):
            print("confirmation scan, tickets_to_give = " + str(tickets_to_give))
            #keeps record of products found and their amount so far
            receiving_products_found = {"packs": [], "cards": []}
            rarities_list = self._images.trade["confirm"]["rarity"]
            
            numbers = self._images.get_all_numbers_as_dict(category="trade", phase="preconfirm")
            #confirm products receiving
            #these regions correspond to a single row from each column
            #height for each product is 13px, and 4px buffer vertically between each product slot
            
            receiving_number_region = self.frame_grab.get_trade_frame(app_region=self.app_region, phase="confirm", frame_name="taking_window", subsection="product_quantity_area")
            receiving_rarity_region = self.frame_grab.get_trade_frame(app_region=self.app_region, phase="confirm", frame_name="taking_window", subsection="product_rarity_area")
            receiving_set_region = self.frame_grab.get_trade_frame(app_region=self.app_region, phase="confirm", frame_name="taking_window", subsection="product_set_area")
            receiving_name_region = self.frame_grab.get_trade_frame(app_region=self.app_region, phase="confirm", frame_name="taking_window", subsection="product_name_area")
            
            
            #receiving_number_region = Region(confirm_button.getX()-289, confirm_button.getY()+41, 34, 17)
            #receiving_name_region = Region(confirm_button.getX()-257, confirm_button.getY()+41, 163, 17)
            #receiving_rarity_region = Region(confirm_button.getX()+340, confirm_button.getY()+41, 61, 17)
            #receiving_set_region = Region(confirm_button.getX()+291, confirm_button.getY()+41, 45, 17)
            
            #confirm products giving
            giving_number_region = self.frame_grab.get_trade_frame(app_region=self.app_region, phase="confirm", frame_name="giving_window", subsection="product_quantity_area")
            giving_name_region = self.frame_grab.get_trade_frame(app_region=self.app_region, phase="confirm", frame_name="giving_window", subsection="product_name_area")
            
            #giving_number_region = Region(confirm_button.getX()-291, confirm_button.getY()+391, 34, 17)
            #giving_name_region = Region(confirm_button.getX()-260, confirm_button.getY()+391, 163, 17)
            print("x: " + str(receiving_name_region.x) + ", y: " + str(receiving_name_region.y) + ", w: " + str(receiving_name_region.w) + ", h: " + str(receiving_name_region.h))
            
            found=True
            if settings["CARD_BUYING"] == "search":
                product_names_list = self.card_inventory.get_card_name_list() + self.pack_inventory.get_sorted_pack_list()
                product_names_list.sort()
                while found:
                    if receiving_name_region.exists(self._images.trade["empty"]):
                        break
                    found=False
                    #scan each product one by one for it's name and quantity
                    for product_abbr in product_names_list:
                        try:
                            product = self._images.get_pack_text(phase="confirm", packname=product_abbr)
                            product_type = "pack"
                        except KeyError:
                            try:
                                product = self._images.get_card_text(phase="confirm", cardname=product_abbr)
                            except KeyError:
                                continue
                            else:
                                product_type = "card"
                        print("searching for :" + str(product))
                        print("x: " + str(receiving_name_region.x) + ", y: " + str(receiving_name_region.y) + ", w: " + str(receiving_name_region.w) + ", h: " + str(receiving_name_region.h))
                        if receiving_name_region.exists(Pattern(product).similar(0.8)):
                            print(product_abbr + " found!")
                            #if still at 0 after for loop, error raised
                            amount = 0
                            for number in range(len(numbers)):
                                if number == 0:
                                    continue
                                print("searching for number" + str(number) + " at " + str(receiving_number_region.x) + " " + str(receiving_number_region.y) + " " + str(receiving_number_region.w) + " " + str(receiving_number_region.h) + " ")
                                if receiving_number_region.exists(Pattern(numbers[number]).similar(0.8)):
                                    print(str(number) + " amount of " + product_abbr + " found!")
                                    amount = number

                                    #packs are listed in Magic in the same sequence they are listed in the list of pack keys,
                                    #if a pack is found, all packs including it and before, are removed from the list of packs
                                    #to search
                                    product_index = product_names_list.index(product_abbr) + 1
                                    product_names_list = product_names_list[product_index:]
                                    break

                            if product_type == "pack":
                                product_obj = Product.Product(name=product_abbr, buy=self.pack_inventory.get_buy_price(product_abbr), sell=self.pack_inventory.get_sell_price(product_abbr), quantity=amount)
                                receiving_products_found["packs"].append(product_obj)
                            elif product_type == "card":
                                product_obj = Product.Product(name=product_abbr, buy=self.card_inventory.get_buy_price(product_abbr), sell=self.card_inventory.get_sell_price(product_abbr), quantity=amount)
                                receiving_products_found["cards"].append(product_obj)
                            else:
                                raise ErrorHandler("Product type has not been set, but product detected")
                            
                            if amount == 0:
                                raise ErrorHandler("Could not find a number for product: " + str(product_abbr))
                            found=True
                            
                            self.next_row(receiving_number_region, receiving_name_region)
                            if not found:
                                raise ErrorHandler("Product scanned, but no png file found for it")
                            else:
                                break
            else:
                pack_names_list = self.pack_inventory.get_sorted_pack_list()
                card_names_list = self.card_inventory.get_card_name_list()
                #scan the rarity and the amount to calculate total price
                while found:
                    print("scanning region: " + str(receiving_name_region.getX()) + ", " + str(receiving_name_region.getY()) + ", " + str(receiving_name_region.getW()) + ", " + str(receiving_name_region.getH()))
                    if receiving_name_region.exists(self._images.trade["empty"]):
                        break
                    found = False
                    hover(Location(receiving_name_region.getX()-10, receiving_name_region.getY()))
                    #check if there is a card in the product slot
                    if receiving_rarity_region.exists(self._images.trade["confirm"]["rarity"]["none"]):
                        print("None found")
                        for pack in pack_names_list:
                            print("checking for pack: " + pack)
                            #check if it's a booster pack
                            if receiving_name_region.exists(Pattern(self._images.get_pack_text(phase="confirm", packname=pack)).similar(0.9)):
                                for number in range(len(numbers)):
                                    if number == 0:
                                        continue
                                    if receiving_number_region.exists(Pattern(numbers[number]).similar(0.9)):
                                        found = True
                                        print("found " + str(number) + " product")
                                        amount = number
                                        break
                                print("found " + str(self._images.get_pack_text(phase="confirm", packname=pack)))
                                product_obj = Product.Product(name=pack, buy=self.pack_inventory.get_buy_price(pack), sell=self.pack_inventory.get_sell_price(pack), quantity=number)
                                receiving_products_found["packs"].append(product_obj)
                                new_index = pack_names_list.index(pack)+1
                                pack_names_list = pack_names_list[new_index:]
                                if not found:
                                    raise ErrorHandler("Pack found but no png found for it")
                                else:
                                    break
                    else:
                        print("None is not found")
                        #check to see if it's a card.  cards are bought in bulk, so name isn't scanned, just rarity
                        for rarity, valid in bulkcardbuying["rarity"].items():
                            if valid == "yes":
                                print("checking for card of rarity: " + rarity)
                                if receiving_rarity_region.exists(Pattern(self._images.trade["confirm"]["rarity"][rarity]).similar(1)):
                                    for number in range(len(numbers)):
                                        if number == 0:
                                            continue
                                        if receiving_number_region.exists(Pattern(numbers[number]).similar(0.9)):
                                            found = True
                                            print("found " + str(number) + " product")
                                            amount = number
                                            break
                                    print("found a " + str(self._images.trade["confirm"]["rarity"][rarity]))
                                    product_obj = Product.Product(name=rarity, buy=settings["BULK_BUY_OPTIONS"]["prices"][rarity], sell=0, quantity=number)
                                    receiving_products_found["cards"].append(product_obj)
                                if not found:
                                    raise ErrorHandler("Bulk card found but no valid rarity found")
                                else:
                                    break
                    self.next_row(receiving_number_region, receiving_name_region, receiving_rarity_region)

            #get image of number expected to scan for it first, to save time, else search through all other numbers
            expected_number = 0
            for product_type, products in receiving_products_found.items():
                for product in products:
                    expected_number += product["quantity"] * product["buy"]
            expected_number -= credit
            print("expected number of tickets " + str(expected_number))

            if not expected_number == tickets_to_give:
                return False

            hover(Location(giving_number_region.getX(), giving_number_region.getY()))
            print("scanning region for number " + str(giving_name_region.x) + " " + str(giving_name_region.y) + " " + str(giving_name_region.w) + " " + str(giving_name_region.h))
            ticket_text_image = Pattern(self._images.get_ticket_text()).similar(1)
            if giving_name_region.exists(ticket_text_image):
                expected_number_image = Pattern(self._images.get_number(number=int(expected_number), category="trade", phase="confirm")).similar(0.9)
                print(str(expected_number_image))
                if giving_number_region.exists(expected_number_image):
                    return receiving_products_found
                else:
                    return False
            else:
                return False

    def complete_purchase(self, customer_credit=0):
        """Will return the transactions details to be recorded if successul
        else will return False"""
    
        #take the products first, then tell customer how many tickets to take
        #requires IChat interface to be passed to tell customers how many tickets to take
        
        #switch to list view in the collection window
        self._slow_click(target=self._images.get_trade("list_view_collection_window"))
        
        running_total = self.search_for_products()
        running_total -= customer_credit
        
        print("running total is " + str(running_total))
        if running_total == 0 or not running_total:
            self.cancel_trade()
            return False
        
        total_tickets_notice = 'Please take %i tickets.' % running_total
        self.Ichat.type_msg(total_tickets_notice)
        
        #wait for the customer to get the tickets, then click confirm
        if not self.preconfirm_scan_purchase(running_total): 
            self.cancel_trade()
        
        self.go_to_confirmation()
        print("starting confirmation scan")
        #run a final confirmation scan to check the products and tickets taken
        products_bought = self.confirmation_scan(tickets_to_give=running_total, credit=customer_credit)
        
        self.Ichat.close_current_chat()
    
        if products_bought:
            self._slow_click(target=self._images.get_trade("confirm_button", "confirm"))
            wait(Pattern(self._images.get_ok_button()), 600)
            self._slow_click(target=self._images.get_ok_button())
            products_bought["total_tickets"] = running_total
            
            return products_bought
            
        else:
            self.cancel_trade()
            return False
