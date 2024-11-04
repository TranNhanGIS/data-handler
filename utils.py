from shapely import wkb, Point
import pandas as pd
import os

# Convert WKB Hexadecimal in the 'geom' field
def convert_wkb_to_lat_lng(geom_hex):
    geometry = wkb.loads(bytes.fromhex(geom_hex))
    if geometry.geom_type != 'Point':
        point = geometry.centroid
    else:
        point = geometry

    if point is not None and hasattr(point, 'x') and hasattr(point, 'y'):
        return pd.Series({'lat': point.y, 'lng': point.x})
    else:
        return pd.Series({'lat': None, 'lng': None})
    
# Create WKB from lat, lng
def create_wkb_from_lat_lng(lat, lng):
    point = Point(lng, lat)
    return wkb.dumps(point, hex=True)
    
# Get files from directory
def get_files(directory, extension):
    files = [f for f in os.listdir(directory) if f.endswith(extension)]
    return files