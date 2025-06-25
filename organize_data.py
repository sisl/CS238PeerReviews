import os
import pandas as pd
import shutil
import sys

assert(len(sys.argv) > 4), "Usage: organize_data.py [csv file] [submissions folder] [new folder] [new csv file]"
csv_file = sys.argv[1]  # Replace with your CSV file path
old_folder_path = sys.argv[2]  # Replace with the path to the submission folders
new_folder_path = sys.argv[3]  # Replace with the path to the new folder
new_csv_file = sys.argv[4]  # Replace with the desired path for the updated CSV
submission_column = "Submission ID"  # Replace with the actual column name for submission IDs
if not os.path.exists(csv_file):
    raise FileNotFoundError(f"The specified CSV file does not exist: {csv_file}")
if not os.path.exists(old_folder_path):
    raise FileNotFoundError(f"The specified folder path does not exist: {old_folder_path}")

df = pd.read_csv(csv_file)

df['Submission ID'] = df['Submission ID'].dropna().astype(int).astype(str)
df = df.dropna(subset=['Submission ID'])

# Create a new folder for the moved files
new_folder = os.path.expanduser(new_folder_path)
os.makedirs(new_folder, exist_ok=True)

# Iterate over the DataFrame
submission_id_to_new_filename = {}
for i, row in df.iterrows():
    submission_id = row[submission_column]
    if submission_id in submission_id_to_new_filename.keys():
        continue
    folder_name = f'submission_{submission_id}'
    folder_path = os.path.expanduser(os.path.join(old_folder_path, folder_name))

    # Find the file in the folder
    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        file_list = os.listdir(folder_path)
        if file_list:
            file_name = file_list[0]
            file_path = os.path.join(folder_path, file_name)
            id = f'{len(submission_id_to_new_filename)+1:03d}'
            new_filename = f'{id}{os.path.splitext(file_name)[1]}'
            new_file_path = os.path.join(new_folder, new_filename)
            
            # Copy and rename the file
            shutil.copy(file_path, new_file_path)
            submission_id_to_new_filename[submission_id] = id
            print(f"moved {folder_path}")
        else:
            print(f"No file found in {folder_path}")
            if submission_id not in submission_id_to_new_filename.keys():
                submission_id_to_new_filename[submission_id] = None
    else:
        submission_id_to_new_filename[submission_id] = None
        print(f'could not find {folder_path}')

print(submission_id_to_new_filename)

# Add the new filenames to the DataFrame and save the updated CSV
df['project_id'] = df['Submission ID'].map(submission_id_to_new_filename)
df.to_csv(new_csv_file, index=False)  # Replace with the desired path for the updated CSV
