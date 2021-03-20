#!/usr/bin/python
"""
Title: reorder_layers.py
Date: 2021-03-20
Author: Virág Varga

Description:
    This program reorders the GeneticOrigins and OpenStreetMap layers, in order to put
        the GeneticOrigins layer (which contains the imported .csv data) on top of the
        basemap.
    This is Step 3 of the QGIS map construction pipeline.
    After use of this script, the user can perform further analyses of their choosing within
        QGIS, or zoom to the desired level and export the created map.

Procedure & Usage:
    1. Open this script in the PyQGIS plugin in QGIS.
    2. After running the basemap.py script, run this script similarly in the QGIS Python
        plugin console.

This script was written within the PyQGIS plugin in QGIS 3.18.0 (Zürich), which utilizes
    Python 3.7.0.
"""

#reorder layers to put the genetic data layer on top

#define layer variables
#variable alayer contains the GeneticOrigins data layer
alayer = QgsProject.instance().mapLayersByName("GeneticOrigins")[0]
#variable root contains the OpenStreetMap basemap
root = QgsProject.instance().layerTreeRoot()

#move the GeneticOrigins layer to the top
#this is accomplished by creating a clone of the basemap layer and inserting it in the desired position
#the original layer is then deleted
myalayer = root.findLayer(alayer.id())
myClone = myalayer.clone()
parent = myalayer.parent()
parent.insertChildNode(0, myClone)
parent.removeChildNode(myalayer)
