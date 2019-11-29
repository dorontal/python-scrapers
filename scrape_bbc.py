#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
scrape_bbc.py - scrape BBC's RSS site for news headlines
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
        s_url = "http://newsrss.bbc.co.uk/rss/newsonline_world_edition/" + \
            "americas/rss.xml"

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
        sobj = ScrapeWashingtonPost("scrape_washington_post.log", "DEBUG")
        pprint(sobj.scrape())


if __name__ == "__main__":
    unittest.main()
