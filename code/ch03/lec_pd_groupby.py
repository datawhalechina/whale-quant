""" lec_pd_groupby.py

Companion codes for the lecture on GroupBy objects
"""

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
df.info()

# Output:
#                                firm action
# date
# 2012-02-16 07:42:00       JP Morgan   main
# 2020-09-23 08:58:55   Deutsche Bank   main
# 2020-09-23 09:01:26   Deutsche Bank   main
# 2020-09-23 09:11:01      Wunderlich   down
# 2020-09-23 11:15:12   Deutsche Bank     up
# 2020-11-18 11:07:44  Morgan Stanley     up
# 2020-12-09 15:34:34       JP Morgan   main

# ----------------------------------------------------------------------------
#   Creating groupby objects
# ----------------------------------------------------------------------------
groups = df.groupby(by='firm')
print(groups)

# Output:
# <pandas.core.groupby.generic.DataFrameGroupBy object at 0x7f8463863640>


print(groups.groups)

# Output:
# {'Deutsche Bank': DatetimeIndex(['2020-09-23 08:58:55', '2020-09-23 09:01:26',
#                '2020-09-23 11:15:12'],
#               dtype='datetime64[ns]', name='date', freq=None),
#  'JP Morgan': DatetimeIndex(['2012-02-16 07:42:00', '2020-12-09 15:34:34'], dtype='datetime64[ns]', name='date', freq=None),
#  'Morgan Stanley': DatetimeIndex(['2020-11-18 11:07:44'], dtype='datetime64[ns]', name='date', freq=None),
#  'Wunderlich': DatetimeIndex(['2020-09-23 09:11:01'], dtype='datetime64[ns]', name='date', freq=None)}


# ----------------------------------------------------------------------------
#   The elements of groups.groups
# ----------------------------------------------------------------------------
for firm, idx in groups.groups.items():
    print(f"Data for Firm == {firm}:")
    print("----------------------------------------")
    print(df.loc[idx])
    print("----------------------------------------")
    print("")


# Output:
#   Data for Firm == Deutsche Bank:
#   ----------------------------------------
#                                 firm action
#   date
#   2020-09-23 08:58:55  Deutsche Bank   main
#   2020-09-23 09:01:26  Deutsche Bank   main
#   2020-09-23 11:15:12  Deutsche Bank     up
#   ----------------------------------------
#
#   Data for Firm == JP Morgan:
#   ----------------------------------------
#                             firm action
#   date
#   2012-02-16 07:42:00  JP Morgan   main
#   2020-12-09 15:34:34  JP Morgan   main
#   ----------------------------------------
#
#   Data for Firm == Morgan Stanley:
#   ----------------------------------------
#                                  firm action
#   date
#   2020-11-18 11:07:44  Morgan Stanley     up
#   ----------------------------------------
#
#   Data for Firm == Wunderlich:
#   ----------------------------------------
#                              firm action
#   date
#   2020-09-23 09:11:01  Wunderlich   down
#   ----------------------------------------


# ----------------------------------------------------------------------------
#   Applying functions to individual groups
# ----------------------------------------------------------------------------
for firm, idx in groups.groups.items():
    nobs = len(df.loc[idx])
    print(f"Number of obs for Firm == {firm} is {nobs}")

# Using the apply method
res = groups.apply(len)
print(res)
print(type(res))


# ----------------------------------------------------------------------------
#   Applying pd.isna to each group
# ----------------------------------------------------------------------------
# using a loop
for firm, idx in groups.groups.items():
    print(f"pd.isna applied to df[df.firm=='{firm}']:")
    print("----------------------------------------")
    print(pd.isna(df.loc[idx]))
    print("----------------------------------------")
    print("")


# using the apply method
res = groups.apply(pd.isna)
print(res)

# Output:
#
#                       firm  action
# date
# 2012-02-16 07:42:00  False   False
# 2020-09-23 08:58:55  False   False
# 2020-09-23 09:01:26  False   False
# 2020-09-23 09:11:01  False   False
# 2020-09-23 11:15:12  False   False
# 2020-11-18 11:07:44  False   False
# 2020-12-09 15:34:34  False   False


