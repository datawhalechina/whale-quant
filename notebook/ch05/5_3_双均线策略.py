import numpy as np
import pandas as pd
import tushare as ts

# my_token = 'xxx'
ts.set_token(my_token)
pro = ts.pro_api()
pro = ts.pro_api(my_token)

# 个股数据 https://tushare.pro/document/2?doc_id=27
df = pro.daily(ts_code='000001.SZ', start_date='20230501', end_date='20230630', fields='ts_code,trade_date,close')
df = df.sort_values(by='trade_date')

df['M5'] = df.close.rolling(window=5).mean().round(2)
df['M10'] = df.close.rolling(window=10).mean().round(2)
df['M20'] = df.close.rolling(window=20).mean().round(2)
df['M30'] = df.close.rolling(window=30).mean().round(2)

df = df.sort_values(by='trade_date', ascending=False)

df.to_csv('index_price.csv', index=False)