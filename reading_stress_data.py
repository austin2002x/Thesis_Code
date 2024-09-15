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

folder_path = 'C:/Users/austi/Documents/GitHub/Thesis_Code/Testing/test'
file_list = glob.glob(folder_path+'/**/*.txt', recursive=True)

results = []

for file_name in file_list:
    df = pd.read_csv(file_name,delimiter='\t')
    df.drop({"S (mm)","X Coordinate (mm)","Y Coordinate (mm)","Z Coordinate (mm)"},inplace=True,axis=1)
    stress_04t = df.loc[0, 'Maximum Principal Stress (MPa)']
    stress_1t = df.loc[1, 'Maximum Principal Stress (MPa)']
    stress_hs = 1.67 * stress_04t - 0.67 * stress_1t
    number = extract_number(file_name)
    
    results.append({
        'File Name': number,
        'HotSpotStress':stress_hs
    })
    
all_results=pd.DataFrame(results)
max_values = all_results.groupby('File Name')['HotSpotStress'].max().round(3)
output=max_values.to_frame()
output.reset_index(inplace=True)