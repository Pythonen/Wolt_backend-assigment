from flask import Flask, request
import requests, json
import math
app = Flask(__name__)


url = 'https://raw.githubusercontent.com/woltapp/summer2020/master/restaurants.json'
response = requests.get(url)

text_form = json.loads(response.text)


@app.route('/restaurants/search')
def query():
    """
    page to make requests
    :return: list of a restaurants in a string.
    """
    args1 = request.args['q']
    args2 = request.args['lat']
    args3 = request.args['lon']
    restaurants = jsonQuery(args1,float(args2),float(args3))
    print(args1)
    return str(restaurants)

def jsonQuery(args1,args2,args3):
    """

    :param args1: first query parameter for example "sushi"
    :param args2: latitude parameter for example lat=24.94167387485504
    :param args3: longitude parameter for example lon=24.94167387485504
    :return:
    """
    restaurants = text_form['restaurants']
    print(restaurants)
    restaurants1 = []
    for restaurant in restaurants:
        lat = float(restaurant['location'][0])
        print(type(lat))
        lon = float(restaurant['location'][1])
        name = restaurant['name'].lower()
        print(name)
        description = restaurant['description'].lower()
        print(description)
        tags = restaurant['tags']
        for tag_ in tags:
            tag = tag_.lower()
        print(tag)
        distance = getDistanceFromLatLonInKm(args2,args3,lat,lon)
        if ((args1 in description) or (args1 in name) or (args1 in tag)) and distance:
            restaurants1.append(restaurant)
            print(restaurant)
        else:
            continue
    return restaurants1


def getDistanceFromLatLonInKm(lat1,lon1,lat2,lon2):
    """
    Calculates the distance between two coordinate points. Core of this function is from StackOverflow since I'm not
    a mathematician.
    :param lat1: argument latitude
    :param lon1: argument longitude
    :param lat2: latitude from restaurants.json
    :param lon2: longitude from restaurants.json
    :return: distance if it's less or equal to 3km
    """

    R = 6371
    dLat = math.radians(lat2-lat1)
    dLon = math.radians(lon2-lon1)
    a = math.sin(dLat/2) * math.sin(dLat/2) + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dLon/2) * math.sin(dLon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a));
    d = R * c
    if (d <= 3):
        return d

if __name__ == '__main__':
    app.run(debug=True)