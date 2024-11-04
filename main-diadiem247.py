import os
import pandas as pd
from utils import get_files, create_wkb_from_lat_lng

diadiem247_input_path = 'input/diadiem247'
diadiem247_output_path = 'output/diadiem247/output.csv'
diadiem247_dfs = []  
columns = ['name', 'address', 'type', 'source', 'lat', 'lng', 'geom']

for file_name in get_files(diadiem247_input_path, '.csv'):
    file_path = os.path.join(diadiem247_input_path, file_name)
    df = pd.read_csv(file_path)

    df['location_address'] = df['location_address'].replace('&#8211;', '-').replace('&nbsp;&nbsp;', '').replace('&nbsp;', ' ').apply(lambda x: ' '.join(x.split()))
    df['source'] = 'diadiem247' if 'source' not in df.columns else df['source']
    df['geom'] = df.apply(lambda x: create_wkb_from_lat_lng(x['lat'], x['lng']), axis=1)

    df = df.drop_duplicates(subset=['location_name', 'location_address'], keep='first')
    df = df.dropna(axis=0, subset=['lng', 'lat'], how='all')
    diadiem247_dfs.append(df)

combined_diadiem247_dfs = pd.concat(diadiem247_dfs, ignore_index=True)
combined_diadiem247_dfs = combined_diadiem247_dfs.rename(columns={
    'location_name': 'name',
    'location_address': 'address',
    'category_name': 'type'
})
combined_diadiem247_dfs = combined_diadiem247_dfs[columns]
combined_diadiem247_dfs.to_csv(diadiem247_output_path, index=False)