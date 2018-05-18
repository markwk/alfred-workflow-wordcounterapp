import os
import sys

import plistlib
import time

def add(x, y): return x + y

today = time.strftime("%Y-%m-%d")
# print today

# read PLIST
records = os.path.expanduser('~/Library/Application Support/WordCounter/app_records.plist')
data = plistlib.readPlist(records)

# print type(data)

# collect per-app totals
apps = data[today]
counts = []
for app in apps:
    count = reduce(add, app["counts"])
    counts.append(count)
    print app["id"] + ": " + str(count)
    
total = reduce(add, counts)
print total
