from collections import defaultdict
from pprint import pprint
import itertools
import re
import csv
import sys

match_line = re.compile("^\[(.*?), (.*)\]\n$")

content = []

for line in sys.stdin.readlines():
    matcher = match_line.match(line)
    if (matcher):
        content.append({
            "id": matcher.group(1),
            "value": matcher.group(2)
        })

# remove various common prefixes/suffixes from the string
pattern = re.compile("^(, )?(.*?)$")

def grouper(entry):
    preproc = entry['value'].lower().replace('-', ' ')
    return pattern.match(preproc).group(2)

groups = defaultdict(list)

for group, items in itertools.groupby(content, grouper):
    groups[group] += list(items)

for entries in groups.values():
    if len(entries) > 1 and any(e["value"].startswith(",") for e in entries) and any(not e["value"].startswith(",") for e in entries):
        print(",".join([e["id"] for e in entries]))
