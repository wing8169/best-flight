from geopy.geocoders import GoogleV3
from geopy import distance


def get_countries():
    text = open('map.txt', 'r+')
    content = text.read()
    text.close()
    return content.strip().split("\n")


def get_countries_location():
    countries_names = get_countries()
    countries_location = {}
    geolocator = GoogleV3(api_key='AIzaSyCDnroqbV96qo62f8amzC68k1T-RYqapaA')
    for country in countries_names:
        location = geolocator.geocode(country, language='en')
        if location is not None:
            countries_location[country] = location.raw["geometry"]["location"]
        else:
            print("No location!", location)
    return countries_location


countries = get_countries_location()


def get_distance(country1, country2):
    global countries
    return distance.distance(
        (countries[country1]["lat"],
         countries[country1]["lng"]),
        (countries[country2]["lat"],
         countries[country2]["lng"]),
    ).km


def get_countries_links():
    text = open('map_route.txt', 'r+')
    content = text.read()
    text.close()
    tmp = content.strip().split("\n")
    for i in range(len(tmp)):
        newls = tmp[i].strip().split(",")
        newls.append(get_distance(newls[0], newls[1]))
        tmp[i] = newls
    return tmp


countries_links = get_countries_links()

if __name__ == '__main__':
    # Kuala Lumpur (KUL)
    # Tokyo - Haneda (HND)
    # Bali (DPS)
    # Beijing (PEK)
    # Bangkok - Don Mueang (DMK)
    # Brunei (BWN)
    # Melbourne - Avalon (AVV)
    print(get_countries_links())
    # print(
    #     get_countries_links()
    # )
    # print(get_countries_location())
