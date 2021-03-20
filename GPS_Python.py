#!/usr/bin/python
"""
Title: GPS_Python.py
Date: 2021-03-20
Author: Virág Varga

Description:
	This program takes 3 input files (a file containing genetic-geographical association
		data for test individuals, a dataset giving the geographical locations of a variety
		of sample populations, and a file containing genetic-geographical association data
		for sample populations), and outputs a file predicting the geographical origins of
		the test individuals.
	The results file is in .txt format, and can be used as input for the CSV_Conversion.py file,
		in order to produce a file formatted in such a way as to be mapped in QGIS.

Citation Note:
This program is a derivative work.
The GPS_Python.py script is a translation into Python from R of the GPS.r script
	found at https://github.com/homologus/GPS/blob/master/GPS.r written by Homolog.us
	(@homologus on GitHub: https://github.com/homologus).
The larger GPS program, which includes more than the GPS.r script, can be found at
	https://github.com/homologus/GPS.
Program Citation:
	Homolog.us (2017, November 14). homologus/gps. Retrieved March 8, 2021, from https://github.com/homologus/GPS

List of Functions:
	GPS

List of Standard & Non-Standard Modules:
	sys
	numpy
	pandas
	sklearn

Procedure:
	1. Necessary modules are loaded, including the sklearn objects that will be used to
		calculate the Euclidian Distance Matrix and Linear Regression. The inputs and
		output are defined.
	2. The GPS function is defined. Within the function, the following processes occur:
		a. Input files are opened with Pandas.
		b. The Euclidian Distance Matrices and Linear Regression are calculated with sklearn.
		c. The contents of the 3 input files are parsed in order to create the results file.
	3. The program is executed.

Input & Output Files:
	There are 3 input files necessary for this program to run, all in .csv format. Details
		about the formatting and contents of these files are described below:
	- data_file: This is the file containing genetic-geographical association data for test
		individuals. It contains sample ids, geographical-genetic association data, and a
		population group assignment.
		Its column formatting is as follows:
		SAMPLE_ID, NORTHEASTASIAN, MEDITERRANIAN, SOUTHAFRICA, SOUTHWESTASIAN, NATIVEAMERICAN,
		OCEANIAN, SOUTHEASTASIA, NORTHERNEUROPEAN, SUBSAHARANAFRICA, GROUP_ID
	- geo_file: This file contains the geographical locations of various sample populations.
		Its column formatting is as follows:
		POPULATION, Lat, Long
	- gen_file: This file contains genetic-geographical association data for a variety of sampled
		populations. This file does not contain headers, but its contents align with the genetic-
		geographical associations columns present in the data_file, preceded by a column containing
		the sample group ids.
	The output file contains the results of the file parsing accomplished in this program. It is
		a .txt file, and its contents are found under the following column names:
		Population, Sample_no, Sample_id, Prediction, Lat, Lon
	To download sample files and test the program, please visit the website of the original program,
		linked above in the Citation Note section.

Known Bugs & Limitations:
	- The input files have to look exactly as described above, and be in the order listed in
		the usage instructions below. Any deviation will cause either program failure or unusable
		results.
	- No error-checking has been integrated into this program: it is up to the user to unsure the
		correct files and file formats are provided to the program, and the determine which file(s)
		is/are causing an issue if the program does not run.
	- The quality of the geographical predictions is limited by the diversity of the population and
		group data provided. The greater the diversity of the input data, the more accurate the
		predictions will be.
	- The name assigned to the output file is pre-determined, and can only be changed from within
		the script.
	- The user may encounter the following error message:
		".\GPS_Python.py:216: RuntimeWarning: invalid value encountered in true_divide
  			W = (minE[0]/minE)**4"
		This error message can be safely ignored - the program will complete running not much later.
		

Usage:
	./GPS_Python.py data_file geo_file gen_file
	OR
	python GPS_Python.py data_file geo_file gen_file

This script was written with Python 3.8.6 in Spyder 4.
"""

#import necessary modules
#sys allows command-line specification of input files
import sys
#numpy allows manipulation of arrays and mathematical operations
import numpy as np
#pandas allows manipulation of dataframes
import pandas as pd

#necesary sklearn functions are imported below:
#Euclidian Distance Matrix calculator from the sklearn module
from sklearn.neighbors import DistanceMetric
dist = DistanceMetric.get_metric('euclidean')

'''
Note:
	There is some minor discrepancy of the latitude and longitude coordinates calculated in this
		Python program, vs. the original program written in R. This has been determined to be due
		to the usage of the sklearn module in order to calculate the Euclidian Distance Matices.
	The `dist()` command accomplishes this task in R, but the sklearn module's DistanceMetric
		command actually calculates the values in the distance matrices to a higher number of
		decimal places. The succeeding mathematical operations (which include transformation via
		the use of exponents), cause these originally quite small deviations to become noticable
		in the final output of the program.
'''

#Linear Regression calculator from the sklearn module
from sklearn import linear_model
regressor = linear_model.LinearRegression()


#defining inputs & outputs
#the inputs are user-defined from the command line
data_file = sys.argv[1]
geo_file = sys.argv[2]
gen_file = sys.argv[3]
#the output file has a pre-determined name
output_file = "GPS_Py_results.txt"


