from city_explorer import *
from datetime import datetime, timedelta

def get_route_details_bonus(google_api_key, point1, point2, type_of_transport, when=None):
	gmaps = googlemaps.Client(key=google_api_key)
	try:
		res = gmaps.distance_matrix(origins=point1, destinations=point2, mode=type_of_transport, departure_time=when)

		t = res['rows'][0]['elements'][0]['duration']['value']
		d = res['rows'][0]['elements'][0]['distance']['value']

		return [t / 60.0, d / 1000.0]         #αλλαξα λιγο τη συναρτηση γιατι με βολευε στο min να ειναι πρωτος ο χρονος
	except:
		return [1000, 1000]                   #με το μηδεν οταν εψαχνε το min μπερδευοταν

print("**************************************************************")
print("Hello traveler!!!")
city = input("Give me the city you want to visit: ")

google_api_key = "AIzaSyBsMDBpKe9sfCNv-wqMiNGOkevIJ3rniOw"
wanavisitlist = []

hotels = get_city_landmarks(google_api_key, city, "hotel")
print("********************************************************************")
print("Choose where do you want to stay.\n")
print("********************************************************************")

length = 1
for hotel in hotels:
    print("Hotel number :", length, hotel)
    length += 1
print("********************************************************************")
hotelnumber = int(input("Please give me the hotel's number: "))
print("********************************************************************")

hotelnumber -= 1
hotelname = hotels[hotelnumber]
wanavisitlist.append(hotelname) #to onoma tou hotel pou dialegei

d1 = datetime.now()
while True:
    try:
        start_time = datetime.strptime(input('Please specify time (in HH:MM format) you will start: '), "%H:%M")
        break
    except ValueError:
        print("Oops! That was no valid time. Try again...")

hours = start_time.hour
minutes = start_time.minute
xronos_start = datetime(d1.year, d1.month, d1.day, hours, minutes) #h wra pou 8a arxisei to tour
xronos_finish = datetime(d1.year, d1.month, d1.day, 22, 00)

print("This may take a while... Please wait.")

landmarktypelist = ['aquarium', 'art gallery', 'church', 'museum', 'park', 'zoo']
all_landmarks_list = [] #h lista pou painoyn olon twn eidwn ta axiotheata
for landmark_type in landmarktypelist:
    all_landmarks_list.extend(get_city_landmarks(google_api_key, city, landmark_type)) #lista me ola ta landmarks ths polhs

for hotel in hotels:
    all_landmarks_list.remove(hotel) #afairw ola ta xenodoxeia apthn lista gia na mhn phgainei gia episkepsi se hotel
all_landmarks_list.append(hotelname)
transportlist = ['transit', 'walking']

walking, walkingtime, transit, transittime, lista, minimum_landmarkstime_list = ([] for i in range(6))
dromologiatime = 0.0
finishtime = xronos_start
arrival_time = xronos_start
i = 0
while (finishtime + timedelta(minutes=dromologiatime)) < xronos_finish:
    all_landmarks_list.remove(wanavisitlist[i]) #se ka8e rep remove to trexon landmark wste na mhn kanei th sygrisi xana mazi tou
    for typeoftransport in transportlist:
        for landmark in all_landmarks_list:
            if typeoftransport == 'transit':
                transit.append(landmark)                #sthn transit mpainoyn ta axiotheata me tis info gia thn diadromi
                transit.append(get_route_details_bonus(google_api_key, wanavisitlist[i], landmark, typeoftransport, when=None))
            elif typeoftransport == 'walking':
                walking.append(landmark)                 #sthn walking mpainoyn ta axiotheata me tis info gia thn diadromi
                walking.append(get_route_details_bonus(google_api_key, wanavisitlist[i], landmark, typeoftransport,when=None))

        if typeoftransport == 'transit':
            pos = 1
            while pos < len(transit):
                transittime.append(transit[pos])    #sthn transittime mpainoyn oi xronoi apo thn transit
                pos += 2
            timelisttr = min(transittime)           #briskw to min xrono
            position_of_landmark = transittime.index(min(transittime)) * 2 #briskw th thesi tou axiotheatos me ton min xrono
            minimum_landmarkstime_list.append(transit[position_of_landmark])    #vazw to landmark to xrono gia na paei ekei
            minimum_landmarkstime_list.append("by transit")                     #kai me poio tropo
            minimum_landmarkstime_list.append(timelisttr[0])
        elif typeoftransport == 'walking':
            pos = 1
            while pos < len(walking):
                walkingtime.append(walking[pos])     #sthn walkingtime mpainoyn oi xronoi apo thn walking
                pos += 2
            timelistwa = min(walkingtime)           #briskw to min xrono
            position_of_landmark = walkingtime.index(min(walkingtime)) * 2   #briskw th thesi tou axiotheatos me ton min xrono
            minimum_landmarkstime_list.append(walking[position_of_landmark])     #vazw to landmark to xrono gia na paei ekei
            minimum_landmarkstime_list.append("by walking")                      #kai me poio tropo
            minimum_landmarkstime_list.append(timelistwa[0])

        if len(minimum_landmarkstime_list) == 6:        #otan h lista tha exei 6 stoixeia
            lista = minimum_landmarkstime_list[2::3]    #3 gia to min xrono tropo kai landmark me walking kai 3 gia transit
            minimum_time = min(lista)                   #vriskei ton teliko min xrono
            nearest_landmark_pos = lista.index(min(lista)) * 3
            nearest_landmark = minimum_landmarkstime_list[nearest_landmark_pos]
            dromologiatime = dromologiatime + minimum_time #krataw to xrono pou thlei gia na paei apo landmark se landmark
            add_hours = timedelta(hours=2)  #add tis 2 wres gia thn episkepsi
            add_mimutes = timedelta(minutes=minimum_time * 2)       #add ta lepta na paei kai na gyrisei se kathe axiotheato
            arrival_time2 = arrival_time + timedelta(minutes=minimum_time) #o xronos afixhs se kathe axiotheato

            arrival_time = arrival_time2 + add_hours
            finishtime = finishtime + add_hours + add_mimutes

            if finishtime < xronos_finish:
                print("------------------------------------------------------")
                print("You have to travel %s to %s for about %d minutes." % (minimum_landmarkstime_list[nearest_landmark_pos + 1], minimum_landmarkstime_list[nearest_landmark_pos],minimum_time))
                print('The arrival time is ', arrival_time2.time())
                wanavisitlist.append(minimum_time)
                wanavisitlist.append(nearest_landmark)
                print(wanavisitlist)
            else:
                dromologiatime = dromologiatime - minimum_time #afairei apo to synolo ths wras twn dronologiwn to min time apo thn teleytaa epanalhpsi
                print("------------------------------------------------------")
                print("You will be back to %s in about %d minutes." %(hotelname,dromologiatime))
                hotel_time = arrival_time - add_hours + timedelta(minutes=dromologiatime) -timedelta(minutes=minimum_time)
                print('The arrival time at the hotel is ', hotel_time.time())

            walking, walkingtime, transit, transittime, minimum_landmarkstime_list, lista = ([] for i in range(6))
            i += 2

wanavisitlist.append(dromologiatime)
wanavisitlist.append(hotelname)
print(wanavisitlist)
print("See you next time...")