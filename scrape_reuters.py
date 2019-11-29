#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
scrape_reuters.py - scrape Reuters' RSS site for news headlines
"""

import unittest
from pprint import pprint
from scraper_base import ScraperBase


class ScrapeReuters(ScraperBase):
    """
    scrape Reuters' RSS site for news headlines
    """
    def scrape_worker(self):
        """
        abstract method implementation - does all the scraping work
        """
        s_url = "http://feeds.reuters.com/reuters/topNews"

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
        sobj = ScrapeReuters("scrape_reuters.log", "DEBUG")
        pprint(sobj.scrape())


if __name__ == "__main__":
    unittest.main()
