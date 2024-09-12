import pandas as pd
import itertools
import numpy as np
import openpyxl

np.random.seed(20)


factors = {
    "Pipe DN":[50,65,80,90,100,125,150,200,250,300,400],
    "Pipe Schedule":['40','STD','80','XS','XXS'],
    "Lumped Mass":[0.0001,1,2,3],
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

df_combo2['Raised Face Depth'] = np.where(df_combo2['Flange Class'].isin([150, 300]), 1.5, 6.4)
df_combo2['Flange Thickness D (mm)'] = np.where(df_combo2['Flange Class'].isin([150, 300]), df_combo2['Flange Thickness D (mm)'] - 1.5, df_combo2['Flange Thickness D (mm)'])

df_combo2 = df_combo2.reindex(['Pipe DN','Pipe Schedule','Flange Class','Outside Diamter (mm)', 'Length', 'Length2','Wall Thickness (mm)','Lumped Mass','Raised Face Depth','W Neck C (mm)','Flange OD A (mm)','Flange Thickness D (mm)','Raised Face Diam. G (mm)'], axis=1)
df_combo2['Length'] = (df_combo2['Length']*1000).round(0)
df_combo2['Length2'] = (df_combo2['Length2']*1000).round(0)
df_combo2["Flange OD A (mm)"] = df_combo2["Flange OD A (mm)"]/2
df_combo2['Raised Face Diam. G (mm)']=df_combo2['Raised Face Diam. G (mm)']/2
df_combo2 = df_combo2.rename(columns={"Length": "Length1", "Flange OD A (mm)" : "Flange Outer Radius","Raised Face Diam. G (mm)":"Raised Face Radius"})
df_combo2['new_col'] = np.arange(1, df_combo2.shape[0] + 1)

file_path_3 = 'C:\\Users\\austi\\Documents\\GitHub\\Thesis_Code\\Lumped_Mass.csv'
LumpMassDF = pd.read_csv(file_path_3)
df_combo3 = pd.merge(df_combo2,LumpMassDF, on=["Pipe DN","Flange Class"])

df_combo3['Lumped Mass'] = np.where(df_combo3['Lumped Mass'] == 1, df_combo3['Lumped Mass (kg)'], df_combo3['Lumped Mass'])
df_combo3.drop('Lumped Mass (kg)', axis=1, inplace=True)

file_path_4 = 'C:\\Users\\austi\\Documents\\GitHub\\Thesis_Code\\Lumped_Mass_2.csv'
LumpMassDF_2 = pd.read_csv(file_path_4)
df_combo3 = pd.merge(df_combo3,LumpMassDF_2, on=["Pipe DN","Flange Class"])

df_combo3['Lumped Mass'] = np.where(df_combo3['Lumped Mass'] == 2, df_combo3['Lumped Mass (kg)'], df_combo3['Lumped Mass'])
df_combo3.drop('Lumped Mass (kg)', axis=1, inplace=True)

file_path_5 = 'C:\\Users\\austi\\Documents\\GitHub\\Thesis_Code\\Lumped_Mass_3.csv'
LumpMassDF_3 = pd.read_csv(file_path_5)
df_combo3 = pd.merge(df_combo3,LumpMassDF_3, on=["Pipe DN","Flange Class"])

df_combo3['Lumped Mass'] = np.where(df_combo3['Lumped Mass'] == 3, df_combo3['Lumped Mass (kg)'], df_combo3['Lumped Mass'])
df_combo3.drop('Lumped Mass (kg)', axis=1, inplace=True)


df_combo3.to_csv('final.csv', index=False)