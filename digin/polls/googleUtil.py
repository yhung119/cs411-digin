import pprint
import googlemaps
from datetime import datetime
from .google_api_config import API_KEY
import time
gmaps = googlemaps.Client(key=API_KEY)

def find_place_by_id(place_id):
    detail = gmaps.place(place_id)#, fields=["name", "formatted_address", "rating", "price_level", "formatted_phone_number", "opening_hours", "website"])
    return detail

def get_attr(obj, key, null_value):
    if key in obj:
        return obj[key]
    return null_value

def get_restaurant_attr(place_id):
    if place_id == "":
        return ["unknown place name", "unknown address", '000-000-0000', 2, 2, "DUMMY_PLACE_ID", [], 0, 0, "www.google.com"]
    db_attributes = []
    detail = find_place_by_id(place_id)
    if detail["status"]=="OK":
        placename = get_attr(detail['result'], 'name', "unknown place name")
        print("Place found ({})".format(placename))
    else:
        print("Place not found")
        return ["unknown place name", "unknown address", '000-000-0000', 2, 2, "DUMMY_PLACE_ID", [], 0, 0, "www.google.com"]

    db_attributes.append(get_attr(detail['result'], 'name', "unknown place name"))
    db_attributes.append(get_attr(detail['result'], 'formatted_address', "unknown address"))
    db_attributes.append(get_attr(detail['result'], 'formatted_phone_number', '000-000-0000'))
    db_attributes.append(get_attr(detail['result'], 'rating', 2))
    db_attributes.append(get_attr(detail['result'], 'price_level', 2))
    db_attributes.append(detail['result']['place_id'])

    reviews = []
    if 'reviews' in detail['result']:
        for r in detail['result']['reviews']:
            reviews += [r['text']]
    db_attributes.append(reviews)
    db_attributes.append(detail['result']['geometry']['location']['lat'])
    db_attributes.append(detail['result']['geometry']['location']['lng'])
    db_attributes.append(get_attr(detail['result'],'website', "www.google.com"))
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
        user = "yi",
        passwd = "password",
        database = "digin"
    )
    cursor = db.cursor()
    import json
    count = 0
    for key, value in r_dict.items():
        attrs = value
        attrs[6] = json.dumps(attrs[6])
        cursor.execute("SELECT * FROM polls_place WHERE place_id=%s",[attrs[5]])
        records = cursor.fetchall()
        if len(records)==0:
            cursor.execute("INSERT INTO polls_place"
                        "(name, address, phone, rating, price_level, place_id, reviews, latitude, longitude, website)"
                        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                        attrs)
            count += 1
    db.commit()
    print("{} records added.".format(count))
if __name__ == '__main__':
    load_restaurant_to_database()