# coding: utf-8

"""
Main script for testQuepy quepy.
"""

import quepy
testquepy = quepy.install("dbpedia")
target, query, metadata = testquepy.get_query("what is a blowtorch?")
print query