# ----------------------------------------------------------------------------
#   The get_last function
# ----------------------------------------------------------------------------
def get_last(df):
    """ Sorts the dataframe on its index and returns
        last row of the sorted dataframe
    """
    df.sort_index(inplace=True)
    return df.iloc[-1]


for firm, idx in groups.groups.items():
    print(f"get_last applied to df[df.firm=='{firm}']:")
    print("----------------------------------------")
    print(get_last(df.loc[idx]))
    print("----------------------------------------")
    print("")

res = groups.apply(get_last)
print(res)


# Some group by operations are so common that Pandas implements them directly
# on any created instance of `GroupBy`. Here are some examples:
#
# - `GroupBy.count`: count observations per group (exclude missing values)
# - `GroupBy.size`: get group size, i.e., count observations per group (including missing values)
# - `GroupBy.last`: select last of observation in each group

# The dataframe
print(df)


# Count the number of observations inside each group:
# (includes missing values if any)
print(df.groupby('firm').size())

# Select last obs by group
print(df.groupby('firm').last())


# ----------------------------------------------------------------------------
#   Grouping by multiple columns
# ----------------------------------------------------------------------------
# Create the 'event_date' column
df.loc[:, 'event_date'] = df.index.strftime('%Y-%m-%d')
print(df)

# Split the data into groups
groups = df.groupby(['event_date', 'firm'])

# Select the most recent obs for each group
res = groups.last()
print(res)

# The index of the new series is a MultiIndex
print(res.index)


# Converting the index to columns
res.reset_index(inplace=True)
print(res)


# ----------------------------------------------------------------------------
#   The DataFrame.apply method
# ----------------------------------------------------------------------------
# Applying `len` to df
print(df)
# Output:
#                                firm action  event_date
# date
# 2012-02-16 07:42:00       JP Morgan   main  2012-02-16
# 2020-09-23 08:58:55   Deutsche Bank   main  2020-09-23
# 2020-09-23 09:01:26   Deutsche Bank   main  2020-09-23
# 2020-09-23 09:11:01      Wunderlich   down  2020-09-23
# 2020-09-23 11:15:12   Deutsche Bank     up  2020-09-23
# 2020-11-18 11:07:44  Morgan Stanley     up  2020-11-18
# 2020-12-09 15:34:34       JP Morgan   main  2020-12-09

# By default, DataFrame.apply will apply the function to each column of the data frame
res = df.apply(len)
print(res)


# Output:
# firm          7
# action        7
# event_date    7
# dtype: int64

# To apply the function to each row, set axis=1
res = df.apply(len, axis=1)
print(res)


# Output:
# date
# 2012-02-16 07:42:00    3
# 2020-09-23 08:58:55    3
# 2020-09-23 09:01:26    3
# 2020-09-23 09:11:01    3
# 2020-09-23 11:15:12    3
# 2020-11-18 11:07:44    3
# 2020-12-09 15:34:34    3
# dtype: int64


def first_two(ser):
    return ser.iloc[0:2]

# Apply to each columns
res = df.apply(first_two, axis=0)
print(res)


# Apply to each row
res = df.apply(first_two, axis=1)
print(res)


# ----------------------------------------------------------------------------
#   Creating copies of each row of a data frame
# ----------------------------------------------------------------------------
# First row of `df`
ser = df.iloc[0]


# initial version of five_copies
def five_copies0(ser):
    """ concatenate `ser` five times
    """
    ser_lst = [ser] * 5
    return pd.concat(ser_lst)

res = five_copies0(ser)
print(res)


# New version of five_copies
def five_copies1(ser):
    """ concatenate `ser` five times
    """
    ser_lst = [ser] * 5
    return pd.concat(ser_lst, axis=1)

# First row of `df`
res = five_copies1(ser)
print(res)

# New version of five_copies
def five_copies2(ser):
    """ concatenate `ser` five times
    """
    ser_lst = [ser] * 5
    wrong_df = pd.concat(ser_lst, axis=1)
    right_df = wrong_df.transpose()
    return right_df

res = five_copies2(ser)
print(res)