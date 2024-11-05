import os
import pandas as pd
import geopandas as gpd
from shapely import Point
from utils import get_files, convert_wkb_to_lat_lng

OSM_input_path = 'input/OSM'
OSM_output_path = 'output/OSM/output.csv'
OSM_dfs = []  
columns = ['name', 'address', 'type', 'source', 'lat', 'lng', 'geom']

for file_name in get_files(OSM_input_path, '.csv'):
    file_path = os.path.join(OSM_input_path, file_name)
    df = pd.read_csv(file_path, dtype={'type': str}, low_memory=False)

    df['name'] = df['name'].fillna(df['name_en'])
    df['address'] = ''
    df['source'] = 'OSM'
    
    lat_lng_df = df['geometry'].apply(convert_wkb_to_lat_lng)
    df = pd.concat([df, lat_lng_df], axis=1)
    
    point_geom = [Point(xy) for xy in zip(df['lng'], df['lat'])]
    gdf = gpd.GeoDataFrame(df, geometry=point_geom, crs='EPSG:4326')

    prov_gdf = gpd.read_file('input/base/vn_provinces.shp')

    if gdf.crs != prov_gdf.crs:
        gdf = gdf.to_crs(prov_gdf.crs)

    df = gpd.overlay(gdf, prov_gdf, how='intersection')
    OSM_dfs.append(df)

combined_OSM_dfs = pd.concat(OSM_dfs, ignore_index=True)
combined_OSM_dfs = combined_OSM_dfs.rename(columns={
    'name_1': 'name',
    'geometry': 'geom'
})
combined_OSM_dfs = combined_OSM_dfs[columns]
combined_OSM_dfs.to_csv(OSM_output_path, index=False)

for type_value, group in combined_OSM_dfs.groupby('type'):
    type_value = type_value.replace("/", "-")
    group.to_csv(f'output/osm/layers/{type_value}.csv', index=False)
