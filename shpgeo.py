from shpgeo import *
import os, ogr, osr
#import shapefile
import fiona
import json

def getshp(path):
	shapeList = []

	for file in os.listdir(path):
		if file.endswith(".shp"):
			shapeList.append(file)
	return shapeList

def openlist(shapelist):
	from osgeo import ogr
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
	from osgeo import ogr
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



#def mergeshp():
def mergeshp(firstshp, secondshp, index):
 	exportname = 'mergeshp_' + str(index) + '.shp'
	meta = fiona.open(firstshp).meta
	with fiona.open(exportname , 'w', **meta) as output:
	   for features in fiona.open(firstshp):
	       output.write(features)
	   for features in fiona.open(secondshp):
	       output.write(features)
	return exportname

def addvalues(filename, valuelist):
	driver = ogr.GetDriverByName('ESRI Shapefile')
	dataSource = driver.Open(filename, 1)
	layer = dataSource.GetLayer()
	#help(layer)
	#provider = layer.dataProvider()

	feats = [ feat for feat in layer.getFeatures() ]

	n = len(feats)

	for i in range(n):
	    new_values = { 1 : valuelist[0], 2: valuelist[1],\
	    3 : valuelist[2], 4: valuelist[3], 5 : valuelist[4]} #row 1, value 15
	    provider.changeAttributeValues( {i:new_values} )
	with fiona.open(filename, 'w') as f:
		f.write({'properties':{'foo':'bar'}})


def open_output(arg):
	import sys
	if arg == sys.stdout:
		return arg
	else:
		return open(arg, 'w')

def crs_uri(crs):
    """Returns a CRS URN computed from a crs dict."""
    # References version 6.3 of the EPSG database.
    # TODO: get proper version from GDAL/OGR API?
    if crs['proj'] == 'longlat' and (
            crs['datum'] == 'WGS84' or crs['ellps'] == 'WGS84'):
        return 'urn:ogc:def:crs:OGC:1.3:CRS84'
    elif 'epsg:' in crs.get('init', ''):
        epsg, code = crs['init'].split(':')
        return 'urn:ogc:def:crs:EPSG::%s' % code
    else:
        return None

def addfieldpercent(filePath, fieldName1, newFieldName, driverName = 'ESRI Shapefile'):
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
    ALLArea = -1
    for feature in layer:
    	fid = feature.GetFID()
    	if feature.GetField('SPECIES') == 'ALL':
    		ALLArea = feature.GetField(fieldName1)
    		break

    for feature in layer:
        fid = feature.GetFID()
        fieldValue1 = feature.GetField(fieldName1)
        print(feature.GetField('Month'))
        print (fieldValue1)
        print (ALLArea)
        if fieldValue1 is None:
            continue
        newFieldValue = fieldValue1/ALLArea
        newFieldValues[fid] = newFieldValue
    print newFieldValues

    # Feed that new dictionary into addNewFieldToSpatialFile
    addNewFieldToSpatialFile(filePath, driverName, newFieldName, 'Float', newFieldValues)
    return
def getLayer(filePath, driverName, mode=0, osmLayer=None):
    """
    This function reads in an existing spatial file and returns its layer and data source (to keep it in scope)
    :param filePath: String. Path to spatial file
    :param driverName: String. Type of spatial file (eg, 'ESRI Shapefile', 'OSM', 'GeoJSON', 'KML', 'SQLite')
    :param mode: 0 to read, 1 to write
    :param osmLayer: 0 for points, 1 for lines, 2 for multilines, 3 for multipolygons, 4 for other relations
    :return: Layer, DataSource
    """

    # Open the data source (with specific driver if given)
    driver = ogr.GetDriverByName(driverName)
    dataSource = driver.Open(filePath, mode)

    # Make sure data source was properly opened before getting the layer
    if dataSource is None:
        raise Exception('Could not open', dataSource)

    # Get the layer
    if osmLayer is not None:
        layer = dataSource.GetLayer(osmLayer)
    else:
        layer = dataSource.GetLayer()

    # Must return both layer and dataSource to previous scope to prevent layer from becoming unusable & causing crash
    return layer, dataSource

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
        if newFieldValue is None:
            continue
        newFieldValues[fid] = newFieldValue

    # Feed that new dictionary into addNewFieldToSpatialFile
    addNewFieldToSpatialFile(filePath, driverName, newFieldName, 'Float', newFieldValues)
    return 

