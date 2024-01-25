""" lec_pd_numpy.py

Companion codes for the lecture on Numpy
"""

import numpy as np
import pandas as pd


# ----------------------------------------------------------------------------
#   The dates and prices lists
# ----------------------------------------------------------------------------
dates = [
  '2020-01-02',
  '2020-01-03',
  '2020-01-06',
  '2020-01-07',
  '2020-01-08',
  '2020-01-09',
  '2020-01-10',
  '2020-01-13',
  '2020-01-14',
  '2020-01-15',
  ]

prices = [
  7.1600,
  7.1900,
  7.0000,
  7.1000,
  6.8600,
  6.9500,
  7.0000,
  7.0200,
  7.1100,
  7.0400,
  ]

# Trading day counter
bday = [
  1,
  2,
  3,
  4,
  5,
  6,
  7,
  8,
  9,
  10]

# ----------------------------------------------------------------------------
#   Create two series
# ----------------------------------------------------------------------------

# Series with prices
prc_ser = pd.Series(data=prices, index=dates)

# Series with trading day
bday_ser = pd.Series(data=bday, index=dates)


# ----------------------------------------------------------------------------
#   Create a dataframe
# ----------------------------------------------------------------------------
# Data Frame with close and Bday columns
df = pd.DataFrame({'Close': prc_ser, 'Bday': bday_ser})
#print(df)

#df.info()

# Get the series containing "Close" prices
ser = df['Close']

# Get the underlying data array
print(ser.array)

# and the type
print(type(ser.array))


# The .values attribute will give you a numpy array
# with the contents of the series
#print(ser.values)

# The type is <class 'numpy.ndarray'>
#print(type(ser.values))

# ----------------------------------------------------------------------------
#   Working with missing data
# ----------------------------------------------------------------------------

# Add an empty row to the `df` dataframe
# Create a copy
df_nan = df.copy()

# Add an emtpy row to the `df_nan` dataframe
df_nan.loc['3000-01-01'] = [np.nan, np.nan]
print(df_nan)

# Note that the dtypes changed
#print("\nThis is the `df` dataframe:")
#print(df.info())
#print("\nThis is the `df_nan` dataframe:")
#print(df_nan.info())

# Convert dtypes
#df_new = df_nan.convert_dtypes()
#print(df_new.info())

#print(df_new.loc['3000-01-01'])
#print(type(df_new.loc['3000-01-01', 'Bday']))


# ----------------------------------------------------------------------------
#   The df.info method
# ----------------------------------------------------------------------------

#data = {
#      'col_a': [1, 2, 3],
#      'col_b': [10.0, None, 13.0],
#      }
#

# First a data frame without a user-defined index

#df0 = pd.DataFrame(data)
#print('\nprint(df0) -->')
#print(df0)
#print('\ndf0.info() --> ')
#df0.info()
#


# A data frame with a strings as index labels

#idx = ['2020-01-01', '2020-01-02', '2020-01-03']
#df1 = pd.DataFrame(data, index=idx)
#print('\nprint(df1) -->')
#print(df1)
#print('\ndf1.info() --> ')
#df1.info()
#

# A data frame with a datetime objs as index labels

#idx_dt = pd.to_datetime(idx)
#df2 = pd.DataFrame(data, index=idx_dt)
#print('\nprint(df2) -->')
#print(df2)
#print('\ndf2.info() --> ')
#df2.info()
