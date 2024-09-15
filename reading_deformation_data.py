import pandas as pd
import numpy as np
import glob
import os
import re

def extract_number(filename):
    match = re.search(r"(\d+)", filename)
    if match:
        return int(match.group(1))
    else:
        return None

folder_path = 'C:/Users/austi/Documents/GitHub/Thesis_Code/Text_Files/1/deformation'
file_list = glob.glob(f"{folder_path}/*.txt")

results = []

for file_name in file_list:
    df = pd.read_csv(file_name,delimiter='\t')
    max_deformation_row = df.loc[df['Total Deformation (mm)'].idxmax()]
    file_name = os.path.basename(file_name)
    max_deformation = max_deformation_row['Total Deformation (mm)']
    x_location = max_deformation_row['X Location (mm)']
    y_location = max_deformation_row['Y Location (mm)']
    z_location = max_deformation_row['Z Location (mm)']

    number = extract_number(file_name)
    if number is not None:
        print(number)
    else:
        print("No number found in the filename.")


    results.append({
        'File Name': number,
        'Max Deformation': max_deformation,
        'X': x_location,
        'Y': y_location,
        'Z': z_location
    })

output=pd.DataFrame(results)
output.head()