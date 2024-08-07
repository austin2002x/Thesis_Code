import pandas as pd
import openpyxl

# Load the Excel file
file_path = 'C:\\Users\\austi\\Documents\\GitHub\\Thesis_Code\\ASME B36.10M.csv'  # Replace with your file path
df = pd.read_csv(file_path)


# Specify the columns to check for NaN values
columns_to_check = ['Identification', 'Schedule Number']  # Replace with your column names

# Drop rows where both specified columns are NaN
df_cleaned = df.dropna(subset=columns_to_check, how='all')

#df_cleaned["Schedule Number"] = df_cleaned['Schedule Number'].astype("Int64")

df_cleaned['Schedule Number'] = df_cleaned['Schedule Number'].fillna(df_cleaned['Identification'])

schedule_values_to_keep = [40.0,80.0,'STD','XS','XXS']
filtered_df = df_cleaned[df_cleaned['Schedule Number'].isin(schedule_values_to_keep)]
filtered_df.drop(columns='Identification',inplace=True)

df_cleaned.to_csv('cleaned_data.csv', index=False)
filtered_df.to_csv('filtered_data.csv', index=False)

