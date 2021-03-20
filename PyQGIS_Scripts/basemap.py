#!/usr/bin/python
"""
Title: basemap.py
Date: 2021-03-20
Author: Virág Varga

Description:
    This program loads the basemap, which in this case is the QGIS inbuilt OpenStreetMap.
    This is Step 2 of the QGIS map construction pipeline.
    Use of this script should be followed by use of the reorder_layers.py script.

Procedure & Usage:
    1. Open this script in the PyQGIS plugin in QGIS.
    2. After running the gen_vector.py script, run this script similarly in the QGIS Python
        plugin console.

This script was written within the PyQGIS plugin in QGIS 3.18.0 (Zürich), which utilizes
    Python 3.7.0.
"""

#add OpenStreetMap, using the PyQGIS Cookbook suggestions

#create a function to complete the mapping
def loadXYZ(url, name):
    #XYZ tile layers and map layers like the OpenStreetMap are interpreted as raster layers
    rasterLyr = QgsRasterLayer("type=xyz&url=" + url, name, "wms")
    QgsProject.instance().addMapLayer(rasterLyr)

#give the URL for the map source
urlWithParams = 'https://tile.openstreetmap.org/%7Bz%7D/%7Bx%7D/%7By%7D.png&zmax=19&zmin=0&crs=EPSG3857'
loadXYZ(urlWithParams, 'OpenStreetMap')
