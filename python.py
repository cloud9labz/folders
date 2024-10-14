import os
import subprocess
import csv
import re

# Function to get the last commit time of a folder
def get_commit_time(folder_path):
    try:
        # Get the last commit time for the folder
        commit_time = subprocess.check_output(
            ['git', 'log', '-1', '--format=%cd', '--', folder_path],
            encoding='utf-8'
        ).strip()
        return commit_time
    except subprocess.CalledProcessError:
        return None

# Regex for 14-digit numbers
fourteen_digit_regex = re.compile(r'^\d{14}$')

# Collecting folders
folders = []

# Check the 'migration' folder
migration_folder = 'migration'

if os.path.exists(migration_folder):
    for item in os.listdir(migration_folder):
        item_path = os.path.join(migration_folder, item)
        
        if os.path.isdir(item_path) and not item.isdigit():
            # Check for 14-digit folders within the current non-numerical folder
            for sub_item in os.listdir(item_path):
                sub_item_path = os.path.join(item_path, sub_item)
                
                if os.path.isdir(sub_item_path) and fourteen_digit_regex.match(sub_item):
                    commit_time = get_commit_time(item_path)
                    if commit_time:
                        folders.append((item, sub_item, commit_time))

# Writing to CSV
output_file = 'folders_with_commit_times.csv'
with open(output_file, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Non-numerical Folder', '14-digit Folder', 'Commit Time'])
    writer.writerows(folders)

print(f"CSV file '{output_file}' created successfully.")
