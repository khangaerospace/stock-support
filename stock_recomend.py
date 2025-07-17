import yfinance as yf
import pandas as pd

from support_handler import stock_handler

def get_all_data():
    Stock_Data =  stock_handler()
    stock_list = Stock_Data.get_all_stock_symbols()
    return stock_list

def get_currentstock():
    return ['CEU.TO', 'CCO.TO', 'TSAT.TO']

if __name__ == "__main__":
    Stock_Data =  stock_handler()
    Stock_Data.print_stock_info('CEU.TO')

    

