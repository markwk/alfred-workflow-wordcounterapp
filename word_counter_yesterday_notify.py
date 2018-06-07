import plistlib
import os
import time

def add(x, y): return x + y

#today = time.strftime("%Y-%m-%d")

import datetime as DT
today = DT.date.today()
yesterdayRaw = today - DT.timedelta(days=1)
yesterday = yesterdayRaw.strftime("%Y-%m-%d")
# yesterday = DT.date.today.("%Y-%m-%d")

# read PLIST
records = os.path.expanduser('~/Library/Application Support/WordCounter/app_records.plist')
data = plistlib.readPlist(records)

# collect per-app totals
apps = data[yesterday]
counts = []
for app in apps:
    count = reduce(add, app["counts"])
    counts.append(count)
    print app["id"] + ": " + str(count)
    
total = reduce(add, counts)
print total

def notify(title, text):
    os.system("""
              osascript -e 'display notification "{}" with title "{}"'
              """.format(text, title))

message = "%s Total Words Written Yesterday." % (total)
notify("Word Count Yesterday", message)


