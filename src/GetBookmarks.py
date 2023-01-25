#! /usr/bin/python

#
# Description:
# ================================================================
# Time-stamp: "2023-01-25 14:03:32 trottar"
# ================================================================
#
# Author:  Richard L. Trotta III <trotta@cua.edu>
#
# Copyright (c) trottar
#
import pandas as pd
import chrome_bookmarks
from urllib.parse import parse_qs, urlparse
import urllib
from bs4 import BeautifulSoup
from http.client import IncompleteRead
import html
import time

import Tools

from SummarizeLink import grabText

pd.set_option('display.max_colwidth', None)
        
def import_bookmarks():
    
    bookmarkDict = {}
    df = pd.DataFrame()

    for folder in chrome_bookmarks.folders:
        print("\nImporting data for bookmarks from {}...".format(folder.name))
        for i,url in enumerate(folder.urls):
            #ERROR=False
            bookmarkDict.update({"folder" : folder.name})
            bookmarkDict.update({"title" : url.name.lower()})
            bookmarkDict.update({"url" : html.escape(url.url)})
            bookmarkDict.update({"summary" : grabText(html.escape(url.url))})
            #print("\t-> ",url.name.lower())
            bookmarkDict = {k : bookmarkDict[k] for k in sorted(bookmarkDict.keys())}
            df = df.append(bookmarkDict,ignore_index=True)
            if len(folder.urls) > 1:
                Tools.progressBar(i, len(folder.urls)-1,bar_length=25)
            else:
                Tools.progressBar(i, len(folder.urls),bar_length=25)
            print("\n")
    print("-"*70)
    print(df)
    print("-"*70)
    return df
