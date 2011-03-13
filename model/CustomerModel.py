#handles reading and writing to customer records like saved credits
from sikuli.Sikuli import *
path_to_bot = getBundlePath().split("bot.sikuli")[0]

from sys import *

class CustomerModel(object):
    
    def __init__(self, customer_name):
        try:
            customer_file = open(open_to_bot + "/customers/" + str(customer_name) + ".txt", "r+")
        except IOError:
            print("For some reason, wasn't able to open/create customer file for " + customer_name + ".")
            print("Will write to unkown customer file")
            try:
                customer_file = open(open_to_bot + "/customers/unknown.txt", "r+")
            except:
                print("Had trouble accessing/creating unkown.txt")
                raise IOError("Fatal exception trying to access or create customer records file for " + str(customer_name))
    
    def read_row(self):
        #read out the number of credits customer has
        pass
    
    def write_row(self, string):
        #write out the number of credits customer has
        
        #copy file contents first, file will be overwritten
        
        #then rewrite all content with adjustments
        
        pass
        