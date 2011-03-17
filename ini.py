from sikuli.Sikuli import *

#this object will hold all global settings for the application
#ERRORHANDLERAPP = How the app will output errors, possible values: Notepad

#USERNAME = Your Magic Online username

#PASSWORD = Your Magic Online password

#NETWORK = Whether you have other bots that you wish this bot to interact with for chores like farming and juggling products

#DEFAULTMODE = the mode that the bot will automatically go into when a trade is opened, possible values: buy, sell

#CARD_BUYING = Whether the bot will search for specific cards in searchfield or just skim through the collection
#by category.  Search is better if your card buy list is small(less than a dozen or so), all is better if there
#are many cards listed in the card_buy pricelist, meaning there are many cards you would buy.  Valid strings: "bulk", "search"

settings = {"ERRORHANDLERAPP":"Notepad", 
            "LOGIN_WAIT":45, 
            "USERNAME": "yourmagiconlineusername", 
            "PASSWORD":"yourpasswordhere", 
            "NETWORK":False, 
            "DEFAULTMODE":"sell",
            "CARD_BUYING":"bulk"}
            
#these are the settings for bot to use when buying cards in bulk, i.e. when not searching for specific cards,
#but rather when it's buying all cards the customer has available
#Any setting set to yes means the bot will buy cards from that category
#hint: use the find/replace feature in your editor to replace the yes/no text to save time
bulkcardbuying = {"mythic": "yes",
                  "rare": "yes",
                  "uncommon": "yes",
                  "common": "yes",
                  "set": {"Standard": "yes",
                          "Extended": "no",
                          "Classic": "no",
                          "Legacy": "no",
                          "Scars of Mirrodin": "yes",
                          "Mirrodin Besieged": "yes",
                          "Zendikar": "yes",
                          "Worldwake": "yes",
                          "Rise of the Eldrazi": "yes",
                          "Shards of Alara": "no",
                          "Conflux": "noConflux",
                          "Alara Reborn": "no",
                          "Lorwyn": "no",
                          "Morningtide": "no",
                          "Shadowmoor": "no",
                          "Eventide": "no",
                          "Time Spiral": "no",
                          "Timeshifted": "no",
                          "Planar Chaos": "no",
                          "Future Sight": "no",
                          "Ice Age": "no",
                          "Alliance": "no",
                          "Coldsnap": "no",
                          "Ravnica": "no",
                          "Guildpact": "no",
                          "Dissension": "no",
                          "Champions of Kamigawa": "no",
                          "Betrayers of Kamigawa": "no",
                          "Saviors of Kamigawa": "no",
                          "Mirrodin": "no",
                          "Darksteel": "no",
                          "Fifth Dawn": "no",
                          "Onslaught": "no",
                          "Legion": "no",
                          "Scourge": "no",
                          "Odyssey": "no",
                          "Torment": "no",
                          "Judgment": "no",
                          "Invasion": "no",
                          "Planeshift": "no",
                          "Apocalypse": "no",
                          "Urza's Saga": "no",
                          "Urza's Legacy": "no",
                          "Urza's Destiny": "no",
                          "Tempest": "no",
                          "Stronghold": "no",
                          "Exodus": "no",
                          "Mirage": "no",
                          "Visions": "no",
                          "Weatherlight": "no",
                          "Seventh Edition": "no",
                          "Eighth Edition": "no",
                          "Ninth Edition": "no",
                          "Tenth Edition": "no",
                          "Magic 2010": "no",
                          "Magic 2011": "yes",
                          "Masters Edition": "no",
                          "Masters Edition II": "no",
                          "Masters Edition III": "no",
                          "Masters Edition IV":"no"}}
#default is 1
Settings.MoveMouseDelay = 0.2
#default is False, don't show visual guide to actions
setShowActions(False)
#default is 2.0(2 seconds delay on show actions)
Settings.SlowMotionDelay = 1.5
#set this lower if cpu usage is too high
Settings.WaitScanRate = 6
#must be 0.8 to 1, in order to maintain accuracy, MAY NOT affect pixel matching operations besides find()
Settings.MinSimilarity = 0.9
#min pixel change to trigger onChange
Settings.ObserveMinChangedPixels = 200
#all find operations which don't use other regions should use this one
