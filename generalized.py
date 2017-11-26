from __future__ import print_function
import requests
from bs4 import BeautifulSoup


class Scraper:
    """Generalized scraper"""
    url = ''
    startKey = ''
    queryKey = 'q'
    defaultStart = 0
    headers = {
        'User-Agent': (
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) '
            'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 '
            'Safari/537.36'
        )
    }

    def __init__(self):
        pass

    def get_page(self, query, startIndex=0):
        """ Fetch the google search results page
        Returns : Results Page
        """
        payload = {self.queryKey: query, self.startKey: startIndex}
        response = requests.get(self.url, headers=self.headers, params=payload)
        return response

    def parseResponse(self, soup):
        raise NotImplementedError

    def nextStart(self, currentStart, prevResults):
        return currentStart + len(prevResults)

    def search(self, query, numResults):
        """
            Search for the query and return set of urls
            Returns: list
        """
        urls = []
        currentStart = self.defaultStart

        while(len(urls) < numResults):
            response = self.get_page(query, currentStart)
            soup = BeautifulSoup(response.text, 'html.parser')
            newResults = self.parseResponse(soup)
            if newResults is None:
                break
            urls.extend(newResults)
            currentStart = self.nextStart(currentStart, newResults)
        return urls[: numResults]

    def search_without_count(self, query):
        """
            Search for the query and return set of urls
            Returns: list
        """
        urls = []
        payload = {self.queryKey: query}
        response = requests.get(self.url, headers=self.headers, params=payload)
        soup = BeautifulSoup(response.text, 'html.parser')
        urls = self.parseResponse(soup)
        return urls
