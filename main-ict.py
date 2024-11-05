import os
import pandas as pd
import geopandas as gpd
from shapely import Point
from utils import get_files, convert_wkb_to_lat_lng
from data import layers

ICT_input_path = 'input/ICT'
ICT_output_path = 'output/ICT/output.csv'
ICT_dfs = []  
columns = ['name', 'address', 'type', 'source', 'lat', 'lng', 'geom']

for file_name in get_files(ICT_input_path, '.csv'):
    file_path = os.path.join(ICT_input_path, file_name)
    df = pd.read_csv(file_path)

    lat_lng_df = df['geom'].apply(convert_wkb_to_lat_lng)
    df = pd.concat([df, lat_lng_df], axis=1)
    df['layer'] = df['layer'].map(layers).fillna(df['layer'])

    point_geom = [Point(xy) for xy in zip(df['lng'], df['lat'])]
    gdf = gpd.GeoDataFrame(df, geometry=point_geom, crs='EPSG:4326')
    
    ICT_dfs.append(gdf)

combined_ICT_dfs = pd.concat(ICT_dfs, ignore_index=True)
combined_ICT_dfs = combined_ICT_dfs.rename(columns={
    'layer': 'type',
    'geom': 'geom_temp',
    'geometry': 'geom',
})
combined_ICT_dfs = combined_ICT_dfs[columns]
combined_ICT_dfs.to_csv(ICT_output_path, index=False)
