layer_name = "해당레이어이름"

# 레이어 객체 가져오기
layer = QgsProject.instance().mapLayersByName(layer_name)[0]

# 면적 총합 구하기
total_area = 0
for feature in layer.getFeatures():
    total_area += feature.geometry().area()

print("총 면적: {} 제곱미터".format(total_area))
