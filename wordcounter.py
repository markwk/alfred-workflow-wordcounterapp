#!/usr/bin/python
# encoding: utf-8
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

from docopt import docopt

from workflow import (
    ICON_INFO,
    ICON_WARNING,
    ICON_WEB,
    MATCH_ALL,
    MATCH_ALLCHARS,
    Workflow3
)

from config import (
    ICON_TODAY,
    ICON_DAY,
    ICON_DATE_RANGE,
    ICON_CHART,
    ICON_BLD,
    ICON_FILE,
    KEYWORD_WORDCOUNTER
)

locale.setlocale(locale.LC_ALL, 'en_US')

log = None

DELIMITER = u'\u203a'  # SINGLE RIGHT-POINTING ANGLE QUOTATION MARK

ALFRED_AS = 'tell application "Alfred 3" to search "{}"'.format(
    KEYWORD_WORDCOUNTER)

# read PLIST
records = os.path.expanduser('~/Library/Application Support/WordCounter/app_records.plist')
data = plistlib.readPlist(records)

num_days = 6
today = datetime.date.today()
yesterday = today - datetime.timedelta(days=1)
start_date = today - datetime.timedelta(days=num_days)
date_list = [start_date + datetime.timedelta(days=x) for x in range(0, num_days)]

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

def main(wf):
    # todayStats
    today_stats = process_date_stats(today.strftime("%Y-%m-%d"))
    today_text = "Today's Word Count"
    wf.add_item(today_text, today_stats, valid=True, icon=ICON_TODAY)

    # Previous 6 Days
    for d in reversed(date_list):
      total = process_date_stats(d.strftime("%Y-%m-%d"))
      if d == yesterday:
        day = "Yesterday's Word Count"
      else:
        day = d.strftime("%A, %B %d, %Y")
      wf.add_item(day, total, valid=True, icon=ICON_DAY)

    # this month
    this_mo_num_days = calendar.monthrange(today.year, today.month)[1]
    this_mo_days = [datetime.date(today.year, today.month, day) for day in range(1, this_mo_num_days+1)]
    # print mo_days[0]
    this_month_total = word_count_multidays_total(this_mo_days[0], this_mo_num_days)
    wf.add_item(today.strftime("%B %Y Word Count"), this_month_total, valid=True, icon=ICON_DATE_RANGE)

    # this month
    lastmo = this_mo_days[0] - datetime.timedelta(days=1)
    last_mo_num_days = calendar.monthrange(lastmo.year, lastmo.month)[1]
    last_mo_days = [datetime.date(lastmo.year, lastmo.month, day) for day in range(1, last_mo_num_days+1)]
    # print mo_days[0]
    last_month_total = word_count_multidays_total(last_mo_days[0], last_mo_num_days)
    wf.add_item(lastmo.strftime("%B %Y Word Count"), last_month_total, valid=True, icon=ICON_DATE_RANGE)

    wf.send_feedback()

if __name__ == '__main__':
    wf = Workflow3()
    log = wf.logger
    sys.exit(wf.run(main))