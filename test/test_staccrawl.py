import pystac
from staccrawl.catalog import catalog, stac_item


def test_catalog():
    c = catalog()
    assert isinstance(c, pystac.Catalog)


def test_raster_bbox_and_footprint(raster):
    pass


def test_stac_item(url):
    c = catalog()
    stac_item(url, c)
