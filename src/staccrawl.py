import json
import logging
import rasterio
import pystac

from datetime import datetime
from shapely.geometry import Polygon, mapping
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)

load_dotenv()


class CatalogError(rasterio.errors.RasterioIOError):
    pass


def catalog():
    # TODO read existing
    return pystac.Catalog(
        id="mambo-drone-shrubs",
        description="Demonstration for MAMBO WP4 data access from s3.",
    )


def raster_bbox_and_footprint(raster):
    """Accept an s3 URL and read metadata"""
    bbox = footprint = None
    try:
        with rasterio.open(raster) as r:
            bounds = r.bounds
            bbox = [bounds.left, bounds.bottom, bounds.right, bounds.top]
            footprint = Polygon(
                [
                    [bounds.left, bounds.bottom],
                    [bounds.left, bounds.top],
                    [bounds.right, bounds.top],
                    [bounds.right, bounds.bottom],
                ]
            )
    except rasterio.errors.RasterioIOError as err:
        logging.error(err)

    if footprint:
        footprint = mapping(footprint)
    return (bbox, footprint)


def stac_item(url, catalog, default_date=datetime(2024, 8, 18)):
    bbox, footprint = raster_bbox_and_footprint(url)
    # question about temporal metadata preservation
    # For now, safely assume only a known year
    # Item api rigidly expects a datetime with tzinfo method
    item = pystac.Item(
        id=url, geometry=footprint, bbox=bbox, datetime=default_date, properties={}
    )

    print(json.dumps(item.to_dict(), indent=4))

    catalog.add_item(item)

    print(json.dumps(catalog.to_dict(), indent=4))


if __name__ == "__main__":
    # test image
    url = "s3://shrub-prepro/input/Strawberry_ortho_27700.tif"
    c = catalog()
    stac_item(url, c)
