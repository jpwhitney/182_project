import os
import ogr
from vector import *
def getshp(path):
	shapeList = []
	for file in os.listdir(path):
		if file.endswith(".shp"):
			shapeList.append(file)
	return shapeList

def openlist(shapelist):
	driver = ogr.GetDriverByName('ESRI Shapefile')
	layerlist = []
	for shapefile in shapelist:
		dataSource = driver.Open(shapefile, 1)
		layer = dataSource.GetLayer
		layerlist.append(layer)
	return layerlist


def splitname(filename, fieldnames):
	st = filename
	st = st[:-4]
	begin = st[:-1]
	last = st[-1:]
	l = begin.split("_")
	l.extend(last)
	l.reverse()
	c = fieldnames
	z = dict(zip(c,l))
	return z


def addfields(shapefilename, fieldNames):

	shape = shapefilename
	driver = ogr.GetDriverByName('ESRI Shapefile')
	dataSource = driver.Open(shape, 1) #1 is read/write
	layer = dataSource.GetLayer()

	#define  fields
	for field in fieldNames:
		fldDef1 = ogr.FieldDefn(field, ogr.OFTString)
		fldDef1.SetWidth(16) #16 char string width
		layer.CreateField(fldDef1)


	# add values
	for fieldName in fieldNames:
		for fid in range(layer.GetFeatureCount()):
			feature = layer.GetFeature(fid)
			feature.SetField(fieldName, fieldNames[fieldName])
			layer.SetFeature(feature)



def addfeaturearea(filePath, newFieldName, driverName = 'ESRI Shapefile'):
	"""
	Finds the difference between two fields and adds that to the spatial file
	:param filePath: String. Path to existing spatial file
	:param driverName: String. Type of spatial file (eg, 'ESRI Shapefile', 'OSM', 'GeoJSON', 'KML', 'SQLite')
	:param fieldName1: String. Name of first field
	:param fieldName2: String. Name of second field
	:param newFieldName: String. Name of newly generated field
	:return:
	"""
	# Open spatial file
	layer, dataSource = getLayer(filePath, driverName)

	# Loop through layer to calculate difference between fields {FID:newFieldValue}
	newFieldValues = {}
	for feature in layer:
		fid = feature.GetFID()
		geom = feature.GetGeometryRef()
		newFieldValue = geom.GetArea()
		newFieldValues[fid] = newFieldValue

	# Feed that new dictionary into addNewFieldToSpatialFile
	addNewFieldToSpatialFile(filePath, driverName, newFieldName, 'Float', newFieldValues)
	return


def addfieldpercent(filePath, fieldName1, newFieldName, driverName = 'ESRI Shapefile'):
	# Open spatial file
	layer, dataSource = getLayer(filePath, driverName)

	# Loop through layer to calculate difference between fields {FID:newFieldValue}
	newFieldValues = {}
	allArea = -1.0
	allFid = -1.0
	for feature in layer:
		fid = feature.GetFID()
		if feature.GetField('SPECIES') == 'ALL':
			allArea = feature.GetField(fieldName1)
			allFid = fid
			break
	layer.ResetReading()

	for feature in layer:
		fid = feature.GetFID()
		fieldValue1 = feature.GetField(fieldName1)
		newFieldValue = fieldValue1/allArea
		newFieldValues[fid] = newFieldValue
	#newFieldValues[ALLFid] = 1.0


	# Feed that new dictionary into addNewFieldToSpatialFile
	addNewFieldToSpatialFile(filePath, driverName, newFieldName, 'Float', newFieldValues)
	return


