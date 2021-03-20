#!/usr/bin/python
"""
Title: CSV_Conversion.py
Date: 2021-03-20
Author: Virág Varga

Description:
	This program converts the output results file from the GPS_Python.py program
		(GPS_Py_results.txt) into .csv format for use in plotting of data in QGIS.
	The resulting file is named GPS_Coordinates.csv.

List of Functions:
	No author-defined functions are included in this script.

List of Standard & Non-Standard Modules:
	sys
	pandas

Procedure:
	1. Modules and input data file loaded.
	2. The input data file is opened with pandas. Relevant data columns are extracted into a
		new dataframe, with a new header line.
	3. The new dataframe is printed to a .csv file.

Known Bugs & Limitations:
	This program is intended for use on the results file output by the GPS_Python.py file.
		Input results files with different formatting will not be accepted.
	No error-checking is integrated into this program. It is therefore on the user to ensure
		that the input data file is in the correct format.
	The name of the output file is pre-defined as GPS_Coordinates.csv. If the user wishes to
		use a different name, they must either edit the script or change the file name after
		the file has been created.

Usage:
	./CSV_Conversion.py results_file
	OR
	python CSV_Conversion.py results_file

This script was written with Python 3.8.6 in Spyder 4.
"""

#Import necessary modules
import sys
import pandas as pd


#Define inputs and outputs
input_data = sys.argv[1]
csv_coordinates = "GPS_Coordinates.csv"


#Create CSV coordinates file from GPS results file
with open(input_data, "r"), open(csv_coordinates, "w") as outfile:
	#opening the coordinates data file with pandas
	Data = pd.read_csv(input_data, sep='\t')
	#extracting relevant data columns into a new dataframe, CoordData
	CoordData = [Data["Sample_id"], Data["Lon"], Data["Lat"], Data["Population"], Data["Prediction"]]
	#creating new headers for the columns
	headers = ["Sample_ID", "Easting", "Northing", "Population", "Prediction"]
	#concatenating the contents of the CoordData dataframe with the headers in the GPS_Coord dataframe
	GPS_Coord = pd.concat(CoordData, axis=1, keys=headers)
	#printing the GPS_Coord dataframe to the output .csv file
	GPS_Coord.to_csv(outfile, index=False, line_terminator='\n')
