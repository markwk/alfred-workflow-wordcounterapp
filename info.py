#!/usr/bin/python
# encoding: utf-8
#
# Copyright  (c) 2018 Mark Koester mark@int3c.com
#
# MIT Licence. See http://opensource.org/licenses/MIT
#
# Created on 2014-12-26
#

"""info.py [options] [<query>]

View/manage workflow settings.

Usage:
    info.py [<query>]
    info.py (-h|--help)
    info.py --openhelp
    info.py --logbug

Options:
    -h, --help    Show this message
    --openhelp    Open help file in default browser
    --logbug      Log bug to Bug Tracker

"""

from __future__ import absolute_import

import subprocess
import sys

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
    KEYWORD_SETTINGS,
    README_URL,
    HELP_URL
)


log = None

DELIMITER = u'\u203a'  # SINGLE RIGHT-POINTING ANGLE QUOTATION MARK

ALFRED_AS = 'tell application "Alfred 3" to search "{}"'.format(
    KEYWORD_SETTINGS)


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

    if args.get('--openhelp'):
        subprocess.call(['open', README_URL])
        return

    if args.get('--logbug'):
        subprocess.call(['open', HELP_URL])
        return

    # Parse query ------------------------------------------------------

    if DELIMITER in query:
        return handle_delimited_query(query)

    # Filter options ---------------------------------------------------

    query = query.strip()

    options = [
        dict(title='View Help File',
             subtitle='Open help file in your browser',
             valid=True,
             arg='--openhelp',
             icon=ICON_HELP),

        dict(title='Log a Bug',
             subtitle='Log a bug your browser',
             valid=True,
             arg='--logbug',
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
