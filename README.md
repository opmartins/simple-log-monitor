# Simple Log Monitor

## Input
A system log file (e.g., `/var/log/syslog` or a test file you create).

## Processing
Python script reads the file line by line.

## Logic
If a line matches patterns (e.g., "ERROR", "CRITICAL"), store it.

## Output
- Print to console  
- Write to another file  
- Or send a notification (start simple with print, later add email/Slack API)  

---

## What You’ll Learn
- **File handling**: open, read, write  
- **String handling**: search for keywords, regex  
- **Basic data structures**: store alerts in lists/dicts  
- **Modules**: `os`, `time`, `re`, maybe `smtplib` or `requests` for alerts  
- **DevOps connection**: Understand logs, parsing, automating monitoring tasks  

---

## Extension Steps
1. Watch the file continuously with `tail -f` style (using `time.sleep` or `watchdog`).  
2. Track counts of error levels per hour (data aggregation).  
3. Make a simple dashboard (Flask + HTML).  
4. Dockerize the tool for practice.  
