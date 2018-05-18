import plistlib
import os
import time

def add(x, y): return x + y

# read PLIST
records = os.path.expanduser('~/Library/Application Support/WordCounter/app_records.plist')
data = plistlib.readPlist(records)

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
  print date + "," + str(total)