#defining the GPS function
def GPS(output_file, data_file, geo_file, gen_file):
	#open the necessary files
	with open(data_file, "r") as fname, open(geo_file, "r"), open(gen_file, "r"), open(output_file, "w") as outfile:
		#start by reading in the csv files with pandas
		#after the files are opened, the first column of each is set as the index
		#(the pythonic equivalent of a row name)
		GEO = pd.read_csv(geo_file)
		GEO.set_index("POPULATION", inplace = True)
		GEN = pd.read_csv(gen_file, header=None)
		GEN = GEN.set_index(0)
		TRAINING_DATA = pd.read_csv(fname)
		TRAINING_DATA = TRAINING_DATA.set_index("SAMPLE_ID")

		#euclidian distance matrices are calculated
		#the resulting matrices have to be rearranged with numpy
		#in order to be used in successive operations
		y = dist.pairwise(GEO)
		y = np.array(y).reshape(-1, 1)
		x = dist.pairwise(GEN)
		x = np.array(x).reshape(-1, 1)

		#if the distance is too large or too small, it is set to 0
		for l, v in enumerate(y):
			if y[l] >= 70 or x[l] >= 0.8:
				y[l] = 0
				x[l] = 0

		#compute linear regression between x and y
		eq1 = regressor.fit(x, y)

		#loop over various groups in training data
		#to derive latitude and longitude of unknown sample

		#extract the genetic-geographic association data from the data_file
		TRAINING_DATA.iloc[:, 1:9] = TRAINING_DATA.iloc[:, 1:9].apply(pd.to_numeric, errors='coerce')
		#isolate the unique population groups
		GROUPS = TRAINING_DATA.GROUP_ID.unique()
		#write the header line for the results file
		outfile.write("Population" + "\t" + "Sample_no" + "\t" + "Sample_id" + "\t" + "Prediction" + "\t" + "Lat" + "\t" + "Lon" + "\n")
		#create size-determining variable for choosing best-matching genetic data
		N_best = 10
		N_best = min(N_best, len(GEO[["Lat"]]))
		#loop through the data file according to the population groups
		for GROUP in GROUPS:
			#create subset of data_file based on the examined population group
			Y = TRAINING_DATA.loc[TRAINING_DATA["GROUP_ID"] == GROUP]
			#loop through the members of the group, row by row
			for m, a in enumerate(Y.index):
				#variable X contains the genetic-geographic association data columns from dataframe Y
				X = Y.loc[[a]]
				X = X.iloc[:, 0:9]
				#array E will contain Euclidian distance values
				#comparing the data_file values with the values in the gen_file
				E = np.array([0])
				E = np.repeat(E, len(GEO[["Lat"]]), axis = 0)
				E = E.astype(float)
				#loop through the geo_file
				for n, g in enumerate(GEO.Lat):
					#variable ethnic contains the populations from the geo_file
					ethnic = GEO.index.values[n]
					#variable gene contains the genetic-geographic association data for variable ethnic
					gene = GEN.loc[[ethnic], 1:9]
					#the next two lines combine dataframes gene & X
					#in order to be able to perform mathematical manipulations of their contents
					gene_col = pd.DataFrame(data = gene.values, columns = X.columns)
					geneConcat = pd.concat([gene_col, X])
					#calculating the values to be used in E
					E[n] = np.sqrt(sum(geneConcat.iloc[0].subtract(geneConcat.iloc[1])**2))
				#variable minE contains the lowest values from array E
				minE = []
				minE = sorted(E)[:N_best]
				#variable minG will index the rows with the most best-matching populations
				#in the geo_file, based on minE and E
				minG = []
				minG = np.array([0])
				minG = np.repeat(minG, N_best, axis = 0)
				#loop through the geo_file, and populate minG
				for n, g in enumerate(GEO.Lat):
					for j in range(0, N_best):
						if minE[j] == E[n]:
							minG[j] = n
				#get the corresponding best values from E, based on minG indexes
				radius = E[minG]
				#get the populations from the GEO file, based on the minG indexing
				best_ethnic = GEO.index.values[minG]
				#apply the linear model
				radius_geo = eq1.coef_*radius[0]
				#variable W is a measure of relatedness
				W = (minE[0]/minE)**4
				W = W/sum(W)
				#get the latitute and longitude origins for each individual
				#make adjustments to the values using radius_geo and W
				latList = GEO.iloc[minG, GEO.columns.get_loc('Lat')].tolist()
				subLat = GEO.iloc[minG, GEO.columns.get_loc('Lat')].tolist()[0]
				delta_lat = [x - subLat for x in latList]
				delta_lat = [round(f, 3) for f in delta_lat]
				lonList = GEO.iloc[minG, GEO.columns.get_loc('Long')].tolist()
				subLon = GEO.iloc[minG, GEO.columns.get_loc('Long')].tolist()[0]
				delta_lon = [x - subLon for x in lonList]
				delta_lon = [round(f, 3) for f in delta_lon]
				new_lon = sum(W*delta_lon)
				new_lat = sum(W*delta_lat)
				lo1 = new_lon*min(1, (radius_geo/np.sqrt((new_lon**2)+(new_lon**2))))
				la1 = new_lat*min(1, (radius_geo/np.sqrt((new_lat**2)+(new_lat**2))))

				#reformat some data for the output
				lat_print = str(GEO.iloc[minG[0]].tolist()[1] + la1)
				lat_print = lat_print.replace('[', '').replace(']', '')
				long_print = str(GEO.iloc[minG[0]].tolist()[0] + lo1)
				long_print = long_print.replace('[', '').replace(']', '')
				#write the results to the output file
				outfile.write(GROUP + "\t" + str(m+1) + "\t" + a + "\t" + best_ethnic[0] + "\t" + long_print + "\t" + lat_print + "\n")

	print("Done!")


GPS(output_file, data_file, geo_file, gen_file)
