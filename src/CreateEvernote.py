#! /usr/bin/python

#
# Description:
# ================================================================
# Time-stamp: "2023-01-25 19:16:06 trottar"
# ================================================================
#
# Author:  Richard L. Trotta III <trotta@cua.edu>
#
# Copyright (c) trottar
#
from evernote.api.client import EvernoteClient
import evernote.edam.type.ttypes as Types
import evernote.edam.error.ttypes as Errors
from evernote.edam.notestore.ttypes import NoteFilter, NoteList


def makeNote(noteStore, noteTitle, noteBody, noteTag=None, parentNotebook=None):

    print("\nAdding note to notebook '{}'...\n".format(parentNotebook.name))
    
    nBody = '<?xml version="1.0" encoding="UTF-8"?>'
    nBody += '<!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd">'
    nBody += '<en-note>%s</en-note>' % noteBody

    ## Create note object
    ourNote = Types.Note()
    ourNote.title = noteTitle
    ourNote.content = nBody

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
        
        #note_filter = NoteFilter(notebookGuid=ourNote.notebookGuid)
        note_filter = NoteList(searchedWords=ourNote.title)
        print(note_filter)
        #note_filter.words = "title:"+ourNote.title
        note_filter.words = ourNote.title
        #note_filter.words = "plank"
        #print(note_filter)
        print(note_filter.words)
        #print(noteStore.findNoteCounts(note_filter, False).notebookCounts)
        search_result = noteStore.findNotes(note_filter, 0, 100000)
        print(search_result)
        print(ourNote.notebookGuid)
 
        if len(search_result.notes) == 0:
            print("{} -> Note does not exist".format(ourNote.title))
        else:
            print("{} -> Note already exists".format(ourNote.title))

    ## Attempt to create note in Evernote account
    try:
        
        if noteTag != None:
            ourTag = noteStore.getTag(ourTag.guid)
            ourNote.tagGuids = [ourTag.guid]
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
