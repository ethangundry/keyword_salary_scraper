"""
This program scrapes data from indeed.com, associating keywords with an
average salary.
"""

import logging
from typing import List
# TODO: Fix type hints for nested lists.


from graph import graph_data
from scrape import collect_postings, scrape_posting, scrape_data

logging.basicConfig(level=logging.INFO)

# TODO: Refactor functions into separate files.
# TODO: Add multithreading to speed up process.

# TODO: Add function to simply search for number of occurrences among 
# given jobs.

def main():
    user_val = "1"
    search = input("Please enter the job you wish to search for keywords in.")
    pages = int(input("How many pages would you like to search through?"))
    keywords = []
    while user_val:
        # TODO: Add support for one-letter keywords (C, R, etc.) by
        # automatically adding spaces and HTML values for bullet 
        # points to the keyword.
        user_val = input("Please enter keywords you wish to search for. "
                              "If you are done entering keywords, simply enter"
                              " nothing.")
        print(user_val)
        if user_val == "":
            pass
        else:
            keywords.append(user_val)

    x = scrape_data(collect_postings(search, pages), keywords)
    graph_data(x)
    print(f"Total job postings scraped: {pages * 10}")






if __name__ == "__main__":
    main()
