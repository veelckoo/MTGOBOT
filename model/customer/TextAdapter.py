"""Handles writing customer records to plain text files"""
from sikuli.Sikuli import *
path_to_bot = getBundlePath().rsplit("\\", 1)[0] + "\\"

from sys import *

class TextAdapter(object):
    
    def __init__(self, customer_name):
        try:
            customer_file = open(path_to_bot + "/customers/" + str(customer_name) + ".txt", "a")
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
        customer_file = open(path_to_bot + "customers/" + self.customer_filename + ".txt", "r")
        value = None
        for line in customer_file:
            if row_name in line:
                value = line.split(row_name + ":")
        
        customer_file.close()
        if value:
            return value[1].strip()
        if not value:
            return False
    
    def write_single_row(self, row_name, row_data):
        try:
            customer_file = open(path_to_bot + "/customer" + self.customer_filename, "r+")
            for line in customer_file:
                if row_name in line:
                    row_to_write = row_name + " : " + row_data
                else:
                    file_data += line
            customer_file.close()
        except:
            return False
        else:
            return True
                    
    def write_all_rows(self, record):
        #an iterable sequence is passed that contains all information to write
        try:
            #record the data that is currently in the text file, because once we open it in write mode, everything already on it is erased
            customer_file = open(path_to_bot + "/customer/" + self.customer_filename, "r")
            current_data = []
            for line in customer_file:
                current_data.append(line)
            customer_file.close()
            
            #now combine the current data with the new data into a new list
            record_formatted_to_list = [row_name + " : " + str(value) for row_name, value in record.items()]
            data_to_write = customer_file + record_formatted_to_list
            
            #now write out everything including the data that was already in the file
            customer_file = open(path_to_bot + "/customer/" + self.customer_filename, "w")
            for line in current_data:
                customer_file.writelines(data_to_write)
            self.customer_file.close()
        except:
            return False
        else:
            return True