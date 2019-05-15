from geopy.geocoders import GoogleV3


def get_countries():
    text = open('map.txt', 'r+')
    content = text.read()
    text.close()
    return content.strip().split("\n")


def get_countries_location():
    countries = get_countries()
    countries_location = {}
    geolocator = GoogleV3(api_key='AIzaSyCDnroqbV96qo62f8amzC68k1T-RYqapaA')
    for country in countries:
        location = geolocator.geocode(country, language='en')
        if location is not None:
            countries_location[country] = location.raw["geometry"]["location"]
        else:
            print("No location!", location)
    return countries_location


if __name__ == '__main__':
    print(get_countries_location())
