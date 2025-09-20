import yaml
import re
import sys
import os
import shutil
import json

def read_log_file(filepath):
    """
    Reads the content of a log file and returns it as a list of lines.
    
    Args:
        filepath (str): The path to the log file.
    
    Returns:
        list: A list of strings, where each string is a line from the file.
        Returns an empty list if the file is not found.
    """
    try:
        with open(filepath, 'r') as f:
            lines = f.readlines()
            print(f"Successfully read {len(lines)} lines from '{filepath}'.")
            return lines
    except FileNotFoundError:
        print(f"Error: Log file not found at '{filepath}'.")
        return []
    except Exception as e:
        print(f"An unexpected error occurred while reading the log file: {e}")
        return []

def read_rules_file(filepath):
    """
    Reads and parses a YAML file containing a list of search patterns.
    
    Args:
        filepath (str): The path to the rules.yaml file.
        
    Returns:
        list: A list of dictionaries, where each dictionary contains a
              'name' and 'regex' key. Returns an empty list on error.
    """
    try:
        with open(filepath, 'r') as f:
            rules = yaml.safe_load(f)
            print(f"Successfully loaded search rules from '{filepath}'.")
            return rules
    except FileNotFoundError:
        print(f"Error: Rules file not found at '{filepath}'.")
        return []
    except yaml.YAMLError as e:
        print(f"Error: Failed to parse the YAML file. Please check the format. Details: {e}")
        return []

def find_patterns_in_log(log_content, rules):
    """
    Finds lines in the log that match the regex patterns in the rules.
    
    Args:
        log_content (list): A list of strings from the log file.
        rules (list): A list of rule dictionaries.
        
    Returns:
        dict: A dictionary where each key is a rule name and the value is a
              list of matching log lines.
    """
    matches = {}
    for rule in rules:
        rule_name = rule.get('name')
        pattern = rule.get('regex')
        
        if not rule_name or not pattern:
            print(f"Warning: Skipping malformed rule: {rule}")
            continue

        try:
            # Use re.IGNORECASE to perform a case-insensitive search
            compiled_pattern = re.compile(pattern, re.IGNORECASE)
            matches[rule_name] = [
                line.strip() for line in log_content if compiled_pattern.search(line)
            ]
        except re.error as e:
            print(f"Warning: Invalid regex pattern '{pattern}' for rule '{rule_name}'. Details: {e}")
    
    return matches

def main():
    """
    Main function to orchestrate reading the log and rules files, finding matches,
    and then processing the files.
    """
    # Check for command-line arguments
    if len(sys.argv) < 3:
        print("Usage: python log_reader.py <log_file_path> <rules_file_path>")
        sys.exit(1)

    log_file_path = sys.argv[1]
    rules_file_path = sys.argv[2]
            
    # Read the log file
    log_content = read_log_file(log_file_path)
    if not log_content:
        sys.exit(1)
    
    # Read the rules file
    search_rules = read_rules_file(rules_file_path)
    if not search_rules:
        sys.exit(1)
    
    # Find patterns in the log content
    found_matches = find_patterns_in_log(log_content, search_rules)
    
    # Print the findings in a structured way
    print("\n--- Search Results ---")
    if not found_matches:
        print("No matches found or no rules were processed.")
    else:
        for rule_name, lines in found_matches.items():
            print(f"\nMatches for '{rule_name}':")
            if lines:
                for line in lines:
                    print(f"  - {line}")
            else:
                print("  (No matches found for this rule)")
    
    # Print the total number of matches per rule
    print("\n--- Summary of Matches ---")
    match_counts = {rule_name: len(lines) for rule_name, lines in found_matches.items()}
    for rule_name, count in match_counts.items():
        print(f"Rule '{rule_name}': {count} total matches")

    # --- Post-processing: Move log file and write metrics ---
    try:
        # Create directories if they don't exist
        processed_dir = 'processed'
        metrics_dir = 'metrics'
        os.makedirs(processed_dir, exist_ok=True)
        os.makedirs(metrics_dir, exist_ok=True)

        log_filename = os.path.basename(log_file_path)
        
        # Write the metrics file
        metrics_file_path = os.path.join(metrics_dir, f"{os.path.splitext(log_filename)[0]}.json")
        with open(metrics_file_path, 'w') as f:
            json.dump(match_counts, f, indent=4)
        print(f"\nSuccessfully wrote metrics to '{metrics_file_path}'.")
        
        # Move the log file
        new_log_file_path = os.path.join(processed_dir, log_filename)
        shutil.move(log_file_path, new_log_file_path)
        print(f"Successfully moved '{log_file_path}' to '{new_log_file_path}'.")

    except Exception as e:
        print(f"\nAn error occurred during post-processing: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
