import logging
import rasterio

from shapely.geometry import Polygon, mapping


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
