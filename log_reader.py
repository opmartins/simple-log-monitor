
log_file = 'log.log'

with open(log_file, 'r') as file:
    for line in file:
        if 'CRITICAL' in line or 'ERROR' in line:
            print(line.strip())