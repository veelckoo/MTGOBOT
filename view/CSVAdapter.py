
from sikuli.Sikuli import *
path_to_bot = getBundlePath().split("bot.sikuli")[0]

class CSVAdapter(object):
    
    def read_inventory_file(self, path_to_csv):
        #parse file info
        try:
            inventory_file = open(path_to_csv, "r")
        except IOError:
            raise ErrorHandler("Unable to read inventory file")
        else:
            inventory = {}
            
            for line in inventory_file:
            
                row = line.split(",")
                inventory[row[0]]["set"] = row[4]
            
                if inventory[row[6]] == "Yes":
                    version = "foil"
                elif inventory[row[6]] == "No":
                    version = "regular"
                else:
                    raise ErrorHandler("Something done broke")
                    
                inventory[row[0]][version]["online"] = row[1]
                inventory[row[0]][version]["for_trade"] = row[2]
                inventory[row[0]][version]["set"] = row[4]
                
            return inventory
            
        return False
        
    def create_inventory_file(self, inventory_data):
        if not inventory_data:
            raise Errorhandler("create_inventory_file called, but no inventory data passed")
        
        inventory_file = open(path_to_bot + "/inventory/trade_data.csv", "w")
        
        for line in inventory_data:
            line_formatted = line.title()
            inventory_file.writelines(line + "\n")
            
        inventory_file.close()