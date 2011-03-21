from sikuli.Sikuli import *
path_to_bot = getBundlePath().split("bot.sikuli")[0]

import sys
sys.path.append(path_to_bot + "model/pricelist")
import ProductPriceModel


class CardPricesDAL(object):
    #DAL layer for pricelist for buying and selling single cards
    def __init__(self):
        price_model = ProductPriceModel.ProductPriceModel()
        self.buy = price_model.get_prices(product="cards", list="buy")
        self.sell = price_model.get_prices(product="cards", list="sell")
       
    #set prices is to be done in gui bot settings prior to transaction
    def set_buy_price(self, name, price):
        self.buy[name.upper()] = price
    def set_sell_price(self, name, price):
        self.sell[name.upper()] = price
        
    def get_buy_price(self, name):
        return self.buy[name.upper()]
    def get_sell_price(self, name):
        return self.sell[name.upper()]