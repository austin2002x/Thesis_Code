import pandas as pd
import openpyxl

# Load the Excel file
file_path = 'C:\\Users\\austi\\Documents\\GitHub\\Thesis_Code\\ASME B16.5.csv'  # Replace with your file path
df = pd.read_csv(file_path)

columns_to_select =["Class", "DN", "Flange OD A (mm)", "Flange Thickness D (mm)", "Raised Face Diam. G (mm)", "W Neck C (mm)"]

new_df=df[columns_to_select]



DN_to_keep = [50,65,80,90,100,125,150,200,250,300,400]
filtered_df = new_df[new_df['DN'].isin(DN_to_keep)]


filtered_df.to_csv("ASME_B16.5_reduced.csv",index=False)

