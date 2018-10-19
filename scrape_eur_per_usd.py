#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2017 Doron Tal
"""
scrape_eur_per_usd.py - scrape a website for EUR / USD conversion right now
"""

import unittest
import re
from scraper_base import ScraperBase

URL = "http://www.xe.com/currencyconverter/convert/?Amount=1&From=USD&To=EUR"

class ScrapeEurPerUsd(ScraperBase):
    """
    scraper for retrieving Euros per US dollar
    """
    def scrape_worker(self):
        """
        the abstract method implementation - does all the scraping work
        """
        s_html = self.fetch_html(URL)[0]

        match = re.search(r"1 USD = (\d*)\.(\d*) EUR", s_html)
        if match is None:
            raise Exception("regexp no longer works in scraping!")

        eur = float(match.group(1) + "." + match.group(2))

        return eur


class ModuleTests(unittest.TestCase):
    """
    module tests
    """
    @staticmethod
    def test01():
        """
        tests class derivation and scraping
        """
        sobj = ScrapeEurPerUsd("scrape_eur_per_usd.log", "DEBUG")
        eur = sobj.scrape()

        print "EUR/USD = %f" % (eur,)
        print "USD/EUR = %f" % (1.0/eur,)

if __name__ == "__main__":
    unittest.main()
