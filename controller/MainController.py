from sikuli.Sikuli import *

path_to_bot = getBundlePath().rsplit("\\", 1)[0] + "\\"

exec(open(path_to_bot + "ini.py", "rb").read())

#date required for transaction recording
from datetime import datetime

import sys
sys.path.append(path_to_bot + "model")
sys.path.append(path_to_bot + "controller")
sys.path.append(path_to_bot + "view")
import ErrorHandler

sys.path.append(path_to_bot + "model/customer")
import CustomerDAL

import ITrade
import ISell
import IBuy
import ISignIn
import IClassified
import IChat

class MainController(object):
    #this class will control and instanciate all the other classes
    #it will contain the logic and manipulate all the data
    #and pass data between the classes it owns
    
    def __init__(self):
        
        self.Itrade = ITrade.ITrade()
        self.Isell = ISell.ISell()
        self.Ibuy = IBuy.IBuy()
        self.Isignin = ISignIn.ISignIn()
        self.Iclassified = IClassified.IClassified()
        self.Ichat = IChat.IChat()
        self.selling_greeting = "Entering selling mode.  When you are finished taking products, please type the word \"DONE\" in all lowercase, and click confirm."
        self.buying_greeting = "Entering buying mode.  I will search your collection for products to buy.  This may take several minutes depending how much you have available.  Please wait..."
        
        #run the controllers startup method on instanciation
        self.mode = settings["DEFAULTMODE"]
        
    def startup(self):
        #log into Magic Online
        self.define_region()
        if self.Isignin_in.log_in():
            #run maintanence and inventory check
            self.maintenance_mode()
            #once everything is clear and ready, start selling
            self.Iclassified.set_posting()
            if(self.mode == "default"):
                self.default_mode()
            elif(self.mode == "buy"):
                self.buy_mode()
            elif(self.mode == "maintenance"):
                self.maintenance_mode()
            else:
                raise ErrorHandler("Default mode not set in bot settings")
                
    def trade_mode(self, mode=None):
        """if you wish to set the bot to only sell or buy, then set param mode to
        "sell" or "buy" to force the bot mode"""
        
        #puts the bot into sell mode, will wait for trade request
        if(self.Itrade.start_wait("incoming_request")):
            #minimize the chat window to the side
            if(self.Itrade.accept_trade()):
                self.Ichat.minimize_chat_window()
                  
                ## DEBUG: onChange method is not working correctly, ##
                #signals that the customer is taking something and the transaction will be a sale
                #wait(2)
                #self.Itrade.giving_window_region.onChange(self.set_mode("sell"))
                if not mode:
                    mode=settings["DEFAULTMODE"]
                
                self.set_mode(mode=mode)
                
                #if done too quickly, the customers name isn't in place yet
                wait(4)
                customer_name = self.Itrade.get_customer_name()
                customer_model = CustomerDAL.CustomerDAL(adapter=settings["RECORD_OUTPUT_FORMAT"], customer_name=customer_name)
                
                #enter selling mode
                if self.get_mode() == "sell":
                    self.Ichat.type_msg(self.selling_greeting + " You have " + str(customer_model.read_credits()) + " credits saved.")
                    self.Isell.set_windows()
                    products_sold = self.Isell.complete_sale(customer_credit=customer_model.read_credits())
                    
                    receipt = None
                    if products_sold:
                        receipt = {"sold":{}, "bought":{}}
                        for product in products_sold:
                            customer_model.write_transaction(type="sale", product=product["name"], quantity=product["quantity"])
                        customer_model.write_credits((1-(products_bought["total_tickets"]%1)))
                        customer_model.write_transaction_date(time=datetime.now())

                    
                #enter buying mode
                elif self.get_mode() == "buy":
                    self.Ichat.type_msg(self.buying_greeting + " You have " + str(customer_model.read_credits()) + " credits saved.")
                    self.Ibuy.set_windows()
                    #take packs from the customer
                    products_bought = self.Ibuy.complete_purchase(customer_credit=customer_model.read_credits())
                    
                    receipt = None
                    if products_bought:
                        total_sale = 0
                        receipt = {"sold":{}, "bought":{}}
                        for product in products_bought:
                            customer_model.write_transaction(type="purchase", product=product["name"], quantity=product["quantity"])
                        customer_model.write_credits(products_bought["total_tickets"] % 1)
                        customer_model.write_transaction_date(time=datetime.now())
                    
                    
        self.trade_mode()
        
    def transfer_mode(self):
        #puts the bot into transfer mode, will check inventory and transfer items to other bots
        #check if bot is part of network
        if(BotSetting.getSetting("NETWORK")):
            pass
            
    def maintenance_mode(self):
        #puts the bot maintanence mode to check inventory
        pass
        
    def set_mode(self, mode):
        #set the bot mode to sell or buy
        self.status = mode
        
    def get_mode(self):
        #get the current mode
        if self.status:
            return self.status
        else:
            raise ErrorHandler("Current Mode Uknown")