import json
import os
import sys
import re

import yaml

if len(sys.argv) < 3:
    print("Usage: python example_reader.py <logfile> <rulesfile>")
    sys.exit(1)

# i.e. logs/log.log
log_file_path = sys.argv[1]
# log.log
log_file_name = os.path.basename(log_file_path)
# log
log_file_name_no_ext = os.path.splitext(log_file_name)[0]

rules_file_path = sys.argv[2]

logs_file = open(log_file_path, 'r').readlines()
rules = yaml.safe_load(open(rules_file_path, 'r'))

matches = {rule['name']: 0 for rule in rules}
for line in logs_file:
    for rule in rules:
        if re.compile(rule['regex']).search(line):
            matches[rule['name']] += 1


os.rename(log_file_path, f'processed/{log_file_name}')
with open(f'metrics/{log_file_name_no_ext}.json', 'w') as f:
    json.dump(matches, f, indent=4)

print(matches)