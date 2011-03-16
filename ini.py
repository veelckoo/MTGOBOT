from sikuli.Sikuli import *

#this object will hold all global settings for the application
#ERRORHANDLERAPP = How the app will output errors, possible values: Notepad

#USERNAME = Your Magic Online username

#PASSWORD = Your Magic Online password

#NETWORK = Whether you have other bots that you wish this bot to interact with for chores like farming and juggling products

#DEFAULTMODE = the mode that the bot will automatically go into when a trade is opened, possible values: buy, sell

#CARD_BUYING = Whether the bot will search for specific cards in searchfield or just skim through the collection
#by category.  Search is better if your card buy list is small(less than a dozen or so), all is better if there
#are many cards listed in the card_buy pricelist, meaning there are many cards you would buy

settings = {"ERRORHANDLERAPP":"Notepad", 
            "LOGIN_WAIT":45, 
            "USERNAME": "yourmagiconlineusername", 
            "PASSWORD":"yourpasswordhere", 
            "NETWORK":False, 
            "DEFAULTMODE":"buy",
            "CARD_BUYING":"search"}

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
