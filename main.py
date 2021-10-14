"""
This program scrapes data from indeed.com, associating keywords with an
average salary.
"""

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


# TODO: Define function to search for keyword in given block of scraped
# data, to easily use any keywords desired. e.g. search if 'python' is
# in the passed data block.


# TODO: Define function to accept input of keywords from a user.


# TODO: Define function to scrape x number of job postings using some
# search word from indeed.com.
def collect_postings(search: str, num: int = 10, page: int = 1) -> list:
    # TODO: Add 'location' parameter.
    """
    When passed a given search for job postings, will scrape through
    (page * 10) job postings and return a list of all the job urls.

    str search: The job title to search for.
    int num: The amount of job postings to scrape.
    int page: The amount of pages to search through.

    return list[str]: The list of URL postfixes of job postings.

    """
    #search = search.replace(' ', '%20')
    # Indeed uses &start=x to track its pages, where x is the page 
    # number you're on times 10, minus 10. So page 1 is 0, page 2 is 10
    # etc.
    url = (f"https://www.indeed.com/jobs?q={search}&l=seattle"
           f"&start={page * 10 - 10}")
    headers = {'User-Agent':
               'Mozilla/5.0 (X11; Linux x86_64; rv:91.0)'
               'Gecko/20100101 Firefox/91.0'}
    jobs = requests.get(url, headers)

    url_list = []
    soup = BeautifulSoup(jobs.content, "html.parser")
    for link in soup.find_all('a'):
        try:
            if 'tapItem' in link.get('class'):
                url_list.append("http://indeed.com" + link.get('href'))
        # Occurs when there is no class.
        except TypeError:
            continue

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
    #print(soup)
    # If the job doesn't have a salary listing, simply return None.
    if not soup.find("div", string="Salary"):
        print("Salary not found.")
        return None


    # TODO: Clean up regex. Make it faster and easier to read.

    salary = soup.find("div", string="Salary").parent.span.text
    print(f"PRE-REGEX SALARY: {salary}")
    # Match a string that begins with $ and 1 or more numeric digits
    # after the dollar sign, with room included for commas in the
    # salary. Then, gets everything past the dollar sign.
    # TODO: Add options for a salary range as well, e.g. 
    # $100,000 - $180,000. 
    salary_pattern = re.compile(r".*(\$\d+,*\d+).*")
    # Gets everything past the dollar sign and replaces the commas with
    # empty space, so an int can be returned.
    print("SALARY PATTERN GROUP 0:")
    print(salary_pattern.match(salary).group(0))
    print("SALARY PATTERN GROUP 1:")
    print(salary_pattern.match(salary).group(0))

    salary = int(salary_pattern.match(salary).group(1)[1:].replace(',', ''))

    # Convert to lower for comparison to text.
    keyword = keyword.lower()
    job_text = soup.find("div", id="jobDescriptionText").text
    print(f"SCRAPED SALARY: {salary}")

    if keyword in job_text.lower():
        print(f"Keyword {keyword} found with salary of {salary}")
        return salary
    else:
        print(f"{keyword} was not found in current posting.")
        return None

    # TODO: Check to make sure function only accepts full-time jobs.
    # TODO: Make optional parameter to check for full-time jobs, 
    # part-time jobs, or both.


def scrape_data(urls: list):
    """
    When passed a list of indeed.com url postfixes, will scrape those
    job postings for keywords and their salary.

    urls: A list of indeed.com job posting urls.
    return: A 2d Pandas Dataframe object, consisting of the average
    salary for each keyword.
    """
    # TODO: Add parameter to pass in a custom list of comma-separated
    # keywords.
    KEYWORDS = ["python", "SQL", "analytics"]

    # TODO: Change to Pandas dataframe.
    kw_salaries = {}
    # TODO: Find more Pythonic way to do this; perhaps by using .get?
    for keyword in KEYWORDS:
        kw_salaries[keyword] = []

    for url in urls:
        print(url)
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:91.0)'
               'Gecko/20100101 Firefox/91.0'}
        r = requests.get(url, headers)
        assert r

        # For each keyword in the list, check if the current job 
        # posting contains that keyword. If so add it to the dataframe.
        for keyword in KEYWORDS:
            s = scrape_posting(r, keyword)
            if s:
                print(f"Salary:{s}")
                kw_salaries[keyword].append(s)

    print(kw_salaries)


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

    print(data)
    sns.set_theme(style="whitegrid")
    ax = sns.barplot(data=data, orient="h")
    plt.show()

if __name__ == "__main__":
    #headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:91.0)'
    #           'Gecko/20100101 Firefox/91.0'}
    #r = requests.get('https://www.indeed.com/viewjob?jk=15579aadbf315030&from=serp&vjs=3', headers)
    #print(scrape_posting(r, "Analysis"))
    scrape_data(collect_postings("data scientist"))
    #collect_postings("data scientist")
    #graph_data(load_data())
