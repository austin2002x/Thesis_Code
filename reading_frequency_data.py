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

folder_path = 'C:/Users/austi/Documents/GitHub/Thesis_Code/Text_Files/count'
file_list = glob.glob(f"{folder_path}/*.txt")

results = []

#test='C:/Users/austi/Documents/GitHub/Thesis_Code/Text_Files/1/freq/Frequency_1.0.txt'
for file in file_list:
    current_file=open(file,'r')
    content = current_file.read()
    

    # Assuming the numeric value is always in the format "x.xxxx [Hz]"
    if '.' in content:
        match = re.search(r"(\d+\.\d+)", content)
    else:
        match = re.search(r"(\d+)", content)
    file_name = os.path.basename(file)
    number=extract_number(file_name)
    freq=float(match.group(1))
    results.append({'File Name': number,'Frequency':freq})
    current_file.close()
    

output=pd.DataFrame(results)
output.head()
