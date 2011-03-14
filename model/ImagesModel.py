from sikuli.Sikuli import *

path_to_bot = getBundlePath().split("bot.sikuli")[0]


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
    def get_all_numbers_as_dict(self, category, phase=None):
        numbers_list = dict((num, self.get_number(number=num, category=category, phase=phase)) for num in range(75) if num is not 0)
        return numbers_list  
          
    #stores images for the classified window
    __classified = {'posting': "../Images/posting_text_area.png", 
                    "submit_posting": "../Images/submit_posting_button.png", 
                    'cancel_edit': "../Images/cancel_edit_button.png", 
                    'submit_edit': "../Images/submit_edit_button.png", 
                    'edit_posting': "../Images/edit_posting_button.png", 
                    "search_posts":"../Images/search_posts.png"}
                    
    def get_classified(self, filename):
        return self.__classified[filename]
    
    #stores the screencaps for trade window
    __trade = {"confirm":{"confirm_button":"../Images/trade/confirm_window/confirm_button_confirm.png", 
                          "confirm_cancel":"../Images/trade/confirm_window/confirm_cancel.png", 
                          "cancel_button":"../Images/trade/confirm_window/cancel_button.png"}, 
               "canceled_trade": "canceled_trade.png", 
               "sort_name": "../Images/trade/sort_name.png", 
               "list_view_collection_window":"../Images/trade/list_view_button_collection_window.png", 
               "thumbnail_view_collection_window":"../Images/trade/thumbnail_view_button_collection_window.png", 
               "confirm_button":"../Images/trade/confirm_button.png", 
               "cancel_button":"../Images/trade/cancel_button.png", 
               "incoming_request": "../Images/incoming_request.png", 
               "yes_button": "../Images/yes_button.png",  
               "turn_right": "../Images/turn_right.png", 
               "turn_left": "../Images/turn_left.png", 
               "version_menu":"../Images/trade/version_menu.png", 
               "version_menu_regular":"../Images/trade/version_menu_regular.png", 
               "version_menu_packs_tickets":"../Images/trade/version_menu_packs_tickets.png", 
               "version_menu_premium":"../Images/trade/version_menu_premium.png", 
               "giving_window":"../Images/trade/products_giving.png", 
               "taking_window":"../Images/trade/products_taking.png", 
               "scroll_bar_regular":"../Images/trade/scroll_bar_regular.png", 
               "scroll_bar_mini":"../Images/trade/scroll_bar_mini.png"}

    def get_trade(self, filename, phase=None):
        if phase == None:
            return self.__trade[filename]
        else:
            return self.__trade[phase][filename]
            
    #stores the screencaps for chat window
    __chat = {"minimize":"../Images/chat/minimize_button.png", 
              "expand_close":"../Images/chat/expand_close_button.png", 
              "type_area":"../Images/chat/type_area.png", 
              "buddies": "../Images/buddies_tab.png", 
              'my_cart': "../Images/my_cart_tab.png", 
              'games': "../Images/games_tab.png", 
              'card': "../Images/card_tab.png", 
              'text':{"done":"../Images/chat/text/done.png"}}
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
    __card_names_list = {"M11": {"Primeval Titan":""}, 
                    "ME4": {},
                    "MBS": {"Tezzeret, Agent of Bolas": ""},
                    "ROE": {"Gideon Jura": ""},
                    "SOM": {"Venser, the Sojourner": ""},
                    "WWK": {"Jace, the Mind Sculptor": ""},  
                    "ZEN": {"":""}}
    def get_card_text(self, cardname, phase=None):
        if not cardname in self.__card_names_list:
            raise KeyError("Card name not found in cards_names_list")
            return None
        else:
            filepath = "../Images/product/cards/text/"
            if phase == "confirm":
                filepath += "confirm/"
            filepath += str(cardname) + ".png"
            return filepath
    def get_card_text(self, phase, cardname):
        try:
            open(path_to_bot + "Images/product/cards/text/" + phase + "/" + cardname + ".png", "r")
        except IOError:
            raise KeyError(cardname + " not found")
        else:
            filepath = "../Images/product/cards/text/" + phase + "/" + cardname + ".png"
            return filepath
    def get_card_image(self, set, cardname):
        try:
            open(path_to_bot + "Images/product/cards/img/" + phase + "/" + cardname + ".png", "r")
        except IOError:
            raise KeyError(cardname + " not found")
        else:
            filepath = "../Images/product/cards/img/" + phase + "/" + cardname + ".png"
            return filepath
    
    __card_names_list = ["Primeval Titan", "Tezzeret, Agent of Bolas", "Gideon Jura", "Venser, the Sojourner", "Jace, the Mind Sculptor"]
    def get_card_keys(self):
        return self.__card_names_list
    
    #stores the images of each pack
    #this is a list of all packs to buy and sell
    __pack_names_list = ["M11", "ME4", "MBS", "ROE", "SOM", "WWK", "ZEN"]
    
    def get_pack_keys(self):
        return self.__pack_names_list
    
    def get_pack_text(self, phase, packname):
        try:
            open(path_to_bot + "Images/product/packs/text/" + phase + "/" + packname + ".png", "r")
        except IOError:
            raise KeyError(packname + " not found")
        else:
            filepath = "../Images/product/packs/text/" + phase + "/" + packname + ".png"
            return filepath

    def get_all_pack_text_as_dict(self, phase):
        packs_dict = dict((abbr, self.get_packs_text(phase=phase, packname=abbr)) for abbr in self.__pack_names_list)
        return packs_dict
    
    def get_pack_image(self, packname):
        try:
            open(path_to_bot + "/Images/product/packs/img/" + packname + ".png", "r")
        except:
            raise KeyError(packname + " not found")
        else:
            filepath = "../Images/product/packs/" + packname + ".png"
            return filepath
        
    def get_all_pack_image_as_dict(self):
        packs_dict = dict((abbr, self.get_packs_image(abbr)) for abbr in self.__pack_names_list)
        return packs_dict
        
    #stores image of login screen
    __login = {'password_field': "../Images/password_field.png" , 
               'login_success': "../Images/login_success.png" , 
               'login_fail': "../Images/login_fail.png" , 
               'login_button': "../Images/login_button.png" }
    def get_login(self, filename):
        return self.__login[filename]
    
    #stores image of menu options
    __menu = {'community': "../Images/community_button.png", 
              'menu': "../Images/menu_button.png", 
              'collection': "../Images/collection_button.png", 
              'home': "../Images/home_button.png", 
              'marketplace': "../Images/marketplace_button.png", 
              'classified': "../Images/classified_button.png"}
    def get_menu(self, filename):
        return self.__menu[filename]