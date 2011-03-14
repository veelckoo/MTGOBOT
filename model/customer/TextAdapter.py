"""Handles writing customer records to plain text files"""
from sikuli.Sikuli import *
path_to_bot = getBundlePath().split("bot.sikuli")[0]

from sys import *

class TextAdapter(object):
    
    def __init__(self, customer_name):
        try:
            customer_file = open(open_to_bot + "/customers/" + str(customer_name) + ".txt", "a")
        except IOError:
            print("For some reason, wasn't able to open/create customer file for " + customer_name + ".")
            print("Will write to unkown customer file")
            try:
                customer_file = open(open_to_bot + "/customers/unknown.txt", "r")
            except:
                print("Had trouble accessing/creating unkown.txt")
                raise IOError("Fatal exception trying to access or create customer records file for " + str(customer_name))
            else: self.customer_filename = "unknown.txt"
        else:
            self.customer_filename = customer_name
        
        customer_file.close()
        
    def read_row(self, row_name):
        #return a specific row
        customer_file = open(path_to_bot + "/customers/" + self.customer_filename, "r")
        for line in customer_file:
            if row_name in line:
                value = line.split(row_name + ":")
        
        customer_file.close()
        return value[1].strip()
    
    def write_all_rows(self, record):
        #an iterable sequence is passed that contains all information to write
        try:
            customer_file = open(path_to_bot + "/customer/" + self.customer_filename, "w")
            self.customer_file.writelines(record)
            self.customer_file.close()
        except:
            return False
        else:
            return True