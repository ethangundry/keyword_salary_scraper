"""
Functions for scraping data from indeed.com.
"""

import logging
import re
from typing import List

import bs4
from bs4 import BeautifulSoup
import pandas as pd
import requests

# TODO: Define function to scrape x number of job postings using some
# search word from indeed.com.
def collect_postings(search: str, page: int = 1) -> list:
    # TODO: Add 'location' parameter.
    """
    When passed a given search for job postings, will scrape through
    (page * 10) job postings and return a list of all the job urls.

    str search: The job title to search for.
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
        url = (f"https://www.indeed.com/jobs?q={search}&l=new york"
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

# TODO: Make a function that scrapes a posting simply to check if the
# passed keyword exists or not.

def scrape_posting(response, keyword: str, salary: bool = False):
    """
    When passed the request object containing an indeed.com job posting
    page, will check whether the page contains the given keyword, and
    if so, returns True. Else, returns False.

    response: A requests response object.
    str keyword: The keyword to search for.
    bool salary: Whether or not to include the salary in the return.
                 False by default.

    return list: If salary is True, the list contains [bool, int].
                 Otherwise, simply contains [bool].
    """

    return_value = [False, -1]
    soup = BeautifulSoup(response.content, 'html.parser')


    # Convert to lower for comparison to text.
    keyword = keyword.lower()
    # TODO: Add options for alternative forms of the webpage that don't
    # use "jobDescriptionText" in the CSS.
    try:
        job_text = soup.find("div", id="jobDescriptionText").text
    except AttributeError:
        logging.warning("This job does not have a jobDescriptionText id in its"
                        " text.")
        return return_value

    if keyword in job_text.lower():
        logging.info(f"Keyword {keyword} found")
        return_value[0] = True
        pay = scrape_salary(soup)
        if pay >= 0:
            return_value[1] = pay
    else:
        logging.info(f"{keyword} was not found in current posting.")
        return_value[0] = False

    return return_value

    # TODO: Check to make sure function only accepts full-time jobs.
    # TODO: Make optional parameter to check for full-time jobs, 
    # part-time jobs, or both.

def scrape_salary(text):
    """
    When passed a beautifulsoup object, returns the salary if there is
    one within the text.

    text text: The beautifulsoup text.

    return int: The salary in the text. -1 if the salary is not found.
    """
    # If the job doesn't have a salary listing, simply return None.
    if not text.find("div", string="Salary"):
        logging.info("Salary not found.")
        return -1

    hourly = False
    monthly = False

    # TODO: Clean up regex. Make it faster and easier to read.

    salary = text.find("div", string="Salary").parent.span.text
    # TODO: Add ability to set the ratio of hourly jobs to annual pay;
    # e.g. whether to assume salaried people work 50 hours a work 
    # instead of 40.
    if "hour" in salary:
        logging.info("Pays hourly")
        hourly = True
    elif "month" in salary:
        monthly = True

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
    logging.info(f"SCRAPED SALARY: {salary}")

    if hourly:
        # Assume 40 hours of work a week. 
        return salary * 40 * 12
    elif monthly:
        return salary * 12
    return salary


def scrape_data(urls: list, keywords: list):
    """
    When passed a list of indeed.com url postfixes, will scrape those
    job postings for keywords and their salary.

    list[str] urls: A list of indeed.com job posting urls.
    list[str] keywords: The keywords to search for.

    return: A Pandas Series object containing a list of salaries for
    each keyword.
    """

    # TODO: Consider changing to Pandas dataframe.
    kw_salaries = {}
    # TODO: Find more Pythonic way to do this; perhaps by using .get?
    for keyword in keywords:
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
        for keyword in keywords:
            s = scrape_posting(r, keyword, salary=True)
            if s[1] != -1:
                logging.info(f"Salary:{s}")
                kw_salaries[keyword].append(s[1])

    # TODO: Fix sloppy Pandas code.
    for i, v in kw_salaries.items():
        kw_salaries[i] = pd.Series(v)
    logging.info(f"Keyword salaries: {kw_salaries}")
    return pd.DataFrame.from_dict(kw_salaries)
