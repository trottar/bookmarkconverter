#! /usr/bin/python

#
# Description:
# ================================================================
# Time-stamp: "2023-01-25 04:02:34 trottar"
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

bm_df = import_bookmarks()

EVERNOTE_DEV = os.getenv('EVERNOTE_DEV')
client = EvernoteClient(token=str(EVERNOTE_DEV))
userStore = client.get_user_store()
user = userStore.getUser()
print("\nRunning for {}...\n\n".format(user.username))

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
print("-"*30)

for i, row in bm_df.iterrows():
    print(row["folder"])
    if row["folder"] not in nb_name_list:
        notebook = Types.Notebook()
        notebook.name = row["folder"]
        notebook = noteStore.createNotebook(notebook)
        nb_list.append(notebook)
    inp_nb = nb_list[nb_list.index(row["folder"])]
    print(inp_nb)
    url_str = \
    '''
    <a href="{0}">{0}</a>
    <br/>
    <br/>
    <br/>
    Quick Summary:
    <br/>
    <br/>
    {1}
    <br/>
    '''.format(row["url"],row["summary"].replace('\n', '<br/>'))
    makeNote(EVERNOTE_DEV, noteStore, row["title"], url_str, inp_nb)

