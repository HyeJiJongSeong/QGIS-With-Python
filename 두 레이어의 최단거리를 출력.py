from qgis.core import QgsVectorLayer

# Define layer names
layer1_name = '첫번째 레이어 이름(단일피처)'
layer2_name = '두번째 레이어 이름(피쳐가 여러개)'

# Get the layers by name
layer1 = QgsProject.instance().mapLayersByName(layer1_name)[0]
layer2 = QgsProject.instance().mapLayersByName(layer2_name)[0]

# Define selected features as a processing feature source definition
# 두번째 레이어에서 선택한 피처와 첫번째 레이어간의 최단거리를 구해야할 때 활용, 레이어 미 선택시 오류발생
layer2 = QgsProcessingFeatureSourceDefinition(layer2.source(), True)

# Reproject layers to EPSG:5186 and save them as memory layers
# 레이어간의 좌표계를 통일시켜야만 오류가 안 뜸
reprojected_layer_1 = processing.run("native:reprojectlayer", 
                                     {"INPUT":layer1,
                                      "TARGET_CRS":QgsCoordinateReferenceSystem('EPSG:5186'),
                                      "OUTPUT":"memory:"})["OUTPUT"]
reprojected_layer_2 = processing.run("native:reprojectlayer", 
                                     {"INPUT":layer2,
                                      "TARGET_CRS":QgsCoordinateReferenceSystem('EPSG:5186'),
                                      "OUTPUT":"memory:"})["OUTPUT"]

# Add reprojected layers to the project
#QgsProject.instance().addMapLayer(reprojected_layer_1)
#QgsProject.instance().addMapLayer(reprojected_layer_2)




# Convert polygon layers into points
point_layer_1 = processing.run("native:extractvertices", 
                                {"INPUT":reprojected_layer_1,
                                 "OUTPUT":"memory:"})["OUTPUT"]
point_layer_2 = processing.run("native:extractvertices", 
                                {"INPUT":reprojected_layer_2,
                                 "OUTPUT":"memory:"})["OUTPUT"]
#QgsProject.instance().addMapLayer(point_layer_1)
#QgsProject.instance().addMapLayer(point_layer_2)
#레이어의 경계로부터 점변환을 통해서 이 두 점집단간의 최단거리를 distance matrix(거리행렬)을 통해서 산출
# Calculate distance matrix
params = {
    'INPUT': point_layer_1,
    'TARGET': point_layer_2,
    'MATRIX_TYPE': 0,
    'INPUT_FIELD': 'vertex_index',
    'TARGET_FIELD': 'vertex_index',
    'NEAREST_POINTS' : 1,
    'OUTPUT': 'memory:'
}

result = processing.run('qgis:distancematrix', params)

distance_matrix = result['OUTPUT']



# Add the output layer to the map
#QgsProject.instance().addMapLayer(distance_matrix)
#최단거리를 찾아내는 과정
shortest_distance = None
shortest_point1_id = None
shortest_point2_id = None

for feature in distance_matrix.getFeatures():
    distance = feature['Distance']
    point1_id = feature['InputID']
    point2_id = feature['TargetID']
    
    # If this is the first distance, set it as the shortest
    if shortest_distance is None:
        shortest_distance = distance
        shortest_point1_id = point1_id
        shortest_point2_id = point2_id
    # If the current distance is shorter than the previous shortest, update the values
    elif distance < shortest_distance:
        shortest_distance = distance
        shortest_point1_id = point1_id
        shortest_point2_id = point2_id

#print(shortest_point1_id)
#print(shortest_point2_id)
#shortest_point1 = point_layer_1.getFeature(shortest_point1_id+1)
#shortest_point2 = point_layer_2.getFeature(shortest_point2_id+1)
request1 = QgsFeatureRequest().setFilterExpression(f'"vertex_index" = {shortest_point1_id}')
shortest_point1 = point_layer_1.getFeatures(request1).__next__()
request2 = QgsFeatureRequest().setFilterExpression(f'"vertex_index" = {shortest_point2_id}')
shortest_point2 = point_layer_2.getFeatures(request2).__next__()


# Create a line layer between the shortest points
# 최단거리간의 선을 긋고 최단거리를 소숫점 첫째자리까지 반올림하여 결과창에 
line_geom = QgsGeometry.fromPolyline([QgsPoint(shortest_point1.geometry().asPoint()), QgsPoint(shortest_point2.geometry().asPoint())])
line_layer = QgsVectorLayer("LineString?crs=EPSG:5186", "Shortest Line", "memory")
pr = line_layer.dataProvider()
f = QgsFeature()
f.setGeometry(line_geom)
pr.addFeatures([f])
line_layer.updateExtents()
print(f"{round(shortest_distance, -1):,.0f}")
print(f"최단거리는 {shortest_distance/1000:.1f}킬로미터")
QgsProject.instance().addMapLayer(line_layer).setName("최단거리")
