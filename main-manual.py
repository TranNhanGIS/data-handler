import os
import pandas as pd
import geopandas as gpd
from shapely import Point
from utils import get_files

manual_input_path = 'input/manual'
manual_output_path = 'output/manual/output.csv'
manual_dfs = []  
columns = ['name', 'address', 'type', 'source', 'lat', 'lng', 'geom']

for file_name in get_files(manual_input_path, '.csv'):
    file_path = os.path.join(manual_input_path, file_name)
    df = pd.read_csv(file_path)

    point_geom = [Point(xy) for xy in zip(df['lng'], df['lat'])]
    gdf = gpd.GeoDataFrame(df, geometry=point_geom, crs='EPSG:4326')

    manual_dfs.append(gdf)

combined_manual_dfs = pd.concat(manual_dfs, ignore_index=True)
combined_manual_dfs = combined_manual_dfs.rename(columns={
    'geometry': 'geom'
})
combined_manual_dfs = combined_manual_dfs[columns]
combined_manual_dfs.to_csv(manual_output_path, index=False)