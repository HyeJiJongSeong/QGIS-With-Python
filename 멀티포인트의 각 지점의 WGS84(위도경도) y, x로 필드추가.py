# 필요한 라이브러리 import
from qgis.core import QgsCoordinateReferenceSystem, QgsField, edit, QgsProject
from PyQt5.QtCore import QVariant

# 레이어 이름 설정
layer_name = "레이어이름"

# 멀티포인트 레이어를 가져옴
layer = QgsProject.instance().mapLayersByName(layer_name)[0]

# WGS84 좌표계 객체 생성
crs_wgs84 = QgsCoordinateReferenceSystem('EPSG:4326')

# 좌표 변환 객체 생성
transform = QgsCoordinateTransform(layer.crs(), crs_wgs84, QgsProject.instance())

# 속성 테이블에 x, y 필드 추가
with edit(layer):
    provider = layer.dataProvider()
    provider.addAttributes([QgsField('x', QVariant.Type.Double), QgsField('y', QVariant.Type.Double)])
    layer.updateFields()

# 멀티포인트 레이어의 모든 포인트에 대해 x, y 좌표를 속성 테이블에 추가
with edit(layer):
    for feature in layer.getFeatures():
        if not feature.geometry():
            continue
        multipoint = feature.geometry()
        points = multipoint.asMultiPoint()
        for point in points:
            if point is None:
                continue
            new_point = transform.transform(point)
            x, y = new_point.x(), new_point.y()
            feature['x'] = x
            feature['y'] = y
            
            print("{:.3f}, {:.3f}".format(x, y))
            layer.updateFeature(feature)
