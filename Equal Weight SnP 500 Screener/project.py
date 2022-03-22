########################################################################
# Here we will make an equal weight version of the SnP 500 # 
#########################################################################
import numpy as np
import pandas as pd
import requests
import xlsxwriter
import math


stocks = pd.read_csv('sp_500_stocks.csv')

#Acquiring API token- sandbox mode of IEX
api_url = 'https://sandbox.iexapis.com/stable'
IEX_CLOUD_API_TOKEN = 'Tpk_059b97af715d417d9f49f50b51b1c448'

#making api calls
#we need market cap of each stock, price of each stock
'''all_stock_list = []
for stock in stocks['Ticker'][:5]:
    sym = stock
    api_url = 'https://sandbox.iexapis.com/stable'
    endpoint = f'/stock/{sym}/quote/?token={IEX_CLOUD_API_TOKEN}'  #this is the Key to get market cap and price
    api_url = api_url + endpoint
    #print(api_url)

    data  = requests.get(api_url).json()

    price = data['latestPrice']
    market_cap = data['marketCap']

    df_temp_list = [sym, price, market_cap, 'NA']
    all_stock_list.append(df_temp_list)

print(all_stock_list)
my_columns = ['Ticker', 'Stock Price', 'Market Cap', 'Number of Shares to buy']
final_df = pd.DataFrame(all_stock_list, columns = my_columns)

print(final_df)'''



#using batch apis
def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i+n]


symbol_groups = list(chunks(stocks['Ticker'], 100))
symbol_strings = []
for i in range(len(symbol_groups)):
    symbol_strings.append(','.join(symbol_groups[i]))



all_stock_list = []
for symbol_string in symbol_strings:
    batch_api_call_url = api_url + f'/stock/market/batch/?types=quote&symbols={symbol_string}&token={IEX_CLOUD_API_TOKEN}'
    data  = requests.get(batch_api_call_url).json()
    
    for symbol in symbol_string.split(','):
        try:
            x = data[symbol]['quote']['marketCap']
            df_temp_list = [symbol, data[symbol]['quote']['latestPrice'], data[symbol]['quote']['marketCap'], 'N/A']
            all_stock_list.append(df_temp_list)
        except:
            print(f'symbol {symbol} not found')


my_columns = ['Ticker', 'Stock Price', 'Market Cap', 'Number of Shares to buy']
final_df = pd.DataFrame(all_stock_list, columns = my_columns)

print(final_df)


#calculate Number of Shares to buy
portfolio_size = int(input('Enter the value of your postfolio: '))

position_size = portfolio_size/len(final_df.index)



for i in range(len(final_df.index)):
    final_df.loc[i, 'Number of Shares to buy'] = position_size//final_df.loc[i, 'Stock Price']


print(final_df)
writer = pd.ExcelWriter('recommended trades.xlsx', engine = 'xlsxwriter')
final_df.to_excel(writer, 'Recommended Trades', index = False)

writer.save()