from shpgeo import *

cwd = os.getcwd()
# a = splitname("2015_06_21_11D.shp")
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


#merge shapefiles
numfiles = len(shapelist)

#merge first two files in the list
i=0
mergedshp = mergeshp(shapelist[i],shapelist[i+1], i)
i += 2

#merge the rest
while i<numfiles:
	mergedshp = mergeshp(mergedshp, shapelist[i], i)
	i += 1
print("Shapefiles merged")




#export to geojson
# exporttogjson(mergedshp, mergedshp[:-4] + ".geojson")

# print("Export to geojson successful")
