"""handles reading and writing to customer records like saved credits
using this as a data abstraction layer will allow me to switch out the CustomerModel
which handles all the db adapter functions, useful if I later switch 
to a different db, i.e. Excel, MySQL, etc"""

from sikuli.Sikuli import *
path_to_bot = getBundlePath().split("bot.sikuli")[0]

from sys import *
sys.path.append(path_to_bot + "model")
import CustomerModel

class CustomerDAL(object):
    
    def __init__(self, customer_name):
        self.db_adapter = CustomerModel.CustomerModel(customer_name)
        
    def read_credits(self):
        pass
    
    def write_transaction_id(self, id):
        self.transaction_id = id
    
    def write_credits(self, amount):
        self.credits_to_write = amount
    
    def write_comments(self, comment):
        self.comments_to_write = comment
    
    def save(self):
        try:
            int(amount)
        except ValueError:
            amount = "Error creating transaction id number."
        #call the write_row method for each of the transaction rows