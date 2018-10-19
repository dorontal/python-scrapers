#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2017 Doron Tal
"""
scrape_nyt.py - scrape the New York Times's website for news headlines
"""


import unittest
from pprint import pprint
from scraper_base import ScraperBase


class ScrapeNYT(ScraperBase):
    """
    scraper for Associated Press news titles RSS feed
    """
    def scrape_worker(self):
        """
        the abstract method implementation - does all the scraping work
        returns a list of current titles from the NY Times rss feed
        """
        s_url = "http://www.nytimes.com/services/xml/rss/nyt/HomePage.xml"

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
        sobj = ScrapeNYT("scrape_nyt.log", "DEBUG")
        pprint(sobj.scrape())


if __name__ == "__main__":
    unittest.main()
