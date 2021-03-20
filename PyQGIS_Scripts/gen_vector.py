#!/usr/bin/python
"""
Title: gen_vector.py
Date: 2021-03-20
Author: Virág Varga

Description:
    This program loads the genetic data .csv file output from the CSV_Conversion.py script
        as a delimited layer in QGIS. After it is imported, the layer will be handled by QGIS
        as a vector layer.
    This is Step 1 of the QGIS map construction pipeline.
    Use of this script should be followed by use of the basemap.py script.

Procedure & Usage:
    1. After opening the PyQGIS plugin within QGIS, open this script.
    2. Alter this script to give the full file path for the GPS_Coordinates.csv
        available on the user's computer.
    3. Run the script within PyQGIS.

This script was written within the PyQGIS plugin in QGIS 3.18.0 (Zürich), which utilizes
    Python 3.7.0.
"""

#loading the genetic information layer
uri='file:///INSERT/USER/FILE/PATH/HERE/GPS_Coordinates.csv?delimiter=,&yField=Northing&xField=Easting'
layer = QgsVectorLayer(uri, 'GeneticOrigins', 'delimitedtext')

#check that the layer is valid; if so, create the map
if not layer.isValid():
    print("Layer failed to load!")
else:
    QgsProject.instance().addMapLayer(layer)
