""" lec_pd_indexing.py

Companion codes for the lecture on indexing pandas objects
"""

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
#   Create instances
# ----------------------------------------------------------------------------

# Create a series object
ser = pd.Series(data=prices, index=dates)
print(ser)

# Data Frame with close and Bday columns
df = pd.DataFrame(data={'Close': ser, 'Bday': bday}, index=dates)
print(df)

# ----------------------------------------------------------------------------
#   Outline:
#
#   1. Selection using loc (label based)
#     1.1 Series:
#       1.1.1 Selection using a single label
#       1.1.2 Selection using sequence of labels
#       1.1.3 Selection using slices
#     1.2 DataFrame:
#       1.2.1 Selection using a single label
#       1.2.2 Selection using sequence of labels
#       1.2.3 Selection using slices
#
#   2. Selection using iloc (position based)
#     2.1 Series:
#       2.1.1 Selection using a single label
#       2.1.2 Selection using sequence of labels
#       2.1.3 Selection using slices
#     2.2 DataFrame:
#       2.2.1 Selection using a single label
#       2.2.2 Selection using sequence of labels
#       2.2.3 Selection using slices
#
#   3. Selection using []
#     3.1 Series:
#       3.1.1 label, list of labels, label slices
#       3.1.2 position, list of positions, position slices
#
#     3.2 DataFrame:
#       3.2.1 column label, list of column labels
#       3.2.2 row label slices
#       3.2.3 row position slices
# ----------------------------------------------------------------------------

# ----------------------------------------------------------------------------
#  1. Selection using .loc
#   (only works with labels)
# ----------------------------------------------------------------------------

# 1.1 Series
# -------------


# 1.1.1 Series.loc: Selection using a single label
# ser.loc[label] --> scalar if label in index, error otherwise

# Set `x` below to be the price on 2020-01-10
x  = ser.loc['2020-01-10']

# The following will raise a KeyError
#ser.loc['3000-01-10']


# Using .loc to set elements
# Copy the series
ser2 = ser.copy()
#print(ser2)


# Set the price for 2020-01-02 to zero
#ser2.loc['2020-01-02'] = 0
#print(ser2)


# 1.1.2 Series.loc: Selection using sequence of labels
# will return a series
x  = ser.loc[['2020-01-03', '2020-01-10']]
#print(x)

#print(type(x))              # --> <class 'pandas.core.series.Series'>


# 1.1.3 Series.loc: Selection using slices
# (endpoints are included!)
# Similarly to selection with series, using slices will also return a series.
# Importantly, the endpoint will be included when selecting with slices!

# Set x so it contains all prices from '2020-01-03' to (and including) '2020-01-10'
x  = ser.loc['2020-01-03':'2020-01-10']
#print(x)


# 1.2 DataFrames
# -------------

# 1.2.1 Dataframe.loc: Selection using a single label:
# A single row and column labels will return a single value (scalar)

# For instance, selecting the close price on January 3, 2020
x  = df.loc['2020-01-03', 'Close']
#print(x)  # --> 7.19

# A single row **or** a single column label will return a series:
# The following will return a series corresponding to the column "Close"
x  = df.loc[:,'Close']
#print(x)

#print(type(df.loc[:,'Close'])) # --> <class 'pandas.core.series.Series'>

y  = df.loc['2020-01-03', :]
#print(y)

#print(type(df.loc['2020-01-03', :])) # --> <class 'pandas.core.series.Series'>

# When omitting column labels, pandas will return a series if the row label
# exists. Otherwise it will raise an exception

# This is equivalent to df.loc['2020-01-03',:]
#x = df.loc['2020-01-03']
#print(x)

#print(type(df.loc['2020-01-03'])) # --> <class 'pandas.core.series.Series'>

# This will raise an exception because the label does not exist
#df.loc['2020-01-01']

# 1.2.2 Dataframe.loc: Selection using sequence of labels
# Set x so it contains the closing prices for '2020-01-02' and '2020-01-03'
x  = df.loc[['2020-01-02', '2020-01-03'], 'Close']
#print(x)


# 1.2.3 Dataframe.loc: Selection using slices
# Using slices will return
#  - A series if the other index is a single label
#  - A data frame otherwise

# The next statement is equivalent to x = df.loc['2020-01-01':'2020-01-10']
x  = df.loc['2020-01-01':'2020-01-10', :]
#print(x)
#print(type(x))


# This will return an empty DF
#x = df.loc['2999-01-01':'2999-01-10', :]
#print(x)

# Slices can be open ended
# However, single row labels and open column slices will NOT return a
# dataframe, they will return a series!!!

#x = df.loc['2020-01-06':, :]
#print(x)

#print(type(df.loc['2020-01-06':, :])) # --><class 'pandas.core.frame.DataFrame'>

#x = df.loc['2020-01-06', 'Close':]
#print(x)


# Slices do not work as expected if the data is not sorted
# NOTE: don't worry about the rename method now

#df2 = df.copy()

#df2.rename(index={'2020-01-08':'1900-01-01'}, inplace=True)
#print(df2)

