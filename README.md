# README.md


## GPS Origin Determination & Mapping

Author: Virág Varga

Date: 20.03.2021


## Description

The largest script in this program (GPS_Python.py) parses three input files in order to determine the likely genetic origins of individuals whose genetic-geographic information has been provided.

The results file can then be reformatted with the use of the CSV_Conversion.py script, in order to prepare the data for mapping in QGIS (Quantum Geographic Information System).

Finally, a series of 3 small scripts has been written (gen_vector.py, basemap.py, and reorder_layers.py) in order to map the data within the PyQGIS Python plugin for the QGIS program.


## References

This program is a derivative work. The largest piece of code present in this project is the GPS_Python.py program, which is a translation into Python from R of the GPS.r script found [here](https://github.com/homologus/GPS/blob/master/GPS.r "GPS.r") written by [Homolog.us](https://github.com/homologus "@homologus"). The larger GPS program can be found [here](https://github.com/homologus/GPS "GPS").

Homolog.us (2017, November 14). homologus/gps. Retrieved March 8, 2021, from https://github.com/homologus/GPS

The GPS program was created to analyze data for the following article:

Elhaik, E., Tatarinova, T., Chebotarev, D., Piras, I. S., Calò, C. M., De Montis, A., Atzori, M., Marini, M., Tofanelli, S., Francalacci, P., Pagani, L., Tyler-Smith, C., Xue, Y., Cucca, F., Schurr, T. G., Gaieski, J. B., Melendez, C., Vilar, M. G., Owings, A. C., … Ziegle, J. S. (2014). Geographic population structure analysis of worldwide human populations infers their biogeographical origins. _Nature Communications_, 5(1), 1–13. https://doi.org/10.1038/ncomms4513

The article can be found [here](https://www.nature.com/articles/ncomms4513 "Geographic population structure analysis of worldwide human populations infers their biogeographical origins").


## Usage

### Step 0: Program and Module Installation

#### Python Library: Pandas

Pandas is Python library built to facilitate the handling of dataframes within Python. Its website can be found [here](pandas.pydata.org "Pandas Library Homepage").

Detailed instructions for the installation of Pandas can be found [here](https://pandas.pydata.org/getting_started.html "Pandas Installation Instructions"). If `conda` is installed on the user's computer, pandas can be installed as follows:

```bash
conda install -c anaconda pandas
```

#### Python Library: Scikit-learn

Scikit-learn is a Python library built to perform various scientific tests on datasets in Python. In scripts it is referred to as the `sklearn` module. Its website can be found [here](https://scikit-learn.org/stable/ "Scikit-learn/sklearn Library Homepage").

Detailed instructions for the installation of Scikit-learn can be found [here](https://scikit-learn.org/stable/install.html "Scikit-learn Installation Instructions"). If `conda` is installed on the user's computer, Scikit-learn can be installed as follows:

```bash
conda install -c conda-forge scikit-learn
```

#### Python Library: Numpy

Numpy is a Python library used for expanding the sorts of mathematical calculations that can be performed in a Python script. Its website can be found [here](https://numpy.org/ "Numpy Homepage").

Detailed instructions for the installation of Numpy can be found [here](https://numpy.org/install/ "Numpy Installation Instructions"). If `conda` is installed on the user's computer, pandas can be installed as follows:

```bash
conda install -c anaconda numpy
```

#### QGIS

Quantum Geographic Information System (QGIS) is a free and open source GIS mapping software available from the QGIS Project website, [here](https://qgis.org/en/site/ "QGIS Homepage"). Installation instructions can be found [here](https://qgis.org/en/site/forusers/download.html "QGIS Installation").


### Step 1: Data parsing & production with GPS_Python.py

This program takes 3 input files (a file containing genetic-geographical association
  data for test individuals, a dataset giving the geographical locations of a variety
  of sample populations, and a file containing genetic-geographical association data
  for sample populations), and outputs a file predicting the geographical origins of
  the test individuals.
The results file is in .txt format, and can be used as input for the CSV_Conversion.py file,
  in order to produce a file formatted in such a way as to be mapped in QGIS.

#### Input Files

There are 3 input files necessary for this program to run, all in .csv format. Details about the formatting and contents of these files are described below:
 - data_file: This is the file containing genetic-geographical association data for test individuals. It contains sample ids, geographical-genetic association data, and a population group assignment. Its column formatting is as follows:

```text
SAMPLE_ID, NORTHEASTASIAN, MEDITERRANIAN, SOUTHAFRICA, SOUTHWESTASIAN,
NATIVEAMERICAN, OCEANIAN, SOUTHEASTASIA, NORTHERNEUROPEAN, SUBSAHARANAFRICA,
GROUP_ID
```

 - geo_file: This file contains the geographical locations of various sample populations. Its column formatting is as follows:

```text
POPULATION, Lat, Long
```

 - gen_file: This file contains genetic-geographical association data for a variety of sampled populations. This file does not contain headers, but its contents align with the genetic-geographical associations columns present in the data_file, preceded by a column containing the sample group ids.

Samples files to test the program are provided in the Sample_Files folder. In order to test the program with the original data it was written for, please visit the website of the original program, linked above in the Citation Note section.

#### Running the Script

The GPS_Python.py script can be run from the command line as follows:

```bash
./GPS_Python.py data_file geo_file gen_file
#OR
python GPS_Python.py data_file geo_file gen_file
```

#### Results

The output file contains the results of the file parsing accomplished in this program. It is a .txt file, and its contents are found under the following column names:

```text
Population, Sample_no, Sample_id, Prediction, Lat, Lon
```


### Step 2: Data reformatting with CSV_Conversion.py

This program converts the output results file from the GPS_Python.py program (GPS_Py_results.txt) into .csv format for use in plotting of data in QGIS. Specific columns are extracted and reordered, new headers are created, and the resulting dataframe is written out to a .csv file for mapping in QGIS.

#### Input File

The output file from Step 1 (GPS_Py_results.txt) should be used as the input file for this stage of the analysis.

#### Running the Script

This script can be run from the command line as follows:

```bash
./CSV_Conversion.py results_file
#OR
python CSV_Conversion.py results_file
```

#### Results

The resulting file is named GPS_Coordinates.csv, and is appropriately formatted for mapping in QGIS.


### Step 3: Mapping in QGIS

#### Input File

The output of the CSV_Conversion.py script (GPS_Coordinates.csv) should be used

#### Running the Scripts

After opening QGIS, hover over the "Plugins" dropdown menu along the top of the screen. Select the "Python Console" option, and the PyQGIS Python plugin console will open. Next, click the "Show Editor" button, and then the "Open Script..." option. Open the three PyQGIS mapping script here.

Begin by editing the gen_vector.py script file to include the correct path to the GPS_Coordinates.csv file on the user's computer. Then select "Run". A project does not already need to be open in order for the script to run. Points should appear on a blank white backdrop. The GeneticOrigins vector layer mapping the genetic-geographic data has been created.

Next, run the basemap.py script. This will add the OpenStreetMap background layer. The plotted points will disappear at this stage, as new layers are automatically placed on top of the previous.

Finally, run the reorder_layers.py script. This place the basemap on the bottom, and the GeneticOrigins layer on the top. The coordinates may look to be inaccurately positioned, but this is not cause for concern. Viewing the entire 2-Dimensional projection of the globe can cause distortions in the way coordinates are displayed; zooming in slightly (with ex. scrolling with a mouse or mousepad) will fix this issue. 

At this stage, the user is free to explore the map and data, and export whichever portion(s) of the map they wish, using the QGIS GUI.

Note: The gen_vector.py script must be run before the basemap.py script. Creating the basemap before plotting the data layer will result in inaccurate projections. While it may seem like more work, it produces far better results to map the genetic-geographic data as a vector layer first, and then to map the OpenStreetMap raster layer on top of it. The vector layer provides points of reference, of a sort, to ensure accurate mapping of the raster layer.

#### Results

The results produced will vary depending on the dataset, and which portions of the map the user wishes to export. The example image below shows the mapping completed on the data from the original GPS program, which can be found [here](https://github.com/homologus/GPS/tree/master/GPS-original-code "GPS Original Input Data").

The example map below was created using the data for which the original [GPS](https://github.com/homologus/GPS "GPS") program was created, ie. Elhaik et al. 2014.

![Example Map](Results/GenMap_East.png)

## Support

With questions, please contact the author of this program at:

virag.varga.bioinfo@gmail.com

### Software Versions:

For additional clarity and quality-checking, please note below are the versions of all software used in this analysis:
 - Python: 3.8.6
   - Numpy: 1.20.1
   - Pandas: 1.2.1
   - Scikit-learn (called in scripts as `sklearn`): 0.24.1
 - QGIS: 3.18.0 (Zürich)
   - PyQGIS plugin utilizes Python 3.7.0
 - Spyder: 4.2.3


## Project Status

Current Version: 1.0

While I have no explicit plans for a timeline to continue development of this program, I may eventually return to accomplish the following tasks:
 - Work out some of the known bugs and limitations
 - Add input error- and quality-checking functionality
 - Add help messages to the Python scripts
 - Combine the PyQGIS Python scripts into one script
 - Work out a script to allow differential coloration of the symbols representing the mapped populations, based on group affinity


## License

[MIT](https://choosealicense.com/licenses/mit/)
