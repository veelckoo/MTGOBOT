from sikuli.Sikuli import *
path_to_bot = getBundlePath().split("bot.sikuli")[0]

import sikuli.Sikuli


class DataStorage(object):
    #object that will handle exporting transaction history
    #you must have the program that you want to send the transaction to, open
    #methods of storage being considered, xml, excel, mysql
        
    def write(self, transaction):
        #write the transaction record to a text file
        current_transaction = self.convert_trans_to_string(transaction)
        #now write the transaction to the file
        try:
            transaction_file = open(path_to_bot + "transaction_records/transactions.txt", "a")
            transaction_file.writelines(current_transaction)
            transaction_file.close()
        except OIError:
            print("IO error: Could not write following line to transaction records.")
            print(transaction_file)
        
    def convert_trans_to_string(self, transaction):
        """takes the transaction variable created in Session class and converts it to string"""
        #note, repr will not work because it doesn't remove curly brackets and colons
        record_list = []
        for attribute, value in transaction.iteritems():
            if attribute == "bought" or attribute == "sold":
                record_list.append(str("mode: " + attribute + "  "))
                for product,quantity in value.iteritems():
                    record_list.append(str(product + ":"))
                    record_list.append(str(quantity) + " ")
            else:
                record_list.append(str(attribute + ": " + value + " "))
            
        record_string = "".join(record_list) + "\n"
        return record_string