def addNewFieldToSpatialFile(filePath, driverName, fieldName, fieldType, fieldValues):
    """
    Adds a new field with values to a spatial file
    WARNING: Should not use on file already open in write mode!
    :param filePath: String. Path to existing spatial file
    :param driverName: String. Type of spatial file (eg, 'ESRI Shapefile', 'OSM', 'GeoJSON', 'KML', 'SQLite')
    :param fieldName: Name to give new field
    :param fieldType: 'Integer', 'Float', or 'String'
    :param fieldValues: Must be a dictionary of form FID:Value
    :return
    """
    # Open file
    layer, dataSource = getLayer(filePath, driverName, mode=1)

    # Make sure fieldName is 10 characters or less because of shapefile limitations
    if len(fieldName) > 10:
        raise Exception('Field name must be 10 characters or less.')

    # Translate fieldType to OGR
    if fieldType == 'Integer':
        ogrFieldType = ogr.OFTInteger
    elif fieldType == 'Float':
        ogrFieldType = ogr.OFTReal
    elif fieldType == 'String':
        ogrFieldType = ogr.OFTString
    else:
        raise Exception('Field type not recognized: ' + fieldType)

    # Check for the field and create if necessary, overwrite otherwise
    fieldIndex = layer.GetLayerDefn().GetFieldIndex(fieldName)
    if fieldIndex != -1:
        layer.DeleteField(fieldIndex)
    fieldDefinition = ogr.FieldDefn(fieldName, ogrFieldType)
    layer.CreateField(fieldDefinition)

    # Loop through features to add values
    for FID, fieldValue in fieldValues.items():

        if fieldValue is None:
            print 'FID ' + str(FID) + ' had None value.'
            continue

        # Get the feature
        feature = layer.GetFeature(FID)

        # Set value of feature
        feature.SetField(fieldName, fieldValue)
        layer.SetFeature(feature)

    return


# export merged shapefile
def exporttogjson(infile, outfile):
	dump_kw = {'sort_keys': True}
	
	with fiona.drivers():
		with open_output(outfile) as sink:
			with fiona.open(infile) as source:
				meta = source.meta.copy()
				meta['fields'] = dict(source.schema['properties'].items())
	                # Buffer GeoJSON data at the collection level. The default.
	                                # Buffer GeoJSON data at the feature level for smaller
	                # memory footprint.

	                # indented = bool(args.indent)
	                rec_indent = "\n" + " " * (2 * 0)

	                collection = {
	                    'type': 'FeatureCollection',  
	                    'fiona:schema': meta['schema'], 
	                    'fiona:crs': meta['crs'],
	                    '_crs': crs_uri(meta['crs']),
	                    'features': [] }
	                # if args.use_ld_context:
	                    # collection['@context'] = make_ld_context(
	                        # args.ld_context_items)
	                
	                head, tail = json.dumps(collection, **dump_kw).split('[]')
	                
	                sink.write(head)
	                sink.write("[")
	                
	                itr = iter(source)
	                
	                # Try the first record.
	                try:
	                    i, first = 0, next(itr)
	                    # if args.use_ld_context:
	                    #     first = id_record(first)
	                    # if indented:
	                        # sink.write(rec_indent)
	                    sink.write(
	                        json.dumps(first, **dump_kw
	                            ).replace("\n", rec_indent))
	                except StopIteration:
	                    pass
	                except Exception as exc:
	                    # Ignoring errors is *not* the default.
	                    if ignore_errors:
	                        logger.error(
	                            "failed to serialize file record %d (%s), "
	                            "continuing",
	                            i, exc)
	                    else:
	                        # Log error and close up the GeoJSON, leaving it
	                        # more or less valid no matter what happens above.
	                        logger.critical(
	                            "failed to serialize file record %d (%s), "
	                            "quiting",
	                            i, exc)
	                        sink.write("]")
	                        sink.write(tail)
	                        if indented:
	                            sink.write("\n")
	                        return 1
	                
	                # Because trailing commas aren't valid in JSON arrays
	                # we'll write the item separator before each of the
	                # remaining features.
	                for i, rec in enumerate(itr, 1):
	                    try:
	                        if args.use_ld_context:
	                            rec = id_record(rec)
	                        if indented:
	                            sink.write(rec_indent)
	                        sink.write(item_sep)
	                        sink.write(
	                            json.dumps(rec, **dump_kw
	                                ).replace("\n", rec_indent))
	                    except Exception as exc:
	                        if ignore_errors:
	                            logger.error(
	                                "failed to serialize file record %d (%s), "
	                                "continuing",
	                                i, exc)
	                        else:
	                            logger.critical(
	                                "failed to serialize file record %d (%s), "
	                                "quiting",
	                                i, exc)
	                            sink.write("]")
	                            sink.write(tail)
	                            if indented:
	                                sink.write("\n")
	                            return 1
	                
	                # Close up the GeoJSON after writing all features.
	                sink.write("]")
	                sink.write(tail)
	                if indented:
	                    sink.write("\n")

	return 0