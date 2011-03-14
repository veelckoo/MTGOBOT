"""handles reading and writing to customer records like saved credits
using this as a data abstraction layer will allow me to switch out the CustomerModel
which handles all the db adapter functions, useful if I later switch 
to a different db, i.e. Excel, MySQL, etc"""

from sikuli.Sikuli import *
path_to_bot = getBundlePath().split("bot.sikuli")[0]

from sys import *
sys.path.append(path_to_bot + "model/customer" )
import TextAdapter
import MySQLAdapter

from datetime from datetime

class CustomerDAL(object):

    def __init__(self, adapter):
        adapters = {"text":TextAdapter.TextAdapter(),
                    "excel":ExcelAdapter.ExcelAdapter(),
                    "mysql":MySQLAdapter.MySQLAdapter()}
        self.db_adapter = adapters.get(adapter, lambda: None)
        self.record = {}

    def read_credits(self):
        return self.db_adapter.read_row("credits")

    def write_credits(self, amount):
        self.record.append("credit: " + str(amount))
        
    def write_transaction_id(self, id):
        self.record.append("id: " + str(id))

    def write_comments(self, comment):
        full_comment_string = []
        full_comment_string.append("comment: ")
        full_comment_string.append(comment)
        full_comment_string.append(datetime.now())
        
        self.record.append(" ".join(full_comment_string))

    def save(self):
        #validate the customer information, if no exceptions, then write to file
        try:
            int(amount)
        except ValueError:
            amount = "Error creating transaction id number."
        #call the write_row method for each of the transaction rows
        
        self.db_adapter.write_records(self.record)