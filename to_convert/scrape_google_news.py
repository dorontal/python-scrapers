#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2017 Doron Tal
"""
scrape_google_news - scrape google news website for news headlines
"""

import unittest
from pprint import pprint
from scraper_base import ScraperBase


class ScrapeGoogleNews(ScraperBase):
    """
    scraper for Associated Press news titles RSS feed
    """
    def scrape_worker(self):
        """
        the abstract method implementation - does all the scraping work
        returns a list of current titles from the google news rss feed
        """
        s_url = "http://news.google.com/nwshp?hl=en&tab=wn&q=&output=atom"
        feed = self.fetch_rss(s_url)

        return [post.title for post in feed.entries]


class ModuleTests(unittest.TestCase):
    """
    module tests
    """
    @staticmethod
    def test01():
        """
        tests class derivation and scraping
        """
        sobj = ScrapeGoogleNews("scrape_google_news.log", "DEBUG")
        pprint(sobj.scrape())


if __name__ == "__main__":
    unittest.main()
