import pandas as pd
import itertools
import numpy as np

np.random.seed(20)


factors = {
    "Pipe OD":[50,65,80,90,100,125,150,200,250,300,400],
    "Pipe Schedule":['40','STD','80','XS','XXS'],
    "Lumped Mass":[0,25,50,100,250,500],
    "Flange Class":[150,300,600],
    "Length":[1,2,3,4,5]
}

combinations = list(itertools.product(*factors.values()))

design_df = pd.DataFrame(combinations, columns=factors.keys())

pipe_length_min = 0.3
pipe_length_max = 5

design_df['Length'] = np.random.uniform(pipe_length_min, pipe_length_max, len(design_df))
design_df['Length2'] = np.random.uniform(pipe_length_min, pipe_length_max, len(design_df))
print(design_df)

design_df.to_csv('combinations.csv', index=False)