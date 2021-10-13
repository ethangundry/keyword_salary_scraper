"""
This program scrapes data from indeed.com, associating keywords with an
average salary.
"""

from csv import reader
from typing import List
# TODO: Fix type hints for nested lists.

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


def load_data() -> List[str]:
    # TODO: Scrape data from Indeed.com.
    with open('data.csv', 'r') as f:
        return pd.read_csv(f)

def load_keywords() -> List:
    with open('keywords.txt', 'r') as f:
        return f.readlines()


# TODO: Define function to search for keyword in given block of scraped
# data, to easily use any keywords desired. e.g. search if 'python' is
# in the passed data block.


# TODO: Add option for scatterplots instead of bar charts.
# TODO: Define function to output graph of data, where the y-axis is
# the keywords and the x-axis is the average salary of each keyword.
def graph_data(data, keywords: List[str]) -> None:
    """
    When passed a List of keywords and a row of salaries for each
    keyword, creates a graph based on the average salary of each
    keyword.

    Dataframe data: A Pandas dataframe of salaries for each keyword.
                    The first column in each row must be the name of a
                     keyword passed in the keywords argument.
    List[str] keywords: A List of keywords to search for the average
                        salary of.

    return: None
    """

    print(data)
    sns.set_theme(style="whitegrid")
    ax = sns.barplot(data=data, orient="h")
    plt.show()

if __name__ == "__main__":
    graph_data(load_data(), load_keywords())
