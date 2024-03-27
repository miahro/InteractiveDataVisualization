"""Module for data cleaning and processing"""

import pandas as pd
import numpy as np


def read_data():
    """Reads the data from the csv file and returns a pandas dataframe."""
    df = pd.read_csv('./data/data.csv')
    return df


def count_distinct_values(df):
    """Checks the number of distinct values in each column of the dataframe."""
    distinct_counts = df.nunique()
    print(f"Distinc values in df: {distinct_counts}")
    zero_counts = df.select_dtypes(
        include=[np.number]).apply(lambda x: (x == 0).sum())
    print("\nZero counts in numeric columns:\n", zero_counts)


def drop_column(df, column_name):
    """Drops the column from the dataframe."""
    df = df.drop(column_name, axis=1)
    return df


def drop_row(df, col, value):
    """Drops the rows from the dataframe where the column value is equal to the given value."""
    df = df[df[col] != value]
    return df


def count_non_zero(df, col):
    """Counts the number of non-zero values in the given column."""
    non_zero_count = np.count_nonzero(df[col])
    return non_zero_count


def explore_data(df):
    """Prints the head, info, describe, columns and shape of the dataframe."""
    print(df.head())
    print(df.info())
    print(df.describe())
    print(df.columns)
    print(df.shape)


def convert_age_to_categorical(df):
    """Converts the age column to categorical column."""
    bins = [0, 24, 34, 45, 54, 64, 74, 90]
    labels = ['-24', '25-34', '35-44', '45-54', '55-64', '65-74', '75-']
    df['Age'] = pd.cut(df['Age'], bins=bins,
                       labels=labels, include_lowest=True)
    return df


def drop_rows(df, cat_vars, freq_limit):
    """Drops the rows from the dataframe where the frequency of the 
    categorical variables is less than the given limit."""
    for cat_var in cat_vars:
        value_counts = df[cat_var].value_counts()
        to_remove = value_counts[value_counts < freq_limit].index
        df = df[~df[cat_var].isin(to_remove)]
    return df
