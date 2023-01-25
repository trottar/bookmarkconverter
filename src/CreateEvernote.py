#! /usr/bin/python

#
# Description:
# ================================================================
# Time-stamp: "2023-01-25 15:22:33 trottar"
# ================================================================
#
# Author:  Richard L. Trotta III <trotta@cua.edu>
#
# Copyright (c) trottar
#
from evernote.api.client import EvernoteClient
import evernote.edam.type.ttypes as Types
import evernote.edam.error.ttypes as Errors

def makeNote(authToken, noteStore, noteTitle, noteBody, noteTag=None, parentNotebook=None):

    print("\nAdding note to {}...\n".format(parentNotebook.name))
    
    nBody = '<?xml version="1.0" encoding="UTF-8"?>'
    nBody += '<!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd">'
    nBody += '<en-note>%s</en-note>' % noteBody

    ## Create note object
    ourNote = Types.Note()
    ourNote.title = noteTitle
    ourNote.content = nBody

    if noteTag != None:
        tags = noteStore.listTags()
        tags_list = []
        for t in tags:
            tags_list.append(t.name)
        if noteTag.name not in tags_list:
            noteTag = noteStore.createTag(noteTag)
    
    print('''

     {0}
    |{1}
    |{2}
    |{3}
    |{4}

    '''.format("_"*len(noteTitle),noteTitle,"-"*len(noteTitle),noteBody,"_"*len(noteTitle)))

    ## parentNotebook is optional; if omitted, default notebook is used
    if parentNotebook != None:
        ourNote.notebookGuid = parentNotebook.guid

    ## Attempt to create note in Evernote account
    try:
        if noteTag != None:
            ourTag = noteStore.getTag(noteTag.guid)
            ourNote.tagGuids = [ourTag.guid]
        note = noteStore.createNote(authToken, ourNote)
    except Errors.EDAMUserException as edue:
        ## Something was wrong with the note data
        ## See EDAMErrorCode enumeration for error code explanation
        ## http://dev.evernote.com/documentation/reference/Errors.html#Enum_EDAMErrorCode
        print("EDAMUserException:", edue)
        return None
    except Errors.EDAMNotFoundException as ednfe:
        ## Parent Notebook GUID doesn't correspond to an actual notebook
        print("EDAMNotFoundException: Invalid parent notebook GUID")
        return None

    ## Return created note object
    return note
