import pandas as pd
import itertools
import numpy as np
import openpyxl

np.random.seed(20)


factors = {
    "Pipe DN":[50,65,80,90,100,125,150,200,250,300,400],
    "Pipe Schedule":['40','STD','80','XS','XXS'],
    "Lumped Mass":[0,25,50,100,250,500],
    "Flange Class":[150,300,600],
    "Length":[1,2,3,4,5]
}

combinations = list(itertools.product(*factors.values()))

design_df = pd.DataFrame(combinations, columns=factors.keys())

pipe_length_min = 0.3
pipe_length_max = 5

design_df['Length'] = (np.random.uniform(pipe_length_min, pipe_length_max, len(design_df))).round(3)
design_df['Length2'] = (np.random.uniform(pipe_length_min, pipe_length_max, len(design_df))).round(3)

# Load the Excel file
file_path_1 = 'C:\\Users\\austi\\Documents\\GitHub\\Thesis_Code\\ASME B36.10M.csv'  # Replace with your file path
df_B36 = pd.read_csv(file_path_1)
# Specify the columns to check for NaN values
columns_to_check = ['Identification', 'Schedule Number']  # Replace with your column names

# Drop rows where both specified columns are NaN
df_cleaned = df_B36.dropna(subset=columns_to_check, how='all')
df_cleaned['Schedule Number'] = df_cleaned['Schedule Number'].astype('Int64')
df_cleaned_test=df_cleaned.copy()
df_cleaned_test.drop(columns='Schedule Number',inplace=True)
df_cleaned_test.dropna(inplace=True)

df_cleaned_test.rename(columns={'Identification': 'Schedule Number'}, inplace=True)


schedule_values_to_keep = [40,80]
filtered_df = df_cleaned[df_cleaned['Schedule Number'].isin(schedule_values_to_keep)]
filtered_df.drop(columns='Identification',inplace=True)

df_reduced_B16 = pd.concat([filtered_df,df_cleaned_test],ignore_index=True)


file_path_2 = 'C:\\Users\\austi\\Documents\\GitHub\\Thesis_Code\\ASME B16.5.csv'  # Replace with your file path
df = pd.read_csv(file_path_2)

columns_to_select =["Class", "DN", "Flange OD A (mm)", "Flange Thickness D (mm)", "Raised Face Diam. G (mm)", "W Neck C (mm)"]

new_df=df[columns_to_select]

DN_to_keep = [50,65,80,90,100,125,150,200,250,300,400]
df_reduced_B36 = new_df[new_df['DN'].isin(DN_to_keep)]

#Need to Merge All the DF together
#df_reduced_B36
#df_reduced_B16
#design_df

df_reduced_B16.rename(columns={'Schedule Number': 'Pipe Schedule'}, inplace=True)
df_reduced_B36.rename(columns={'Class': 'Flange Class'}, inplace=True)
df_reduced_B36.rename(columns={'DN': 'Pipe DN'}, inplace=True)

design_df["Pipe Schedule"] = design_df["Pipe Schedule"].astype(str)
df_reduced_B16["Pipe Schedule"] = df_reduced_B16["Pipe Schedule"].astype(str)

df_combo = pd.merge(design_df,df_reduced_B16 , on=['Pipe Schedule', 'Pipe DN'])
df_combo2 = pd.merge(df_combo,df_reduced_B36 , on=['Flange Class', 'Pipe DN'])


df_combo2.to_csv('final.csv', index=False)