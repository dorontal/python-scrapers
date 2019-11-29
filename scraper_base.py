#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scraper_base - abstract scraper base class definition and scraping utilities
"""

import abc
import sys
import unittest
# import urllib2
from urllib import request
import time
import re
from bs4 import BeautifulSoup
import feedparser
from log_utils import Logger


# default values:

# maximum number of retries before declaring failure if they all fail
MAX_RETRIES = 10

# delay, in seconds, as a float
RETRY_DELAY_SECONDS = 1.0


NYT_TOP_HEADLINES_URL = \
    "http://www.nytimes.com/services/xml/rss/nyt/HomePage.xml"

class ScraperBase:
    """
    Scraper abstract base class - to derive from this class:
    (1) implement scrape_worker()
    (2) execute scrape(), which wraps scrape_worker()
    """
    __metaclass__ = abc.ABCMeta

    def __init__(self, s_log_filename="scraper_base.log",
                 s_log_level="DEBUG", s_url=None, regexp=None,
                 b_global=False):
        """
        constructor - must supply the logging parameters
        """
        self.log = Logger(s_log_filename, s_log_level)
        self._s_url = s_url
        self._regexp = regexp
        self._retry_delay_seconds = RETRY_DELAY_SECONDS
        self._max_retries = MAX_RETRIES
        self._last_scraped_url = None
        self._b_global = b_global


    @abc.abstractmethod
    def scrape_worker(self):
        """
        this is the function that derived scrapers must implement and which
        does all the scraping work, the rest of this class here is just for
        structural support only
        """
        s_html = None
        if self._s_url is None:
            self.log.warning("this object was initialized without a URL!")
            return None
        else:
            s_html = self.fetch_html(self._s_url)[0]
        if self._regexp is None:
            return s_html
        elif s_html is not None:
            if self._b_global:
                return self._regexp.findall(s_html)
            else:
                match = self._regexp.search(s_html)
                if match is not None:
                    return match.groups()
                else:
                    return None


    def scrape(self):
        """
        calls scrape_worker() but with logging and timing infrastructure
        """
        start_time = time.time()
        response = self.scrape_worker()
        elapsed_time = time.time()-start_time
        self.log.debug("url=%s, duration=%f seconds" %
                       (self._last_scraped_url, elapsed_time))

        return response


    def fetch_rss(self, s_url):
        """
        fetches the rss feed at a url given by url string s_url
        """
        b_noanswer = True
        n_tries = 0
        response = None
        while b_noanswer and n_tries < self._max_retries:
            try:
                response = feedparser.parse(s_url)
                self._last_scraped_url = s_url
                b_noanswer = False
            except RuntimeError as ex:
                self.log.error("Cannot open %s\n%s\nretrying in %2.2f s\n" %
                               (s_url, str(ex), self._retry_delay_seconds))
                time.sleep(1)
                b_noanswer = True
            n_tries += 1

        return response


    def fetch_html(self, s_url):
        """
        fetches the html at a url given by url string s_url
        """

        # spoof the user agent to appear like an iphone's
        # "User-Agent" : "Mozilla/5.0(Windows; U; Windows NT 5.1; en-US) Ap"+
        # "User-Agent" : "Mozilla/5.0 (compatible; VideoSurf_bot +ht...
        #                    ... tp://www.videosurf.com/bot.html)",
        d_headers = {
            "User-Agent" : "",
            "Referer" : "http://python.org"
            }

        # create a request object for the URL
        # request = urllib2.Request(s_url, headers=d_headers)
        req = request.Request(s_url, headers=d_headers)

        # create an opener object
        # opener = urllib2.build_opener()
        opener = request.build_opener()

        # open a connection and receive the http response headers + contents
        b_noanswer = True
        n_tries = 0
        contents = None
        headers = None
        code = None
        while b_noanswer and n_tries < self._max_retries:
            try:
                response = opener.open(req)

                self._last_scraped_url = s_url
                b_noanswer = False
                # return values
                contents = response.read()
                headers = response.headers
                code = response.code
            # except (urllib2.HTTPError, urllib2.URLError) as ex:
            except (request.HTTPError, urllib2.URLError) as ex:
                s_message = "Cannot open %s\n%s\nretrying in %2.2f s\n" % \
                            (s_url, str(ex), self._retry_delay_seconds)
                sys.stderr.write(s_message+"\n")
                self.log.error(s_message)
                time.sleep(1)
                b_noanswer = True
            n_tries += 1


        return contents, headers, code


    @staticmethod
    def get_text_from_html(s_html, s_separator=" "):
        """
        returns list of non-empty text elements in html string snippet 's_html'
        """
        re_text = re.compile('>([^<>]+)<')
        s_result = re_text.findall(str(s_html))[0]

        return s_separator.join(s_result.split())


    @staticmethod
    def get_table_from_html(s_html, i_table=0):
        """
        return a list of lists, each containing the text elements of an
        html table extracted from soup 'soup' (specifically, using zero
        indexing, table 'i_table' of all the tables detected in 'soup')
        """
        soup = BeautifulSoup(s_html, features="html.parser")
        tables = soup('table')
        table = tables[i_table]
        l_text_rows = []
        l_html_rows = table.findAll('tr')
        for html_row in l_html_rows:
            l_text_cells = []
            l_html_cells = html_row.findAll('td')
            for html_cell in l_html_cells:
                l_text_cells.append(ScraperBase.get_text_from_html(html_cell))
            l_text_rows.append(l_text_cells)

        return l_text_rows


class ModuleTests(unittest.TestCase):
    """
    module tests
    """
    @staticmethod
    def test01():
        """
        tests class derivation and basic scraping usage for html
        """
        class YahooCalendarScraper(ScraperBase):
            """
            current yahoo calendar scraper class
            """
            def scrape_worker(self):
                """
                the abstract method implementation - does all the scraping work
                """
                s_url = "http://biz.yahoo.com/c/e.html"
                s_html = self.fetch_html(s_url)[0]
                table = self.get_table_from_html(s_html, 0)
                print('yahoo-calendar-len:', len(table))
                return self.get_table_from_html(s_html, 0)

        sobj = YahooCalendarScraper()
        sobj.scrape()

    @staticmethod
    def test02():
        """
        tests class derivation and basic scraping usage for rss
        """
        class NYTScraper(ScraperBase):
            """
            current yahoo calendar scraper class
            """
            def scrape_worker(self):
                """
                the abstract method implementation - does all the scraping work
                """
                feed = self.fetch_rss(NYT_TOP_HEADLINES_URL)
                print('# of NYT titles:', len(feed.entries))
                return [post.title for post in feed.entries]

        sobj = NYTScraper()
        sobj.scrape()


if __name__ == "__main__":
    unittest.main()
