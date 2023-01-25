#! /usr/bin/python

#
# Description:
# ================================================================
# Time-stamp: "2023-01-24 21:21:23 trottar"
# ================================================================
#
# Author:  Richard L. Trotta III <trotta@cua.edu>
#
# Copyright (c) trottar
#
from evernote.api.client import EvernoteClient
import os

EVERNOTE_DEV = os.getenv('EVERNOTE_DEV')

client = EvernoteClient(token=str(EVERNOTE_DEV))
userStore = client.get_user_store()
user = userStore.getUser()
print(user.username)
