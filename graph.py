import logging
from typing import List
# TODO: Fix type hints for nested lists.

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# TODO: Add option for scatterplots instead of bar charts.
def graph_data(data) -> None:
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

    logging.info(data)
    sns.set_theme(style="whitegrid")
    logging.info(f"Data: \n{data}")
    logging.info(f"Data type: \n{type(data)}")
    ax = sns.barplot(data=data)
    plt.show()

# TODO: Add function to accept user input for job posting & keywords.