#x = df2.loc['2020-01-03':'2020-01-10', :]
#print(x)

# You can avoid these issues by sorting the dataframe first
#df2.sort_index(inplace=True)
#x = df2.loc['2020-01-03':'2020-01-10', :]
#print(x)


# This will return a DataFrame
#x = df.loc['2020-01-03':'2020-01-03']
#print(x)

# This will return a series
#x = df.loc['2020-01-03']
#print(x)


# ----------------------------------------------------------------------------
#  2. Selection using .iloc
#   (only works with positions)
# ----------------------------------------------------------------------------

# 2.1 Series
# -------------


# 2.1.1 Series.iloc: Selection using a single label
# Series.iloc using single index will return a numpy scalar

# ser.iloc[pos] --> scalar if abs(pos) < len(ser), otherwise error
x  = ser.iloc[0]
x  = ser.iloc[-1]

#x = ser.iloc[100] # raises IndexError

# Using .loc for assignment
# Copy the series

#s2 = ser.copy()
#
## assign
#s2.iloc[0] = 0
#print(s2)
#


# 2.1.2 Series.iloc: Selection using sequence of index
# If you specify a sequence of indexes, `iloc` will return a series
# containing the data items at the positional indices:

x  = ser.iloc[[0, 2]]
#print(x)


# 2.1.3 Series.iloc: Selection using slices
# Slices will not include endpoints, otherwise, work like ser.loc
x  = ser.iloc[0,1]
#print(x)

x  = ser.iloc[0,2]
#print(x)

# This will return an empty series
#x = ser.iloc[100:1001]
#print(x)


# 2.2 Dataframe
# -------------

# 2.2.1 Dataframe.iloc: Selection using a single index

# df.iloc[row pos] --> series if abs(pos) < len(df.index)
# --> series with elements from the first "row"
x  = df.iloc[0]
#print(x)

# Equivalent to
#x = df.iloc[0,:]
#print(x)


# x = df.iloc[10] # --> raises IndexError because the DF contains 10 rows


# First column (and all rows):
x  = df.iloc[:,0]
#print(x)


# 2.2.2 Dataframe.iloc: Selection using sequence of indices

# This will return a series with the first two columns as labels:
#x = df.iloc[0,[0,1]]
#print(x)


# This will return a *dataframe* with the first row of df
#x = df.iloc[0:1,:]
#print(x)


# If the column indexer is ommitted, all columns will be returned.

# df.iloc[list of row pos] --> dataframe with rows in the list
# Note: will raise IndexError if pos is out of bounds
x  = df.iloc[[0, 1]]
#print(x)


# However, Pandas will raise an exception if any of the indexes is out of
# bounds:
# x = df.iloc[[0, 10]] # --> raises IndexError

# x = df.iloc[[0,100], :] # --> raises IndexError


# 2.2.3 Dataframe.iloc: Selection using slices

# Slices work like ser.iloc
x  = df.iloc[1:1000, :]
#print(x)

# x--> empty DF
x  = df.iloc[999:1000, :]
#print(x)


# Slices can be open ended
# Set x so it includes all prices starting from the second row
x  = df.iloc[2:, :]
#print(x)

# Set x to be a series with all columns of the first row
x  = df.iloc[0, 0:]
#print(x)

# This will produce an empty series
#x = df.iloc[0, 10:]
#print(x)


# ----------------------------------------------------------------------------
#   3. Selection using []
# ----------------------------------------------------------------------------

# 3.1 Series
# -------------
#print(ser)

# Output:
#    2020-01-02    7.16
#    2020-01-03    7.19
#    2020-01-06    7.00
#    2020-01-07    7.10
#    2020-01-08    6.86
#    2020-01-09    6.95
#    2020-01-10    7.00
#    2020-01-13    7.02
#    2020-01-14    7.11
#    2020-01-15    7.04
#    dtype: float64

# 3.1.1 label, list of labels, label slices

# Single labels
#
# | Selection     | Result       | Notes                                |
# |---------------|--------------|--------------------------------------|
# | series[label] | scalar value | Label must exist, otherwise KeyError |

# Set `x` to be the price for '2020-01-13'
x  = ser['2020-01-13']
#print(x) # --> 7.02

# Try using an index label that does not exist, It will raise a KeyError
# x = ser['3000-01-10']


# List of labels
#
# | Selection              | Result | Notes                                     |
# |------------------------|--------|-------------------------------------------|
# | series[list of labels] | series | All labels must exist, otherwise KeyError |


# Set `x` to be a series with the first two rows of `ser`
x  = ser[['2020-01-02', '2020-01-03']]
#print(x)

# All labels must exist. The following will raise a KeyError because a label
# is not part of ser.index

#x = ser[['2020-01-02', '3000-01-10']]


# Using label slices
#
# | Selection                     | Result | Notes           |
# |-------------------------------|--------|-----------------|
# | series[start_label:end_label] | series | behavior varies |


# (1) If `start_label` and `end_label` are included in the index, returns all
# elements between `start_label` and `end_label` (including endpoints)

