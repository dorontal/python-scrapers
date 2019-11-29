#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
scrape_usatoday.py - scrape USA Today's RSS site for news headlines
"""

import unittest
from pprint import pprint
from scraper_base import ScraperBase


class ScrapeUSAToday(ScraperBase):
    """
    scrape USA Today's RSS site for news headlines
    """
    def scrape_worker(self):
        """
        abstract method implementation - does all the scraping work
        """
        s_url = "http://rssfeeds.usatoday.com/usatoday-NewsTopStories"

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
        sobj = ScrapeUSAToday("scrape_usatoday.log", "DEBUG")
        pprint(sobj.scrape())


if __name__ == "__main__":
    unittest.main()
