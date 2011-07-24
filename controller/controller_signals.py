from sikuli.Sikuli import *
path_to_bot = getBundlePath().split("bot.sikuli")[0]

import sys, copy
sys.path.append(path_to_bot + "event")

from Signal import *

pre_trade_loop = Signal()

pre_trade = Signal()

post_trade_loop = Signal()

post_trade = Signal()

post_transfer_mode = Signal()

pre_sell_mode = Signal()

post_sell_mode = Signal()

pre_buy_mode = Signal()

post_buy_mode = Signal()

pre_transaction_record = Signal(provided_args=["products_bought"])

post_transaction_record = Signal(provided_args=["products_bought"])
