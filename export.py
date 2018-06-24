#!/usr/bin/python
# encoding: utf-8
#
# Copyright  (c) 2018 Mark Koester mark@int3c.com
#
# MIT Licence. See http://opensource.org/licenses/MIT
#
# Created on 2018-06
#

"""

Export Word Counter Stats.

Usage:
    export.py 

"""

import subprocess
import sys
import os
import plistlib
import time
import datetime as datetime
import csv

def add(x, y): return x + y

# read PLIST
records = os.path.expanduser('~/Library/Application Support/WordCounter/app_records.plist')
data = plistlib.readPlist(records)


filepath = os.path.expanduser('~/Documents/WordCounter/export.csv')
directory = os.path.dirname(filepath)
if not os.path.exists(directory):
    os.makedirs(directory)

def notify(title, text):
    os.system("""
              osascript -e 'display notification "{}" with title "{}"'
              """.format(text, title))

with open(filepath, 'w') as file:
  outputWriter = csv.writer(file)
  # add header to csv
  outputWriter.writerow(['date', 'wordcount'])
  results = ''
  # colllect stats for each date key
  for date in data.keys():
    # collect per-app totals
    apps = data[date]
    counts = []
    for app in apps:
        count = reduce(add, app["counts"])
        counts.append(count)
        # Uncomment to print per-app count
        # print app["id"] + ": " + str(count)
    # compute total from collection
    total = reduce(add, counts)
    row = date + "," + str(total)
    # print row
    outputWriter.writerow([date, total])
    results = results + date + "," + str(total) + '\n'
    totalrows = len(data.keys())
  # file.close()
  # return results
  message = "%s Stats Rows Exported to Documents/WordCounter." % (totalrows)
  notify("Word Counter Stats: Succesfully Exported", message)
