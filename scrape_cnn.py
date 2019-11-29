#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2017 Doron Tal
"""
scrape_cnn.py - scrape Associated Press's web site for news headlines
"""

import unittest
from pprint import pprint
from scraper_base import ScraperBase


class ScrapeCNN(ScraperBase):
    """
    scraper for Associated Press news titles RSS feed
    """
    def scrape_worker(self):
        """
        abstract method implementation - does all the scraping work
        """
        s_url = "http://rss.cnn.com/rss/cnn_topstories.rss"
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
        sobj = ScrapeCNN("scrape_cnn.log", "DEBUG")
        pprint(sobj.scrape())


if __name__ == "__main__":
    unittest.main()
