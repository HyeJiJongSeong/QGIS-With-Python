# 구글 지도 API 키
google_maps_api_key = "당신이 발급받은 구글 API를 꼭 꼭 기재해 주세요"

# 검색할 주소
address = "주소를 적어주세요 물론 한글로"
# Google Maps Geocoding API 요청 URL
url = f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={google_maps_api_key}"

# 요청 보내기
import requests
response = requests.get(url)

# 응답 데이터 파싱
data = response.json()
location = data['results'][0]['geometry']['location']
lat, lng = location['lat'], location['lng']

# GeoJSON으로 변환
geojson = {
    "type": "FeatureCollection",
    "features": [{
        "type": "Feature",
        "properties": {
            "name": address,
            "latitude": lat,
            "longitute": lng},
        "geometry": {
            "type": "Point",
            "coordinates": [
                data['results'][0]['geometry']['location']['lng'],
                data['results'][0]['geometry']['location']['lat']
            ]
        }
    }]
}

# QGIS 레이어로 추가
import json
바꿀레이어이름 = address
layer = QgsVectorLayer(json.dumps(geojson), "geojson_layer", "ogr")
QgsProject.instance().addMapLayer(layer)
#레이어의 이름을 주소이름으로 했는데, 바꾸려면 다른거로
layer.setName(바꿀레이어이름)
