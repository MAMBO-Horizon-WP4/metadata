import logging
import geopandas as gpd
from datetime import datetime
from shapely.geometry import mapping, box
import fiona

logging.basicConfig(level=logging.INFO)


def vector_bbox_and_footprint(url):
    """Read properties from a Geodataframe view"""
    bbox = footprint = None
    try:
        with gpd.read_file(url) as src:
            bbox = list(src.total_bounds)
            footprint = box(*bbox)
    except Exception as err:  # probably a pyogrio.errors.DataSourceError
        logging.error(err)

    if footprint:
        footprint = mapping(footprint)
    return (bbox, footprint)


def shp_timestamp(url):
    """With luck, we can read a last update data from DBF metadata"""
    dt = None
    with fiona.open(url) as src:
        tags = src.tags()
        if "DBF_DATE_LAST_UPDATE" in tags:
            # TODO this with more structure
            d = tags["DBF_DATE_LAST_UPDATE"].split("-")
            if len(d) >= 3:
                dt = datetime(d[0], d[1], d[2])
    return dt
