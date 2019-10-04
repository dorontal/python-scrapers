#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2017 Doron Tal
"""
scrape_ap_business.py - scrape Associated Press business RSS feedl for titles
"""

import unittest
from pprint import pprint
from scraper_base import ScraperBase


class ScrapeAPBusiness(ScraperBase):
    """
    scraper for Associated Press news titles RSS feed
    """
    def scrape_worker(self):
        """
        the abstract method implementation - does all the scraping work
        """
        s_url = "http://hosted.ap.org/lineups/"+\
                "BUSINESSHEADS-rss_2.0.xml?SITE=TXBEA&SECTION=HOME"
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
        sobj = ScrapeAPBusiness("scrape_ap_business.log", "DEBUG")
        pprint(sobj.scrape())


if __name__ == "__main__":
    unittest.main()
