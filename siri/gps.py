import requests #요청을 위한 모듈
import json  #json파일을 다루기 위한 모듈
from geopy.geocoders import Nominatim #주소를 GPS로 바꿔주는 모듈
from pyproj import Transformer,CRS  #좌표계 변환 모듈

#IP를 통해 현재 위치 GPS 받기
def ip_gps():
    #위치 정보 요청
    response = requests.get(f'http://www.geoplugin.net/json.gp')
    #json파일을 자료 구조로 변환
    data = json.loads(response.text)
    #데이터 추출
    gps = {'lat': data['geoplugin_latitude'], 'long': data['geoplugin_longitude'], 'region': data['geoplugin_regionName']}
    return gps

#주소를 GPS로
def to_gps(location):
    geolocoder = Nominatim(user_agent = 'South Korea', timeout=None)
    geo = geolocoder.geocode(location)
    gps_location = {'location':location,"lat": str(geo.latitude), "long": str(geo.longitude)}
    return gps_location


