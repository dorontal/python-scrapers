#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2017 Doron Tal
"""
scrape_ntp.py - scrape an ntp site to get the date/time from there
"""

import unittest
import socket
import struct
import time
from scraper_base import ScraperBase


class ScrapeNTP(ScraperBase):
    """
    scraper of ntp server via sockets
    """
    def scrape_worker(self):
        """
        the abstract method implementation - does all the scraping work
        """
        client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # set up request data
        data = "\x1b"+47*"\0"
        s_server_name = "time.apple.com"
        server_port = 123
        # send request
        client.sendto(data, (s_server_name, server_port))
        # receive response
        data, address = client.recvfrom(1024)
        if data:
            l_data = struct.unpack("!12I", data)
            # subtract epoch time:
            result = time.ctime(l_data[10]-2208988800L)
            self.log.debug("Parsed response from %s is %s" %
                           (str(address[0])+":"+str(address[1]), str(result)))
        else:
            self.log.error("Could not get data from server "+s_server_name)
            result = None

        return result


class ModuleTests(unittest.TestCase):
    """
    module tests
    """
    @staticmethod
    def test01():
        """
        tests class derivation and basic scraping usage for html
        """
        sobj = ScrapeNTP("scrape_ntp.log", "DEBUG")
        print sobj.scrape()


if __name__ == "__main__":
    unittest.main()
