#! /usr/bin/python

#
# Description:
# ================================================================
# Time-stamp: "2023-01-27 23:17:30 trottar"
# ================================================================
#
# Author:  Richard L. Trotta III <trotta@cua.edu>
#
# Copyright (c) trottar
#
from evernote.edam.notestore.ttypes import NoteFilter
import evernote.edam.error.ttypes as Errors
import pandas as pd
import chrome_bookmarks
from urllib.parse import parse_qs, urlparse
import urllib
from bs4 import BeautifulSoup
from http.client import IncompleteRead
import html
import socket
import time

import Tools

from SummarizeLink import grabText

pd.set_option('display.max_colwidth', None)
        
def import_bookmarks(noteStore, notebooks):
    
    bookmarkDict = {}
    df = pd.DataFrame()

    for folder in chrome_bookmarks.folders:
        #if "Workout" == folder.name:
        #if "Workout" == folder.name or "Must Read" == folder.name:
        print("\nImporting data for bookmarks from {}...".format(folder.name))
        for i,url in enumerate(folder.urls):
            nb_name_list = []
            nb_list = []
            for nb in notebooks:
                NoteExists = False
                if nb.name == folder.name:
                    try:
                        note_filter = NoteFilter(notebookGuid=nb.guid)
                        search_result = noteStore.findNotes(note_filter, 0, 100000)
                        for note in search_result.notes:
                            if url.name.lower() == note.title:
                                print("{} -> Note already exists".format(url.name.lower()))
                                NoteExists = True
                                break
                    except socket.gaierror as sgai:
                        print("socket.gaierror: ", sgai)
                    except BlockingIOError as bioe:
                        print("BlockingIOError: ", bioe)
                        NoteExists = False
                    except Errors.EDAMUserException as edue:
                        print("EDAMUserException:", edue)
                        NoteExists = False
                    except Errors.EDAMSystemException as edue:
                        print("EDAMSystemException:", edue)
                        NoteExists = False
                    except Errors.EDAMNotFoundException as ednfe:
                        print("EDAMNotFoundException: ", ednfe)
                        NoteExists = False
                if NoteExists == True:
                    break
            if NoteExists == False:
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
