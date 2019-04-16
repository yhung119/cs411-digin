import pprint
import googlemaps
from datetime import datetime
from .google_api_config import API_KEY
import time
gmaps = googlemaps.Client(key=API_KEY)

def find_place_by_id(place_id):
    detail = gmaps.place(place_id)#, fields=["name", "formatted_address", "rating", "price_level", "formatted_phone_number", "opening_hours", "website"])
    return detail

def get_restaurant_attr(place_id):
    db_attributes = []
    detail = find_place_by_id(place_id)
    if detail["status"]=="OK":
        print("Place found")
    else:
        print("Place not found")
        return db_attributes 

    db_attributes.append(detail['result']['name'])
    db_attributes.append(detail['result']['formatted_address'])
    db_attributes.append(detail['result']['formatted_phone_number'])
    db_attributes.append(detail['result']['rating'])
    if 'price_level' not in detail['result']:
        db_attributes.append(2)
    else:
        db_attributes.append(detail['result']['price_level'])
    db_attributes.append(detail['result']['place_id'])

    reviews = []
    for r in detail['result']['reviews']:
        reviews += [r['text']]
    db_attributes.append(reviews)
    db_attributes.append(detail['result']['geometry']['location']['lat'])
    db_attributes.append(detail['result']['geometry']['location']['lng'])
    if 'website' not in detail['result']:
        db_attributes.append("www.google.com")
    else:
        db_attributes.append(detail['result']['website'])
    return db_attributes

def get_restaurants(location, radius, restaurant_dict):
    result = gmaps.places('restaurant', location=location, radius=radius, type = "restaurant")
    db_columns = ['place_id', 'name', 'formatted_address', 'rating', 'price_level']
    page=0
    while True:
        # print("page:{}".format(page))
        if result['status']!='OK':
            print("fail to find nearby restaurants for request {}".format(page))
            pp.pprint(result)
            break
        else:
            restaurants = result['results']
            for restaurant in restaurants:
                if restaurant['place_id'] in restaurant_dict:
                    continue
                restaurant_dict[restaurant['place_id']] = get_restaurant_attr(restaurant['place_id'])
    
        if 'next_page_token' in result:
            time.sleep(3)
            result = gmaps.places('restaurant', page_token=result['next_page_token'])
        else:
            break
        page+=1
    
    print("restaurant list size:{}".format(len(restaurant_dict)))

def load_restaurant_to_database():
    location = (40.1030887, -88.23270169999999)
    r=100
    r_dict = {}
    get_restaurants(location,r,r_dict)
    location = (40.08, -88.25)
    get_restaurants(location,r,r_dict)
    location = (40.08, -88.23)
    get_restaurants(location,r,r_dict)
    location = (40.12, -88.25)
    get_restaurants(location,r,r_dict)
    location = (40.12, -88.23)
    get_restaurants(location,r,r_dict)

    import mysql.connector as mysql
    db = mysql.connect(
        host = "localhost",
        user = "cs411",
        passwd = "cs411",
        database = "test2"
    )
    cursor = db.cursor()
    import json
    for key, value in r_dict.items():
        attrs = get_restaurant_attr(key)
        cursor.execute("INSERT INTO polls_choice"
                    "(choice_text, votes, owner_id, question_id, address, phone, rating, price_level, place_id, reviews, latitude, longitude, website)"
                    "VALUES (%s,   %s,    %s,       %s,          %s,      %s,    %s,     %s,          %s,       %s,       %s,       %s,       %s)",
                    [attrs[0], 0, 1, 1, attrs[1], attrs[2], attrs[3], attrs[4], attrs[5], json.dumps(attrs[6]), attrs[7], attrs[8], attrs[9]]
                    )
    db.commit()