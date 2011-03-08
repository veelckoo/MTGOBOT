#This code was written by Raymond Cheung
#No one is allowed to modify this code
#if you have any questions about it, I can be emailed at Darkray16@yahoo.com
#This is a bot that with automated behavior to run independantly on Magic the Gathering: Online
from sikuli.Sikuli import *
path_to_bot = getBundlePath().split("bot.sikuli")[0]

exec(open(path_to_bot + "ini.py", "rb").read())

import sys

sys.path.append(path_to_bot)

import model
import view
import controller
        

bot_app = controller.MainController()
bot_app.trade_mode()