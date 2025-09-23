import sys
import yaml
import re

log_file_saída = 'log_tratado.log'
log_file = sys.argv[1]
rules_file = sys.argv[2]

# Abre o arquivo de regras
with open(rules_file, 'r') as file:
    rules = yaml.safe_load(file)
    
# Extrai as regras
regex_patterns = [rule['regex'] for rule in rules]
filter_pattern = '|'.join(regex_patterns)


# Main
with open(log_file, 'r') as file, open(log_file_saída, 'w') as file_saída:
    for line in file:
        # Verifica se a linha condiz com as regras informadas
        if re.search(filter_pattern, line):
            file_saída.write(line)