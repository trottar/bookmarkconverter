#! /usr/bin/python

#
# Description:
# ================================================================
# Time-stamp: "2023-01-24 22:18:05 trottar"
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
for n in notebooks:
    print(n.name)

'''
Next, let’s talk about some of the common data types you’re likely to find when exploring the Evernote Cloud API:

1) Types.Note represents a single note in a user’s account.
2) Types.Notebook represents a notebook in a user’s account.
3) A Types.Resource instance describes a file (image, PDF or any other type of file) attached to a note. 
   Read more about working with Resource objects here.
4) Notes can have one or more related instances of Types.Tag attached to them; these are short, 
   textual labels that aid the user in organizing their information within Evernote.
'''

'''
Creating a new Evernote note is as simple as creating a new instance of Types.Note, 
adding a title and content and calling NoteStore.createNote:
'''
note = Types.Note()
note.title = "I'm a test note!"
note.content = '<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd">'
note.content += '<en-note>Hello, world!</en-note>'
note = noteStore.createNote(note)
'''
This will create the note in the user’s default notebook. 
If you want to specify a destination notebook, you’ll need assign the notebook’s GUID to note.notebookGuid before calling createNote.
'''

'''
Notebooks are just as simple to create as notes: make a new Types.Notebook object, give it a name, and call NoteStore.createNotebook:
'''
noteStore = client.get_note_store()
notebook = Types.Notebook()
notebook.name = "My Notebook"
notebook = noteStore.createNotebook(notebook)
print(notebook.guid)
