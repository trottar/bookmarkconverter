#! /usr/bin/python

#
# Description:
# ================================================================
# Time-stamp: "2023-01-25 02:06:41 trottar"
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
import time

import Tools

from SummarizeLink import grabText

pd.set_option('display.max_colwidth', None)
        
def import_bookmarks():
    
    bookmarkDict = {}
    df = pd.DataFrame()

    for folder in chrome_bookmarks.folders:
        if "Must Read" == folder.name:
            print("\nImporting data for bookmarks from {}...".format(folder.name))
            for i,url in enumerate(folder.urls):
                if len(folder.urls) > 1:
                    Tools.progressBar(i, len(folder.urls)-1,bar_length=25)
                else:
                    Tools.progressBar(i, len(folder.urls),bar_length=25)
                bookmarkDict.update({"title" : url.name.lower()})
                bookmarkDict.update({"url" : url.url})
                bookmarkDict.update({"summary" : grabText(url.url)})
                print("\t-> ",url.name.lower())
                #print(url, "\n\n","-"*70)
                url = url.url
                try:
                    with urllib.request.urlopen(url) as response:
                        html = response.read()
                except (urllib.error.HTTPError, urllib.error.URLError, ConnectionError, IncompleteRead) as e:
                    continue
                try:
                    soup = BeautifulSoup(html, "html.parser")
                except:
                    continue
                # Get text from site
                '''
                text = ''
                for para in soup.find_all("p"):
                    text += para.get_text()
                #print(' '.join([line.strip().lower() for line in text.splitlines()]),"\n\n")
                bookmarkDict.update({"transcript" : ' '.join([line.strip().lower() for line in text.splitlines()])})
                '''
                bookmarkDict = {k : bookmarkDict[k] for k in sorted(bookmarkDict.keys())}
                df = df.append(bookmarkDict,ignore_index=True)
            print("\n")
    print("-"*70)
    print(df)
    return df
