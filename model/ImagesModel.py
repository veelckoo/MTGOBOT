class ImagesModel(object):
    #stores the all images to be used by bot into tuples
    #used as a library object, primarily by the interface object
    """returns the images to be used for pixel search"""
    
    #image of blank area
    __blank = "../Images/trade/blank.png"
    def get_blank(self):
        return self.__blank
    
    #image of the ok button, e.g. after completing a trade
    __ok_button = "../Images/ok_button.png"
    def get_ok_button(self):
        return self.__ok_button
        
    #stores image of a ticket
    __ticket =  "../Images/product/misc/ticket.png"
    def get_ticket(self):
        return self.__ticket
        
    #stores image of a ticket text
    __ticket_text = "../Images/product/misc/text/event_ticket_text.png"
    def get_ticket_text(self):
        return self.__ticket_text
        
    __amount = {1:"../Images/trade/context_menu/get_1.png", 4:"../Images/trade/context_menu/get_4.png", 10:"../Images/trade/context_menu/get_10.png", 32:"../Images/trade/context_menu/get_32.png"}
    def get_amount(self, amount):
        return self.__amount[amount]
        
    #store images of each number in a tuple
    #the image for numbers depend on the context, e.g. number images in the giving window are different from the ones in collection or taking_window
    
    def get_number(self, number, category, phase=None):
        filepath = "../Images/numbers/" + str(category) + "/"
        if phase:
            filepath += str(phase) + "/"
        filepath += "number_" + str(number) + ".png"
        return filepath
    def get_all_numbers_as_list(self, category, phase=None):
        numbers_list = {}
        for i in range(75):
            if i == 0:
                continue
            numbers_list[i] = self.get_number(number=i, category=category, phase=phase)
        return numbers_list  
          
    #stores images for the classified window
    __classified = {'posting': "../Images/posting_text_area.png", "submit_posting": "../Images/submit_posting_button.png", 'cancel_edit': "../Images/cancel_edit_button.png", 'submit_edit': "../Images/submit_edit_button.png", 'edit_posting': "../Images/edit_posting_button.png", "search_posts":"../Images/search_posts.png"}
    def get_classified(self, filename):
        return self.__classified[filename]
    
    #stores the screencaps for trade window
    __trade = {"confirm":{"confirm_button":"../Images/trade/confirm_window/confirm_button_confirm.png", "confirm_cancel":"../Images/trade/confirm_window/confirm_cancel.png", "cancel_button":"../Images/trade/confirm_window/cancel_button.png"}, "canceled_trade": "canceled_trade.png", "sort_name": "../Images/trade/sort_name.png", "list_view_collection_window":"../Images/trade/list_view_button_collection_window.png", "thumbnail_view_collection_window":"../Images/trade/thumbnail_view_button_collection_window.png", "confirm_button":"../Images/trade/confirm_button.png", "cancel_button":"../Images/trade/cancel_button.png", "incoming_request": "../Images/incoming_request.png", "yes_button": "../Images/yes_button.png",  "turn_right": "../Images/turn_right.png", "turn_left": "../Images/turn_left.png", "version_menu":"../Images/trade/version_menu.png", "version_menu_regular":"../Images/trade/version_menu_regular.png", "version_menu_packs_tickets":"../Images/trade/version_menu_packs_tickets.png", "version_menu_premium":"../Images/trade/version_menu_premium.png", "giving_window":"../Images/trade/products_giving.png", "taking_window":"../Images/trade/products_taking.png", "scroll_bar_regular":"../Images/trade/scroll_bar_regular.png", "scroll_bar_mini":"../Images/trade/scroll_bar_mini.png"}
    def get_trade(self, filename, phase=None):
        if phase == None:
            return self.__trade[filename]
        else:
            return self.__trade[phase][filename]
            
    #stores the screencaps for chat window
    __chat = {"minimize":"../Images/chat/minimize_button.png", "expand_close":"../Images/chat/expand_close_button.png", "type_area":"../Images/chat/type_area.png", "buddies": "../Images/buddies_tab.png", 'my_cart': "../Images/my_cart_tab.png", 'games': "../Images/games_tab.png", 'card': "../Images/card_tab.png", 'text':{"done":"../Images/chat/text/done.png"}}
    def get_chat_text(self, filename):
        return self.__chat['text'][filename]
    def get_chat_window(self, filename):
        return self.__chat[filename]
    
    #stores the images of each card
    __cards = {}
    def get_cards(self, filename=None):
        if filename:
            return self.__cards[filename]
        else:
            return self.__cards
    
    #card images
    __cards_text = {"M11": {"Primeval Titan":""}, 
                    "ME4": {},
                    "MBS": {"Tezzeret, Agent of Bolas": ""},
                    "ROE": {"Gideon Jura": ""},
                    "SOM": {"Venser, the Sojourner": ""},
                    "WWK": {"Jace, the Mind Sculptor": ""},  
                    "ZEN": {"":""}}
    def get_card_text(self, cardname, phase=None):
        filepath = "../Images/product/cards/text/"
        if phase == "confirm":
            filepath += "confirm/"
        filepath += str(cardname)
        return filepath
    def get_card_images(self, card, set):
        filepath = "../Images/product/cards/set/" + set
        return filepath
    
    __card_names_list = ["Primeval Titan", "Tezzeret, Agent of Bolas", "Gideon Jura", "Venser, the Sojourner", "Jace, the Mind Sculptor"]
    def get_card_keys(self):
        return self.__card_names_list
    
    #stores the images of each pack
    #this is a list of all packs to buy and sell
    __packs_name_list = ["M11", "ME4", "MBS", "ROE", "SOM", "WWK", "ZEN"]
    
    __packs_images = {"M11":"../Images/product/packs/Magic2011.png", "M10":"../Images/product/packs/Magic2010.png", "10E":"../Images/product/packs/UrzasLegacy.png", "9ED":"../Images/product/packs/Magic9.png", "8ED":"../Images/product/packs/Magic8.png", "7ED":"../Images/product/packs/Magic7.png", "MBS": "../Images/product/packs/Besieged.png", "SOM":"../Images/product/packs/Scars.png", "ROE":"../Images/product/packs/RiseEldrazi.png", "WWK":"../Images/product/packs/Worldwake.png", "ZEN":"../Images/product/packs/Zendikar.png","UZS":"../Images/product/packs/UrzasSaga.png", "UZL":"../Images/product/packs/UrzasLegacy.png", "ARB":"../Images/product/packs/AlaraReborn.png", "CSP":"../Images/product/packs/Coldsnap.png", "CON":"../Images/product/packs/Conflux.png", "DIS":"../Images/product/packs/Dissension.png", "EXO":"../Images/product/packs/Exodus.png", "FUT":"../Images/product/packs/Future.png", "CHK":"../Images/product/packs/KamigawaChampions.png", "LEG":"../Images/product/packs/Legions.png", "LRW":"../Images/product/packs/Lorwyn.png", "MOR":"../Images/product/packs/Morningtide.png", "PLC":"../Images/product/packs/PlanarChaos.png", "ALA":"../Images/product/packs/ShardsAlara.png", "STH":"../Images/product/packs/Stronghold.png", "WTH":"../Images/product/packs/Weatherlight.png", "ME4":"../Images/product/packs/Masters4.png", "ME3":"../Images/product/packs/Masters3.png", "ME2":"../Images/product/packs/Masters2.png", "ME1":"../Images/product/packs/Masters1.png", "ALB":"../Images/product/packs/AlaraBlock.png"},
    __packs_text = {"preconfirm": {"M11":"../Images/product/packs/text/Magic2011.png", "M10":"../Images/product/packs/text/Magic2010.png", "10E":"../Images/product/packs/text/UrzasLegacy.png", "9ED":"../Images/product/packs/text/Magic9.png", "8ED":"../Images/product/packs/text/Magic8.png", "7ED":"../Images/product/packs/text/Magic7.png","MBS": "../Images/product/packs/text/Besieged.png", "SOM":"../Images/product/packs/text/Scars.png", "ZEN":"../Images/product/packs/text/Zendikar.png", "WWK":"../Images/product/packs/text/Worldwake.png", "ROE":"../Images/product/packs/text/RiseEldrazi.png", "UZS":"../Images/product/packs/text/UrzasSaga.png", "UZL":"../Images/product/packs/text/UrzasLegacy.png", "ARB":"../Images/product/packs/text/AlaraReborn.png", "CSP":"../Images/product/packs/text/Coldsnap.png", "CON":"../Images/product/packs/text/Conflux.png", "DIS":"../Images/product/packs/text/Dissension.png", "EXO":"../Images/product/packs/text/Exodus.png", "FUT":"../Images/product/packs/text/Future.png", "CHK":"../Images/product/packs/text/KamigawaChampions.png", "LEG":"../Images/product/packs/text/Legions.png", "LRW":"../Images/product/packs/text/Lorwyn.png", "MOR":"../Images/product/packs/text/Morningtide.png", "PLC":"../Images/product/packs/text/PlanarChaos.png", "ALA":"../Images/product/packs/text/ShardsAlara.png", "STH":"../Images/product/packs/text/Stronghold.png", "WTH":"../Images/product/packs/text/Weatherlight.png", "ME4":"../Images/product/packs/text/Masters4.png", "ME3":"../Images/product/packs/text/Masters3.png", "ME2":"../Images/product/packs/text/Masters2.png", "ME1":"../Images/product/packs/text/Masters1.png", "ALB":"../Images/product/packs/text/AlaraBlock.png"},
                    "confirm":{"M11":"../Images/product/packs/text/confirm/Magic2011.png", "ME4":"../Images/product/packs/text/confirm/Masters4.png", "ROE":"../Images/product/packs/text/confirm/RiseEldrazi.png", "MBS": "../Images/product/packs/text/confirm/Besieged.png", "SOM":"../Images/product/packs/text/confirm/Scars.png", "ZEN":"../Images/product/packs/text/confirm/Zendikar.png", "WWK":"../Images/product/packs/text/confirm/Worldwake.png"}}
    def get_pack_keys(self):
        return self.__packs_name_list
    def get_packs_text(self, phase, packname=None):
        if phase == "preconfirm":
            if packname:
                return self.__packs_text["preconfirm"][packname]
            else:
                return self.__packs_text["preconfirm"]
        elif phase == "confirm":
            if packname:
                return self.__packs_text["confirm"][packname]
            else:
                return self.__packs_text["confirm"]
        else:
            return None
    def get_packs_images(self, packname=None):
        if packname :
            return self.__packs_images[packname]
        else:
            return self.__packs_images
    
    #stores image of login screen
    __login = {'password_field': "../Images/password_field.png" , 'login_success': "../Images/login_success.png" , 'login_fail': "../Images/login_fail.png" , 'login_button': "../Images/login_button.png" }
    def get_login(self, filename):
        return self.__login[filename]
    
    #stores image of menu options
    __menu = {'community': "../Images/community_button.png", 'menu': "../Images/menu_button.png", 'collection': "../Images/collection_button.png", 'home': "../Images/home_button.png", 'marketplace': "../Images/marketplace_button.png", 'classified': "../Images/classified_button.png"}
    def get_menu(self, filename):
        return self.__menu[filename]