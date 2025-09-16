# Step 2

- Read the log file from `logs/`.
- Read the search patterns from the `rules.yaml` file.
- For each rule in the YAML, check every log line against its regex.
- At the end, print the total matches per rule.
- Nothing hardcoded: file names are read using arguments.

**Run:**
```bash
python log_reader.py logs/log.log rules.yaml
```

Tip: use argparse for log_path and rules_path.

After successfully processing a log file:
- Move it to a processed/ folder.
- Write a new file to the metrics/ folder.
- The file name should be the same as the log file name.
- Its contents are JSON containing the total matches per rule.

Refer to the example files. Example output to console:

```
Match counts:
errors: 1
criticals: 0
warnings: 2
```

- Push your changes to a new Git branch.

- Open a Pull Request (PR) for review.
