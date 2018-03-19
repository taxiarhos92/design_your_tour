from googleplaces import GooglePlaces, types, lang
import googlemaps
from datetime import datetime,timedelta
import wikipedia

def get_city_landmarks(google_api_key, city, landmark_types,limit=-1):
	google_places = GooglePlaces(google_api_key)
	query_result = google_places.nearby_search(
		location=city, 
		type=landmark_types)
	places_details=[]
	for place in query_result.places:
		places_details.append(place.name)
	return places_details[:limit]

def get_route_details(google_api_key, point1, point2, type_of_transport, when=None):
	gmaps = googlemaps.Client(key=google_api_key)
	try:
		res = gmaps.distance_matrix(origins=point1,destinations=point2,mode=type_of_transport, departure_time=when)

		t = res['rows'][0]['elements'][0]['duration']['value']
		d = res['rows'][0]['elements'][0]['distance']['value']
		
		return [d/1000.0,t/60.0]
	except:
		return [0,0]

def get_route_details_mul_dest(google_api_key, point1, point2, type_of_transport, when=None):
	gmaps = googlemaps.Client(key=google_api_key)
	res = gmaps.distance_matrix(origins=point1,destinations=point2,mode=type_of_transport, departure_time=when)
	data = res['rows'][0]['elements']
	print(point2)
	print(data[1]['distance'])
	for i in data: print(i)
	distances =  map(lambda x:[x['distance']['value']/1000.0,x['duration']['value']/60.0],data)#,map(lambda x:x/60.0,t)]

	places = map(lambda x:[point1,x],point2)

	return(zip(places,distances))

def get_place_details(place):
	try:
		return wikipedia.summary(place)
	except:
		return "-"

