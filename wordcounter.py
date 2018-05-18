#!/usr/bin/python
# encoding: utf-8
#
# Copyright  (c) 2018 Mark Koester mark@int3c.com
#
# MIT Licence. See http://opensource.org/licenses/MIT
#
# Created on 2014-12-26
#

"""wordcounter.py [options] [<query>]

View/manage workflow settings.

Usage:
    wordcounter.py [<query>]
    wordcounter.py (-h|--help)
    wordcounter.py --today
    wordcounter.py --yesterday

Options:
    -h, --help    Show this message
    --today    Today's Word Counter Stats
    --yesterday      Yesterday's Word Counter Stats

"""

from __future__ import absolute_import

import subprocess
import sys
import os
import plistlib
import time
import datetime as datetime

from docopt import docopt

from workflow import (
    ICON_INFO,
    ICON_WARNING,
    ICON_WEB,
    MATCH_ALL,
    MATCH_ALLCHARS,
    Workflow3,
)

from config import (
    ICON_HELP,
    KEYWORD_WORDCOUNTER,
    README_URL,
    HELP_URL
)


log = None

DELIMITER = u'\u203a'  # SINGLE RIGHT-POINTING ANGLE QUOTATION MARK

ALFRED_AS = 'tell application "Alfred 3" to search "{}"'.format(
    KEYWORD_WORDCOUNTER)


def word_counter_lookup(query):

	def add(x, y): return x + y

	# read PLIST
	records = os.path.expanduser('~/Library/Application Support/WordCounter/app_records.plist')
	data = plistlib.readPlist(records)

	def word_count_total(date):
		# collect per-app totals
		apps = data[date]
		counts = []
		for app in apps:
		    count = reduce(add, app["counts"])
		    counts.append(count)
		    # TODO: Hit Enter to Day Report with View of Per App Breakdown
		    # wf.add_item(title=app["id"], subtitle=count, )
		    total = reduce(add, counts)	    
		return total

	# Process Date Arguments
	if query == 'today':		
		today = time.strftime("%Y-%m-%d")
		return word_count_total(today)

	elif query == 'yesterday':
		today = datetime.date.today()
		yesterdayRaw = today - datetime.timedelta(days=1)
		yesterday = yesterdayRaw.strftime("%Y-%m-%d")
		return word_count_total(yesterday)

	# TODO
	elif query == 'previous7':
		return 'TODO'

def main(wf):
    """Run Script Filter.

    Args:
        wf (workflow.Workflow): Workflow object.

    """
    args = docopt(__doc__, wf.args)

    log.debug('args : {!r}'.format(args))

    query = args.get('<query>')

    # bootstrap(wf)

    # Alternative actions ----------------------------------------------

    if args.get('--today'):
        word_counter_lookup("today")
        return

    if args.get('--yesterday'):
        word_counter_lookup("yesterday")
        return

    if args.get('--previous7'):
        word_counter_lookup("previous7")
        return

     

    # Parse query ------------------------------------------------------

    if DELIMITER in query:
        return handle_delimited_query(query)

    # Filter options ---------------------------------------------------

    query = query.strip()

    options = [
        dict(title="Today's Word Count Stats",
             subtitle=word_counter_lookup("today"),
             valid=True,
             # TODO: Copy text to clipboard
             arg='--today',
             # TODO Replace with More Relevant Icon
             icon=ICON_HELP),

        dict(title="Yesterday's Word Count Stats",
             subtitle=word_counter_lookup("yesterday"),
             valid=True,
             arg='--yesterday',
             icon=ICON_HELP),

        dict(title="Previous 7 Days' Word Count Stats",
             subtitle=word_counter_lookup("previous7"),
             valid=True,
             arg='--previous7',
             icon=ICON_HELP),

    ]

    if query:
        options = wf.filter(query, options, key=lambda d: d['title'],
                            min_score=30)

    if not options:
        wf.add_item('No matching options', 'Try a different query?',
                    icon=ICON_WARNING)

    for d in options:
        wf.add_item(**d)

    wf.send_feedback()
    return


if __name__ == '__main__':
    wf = Workflow3()
    log = wf.logger
    sys.exit(wf.run(main))
