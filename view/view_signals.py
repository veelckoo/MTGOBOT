from sikuli.Sikuli import *
path_to_bot = getBundlePath().split("bot.sikuli")[0]

import sys, copy
sys.path.append(path_to_bot + "event")

from Signal import *
