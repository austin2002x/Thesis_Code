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
    
def missing_data(folder_path):

    file_list = glob.glob(f"{folder_path}/*.txt")

    results = []

    for file in file_list:
        file_name = os.path.basename(file)
        number=extract_number(file_name)
        results.append({'File Name': number})

    output=pd.DataFrame(results)
    output.head()

    full_set = set(range(1, 3181))

    # Step 2: Get the set of integers present in the DataFrame
    present_values = set(output['File Name'])

    # Step 3: Find the missing integers by subtracting the present set from the full set
    missing_values = full_set - present_values

    # Step 4: Convert the missing values to a sorted list (if needed)
    missing_values = sorted(list(missing_values))

    # Print or save the missing values
    return ("Missing values:", missing_values)