# Set `x` to include all obs between  '2020-01-13' and '2020-01-14'
x  = ser['2020-01-13':'2020-01-14']
#print(x)


# (2) If either `start_label` or `end_label` not included in the index, the
# result will depend on whether or not the index is sorted
#
#  - If index is sorted, returns the intersection between the slice and index
#  - If index is not sorted, raise a KeyError

# The `ser` above is sorted by index.
# Set `x` to include all obs between '2020-01-13' and '3000-01-01'. The
# end data (obviously) is not part of the series
x  = ser['2020-01-13':'3000-01-01']
#print(x)

# Create a series with an unsorted index
new_ser = pd.Series(data=[1,3,2], index=['a', 'c', 'b'])

# First, select a slice from 'a' to 'b'. Because both labels are included in
# the index, the slice will contain all obs between the indexes 'a' and 'b'
x  = new_ser['a':'b']
#print(x)

# Next, select a slice from 'a' to 'z'. Note that 'z' is not part of the
# index. Since the index is not sorted, the following will result in an error
# x = new_ser['b':'z']


# Series also have a method called `sort_index`, which will return a copy of the
# series with sorted indexes:

# Sort the series
sorted_ser  = new_ser.sort_index()
#print(sorted_ser)


# This will return only the first rows (not the entire series as before)
#x = sorted_ser['a':'b']
#print(x)


# `sorted_ser` is sorted so the following will return the intersection between
# the slice and the row labels
#x = sorted_ser['b':'z']
#print(x)


# 3.1.2 position, list of positions, position slices

# Using the ser created above
# ser:
#    2020-01-02    7.16
#    2020-01-03    7.19
#    2020-01-06    7.00
#    2020-01-07    7.10
#    2020-01-08    6.86
#    2020-01-09    6.95
#    2020-01-10    7.00
#    2020-01-13    7.02
#    2020-01-14    7.11
#    2020-01-15    7.04
#    dtype: float64

# Get the first element of the series
x  = ser[0]

# Get the first and fourth element (series)
x  = ser[[0,3]]

# NOTE: When using slices, the endpoints are NOT included
# This will return a series with the first element only
#x = ser[0:1]

# This will return the first five elements of the series
#x = ser[:5]
#print(x)

# This will return every other element, starting at position 0
#x = ser[::2]
#print(x)

# This returns the series in reverse order
#x = ser[::-1]
#print(x)


new_ser = pd.Series(data=['a','b', 'c'], index=[1, -4, 10])
# This will produce an empty series (because pandas thinks these are positions, not labels)
x = new_ser[1:-4]
#print(x)

# 3.2 Dataframe
# -------------


# The dataframe is:
#
#             Close  Bday
# 2020-01-02   7.16     1
# 2020-01-03   7.19     2
# 2020-01-06   7.00     3
# 2020-01-07   7.10     4
# 2020-01-08   6.86     5
# 2020-01-09   6.95     6
# 2020-01-10   7.00     7
# 2020-01-13   7.02     8
# 2020-01-14   7.11     9
# 2020-01-15   7.04    10

# 3.2.1 column label, list of column labels

#
# | Selection   | Result | Notes              |
# |-------------|--------|--------------------|
# | df[colname] | series | colname must exist |

# df[column label] --> series if column exists, error otherwise
# `x` will be a series with values in Close
#x = df['Close']
#print(x)

# Note that the label is case sensitive. For instance the following
# raises KeyError
#x = df['CLOSE']


# Sequences of labels

# | Selection            | Result | Notes                  |
# |----------------------|--------|------------------------|
# | df[list of colnames] | df     | All colname must exist |

# df[list of column labels] --> dataframe with columns in the same order
# as the column labels
# Note: All column labels must exist, otherwise error
#cols = ['Bday', 'Close']
#x = df[cols]
#print(x)

# Note: Remember that this will NOT work (because it is not a list)
#x = df['Close', 'Bday'] #--> raise error


# 3.2.2 row label slices
# ----------------------------------------------
# IMPORTANT: df[slices] will operate on rows, not columns!
# IMPORTANT: When using label slices, pandas will not raise errors if labels
# not included in the row index
#
# | Selection  | Result | Notes                              |
# |------------|--------|------------------------------------|
# | df[slices] | df     | Operates on row index, not columns |
#
# When using `[]` to slice dataframes, Pandas will look at row labels matching
# the slice, not columns. In addition, will return empty dataframe when slices
# do not match any row label.


# Slices work similar to ser[slice], i.e., they operate on row indexes
# `x` will be an empty datafame because the slice is not part of the row
# labels
#x = df['Close': 'Bday']
#print(x)

# Slicing DFs with [] works very differently than one would expect:
# `x --> dataframe with first two rows
#x = df['2020-01-02':'2020-01-03']
#print(x)

# You can use position instead of row labels, but endpoints are NOT included
# x --> all rows but the last one
#x = df[:-1]
#print(x)

# Will NOT raise error if out of bounds
# x -> returns empty DF
#x = df[100:1001]
#print(x)
# Returns:
# Empty DataFrame
# Columns: [Close, Bday]
# Index: []