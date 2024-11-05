import os
import pandas as pd
import geopandas as gpd
from shapely import Point
from utils import get_files
from data import layers

diadiem247_input_path = 'input/diadiem247'
diadiem247_output_path = 'output/diadiem247/output.csv'
diadiem247_dfs = []  
columns = ['name', 'address', 'type', 'source', 'lat', 'lng', 'geom']

for file_name in get_files(diadiem247_input_path, '.csv'):
    file_path = os.path.join(diadiem247_input_path, file_name)
    df = pd.read_csv(file_path)

    df['address'] = df['address'].replace('&#8211;', '-').replace('&nbsp;&nbsp;', '').replace('&nbsp;', ' ').apply(lambda x: ' '.join(str(x).split()))
    df['type'] = df['type'].map(layers).fillna(df['type'])

    point_geom = [Point(xy) for xy in zip(df['lng'], df['lat'])]
    gdf = gpd.GeoDataFrame(df, geometry=point_geom, crs='EPSG:4326')

    # df = df.drop_duplicates(subset=['name', 'address'], keep='first')
    # df = df.dropna(axis=0, subset=['lng', 'lat'], how='all')
    diadiem247_dfs.append(gdf)

combined_diadiem247_dfs = pd.concat(diadiem247_dfs, ignore_index=True)
combined_diadiem247_dfs = combined_diadiem247_dfs.rename(columns={
    'geometry': 'geom'
})
combined_diadiem247_dfs = combined_diadiem247_dfs[columns]
combined_diadiem247_dfs.to_csv(diadiem247_output_path, index=False)