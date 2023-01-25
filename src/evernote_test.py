#! /usr/bin/python

#
# Description:
# ================================================================
# Time-stamp: "2023-01-25 03:14:22 trottar"
# ================================================================
#
# Author:  Richard L. Trotta III <trotta@cua.edu>
#
# Copyright (c) trottar
#
from evernote.api.client import EvernoteClient
import evernote.edam.type.ttypes as Types
import os

EVERNOTE_DEV = os.getenv('EVERNOTE_DEV')

'''
UserStore is an object used to retrieve information about the current user. 
To create an instance of UserStore, call the get_user_store method from EvernoteClient:
'''
client = EvernoteClient(token=str(EVERNOTE_DEV))
userStore = client.get_user_store()
user = userStore.getUser()
print(user.username)

'''
NoteStore is used to create, update and delete notes, notebooks and other Evernote data found in a user’s account. 
Just like with UserStore, creating an instance of NoteStore is as easy as calling EvernoteClient.get_note_store:
'''
noteStore = client.get_note_store()
notebooks = noteStore.listNotebooks()
print("~"*10,notebooks)
for n in notebooks:
    print(n.name)
