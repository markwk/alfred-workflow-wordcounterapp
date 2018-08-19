import plistlib
import os
import time

def add(x, y): return x + y

import datetime as DT
today = DT.date.today()
yesterdayRaw = today - DT.timedelta(days=1)
yesterday = yesterdayRaw.strftime("%Y-%m-%d")

# notification via osascript
# TODO: Is there a better way to do this? 
def notify(title, text):
    os.system("""
              osascript -e 'display notification "{}" with title "{}"'
              """.format(text, title))

# read PLIST
records = os.path.expanduser('~/Library/Application Support/WordCounter/app_records.plist')
data = plistlib.readPlist(records)

# check if wordcounter tracked yesterday
if yesterday not in data:
    notify("No wordcounter writing tracked yesterday")
    exit()

# collect per-app totals
apps = data[yesterday]
counts = []
for app in apps:
    count = reduce(add, app["counts"])
    counts.append(count)
    print app["id"] + ": " + str(count)
    
total = reduce(add, counts)
print total

message = "%s Total Words Written Yesterday." % (total)
notify("Word Count Yesterday", message)

