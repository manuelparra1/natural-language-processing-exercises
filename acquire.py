# NLP Acquire
from requests import get
from bs4 import BeautifulSoup
import pandas as pd
import re
import os
import json

def get_codeup_links():
    '''
        This is a use-specific function that returns a list
        of links to articles on the Codeup Blog using 
        Requests and BeautifulSoup.

        Returns
        -------
        list :    links to articles found on blog
    '''
    # Codeup Data Science Headers
    headers = {'User-Agent': 'Codeup Data Science'}
    
    # Working URL
    url = 'https://codeup.com/blog/'

    # Basic Requests Response
    response = get(url, headers=headers)

    # Using BeautifulSoup to parse Response output of
    # Codeup Blog
    soup = BeautifulSoup(response.content, 'html.parser')

    # Capturing Specific Tag  that has links for all articles
    # on page
    more_links = soup.find_all('a', class_='more-link')
    
    return [link['href'] for link in more_links]

def get_blog_articles(article_list):
    '''
        This is a use-specific function that uses a 
        list of links to articles on the Codeup Blog
        and returns a list of dictionaries holding 
        information for each article.

        -   Will save a json file with list of dictionaries
            holding metadata and content of articles
        -   Will return a list of dictionaries holding
            metadata and content of articles

        Params
        -------
            first: list of links to articles

        Returns
        -------
        list:   Dictionaries holding metadata and content
                of articles    
    '''
    # chosen name for json file 
    file = 'blog_posts.json'
    
    # check if json file already exists
    # before doing unecessary work
    if os.path.exists(file):
        
    # safer way of handling files, does
    # not require closing of file
        with open(file) as f:
        
            return json.load(f)
    
    # required Data Science headers for access to
    # Codeup Blog
    headers = {'User-Agent': 'Codeup Data Science'}
    
    # temporary empty list used to hold
    # dictionaries of each article
    article_info = []
    
    # looping through list of links to create
    # dictionary and append to empty list
    for article in article_list:
        
        # getting hmtl of article using link in list
        response = get(article, headers=headers)
        
        # parsing and creating BeautifulSoup object
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # dictionary template used to gather article data
        info_dict = {'title': soup.find('h1').text,
                     'link': article,
                     'date_published': soup.find('span', class_='published').text,
                     'content': soup.find('div', class_='entry-content').text}
    
        # append current dictionary to list
        article_info.append(info_dict)
    # save list of dictionaries holding article data
    # as a json file
    with open(file, 'w') as f:
        
        json.dump(article_info, f)
        
    return article_info
