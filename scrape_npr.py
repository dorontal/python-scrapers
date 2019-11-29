#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
scrape_npr.py - scrape NPR's RSS site for news headlines
"""

import unittest
from pprint import pprint
from scraper_base import ScraperBase


class ScrapeWashingtonPost(ScraperBase):
    """
    scraper for Associated Press news titles RSS feed
    """
    def scrape_worker(self):
        """
        abstract method implementation - does all the scraping work
        """
        s_url = "http://www.npr.org/rss/rss.php?id=1001"

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
        sobj = ScrapeWashingtonPost("scrape_npr.log", "DEBUG")
        pprint(sobj.scrape())


if __name__ == "__main__":
    unittest.main()
