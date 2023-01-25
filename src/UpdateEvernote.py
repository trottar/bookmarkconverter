#! /usr/bin/python

#
# Description:
# ================================================================
# Time-stamp: "2023-01-25 00:34:25 trottar"
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
for nb in notebooks:
    print("\t-> ",nb.name)
    if nb.name == "Test":
        inp_nb = nb        
print("-"*30)


for i, row in bm_df.iterrows():
    url_str = '''<a href="{0}">{0}</a>'''.format(row["url"])
    makeNote(EVERNOTE_DEV, noteStore, row["title"], url_str, inp_nb)
