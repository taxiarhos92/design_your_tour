from city_explorer import *
from datetime import datetime, timedelta
from main3 import *

google_api_key = "AIzaSyC9DeK138pXFAK-dcayzCAU6pJRY2XEOUc"
landmark_type = func3()
city = input("Type the city you want to visit: ")
wanavisitlist = []
hotels = get_city_landmarks(google_api_key, city, "hotel")
print("********************************************************************\n")
print("Here is the list with all the hotels you are able to stay.\n")

length = 1
for hotel in hotels:
    print("Hotel number :", length, hotel)
    length += 1

hotelnumber = int(input("Please give me the number of the hotel you want to stay: "))
print("********************************************************************")
while hotelnumber > length - 1:
    print("The number you gave is not in the list.Give a proper number.")
    hotelnumber = int(input("Please give me the number of the hotel you want to stay: "))

hotelnumber -= 1
hotelplace = hotels[hotelnumber]
wanavisitlist.append(hotelplace) #to onoma tou hotel pou dialegei

d1 = datetime.now()
while True:
    try:
        start_time = datetime.strptime(input('Please specify time (in HH:MM format) you will start: '), "%H:%M")
        break
    except ValueError:
        print("Oops!  That was no valid time.  Try again...")

hours = start_time.hour
minutes = start_time.minute
xronos_start = datetime(d1.year, d1.month, d1.day, hours, minutes) #h wra pou 8a arxisei to tour
xronos_finish = datetime(d1.year, d1.month, d1.day, 22, 00)

maxdistance= int(input("Please give me the max distance in Km you want to walk: "))

landmarks = get_city_landmarks(google_api_key, city, landmark_type)
print("Here is the list with all the %s you are able to visit." %(landmark_type))

length = 1
for landmark in landmarks:
    print("Landmark number %s is : %s" %(length, landmark))
    length += 1

print("********************************************************************")
number = int(input("Give me the number of the landmark you want to read: "))

while ((number != 0) and (number < length)) or (number > length - 1):
    if number > length - 1:
        print("The number you gave is not in the list.Give a proper number.")
        print("******************************************************************")
        number = int(input("If you don't want to read anymore type '0': "))
    else:
        number -= 1
        place = landmarks[number]
        print(place)
        print("-" * len(place), "\n")
        description = get_place_details(place)
        print(description, "\n")
        length = 1
        for landmark in landmarks:
            print("Landmark number %s is : %s" % (length, landmark))
            length += 1
        print("******************************************************************")
        visit = input("Would you like to visit this landskape? (Y/y or N/n): ")
        if (visit == "Y") or (visit == "y"):
            boolean = place in wanavisitlist
            if not (boolean):
                wanavisitlist.append(place)

        number = int(input("Give me the number of the landmark you want to read.\nIf you don't want to read anymore type '0': "))
        print("******************************************************************")

if number == 0:
    wanavisitlist.append(hotelplace)
    i = 0
    pos = 1
    while i < len(wanavisitlist)-1 and (pos < len(wanavisitlist)):
        typeoftransport = "walking"
        route = get_route_details(google_api_key, wanavisitlist[i], wanavisitlist[i + 1], typeoftransport, when=None)
        if route[0] > maxdistance:
            typeoftransport = "transit"
            route = get_route_details(google_api_key, wanavisitlist[i], wanavisitlist[i + 1], typeoftransport, when=None)
        add_minutes = timedelta(minutes=route[1])
        arrival_time = xronos_start + add_minutes
        print("The arrival time by %s in %s is %s" % (typeoftransport, wanavisitlist[i + 1], arrival_time))
        add_hours = timedelta(hours=2)
        xronos_start = xronos_start + add_hours + add_minutes
        wanavisitlist.insert(pos, route)
        pos += 2
        i += 2

    print(wanavisitlist)
    xronos_start = xronos_start - add_hours
    if xronos_start > xronos_finish:
        t_delay = xronos_start - xronos_finish
        print("You will arrive to base after 22:00. The delay will be ", t_delay)
    print("See you next time...")