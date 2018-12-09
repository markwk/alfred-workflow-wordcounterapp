#!/usr/bin/python
# encoding: utf-8
#
# Word Counter Data Data Report
# Requires Matplotlib
# install with $ pip install matplotlib
#
# Usage: 
# python report.py NUM_DAYS TARGET_DIR
# python report.py 7 /Users/my-user-name/Desktop/
#
# Copyright  (c) 2018 Mark Koester mark@int3c.com
#
# MIT Licence. See http://opensource.org/licenses/MIT
#
# Created on 2018-05
#

from __future__ import absolute_import

import subprocess
import sys
import os
import plistlib
import time
import datetime as datetime
import calendar
import locale

# data analysis
import matplotlib.pyplot as plt

# read PLIST
records = os.path.expanduser('~/Library/Application Support/WordCounter/app_records.plist')
data = plistlib.readPlist(records)

today = datetime.date.today()

def process_date_stats(date):
  try:
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
    return total
  except:
    return 0

def add(x, y): return x + y

def word_count_multidays_total(date1, num_days):
    date_list = [date1 + datetime.timedelta(days=x) for x in range(0, num_days)]
    total = 0
    # print "date1: " + date1.strftime("%Y-%m-%d")
    for d in date_list:
        # print date.strftime("%Y-%m-%d")
        total = total + process_date_stats(d.strftime("%Y-%m-%d"))
    return locale.format("%d", total, grouping=True)

# TODO: Revise this into a reusable function from main wordcounter.py
# create range of dates from 7 days ago to yesterday
def word_data_report(days, target_dir):
    num_days=days
    # TODO: pass in start date
    start_date = today - datetime.timedelta(days=num_days)
    dates = [start_date + datetime.timedelta(days=x) for x in range(0, num_days)]
    values = []
    for d in dates:
        # get date wcount
        values.append(process_date_stats(d.strftime("%Y-%m-%d")))
    dates_total = word_count_multidays_total(dates[0], num_days)

    plt.figure(1, figsize=(9, 4))
    plt.title(str(dates[0])+' to '+str(dates[6]) + '\n Writing Typing Word Count: ' + str(dates_total))
    plt.bar(dates, values)

    # TODO: add value labels
    #for i, v in enumerate(values):
        # plt.text(v, i, str(v)) 
          # color='black', fontweight='bold')

    # TODO: Save to a Target Directory
    filename=target_dir+str(dates[0])+'_to_'+str(dates[6])+'_writing_typing_report.png' 
    plt.savefig(filename, bbox_inches='tight')

if __name__ == "__main__":
    arg1 = int(sys.argv[1])
    arg2 = sys.argv[2]
    word_data_report(arg1, arg2)

