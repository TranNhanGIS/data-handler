from shapely import wkb, Point
import pandas as pd
import math
import os

# Convert WKB Hexadecimal in the 'geom' field
def convert_wkb_to_lat_lng(geom_hex):
    geometry = wkb.loads(bytes.fromhex(geom_hex))
    if geometry.geom_type != 'Point':
        point = geometry.centroid
    else:
        point = geometry

    if not point.is_empty and hasattr(point, 'x') and hasattr(point, 'y'):
        return pd.Series({'lat': round(point.y, 6), 'lng': round(point.x, 6)})
    else:
        return pd.Series({'lat': None, 'lng': None})
    
# Get files from directory
def get_files(directory, extension):
    files = [f for f in os.listdir(directory) if f.endswith(extension)]
    return files