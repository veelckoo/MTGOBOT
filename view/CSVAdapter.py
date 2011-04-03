
class CSVAdapter(self):
    
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
                inventory[row[0]][version]["rarity"] = row[3]
                inventory[row[0]][version]["set"] = row[4]
                
            return inventory
            
        return False