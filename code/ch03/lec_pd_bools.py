""" lec_pd_bools.py

Companion codes for the lecture about selection obs using booleans in Pandas
"""
import pprint as pp

import pandas as pd


# ----------------------------------------------------------------------------
# Create an example dataset
# ----------------------------------------------------------------------------
data = {
    'date': [
        '2012-02-16 07:42:00',
        '2020-09-23 08:58:55',
        '2020-09-23 09:01:26',
        '2020-09-23 09:11:01',
        '2020-09-23 11:15:12',
        '2020-11-18 11:07:44',
        '2020-12-09 15:34:34',
        ],
    'firm': [
        'JP Morgan',
        'Deutsche Bank',
        'Deutsche Bank',
        'Wunderlich',
        'Deutsche Bank',
        'Morgan Stanley',
        'JP Morgan',
        ],
    'action': [
        'main',
        'main',
        'main',
        'down',
        'up',
        'up',
        'main',
        ],
}

# Convert the values in 'date' from a list to a `DatetimeIndex`
# Note: `pd.to_datetime` will return a `DatetimeIndex` instance if we pass it
# a list
data['date'] = pd.to_datetime(data['date'])
print(type(data['date'])) # --> <class 'pandas.core.indexes.datetimes.DatetimeIndex'>

# Create the dataframe and set the column 'date' as the index
df = pd.DataFrame(data=data).set_index('date')
print(df)

# Output:
#                               firm  action
# date
# 2012-02-16 07:42:00       JP Morgan   main
# 2020-09-23 08:58:55   Deutsche Bank   main
# 2020-09-23 09:01:26   Deutsche Bank   main
# 2020-09-23 09:11:01      Wunderlich   down
# 2020-09-23 11:15:12   Deutsche Bank     up
# 2020-11-18 11:07:44  Morgan Stanley     up
# 2020-12-09 15:34:34       JP Morgan   main

df.info()

# Output:
# <class 'pandas.core.frame.DataFrame'>
# DatetimeIndex: 7 entries, 2012-02-16 07:42:00 to 2020-12-09 15:34:34
# Data columns (total 2 columns):
#  #   Column  Non-Null Count  Dtype
# ---  ------  --------------  -----
#  0   firm    7 non-null      object
#  1   action  7 non-null      object
# dtypes: object(2)
# memory usage: 168.0+ bytes


# ----------------------------------------------------------------------------
#   Using booleans to select rows
# ----------------------------------------------------------------------------
# will be a series with boolean values
cond = df.loc[:, 'action'] == 'up' # --> series with dtype: bool
print(cond)

# We can use this series as an indexer:
# A series of booleans can be used to select rows that meet the criteria
res = df.loc[cond]
print(res)

# Output
#                               firm  action
# date
# 2020-09-23 11:15:12   Deutsche Bank     up
# 2020-11-18 11:07:44  Morgan Stanley     up


# Get the underlying values of `cond` as an array
new_cond = cond.array

# This will produce the same output as above
res = df.loc[new_cond]
print(res)


# Indexer not the same length as the dataframe
#df.loc[cond[:-1]]   # --> raises an exception

# ----------------------------------------------------------------------------
#   Using booleans to select rows and cols
# ----------------------------------------------------------------------------
print(df.loc[:, [True, False]])

# Output:
#                                firm
# date
# 2012-02-16 07:42:00       JP Morgan
# 2020-09-23 08:58:55   Deutsche Bank
# 2020-09-23 09:01:26   Deutsche Bank
# 2020-09-23 09:11:01      Wunderlich
# 2020-09-23 11:15:12   Deutsche Bank
# 2020-11-18 11:07:44  Morgan Stanley
# 2020-12-09 15:34:34       JP Morgan

cond = df.loc[:, 'action'] == 'up'
print(df.loc[cond, [False, True]])

print(df.isna())


#df.loc[df.isna()]  # --> exception

print(df[df.isna()])


# ----------------------------------------------------------------------------
#   Using []
# ----------------------------------------------------------------------------

cond = df.loc[:, 'action'] == 'up'
df['action'][cond] = "UP"
print(df)

# Reverting...
cond = df.loc[:, 'action'] == 'UP'
df.loc[cond, 'action'] = 'up'
print(df)


new_df = df.copy()
cond = df.loc[:, 'action'] == 'up'
new_df.loc[cond] = 'UP'
print(new_df)


# ----------------------------------------------------------------------------
#   Multiple criteria
# ----------------------------------------------------------------------------
# Combine different criteria
crit = (df.loc[:, 'action'] == 'up') | (df.loc[:, 'action'] == 'down')
print(df.loc[crit])

# ----------------------------------------------------------------------------
#   Using the `str.contains` method
# ----------------------------------------------------------------------------
crit = df.loc[:, 'action'].str.contains('up|down')
print(df.loc[crit])
