#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2017 Doron Tal
"""
scrape_ap.py - scrape Associated Press's web site for news headlines
"""

import unittest
from pprint import pprint
from scraper_base import ScraperBase


class ScrapeAP(ScraperBase):
    """
    scraper for Associated Press news titles RSS feed
    """
    def scrape_worker(self):
        """
        abstract method implementation - does all the scraping work
        """
        s_url = "http://hosted.ap.org/lineups/"+\
                "TOPHEADS-rss_2.0.xml?SITE=AZTUS&SECTION=HOME"
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
        sobj = ScrapeAP("scrape_ap.log", "DEBUG")
        pprint(sobj.scrape())


if __name__ == "__main__":
    unittest.main()
