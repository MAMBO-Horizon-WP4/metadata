import os
import json
import rasterio
import urllib.request
import pystac

from datetime import datetime, timezone
from shapely.geometry import Polygon, mapping
from tempfile import TemporaryDirectory
from dotenv import load_dotenv
load_dotenv()
def catalog():
    # TODO read existing
    return pystac.Catalog(id='mambo-drone-shrubs', description='Demonstration for MAMBO WP4 data access from s3.')

def raster_bbox_and_footprint(raster):
    """Accept an s3 URL and read metadata"""
    with rasterio.open(raster) as r:
        bounds = r.bounds
        bbox = [bounds.left, bounds.bottom, bounds.right, bounds.top]
        footprint = Polygon([
            [bounds.left, bounds.bottom],
            [bounds.left, bounds.top],
            [bounds.right, bounds.top],
            [bounds.right, bounds.bottom]
        ])
        
        return (bbox, mapping(footprint))

def stac_item(url, catalog):
    bbox, footprint = raster_bbox_and_footprint(url)
    # question about temporal metadata preservation
    datetime_utc = datetime.now(tz=timezone.utc) 
    item = pystac.Item(id=url,
                 geometry=footprint,
                 bbox=bbox,
                 datetime=datetime_utc,
                 properties={})
    print(json.dumps(item.to_dict(), indent=4))

    catalog.add_item(item)
        
    print(json.dumps(catalog.to_dict(), indent=4))

if __name__ == '__main__':

    # test image
    url = 's3://shrub-prepro/input/Strawberry_ortho_27700.tif'
    c = catalog()
    stac_item(url, c)
