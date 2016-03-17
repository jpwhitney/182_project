from shpgeo import *
from vector import *
import ogr2ogr
import os
cwd = os.getcwd()

#Define fieldnames
fieldnames = ['Site', 'Treatment',  'Day', 'Month', 'Year']

#get the list of shapefiles in cwd
shapelist = getshp(cwd)

#code not used yet, but it could at some#
#point be useful to pass layer objects#
#open the files as layer objects
#layerlist = openlist(shapelist)

#make a dict from the filenames and the layer objects
#layerdict = dict(zip(shapelist, layerlist))

#add fields and values from filename
for layer in shapelist:
	valuedict = splitname(layer, fieldnames)
	addfields(layer, valuedict)
	addfeaturearea(layer, 'Area')
	addfieldpercent(layer,'Area', 'Percent')

print("Fields and Values added")

#merge files into a single .shp file using method in vector.py
mergeSpatialFiles(shapelist, 'mergedshp.shp', 'ESRI Shapefile')

print("Shapefiles merged")

#convert merged .shp file into a .geojson file
ogr2ogr.main(["","-f", "GeoJSON", "out.geojson", "mergedshp.shp"])


print("Export to geojson successful")
