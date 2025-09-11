import logging

from datetime import datetime

logging.basicConfig(level=logging.INFO)


def vector_bbox_and_footprint(src):
    """Read properties from a Geodataframe view"""
    pass


def shp_timestamp(src):
    """With luck, we can read a last update data from DBF metadata"""
    tags = src.tags()
    dt = None
    if "DBF_DATE_LAST_UPDATE" in tags:
        # TODO this with more structure
        d = tags["DBF_DATE_LAST_UPDATE"].split("-")
        if len(d) >= 3:
            dt = datetime(d[0], d[1], d[2])
    return dt
