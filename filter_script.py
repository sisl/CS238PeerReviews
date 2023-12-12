import pandas as pd

# Load the first CSV into a DataFrame
df1 = pd.read_csv('updated_csvfile.csv')  # Replace with your actual file path

# Load the second CSV into a DataFrame
df2 = pd.read_csv('AA228_Fall_2023_roster.csv')  # Replace with your actual file path

df1['Student ID'] = df1['Student ID'].astype(str).str.strip().str.lstrip('0')
df2['SID'] = df2['SID'].astype(str).str.strip().str.lstrip('0')


# Assuming 'student_id' is the column name in both DataFrames that contains the student IDs
# If the column names are different, replace 'student_id' with the actual column names

# Filter df2 to only include rows where the student ID is in df1
filtered_df2 = df2[df2['SID'].isin(df1['Student ID'])]

# Save the filtered DataFrame to a new CSV file if needed
filtered_df2.to_csv('filtered_AA228_Fall_2023_roster.csv', index=False)
