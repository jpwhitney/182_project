from shpgeo import *
from vector import *
import ogr2ogr
import os
cwd = os.getcwd()
# print a
fieldnames = ['Site', 'Treatment',  'Day', 'Month', 'Year']
#get the list of shapefiles in cwd
shapelist = getshp(cwd)
layerlist = openlist(shapelist)
layerdict = dict(zip(shapelist, layerlist))

#add fields and values from filename
for layer in layerdict:
	valuedict = splitname(layer, fieldnames)
	addfields(layer, valuedict)
	addfeaturearea(layer, 'Area')
	addfieldpercent(layer,'Area', 'Percent')

print("Fields and Values added")


mergeSpatialFiles(shapelist, 'mergedshp.shp', 'ESRI Shapefile')

print("Shapefiles merged")

ogr2ogr.main(["","-f", "GeoJSON", "out.geojson", "mergedshp.shp"])


print("Export to geojson successful")
