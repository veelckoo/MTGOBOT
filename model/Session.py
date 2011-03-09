from sikuli.Sikuli import *

path_to_bot = getBundlePath().split("bot.sikuli")[0]

import sys
sys.path.append(path_to_bot + "model")
import DataStorage

class Session(object):
    #object to contain info on each trade session
    
    def __init__(self):
        self.db = DataStorage.DataStorage()
    
    def record(self):
        #send the session info to storage
        self.db.write(self.transaction)
        
    #all the get and set methods
        
    def set_customer(self, name):
        self.customer = Customer(name)
        
    def get_customer(self):
        return self.customer
        
    def set_transaction(self, trans):
        """This function receives a dictionary of items sold, and items bought, and at what price"""
        """Example : trans { "customer" : "john", "bought": { "Magic 2011 Booster":"4", "Scars of Mirrodin Booster":"4", "Magic 2011":"4"}, "sold": {"Frost Titan":"20", "Venser, the Sojouner":"25"}"""
        self.transaction = trans
        print("transaction set")
        
    def get_transaction(self):
        return self.transaction
        
    def set_time(self, time):
        self.time = time
        
    def get_time(self):
        return self.time