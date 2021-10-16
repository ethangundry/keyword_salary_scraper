"""
This program scrapes data from indeed.com, associating keywords with an
average salary.
"""

import logging
import re
import time
from typing import List
# TODO: Fix type hints for nested lists.

import bs4
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests
import seaborn as sns

logging.basicConfig(level=logging.WARNING)

# TODO: Refactor functions into separate files.

def main():
    user_val = "1"
    search = input("Please enter the job you wish to search for keywords in.")
    pages = int(input("How many pages would you like to search through?"))
    keywords = []
    while user_val:
        user_val = input("Please enter keywords you wish to search for. "
                              "If you are done entering keywords, simply enter"
                              " nothing.")
        print(user_val)
        keywords.append(user_val)

    x = scrape_data(collect_postings(search, keywords, ))
    graph_data(x)


# TODO: Define function to scrape x number of job postings using some
# search word from indeed.com.
def collect_postings(search: str, keywords: list, page: int = 2) -> list:
    # TODO: Add 'location' parameter.
    """
    When passed a given search for job postings, will scrape through
    (page * 10) job postings and return a list of all the job urls.

    str search: The job title to search for.
    list[str] keywords: The keywords to search for.
    int page: The amount of pages to search through.

    return list[str]: The list of URL postfixes of job postings.

    """

    headers = {'User-Agent':
               'Mozilla/5.0 (X11; Linux x86_64; rv:91.0)'
               'Gecko/20100101 Firefox/91.0'}
    url_list = []

    for i in range(1, page + 1):
        # Indeed uses &start=x to track its pages, where x is the page 
        # number you're on times 10, minus 10. So page 1 is 0, page 2 is 10
        # etc.
        url = (f"https://www.indeed.com/jobs?q={search}&l=seattle"
               f"&start={i * 10 - 10}")
        logging.info(url)
        jobs = requests.get(url, headers)


        soup = BeautifulSoup(jobs.content, "html.parser")
        for link in soup.find_all('a'):
            try:
                if 'tapItem' in link.get('class'):
                    url_list.append("http://indeed.com" + link.get('href'))
            # Occurs when there is no class.
            except TypeError:
                continue

    logging.info(f"URL LIST: {url_list}")
    assert url_list
    return url_list


def scrape_posting(response, keyword: str):
    """
    When passed the request object containing an indeed.com job posting
    page, will check whether the page contains the given keyword, and
    if so, will return a list containing the salary of the job,
    followed by each valid keyword.

    response: A requests response object.
    str keyword: The keyword to search for.
    """

    soup = BeautifulSoup(response.content, 'html.parser')
    # If the job doesn't have a salary listing, simply return None.
    if not soup.find("div", string="Salary"):
        logging.info("Salary not found.")
        return None


    # TODO: Clean up regex. Make it faster and easier to read.

    salary = soup.find("div", string="Salary").parent.span.text
    # TODO: Add ability to exclude hourly salaries, or convert to 
    # annual salaries.
    if "hour" in salary:
        logging.info("Pays hourly; skipped for now.")
        return None
    elif "month" in salary:
        logging.info("Pays monthly; skipped for now.")
        return None

    logging.info(f"PRE-REGEX SALARY: {salary}")
    # Match a string that begins with $ and 1 or more numeric digits
    # after the dollar sign, with room included for commas in the
    # salary. Then, gets everything past the dollar sign.
    # TODO: Add options for a salary range as well, e.g. 
    # $100,000 - $180,000. 
    salary_pattern = re.compile(r".*(\$\d+,*\d+).*")
    # Gets everything past the dollar sign and replaces the commas with
    # empty space, so an int can be returned.
    logging.info("SALARY PATTERN GROUP 0:")
    logging.info(salary_pattern.match(salary).group(0))
    logging.info("SALARY PATTERN GROUP 1:")
    logging.info(salary_pattern.match(salary).group(1))

    salary = int(salary_pattern.match(salary).group(1)[1:].replace(',', ''))

    # Convert to lower for comparison to text.
    keyword = keyword.lower()
    job_text = soup.find("div", id="jobDescriptionText").text
    logging.info(f"SCRAPED SALARY: {salary}")

    if keyword in job_text.lower():
        logging.info(f"Keyword {keyword} found with salary of {salary}")
        return salary
    else:
        logging.info(f"{keyword} was not found in current posting.")
        return None

    # TODO: Check to make sure function only accepts full-time jobs.
    # TODO: Make optional parameter to check for full-time jobs, 
    # part-time jobs, or both.


def scrape_data(urls: list):
    """
    When passed a list of indeed.com url postfixes, will scrape those
    job postings for keywords and their salary.

    urls: A list of indeed.com job posting urls.

    return: A Pandas Series object containing a list of salaries for
    each keyword.
    """
    # TODO: Add parameter to pass in a custom list of comma-separated
    # keywords.
    KEYWORDS = ["python", "SQL", "Excel"]

    # TODO: Consider changing to Pandas dataframe.
    kw_salaries = {}
    # TODO: Find more Pythonic way to do this; perhaps by using .get?
    for keyword in KEYWORDS:
        kw_salaries[keyword] = []

    for url in urls:
        logging.info(url)
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:91.0)'
               'Gecko/20100101 Firefox/91.0'}
        r = requests.get(url, headers)
        #assert r

        # For each keyword in the list, check if the current job 
        # posting contains that keyword. If so add it to the dataframe.
        # TODO: Add an option to print how many of the job postings
        # contained salary levels, out of the total amount of job
        # postings.
        for keyword in KEYWORDS:
            s = scrape_posting(r, keyword)
            if s:
                logging.info(f"Salary:{s}")
                kw_salaries[keyword].append(s)

    # TODO: Fix sloppy Pandas code.
    for i, v in kw_salaries.items():
        kw_salaries[i] = pd.Series(v)
    logging.info(f"Keyword salaries: {kw_salaries}")
    return pd.DataFrame.from_dict(kw_salaries)


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

if __name__ == "__main__":
    main()
