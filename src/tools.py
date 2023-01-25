#! /usr/bin/python

#
# Description:
# ================================================================
# Time-stamp: "2021-11-20 14:37:55 trottar"
# ================================================================
#
# Author:  Richard L. Trotta III <trotta@cua.edu>
#
# Copyright (c) trottar
#
import sys

def progressBar(value, endvalue, bar_length=50):
    '''
    progressBar(value, endvalue, bar_length=50)
                |      |         |
                |      |         --> bar_length: Length of bar to output to terminal (default = 50)
                |      --> endvalue: End of loop value - 1
                --> value: Iteration value

    ----------------------------------------------------------------------------------------------

    A simple progress bar to use in loops
    '''

    percent = float(value) / endvalue
    arrow = '=' * int(round(percent * bar_length)-1) + '>'
    spaces = ' ' * (bar_length - len(arrow))
    if percent == 1:
        endl = '\n'
    else:
        endl = ''

    sys.stdout.write(" \r[{0}] {1}%\r{2}".format(arrow + spaces, round(percent * 100), endl))
    sys.stdout.flush()
