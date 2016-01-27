from collections import defaultdict
from pprint import pprint
import itertools
import re
import csv
import sys

match_line = re.compile("^\[(.*?), (.*)\]\n$")

content = []

for line in sys.stdin.readlines():
    print(line)
    matcher = match_line.match(line)
    if (matcher):
        content.append({
            "id": matcher.group(1),
            "value": matcher.group(2)
        })

# remove various common suffixes from the string
pattern = re.compile("^(.*?)(ed|ion|ic|ical|y|'s|s)?( film)?$")

def grouper(entry):
    preproc = entry['value'].lower().replace('-', ' ')
    return pattern.match(preproc).group(1)

groups = defaultdict(list)

for group, items in itertools.groupby(content, grouper):
    groups[group] += list(items)

for entries in groups.values():
    # if a group has more than one entry, merge with first entry
    if len(entries) > 1:
        merge_to = entries[0]

        for entry in entries[1:]:
            print(merge_to['id'] + ',' + entry['id'])
