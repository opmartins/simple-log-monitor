
log_file = 'log.log'
log_file_saída = 'log_tratado.log'

with open(log_file, 'r') as file, open(log_file_saída, 'w') as file_saída:
    for line in file:
        if 'CRITICAL' in line or 'ERROR' in line:
            file_saída.write(line)