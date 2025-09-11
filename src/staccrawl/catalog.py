import json
import logging
import rasterio
import pystac

from datetime import datetime
from dotenv import load_dotenv
from staccrawl.raster import raster_bbox_and_footprint

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
