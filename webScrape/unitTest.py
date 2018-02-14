#!/usr/bin/env

from movieScrape import *
import sys

link = getIMDBURL(sys.argv[1])
print(link)
