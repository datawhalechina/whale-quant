""" lec_pd_joins.py

Companion codes for the lecture on combining pandas objects
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
#   Example series and data frame
# ----------------------------------------------------------------------------

# Series with prices
ser = pd.Series(data=prices, index=dates)
# Data Frame with close and bday columns
df = pd.DataFrame({'close': ser, 'bday': bday})


# ----------------------------------------------------------------------------
#   Review: The operator "+" behaves differently depending on the operands
# ----------------------------------------------------------------------------
# Simple sums with integers
print(1 + 1)              # --> 2

# String concatenation
print('1' + '1')          # --> '11'

# List concatenation
print([1] + [2, 3])       # --> [1, 2, 3]


# ----------------------------------------------------------------------------
#   Adding a scalar to a series
# ----------------------------------------------------------------------------
# ser is:
#  2020-01-02    7.16
#  2020-01-03    7.19
#  2020-01-06    7.00
#  2020-01-07    7.10


# Adding an integer to a series of floats
new_ser = ser + 1
print(new_ser)

# Output:
#  2020-01-02    8.16
#  2020-01-03    8.19
#  2020-01-06    8.00
#  2020-01-07    8.10


# If you try to add a string, an exception will be raised
# (Uncomment to test)
#new_ser = ser + '1'  # --> Exception

# We can add a string to a series containing strings
s0 = pd.Series(['1', '2', '3'])
s1 = s0 + '1'
print(s1)

# Output:
#  0    11
#  1    21
#  2    31
#  dtype: object


# ----------------------------------------------------------------------------
#  Adding a series to another
# ----------------------------------------------------------------------------

print(ser)
# Output:
#  2020-01-02    7.16
#  2020-01-03    7.19
#  2020-01-06    7.00
#  2020-01-07    7.10
#  dtype: float64


# Summing two series with the same index
# (obviously, adding a series to itsef will do that...)
print(ser + ser)

# Output:
#  2020-01-02    14.32
#  2020-01-03    14.38
#  2020-01-06    14.00
#  2020-01-07    14.20
#  dtype: float64



# Summing `ser` to the subset ser[:-1]
# Note how the last price is not summed
print(ser + ser[:-1])

# Returns::
#  2020-01-02    14.32
#  2020-01-03    14.38
#  2020-01-06    14.00
#  2020-01-07    14.20
#  2020-01-08    13.72
#  2020-01-09    13.90
#  2020-01-10    14.00
#  2020-01-13    14.04
#  2020-01-14    14.22
#  2020-01-15      NaN
#  dtype: float64

# What happens when there are no common indexes?
# Create another series
s2 = pd.Series([1,2], index=['2900-01-01', '2900-01-02'])
print(s2)
# Output:
#   2900-01-01    1
#   2900-01-02    2
#   dtype: int64

print(ser + s2)

# Output::
#  2020-01-02   NaN
#  2020-01-03   NaN
#  2020-01-06   NaN
#  2020-01-07   NaN
#  2020-01-08   NaN
#  2020-01-09   NaN
#  2020-01-10   NaN
#  2020-01-13   NaN
#  2020-01-14   NaN
#  2020-01-15   NaN
#  2900-01-01   NaN
#  2900-01-02   NaN
#  Length: 12, dtype: float64


# ----------------------------------------------------------------------------
#   Operations between dataframes
# ----------------------------------------------------------------------------

print(df)
# Output:
#              close  bday
#  2020-01-02   7.16     1
#  2020-01-03   7.19     2
#  2020-01-06   7.00     3
#  2020-01-07   7.10     4
#  2020-01-08   6.86     5
#  2020-01-09   6.95     6
#  2020-01-10   7.00     7
#  2020-01-13   7.02     8
#  2020-01-14   7.11     9
#  2020-01-15   7.04    10

# This will be a dataframe with just one column 'bday'
# (Note the column argument is a list of one element)
df2 = df.iloc[1:3, [1]]
print(df2)
# Output:
#              bday
#  2020-01-03     2
#  2020-01-06     3
print(df + df2)
# Output:
#              bday  close
#  2020-01-02   NaN    NaN
#  2020-01-03   4.0    NaN
#  2020-01-06   6.0    NaN
#  2020-01-07   NaN    NaN
#  2020-01-08   NaN    NaN
#  2020-01-09   NaN    NaN
#  2020-01-10   NaN    NaN
#  2020-01-13   NaN    NaN
#  2020-01-14   NaN    NaN
#  2020-01-15   NaN    NaN

# ----------------------------------------------------------------------------
#   Operations between dataframes and series
# ----------------------------------------------------------------------------
# This is a series of 1, indexed by dates
ones_by_dates = pd.Series(1, index=dates)

# In:
print(ones_by_dates)

# Output:
#  2020-01-02    1
#  2020-01-03    1
#  2020-01-06    1
#  2020-01-07    1
#  2020-01-08    1
#  2020-01-09    1
#  2020-01-10    1
#  2020-01-13    1
#  2020-01-14    1
#  2020-01-15    1
#  dtype: int64

# This is a series of 1, indexed by the columns of df
ones_by_cols = pd.Series(1, index=['bday', 'close'])

# In:
print(ones_by_cols)

# Output:
#  bday     1
#  close    1
#  dtype: int64

# This will produce a dataframe of NaN
print(df + ones_by_dates)

# Output:
#  2020-01-02  2020-01-03  2020-01-06  2020-01-07  2020-01-08  2020-01-09  2020-01-10  2020-01-13  2020-01-14  2020-01-15  bday  close
#  2020-01-02         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN   NaN    NaN
#  2020-01-03         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN   NaN    NaN
#  2020-01-06         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN   NaN    NaN
#  2020-01-07         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN   NaN    NaN
#  2020-01-08         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN   NaN    NaN
#  2020-01-09         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN   NaN    NaN
#  2020-01-10         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN   NaN    NaN
#  2020-01-13         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN   NaN    NaN
#  2020-01-14         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN   NaN    NaN
#  2020-01-15         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN   NaN    NaN


# This will add one to each column
print(df + ones_by_cols)

# Output:
#              bday  close
#  2020-01-02     2   8.16
#  2020-01-03     3   8.19
#  2020-01-06     4   8.00
#  2020-01-07     5   8.10
#  2020-01-08     6   7.86
#  2020-01-09     7   7.95
#  2020-01-10     8   8.00
#  2020-01-13     9   8.02
#  2020-01-14    10   8.11
#  2020-01-15    11   8.04


# ----------------------------------------------------------------------------
#   Joins
# ----------------------------------------------------------------------------

# Create two data frames:
#
# Left:
#
# | idx | L  |
# |-----+----|
# | 1   | L1 |
# | 2   | L2 |
# | 3   | L3 |

left = pd.DataFrame(
        data=[('L1'), ('L2'), ('L3')],
        index=[1,2,3],
        columns=['L'],
        )
print(left)



# Right:
#
# | idx | R  |
# |-----+----|
# | 3   | R3 |
# | 4   | R4 |
# | 5   | R5 |

right = pd.DataFrame(
        data=[('R3'), ('R4'), ('R5')],
        index=[3,4,5],
        columns=['R'],
        )
print(right)


#   Understanding the different types of joins:
#
#
#
# We want to merge the Right and Left tables using the column `idx`.
# As you can see, there are some values of `idx` that appear only on the `Left`
# table, some that appear only in the `Right` table, and some that are common to
# both tables. We can think of a merge between these two tables as following:
#
#
# Left:                   Right:              Merged
#
# | idx | L  | Join type    | idx | R  | Result   | idx | L   | R   |
# | 1   | L1 | -----------> | 3   | R3 | -------> | ... | ... | ... |
# | 2   | L2 |              | 4   | R4 |          | ... | ... | ... |
# | 3   | L3 |              | 5   | R5 |
#
# The resulting table will depend on the type of join:


#
# - Left join: Keep all the idxs of the left table (Left)
#
# Left:                   Right:              Merged
# | idx | L |   Left Join   | idx | R |  Result   |idx| L | R |
# | 1   | L1|  -----------> | 3   | R3|  -------> |1  | L1|NaN|
# | 2   | L2|               | 4   | R4|           |2  | L2|NaN|
# | 3   | L3|               | 5   | R5|           |3  | L3| R3|
#
print(left.join(right, how='left'))

# - Right join: Keep all the idxs of the right table (Right)
#
# Left:                   Right:              Merged
# | idx | L  | Right Join   | idx | R  | Result   | idx | L   | R  |
# | 1   | L1 | -----------> | 3   | R3 | -------> | 3   | L3  | R3 |
# | 2   | L2 |              | 4   | R4 |          | 4   | NaN | R4 |
# | 3   | L3 |              | 5   | R5 |          | 5   | NaN | R5 |
#
print(left.join(right, how='right'))

#
# - Inner join: Keep only the idxs that exist in both left and right
#
# Left:                   Right:              Merged
# |idx| L |  Inner Join   |idx| R |  Result   |idx| L | R |
# |1  | L1|  -----------> |3  | R3|  -------> |3  | L3| R3|
# |2  | L2|               |4  | R4|
# |3  | L3|               |5  | R5|
#
print(left.join(right, how='inner'))

# - Outer join: Keep all the idxs in left and right
#
# Left:                   Right:              Merged
# |idx| L |  Outer Join   |idx| R |  Result   |idx| L | R |
# |1  | L1|  -----------> |3  | R3|  -------> |1  | L1|NaN|
# |2  | L2|               |4  | R4|           |2  | L2|NaN|
# |3  | L3|               |5  | R5|           |3  | L3| R3|
#                                             |4  |NaN| R4|
#                                             |5  |NaN| R5|
print(left.join(right, how='outer'))