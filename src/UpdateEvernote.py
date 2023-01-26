#! /usr/bin/python

#
# Description:
# ================================================================
# Time-stamp: "2023-01-25 23:25:19 trottar"
# ================================================================
#
# Author:  Richard L. Trotta III <trotta@cua.edu>
#
# Copyright (c) trottar
#
from evernote.api.client import EvernoteClient
import evernote.edam.type.ttypes as Types
import os

from GetBookmarks import import_bookmarks
from CreateEvernote import makeNote

EVERNOTE_DEV = os.getenv('EVERNOTE_DEV')
client = EvernoteClient(token=str(EVERNOTE_DEV))
userStore = client.get_user_store()
user = userStore.getUser()
print("\nRunning for user '{}'...\n\n".format(user.username))

noteStore = client.get_note_store()    

print("-"*30)
print("List of available notebooks...\n")
notebooks = noteStore.listNotebooks()
nb_name_list = []
nb_list = []
for nb in notebooks:
    print("\t-> ",nb.name)
    nb_list.append(nb)
    nb_name_list.append(nb.name)

print("\nList of available tags...\n")
tags = noteStore.listTags()
tag_name_list = []
tag_list = []
for t in tags:
    print("\t-> ",t.name)
    tag_list.append(t)
    tag_name_list.append(t.name)    
print("-"*30)

bm_df = import_bookmarks(noteStore, notebooks)

for i, row in bm_df.iterrows():
    if row["folder"] not in nb_name_list:
        print("\nCreating notebook '{}' in stack 'Chrome Bookmarks'...\n".format(row["folder"]))
        notebook = Types.Notebook()
        notebook.name = row["folder"]
        notebook = noteStore.createNotebook(notebook)
        nb_list.append(notebook)
        nb_name_list.append(notebook.name)
    inp_nb = nb_list[nb_name_list.index(row["folder"])]
    inp_nb.stack = "Chrome Bookmarks"
    noteStore.updateNotebook(inp_nb)


    if "bookmarks" not in tag_name_list:
        print("\nCreating tag '{}'...\n".format("bookmarks"))
        noteTag = Types.Tag()
        noteTag.name = "bookmarks"
        noteTag = noteStore.createTag(noteTag)
        tag_list.append(noteTag)
        tag_name_list.append(noteTag.name)
    tag = tag_list[tag_name_list.index("bookmarks")]
    
    if row["summary"] == "":
        url_str = \
        '''
        <a href="{0}">{0}</a>
        <br/>
        '''.format(row["url"])
    else:
        url_str = \
        '''
        <a href="{0}">{0}</a>
        <br/>
        <br/>
        <br/>
        <span style="font-weight:bold;color:black;">Quick Summary:</span>
        <hr/>
        <br/>
        <br/>
        {1}
        <br/>
        <br/>
        <hr/>
        <br/>
        '''.format(row["url"],row["summary"].replace('>','').replace('<','').replace('&','').replace('\n', '<br/>'))

    makeNote(noteStore, row["title"], url_str, noteTag=tag, parentNotebook=inp_nb)
    #makeNote(noteStore, row["title"], url_str, parentNotebook=inp_nb)

