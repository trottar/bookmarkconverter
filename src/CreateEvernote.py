#! /usr/bin/python

#
# Description:
# ================================================================
# Time-stamp: "2023-01-27 13:24:18 trottar"
# ================================================================
#
# Author:  Richard L. Trotta III <trotta@cua.edu>
#
# Copyright (c) trottar
#
import evernote.edam.type.ttypes as Types
import evernote.edam.error.ttypes as Errors
from evernote.edam.notestore.ttypes import NoteFilter
import socket


def makeNote(noteStore, noteTitle, noteBody, noteTag=None, parentNotebook=None):
    
    nBody = '<?xml version="1.0" encoding="UTF-8"?>'
    nBody += '<!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd">'
    nBody += '<en-note>%s</en-note>' % noteBody

    ## Create note object
    ourNote = Types.Note()
    ourNote.title = noteTitle
    ourNote.content = nBody

    ## parentNotebook is optional; if omitted, default notebook is used
    if parentNotebook != None:
        ourNote.notebookGuid = parentNotebook.guid
        
        NoteExists = False
        try:            
            note_filter = NoteFilter(notebookGuid=ourNote.notebookGuid)
            search_result = noteStore.findNotes(note_filter, 0, 100000)
            for note in search_result.notes:
                if ourNote.title == note.title:
                    #print("{} -> Note already exists".format(ourNote.title))
                    NoteExists = True
        except:
            NoteExists = False
    if noteTag != None:
        ourTag = noteTag

    if NoteExists == False:
        print("\nAdding note to notebook '{}'...\n".format(parentNotebook.name))
        
        print('''

         {0}
        |{1}
        |{2}
        |{3}
        |{4}

        '''.format("_"*len(noteTitle),noteTitle,"-"*len(noteTitle),noteBody,"_"*len(noteTitle)))
    else:

        print("Bookmark '{}' is already in notebook '{}'...".format(noteTitle,parentNotebook.name))

    ## Attempt to create note in Evernote account
    try:
        
        if noteTag != None:
            ourTag = noteStore.getTag(ourTag.guid)
            ourNote.tagGuids = [ourTag.guid]
        if NoteExists == False:
            note = noteStore.createNote(ourNote)
        else:
            return None
    except Errors.EDAMUserException as edue:
        ## Something was wrong with the note data
        ## See EDAMErrorCode enumeration for error code explanation
        ## http://dev.evernote.com/documentation/reference/Errors.html#Enum_EDAMErrorCode
        print("EDAMUserException:", edue)
        return None
    except Errors.EDAMSystemException as edue:
        ## Something was wrong with the note data
        ## See EDAMErrorCode enumeration for error code explanation
        ## http://dev.evernote.com/documentation/reference/Errors.html#Enum_EDAMErrorCode
        print("EDAMSystemException:", edue)
        return None    
    except Errors.EDAMNotFoundException as ednfe:
        ## Parent Notebook GUID doesn't correspond to an actual notebook
        print("EDAMNotFoundException: ", ednfe)
        return None
    except socket.gaierror as sgai:
        print("socket.gaierror: ", sgai)
        return None
    except BlockingIOError as bioe:
        print("BlockingIOError: ", bioe)
        return None
    ## Return created note object
    return note
