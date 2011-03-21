from sikuli.Sikuli import *

path_to_bot = getBundlePath().split("bot.sikuli")[0]


class ImagesModel(object):
    #stores the all images to be used by bot into tuples
    #used as a library object, primarily by the interface object
    """returns the images to be used for pixel search"""
    
    #image of blank area
    blank = "../Images/trade/blank.png"
    def get_blank(self):
        return self.blank
    
    #image of the ok button, e.g. after completing a trade
    ok_button = "../Images/ok_button.png"
    def get_ok_button(self):
        return self.ok_button
        
    #stores image of a ticket
    ticket =  "../Images/product/misc/ticket.png"
    
    def get_ticket(self):
        return self.ticket
        
    #stores image of a ticket text
    ticket_text = "../Images/product/misc/text/event_ticket_text.png"
    
    def get_ticket_text(self):
        return self.ticket_text
        
    amount = {1:"../Images/trade/context_menu/get_1.png", 4:"../Images/trade/context_menu/get_4.png", 10:"../Images/trade/context_menu/get_10.png", 32:"../Images/trade/context_menu/get_32.png"}
    def get_amount(self, amount):
        return self.amount[amount]
        
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
    classified = {'posting': "../Images/posting_text_area.png", 
                    "submit_posting": "../Images/submit_posting_button.png", 
                    'cancel_edit': "../Images/cancel_edit_button.png", 
                    'submit_edit': "../Images/submit_edit_button.png", 
                    'edit_posting': "../Images/edit_posting_button.png", 
                    "search_posts":"../Images/search_posts.png"}
                    
    def get_classified(self, filename):
        return self.classified[filename]

    #stores the screencaps for trade window
    trade = {"confirm":{"confirm_button":"../Images/trade/confirm_window/confirm_button_confirm.png", 
                        "confirm_cancel":"../Images/trade/confirm_window/confirm_cancel.png", 
                        "cancel_button":"../Images/trade/confirm_window/cancel_button.png",
                        "rarity":{"mythic": "../Images/trade/confirm_window/Mythic.png",
                                  "rare": "../Images/trade/confirm_window/Rare.png",
                                  "uncommon": "../Images/trade/confirm_window/Uncommon.png",
                                  "common": "../Images/trade/confirm_window/Common.png"}}, 
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
           "filters": {"version": {"all_versions": "../Images/trade/version/all_versions.png",
                                   "packs_tickets": "../Images/trade/version/packs_tickets.png",
                                   "premium": "../Images/trade/version/premium.png",
                                   "regular": "../Images/trade/version/regular.png"},
                       "rarity": {"any": "../Images/trade/rarity/Any.png",
                                  "common": "../Images/trade/rarity/Common.png",
                                  "uncommon": "../Images/trade/rarity/Uncommon.png",
                                  "rare": "../Images/trade/rarity/Rare.png",
                                  "mythic": "../Images/trade/rarity/Mythic.png"},
                       "set":{"scroll_down": "../Images/trade/set/scroll_down.png",
                              "scroll_up": "../Images/trade/set/scroll_up.png",
                              "Standard": "../Images/trade/set/Standard.png",
                              "Extended": "../Images/trade/set/Extended.png",
                              "Classic": "../Images/trade/set/Classic.png",
                              "Legacy": "../Images/trade/set/Legacy.png",
                              "Scars of Mirrodin": "../Images/trade/set/Scars of Mirrodin.png",
                              "Mirrodin Besieged": "../Images/trade/set/Mirrodin Besieged.png",
                              "Zendikar": "../Images/trade/set/Zendikar.png",
                              "Worldwake": "../Images/trade/set/Worldwake.png",
                              "Rise of the Eldrazi": "../Images/trade/set/Rise of the Eldrazi.png",
                              "Shards of Alara": "../Images/trade/set/Shards of Alara.png",
                              "Conflux": "../Images/trade/set/Conflux.png",
                              "Alara Reborn": "../Images/trade/set/Alara Reborn.png",
                              "Lorwyn": "../Images/trade/set/Lorwyn.png",
                              "Morningtide": "../Images/trade/set/Morningtide.png",
                              "Shadowmoor": "../Images/trade/set/Shadowmoor.png",
                              "Eventide": "../Images/trade/set/Eventide.png",
                              "Time Spiral": "../Images/trade/set/Time Spiral.png",
                              "Timeshifted": "../Images/trade/set/Timeshifted.png",
                              "Planar Chaos": "../Images/trade/set/Planar Chaos.png",
                              "Future Sight": "../Images/trade/set/Future Sight.png",
                              "Ice Age": "../Images/trade/set/Ice Age.png",
                              "Alliance": "../Images/trade/set/Alliance.png",
                              "Coldsnap": "../Images/trade/set/Coldsnap.png",
                              "Ravnica": "../Images/trade/set/Ravnica.png",
                              "Guildpact": "../Images/trade/set/Guildpact.png",
                              "Dissension": "../Images/trade/set/Dissension.png",
                              "Champions of Kamigawa": "../Images/trade/set/Champions of Kamigawa.png",
                              "Betrayers of Kamigawa": "../Images/trade/set/Betrayers of Kamigawa.png",
                              "Saviors of Kamigawa": "../Images/trade/set/Saviors of Kamigawa.png",
                              "Mirrodin": "../Images/trade/set/Mirrodin.png",
                              "Darksteel": "../Images/trade/set/Darksteel.png",
                              "Fifth Dawn": "../Images/trade/set/Fifth Dawn.png",
                              "Onslaught": "../Images/trade/set/Onslaught.png",
                              "Legion": "../Images/trade/set/Legion.png",
                              "Scourge": "../Images/trade/set/Scourge.png",
                              "Odyssey": "../Images/trade/set/Odyssey.png",
                              "Torment": "../Images/trade/set/Torment.png",
                              "Judgment": "../Images/trade/set/Judgment.png",
                              "Invasion": "../Images/trade/set/Invasion.png",
                              "Planeshift": "../Images/trade/set/Planeshift.png",
                              "Apocalypse": "../Images/trade/set/Apocalypse.png",
                              "Urza's Saga": "../Images/trade/set/Urza's Saga.png",
                              "Urza's Legacy": "../Images/trade/set/Urza's Legacy.png",
                              "Urza's Destiny": "../Images/trade/set/Urza's Destiny.png",
                              "Tempest": "../Images/trade/set/Tempest.png",
                              "Stronghold": "../Images/trade/set/Stronghold.png",
                              "Exodus": "../Images/trade/set/Exodus.png",
                              "Mirage": "../Images/trade/set/Mirage.png",
                              "Visions": "../Images/trade/set/Visions.png",
                              "Weatherlight": "../Images/trade/set/Weatherlight.png",
                              "Seventh Edition": "../Images/trade/set/Seventh Edition.png",
                              "Eighth Edition": "../Images/trade/set/Eighth Edition.png",
                              "Ninth Edition": "../Images/trade/set/Ninth Edition.png",
                              "Tenth Edition": "../Images/trade/set/Tenth Edition.png",
                              "Magic 2010": "../Images/trade/set/Magic 2010.png",
                              "Magic 2011": "../Images/trade/set/Magic 2011.png",
                              "Masters Edition": "../Images/trade/set/Masters Edition.png",
                              "Masters Edition II": "../Images/trade/set/Masters Edition II.png",
                              "Masters Edition III": "../Images/trade/set/Masters Edition III.png",
                              "Masters Edition IV":"../Images/trade/set/Masters Edition IV.png"}},
           "giving_window":"../Images/trade/products_giving.png", 
           "taking_window":"../Images/trade/products_taking.png", 
           "scroll_bar_regular":"../Images/trade/scroll_bar_regular.png", 
           "scroll_bar_mini":"../Images/trade/scroll_bar_mini.png"}
    
    def get_trade(self, filename, *subsection):
        if len(subsection) == 0:
            return self.trade[filename]
        elif len(subsection) == 1:
            return self.trade[subsection[0]][filename]
        elif len(subsection) == 2:
            return self.trade[subsection[0]][subsection[1]][filename]
            
    #stores the screencaps for chat window
    chat = {"minimize":"../Images/chat/minimize_button.png", 
              "expand_close":"../Images/chat/expand_close_button.png", 
              "type_area":"../Images/chat/type_area.png", 
              "buddies": "../Images/buddies_tab.png", 
              'my_cart': "../Images/my_cart_tab.png", 
              'games': "../Images/games_tab.png", 
              'card': "../Images/card_tab.png", 
              'text':{"done":"../Images/chat/text/done.png"}}
    def get_chat_text(self, filename):
        return self.chat['text'][filename]
    def get_chat_window(self, filename):
        return self.chat[filename]
    
    #stores the images of each card
    cards = {}
    def get_cards(self, filename=None):
        if filename:
            return self.cards[filename]
        else:
            return self.cards
    
    #card images
    card_names_list = {"M11": {"Primeval Titan":""}, 
                    "ME4": {},
                    "MBS": {"Tezzeret, Agent of Bolas": ""},
                    "ROE": {"Gideon Jura": ""},
                    "SOM": {"Venser, the Sojourner": ""},
                    "WWK": {"Jace, the Mind Sculptor": ""},  
                    "ZEN": {"":""}}
                    
    def get_card_text(self, cardname, phase=None):
        if not cardname in self.card_names_list:
            raise KeyError("Card name not found in cards_names_list")
            return None
        else:
            filepath = "../Images/product/cards/text/"
            if phase == "confirm":
                filepath += "confirm/"
            filepath += str(cardname) + ".png"
            return filepath
            
    def get_card_text(self, phase, set, cardname):
        try:
            card = open(path_to_bot + "Images/product/cards/text/" + phase + "/" + cardname + ".png", "r")
        except IOError:
            raise KeyError(cardname + " not found")
        else:
            card.close()
            filepath = "../Images/product/cards/text/" + phase + "/" + cardname + ".png"
            return filepath
            
    def get_card_image(self, set, cardname):
        try:
            card = open(path_to_bot + "Images/product/cards/img/" + phase + "/" + cardname + ".png", "r")
        except IOError:
            raise KeyError(cardname + " not found")
        else:
            card.close()
            filepath = "../Images/product/cards/img/" + phase + "/" + cardname + ".png"
            return filepath
    
    card_names_list = ["Primeval Titan", "Tezzeret, Agent of Bolas", "Gideon Jura", "Venser, the Sojourner", "Jace, the Mind Sculptor"]
    
    def get_card_keys(self):
        return self.card_names_list
    
    #stores the images of each pack
    #this is a list of all packs to buy and sell
    pack_names_list = ["M11", "ME4", "MBS", "ROE", "SOM", "WWK", "ZEN"]
    
    def get_pack_keys(self):
        return self.pack_names_list
    
    def get_pack_text(self, phase, packname):
        try:
            pack = open(path_to_bot + "Images/product/packs/text/" + phase + "/" + packname + ".png", "r")
        except IOError:
            raise KeyError(packname + " not found")
        else:
            pack.close()
            filepath = "../Images/product/packs/text/" + phase + "/" + packname + ".png"
            return filepath

    def get_all_pack_text_as_dict(self, phase):
        packs_dict = dict((abbr, self.get_packs_text(phase=phase, packname=abbr)) for abbr in self.__pack_names_list)
        return packs_dict
    
    def get_pack_image(self, packname):
        try:
            pack = open(path_to_bot + "/Images/product/packs/img/" + packname + ".png", "r")
        except:
            raise KeyError(packname + " not found")
        else:
            pack.close()
            filepath = "../Images/product/packs/" + packname + ".png"
            return filepath
        
    def get_all_pack_image_as_dict(self):
        packs_dict = dict((abbr, self.get_packs_image(abbr)) for abbr in self.__pack_names_list)
        return packs_dict
        
    #stores image of login screen
    login = {'password_field': "../Images/password_field.png" , 
               'login_success': "../Images/login_success.png" , 
               'login_fail': "../Images/login_fail.png" , 
               'login_button': "../Images/login_button.png" }
    def get_login(self, filename):
        return self.login[filename]
    
    #stores image of menu options
    menu = {'community': "../Images/community_button.png", 
              'menu': "../Images/menu_button.png", 
              'collection': "../Images/collection_button.png", 
              'home': "../Images/home_button.png", 
              'marketplace': "../Images/marketplace_button.png", 
              'classified': "../Images/classified_button.png"}
    def get_menu(self, filename):
        return self.menu[filename]