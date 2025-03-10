# import os
# import pandas as pd
# import shutil

# # Load the CSV file
# csv_file = 'submission_metadata.csv'  # Replace with your CSV file path
# df = pd.read_csv(csv_file)

# df['Submission ID'] = df['Submission ID'].dropna().astype(int).astype(str)
# df = df.dropna(subset=['Submission ID'])

# # Create a new folder for the moved files
# new_folder = os.path.expanduser('~/Github/CS238PeerReviews/organized_submissions/')  # Replace with the path to the new folder
# os.makedirs(new_folder, exist_ok=True)

# # Iterate over the DataFrame
# submission_id_to_new_filename = {}
# for i, row in df.iterrows():
#     submission_id = row['Submission ID']  # Replace 'submission_id' with the actual column name
#     if submission_id in submission_id_to_new_filename.keys():
#         continue
#     folder_name = f'submission_{submission_id}'
#     folder_path = os.path.expanduser(os.path.join('~/Github/CS238PeerReviews/final_submissions', folder_name))  # Replace with the path to the submission folders

#     # Find the file in the folder
#     if os.path.exists(folder_path) and os.path.isdir(folder_path):
#         file_list = os.listdir(folder_path)
#         if file_list:
#             file_name = file_list[0]
#             file_path = os.path.join(folder_path, file_name)
#             id = f'{len(submission_id_to_new_filename)+1:03d}'
#             new_filename = f'{id}{os.path.splitext(file_name)[1]}'
#             new_file_path = os.path.join(new_folder, new_filename)
            
#             # Move and rename the file
#             shutil.move(file_path, new_file_path)
#             submission_id_to_new_filename[submission_id] = id
#             print(f"moved {folder_path}")
#         else:
#             print(f"No file found in {folder_path}")
#             if submission_id not in submission_id_to_new_filename.keys():
#                 submission_id_to_new_filename[submission_id] = None
#     else:
#         submission_id_to_new_filename[submission_id] = None
#         print(f'could not find {folder_path}')

# print(submission_id_to_new_filename)

# # Add the new filenames to the DataFrame and save the updated CSV
# df['project_id'] = df['Submission ID'].map(submission_id_to_new_filename)
# df.to_csv('updated_csvfile.csv', index=False)  # Replace with the desired path for the updated CSV
