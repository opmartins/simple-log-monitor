import sys
import yaml

log_file = sys.argv[1]

with open("rules.yaml", "r") as rules_file:
    rules = yaml.safe_load(rules_file)
patterns = [rule["regex"] for rule in rules]

log_file_saída = 'log_tratado.log'

with open(log_file, 'r') as file, open(log_file_saída, 'w') as file_saída:
    for line in file:
        if any(pattern in line for pattern in patterns):
            file_saída.write(line)