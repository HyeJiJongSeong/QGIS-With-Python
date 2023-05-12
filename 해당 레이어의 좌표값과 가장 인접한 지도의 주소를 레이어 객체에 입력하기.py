import requests
from qgis.core import *
from qgis.analysis import QgsNativeAlgorithms
from qgis.PyQt.QtCore import QVariant

# supply the layer name and CRS to be reprojected
layer_name = "해당하는 레이어"
crs = QgsCoordinateReferenceSystem("EPSG:4326")

# Get the layer by name
layer = QgsProject.instance().mapLayersByName(layer_name)[0]

if 'address' in layer.fields().names():
    field_index = layer.fields().indexFromName('address')
    layer.startEditing()
    layer.deleteAttributes([field_index])
    layer.commitChanges()

layer_provider = layer.dataProvider()
layer_provider.addAttributes([QgsField('address', QVariant.String)])
layer.updateFields()

# reproject layer to EPSG:4326
reprojected_layer = processing.run("native:reprojectlayer", {
                                    'INPUT': layer,
                                    'TARGET_CRS': crs,
                                    'OUTPUT': 'memory:'
                                  })['OUTPUT']

# 공간 인덱스 생성
index = QgsSpatialIndex(layer.getFeatures())

for feature in reprojected_layer.getFeatures():
    # get the centroid of the MultiPolygon geometry
    point = feature.geometry().centroid().asPoint()
    lat, lon = point.y(), point.x()
    url = f"https://maps.googleapis.com/maps/api/geocode/json?latlng={lat},{lon}&language=ko&key=구글에서받은API를여기에적어야함"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        address = data['results'][0].get('formatted_address', 'N/A')
        feature['address'] = address
        print(feature['address'])
        matching_features = layer.getFeatures(f'fid = {feature["fid"]}')
        for original_feature in matching_features:
            # update address field in original layer
            with edit(layer):
                original_feature['address'] = address
                layer.updateFeature(original_feature)




#QgsProject.instance().addMapLayer(reprojected_layer)
# end the editing session
layer.triggerRepaint()
