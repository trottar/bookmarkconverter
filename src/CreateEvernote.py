#! /usr/bin/python

#
# Description:
# ================================================================
# Time-stamp: "2023-01-25 17:10:47 trottar"
# ================================================================
#
# Author:  Richard L. Trotta III <trotta@cua.edu>
#
# Copyright (c) trottar
#
from evernote.api.client import EvernoteClient
import evernote.edam.type.ttypes as Types
import evernote.edam.error.ttypes as Errors

def makeTag(noteStore, nameTag):


    
    tags = noteStore.listTags()
    tags_list = []
    tags__name_list = []
    for t in tags:
        tags_list.append(t)
        tags_name_list.append(t.name)
    if nameTag not in tags_list:
        print("\nAdding tag {}...\n".format(ourTag.name))
        ourTag = Types.Tag()
        ourTag.name = nameTag
        ourTag = noteStore.createTag(ourTag)
        print("a",ourTag.guid)
    ourTag = ourTag[nameTag.index(nameTag)]       
    return ourTag

def makeNote(noteStore, noteTitle, noteBody, noteTag=None, parentNotebook=None):

    print("\nAdding note to {}...\n".format(parentNotebook.name))
    
    nBody = '<?xml version="1.0" encoding="UTF-8"?>'
    nBody += '<!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd">'
    nBody += '<en-note>%s</en-note>' % noteBody

    ## Create note object
    ourNote = Types.Note()
    ourNote.title = noteTitle
    ourNote.content = nBody

    print("1~~~~~~~",noteTag)
    if noteTag != None:
        ourTag = noteTag
    
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
        print("2~~~~~~~",ourTag)
        if noteTag != None:
            ourTag = noteStore.getTag(ourTag.name)
            print("3~~~~~~~",ourTag)
            ourNote.tagGuids = [ourTag]
        note = noteStore.createNote(ourNote)
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
