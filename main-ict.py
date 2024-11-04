import os
import pandas as pd
from utils import get_files, convert_wkb_to_lat_lng

ICT_input_path = 'input/ICT'
ICT_output_path = 'output/ICT/output.csv'
ICT_dfs = []  
columns = ['name', 'address', 'type', 'source', 'lat', 'lng', 'geom']

for file_name in get_files(ICT_input_path, '.csv'):
    file_path = os.path.join(ICT_input_path, file_name)
    df = pd.read_csv(file_path)

    lat_lng_df = df['geom'].apply(convert_wkb_to_lat_lng)
    df = pd.concat([df, lat_lng_df], axis=1)
    
    ICT_dfs.append(df)

combined_ICT_dfs = pd.concat(ICT_dfs, ignore_index=True)
combined_ICT_dfs = combined_ICT_dfs.rename(columns={'layer': 'type'})
combined_ICT_dfs = combined_ICT_dfs[columns]
combined_ICT_dfs.to_csv(ICT_output_path, index=False)
