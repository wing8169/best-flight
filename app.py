from flask import Flask, render_template, request
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map, icons
from country import *

app = Flask(__name__, template_folder="templates")

GoogleMaps(
    app,
    key="AIzaSyCDnroqbV96qo62f8amzC68k1T-RYqapaA"
)


# draw paths between countries
def get_paths():
    paths = []
    for link in countries_links:
        paths.append(
            {
                'stroke_color': '#0AB0DE',
                'stroke_opacity': 1.0,
                'stroke_weight': 3,
                'path': [
                    countries[link[0]],
                    countries[link[1]],
                ]
            }
        )
    return paths
    # polyline = {
    # 'stroke_color': '#0AB0DE',
    # 'stroke_opacity': 1.0,
    # 'stroke_weight': 3,
    # 'path': [{'lat': 33.678, 'lng': -116.243},
    #          {'lat': 33.679, 'lng': -116.244},
    #          {'lat': 33.680, 'lng': -116.250},
    #          {'lat': 33.681, 'lng': -116.239},
    #          {'lat': 33.678, 'lng': -116.243}]
    # }
    # country_info = get_countries_location()
    # for country, latlng in country_info.items():
    #     paths.append(
    #         {
    #             'lat': latlng['lat'],
    #             'lng': latlng['lng'],
    #             'infobox': country,
    #         }
    #     )
    # return markers


# return the markers of countries
def get_markers():
    # markers = [{
    #     'lat': 59.939,
    #     'lng': 30.315,
    #     'infobox': 'This is a marker'
    # }],
    markers = []
    for country, latlng in countries.items():
        markers.append(
            {
                'lat': latlng['lat'],
                'lng': latlng['lng'],
                'infobox': country,
            }
        )
    return markers


@app.route("/")
def mapview():
    polyline = {
        'stroke_color': '#0AB0DE',
        'stroke_opacity': 1.0,
        'stroke_weight': 3,
        'path': [{'lat': 33.678, 'lng': -116.243},
                 {'lat': 33.679, 'lng': -116.244},
                 {'lat': 33.680, 'lng': -116.250},
                 {'lat': 33.681, 'lng': -116.239},
                 {'lat': 33.678, 'lng': -116.243}]
    }

    path1 = [(33.665, -116.235), (33.666, -116.256),
             (33.667, -116.250), (33.668, -116.229)]

    path2 = ((33.659, -116.243), (33.660, -116.244),
             (33.649, -116.250), (33.644, -116.239))

    path3 = ([33.688, -116.243], [33.680, -116.244],
             [33.682, -116.250], [33.690, -116.239])

    path4 = [[33.690, -116.243], [33.691, -116.244],
             [33.692, -116.250], [33.693, -116.239]]

    custom_map = Map(
        style=(
            "height:90%;"
            "width:90%;"
            "top:50;"
            "left:0;"
            "position:absolute;"
            "z-index:200;"
            "zoom:"
        ),
        markers=get_markers(),
        identifier="collapsible",
        varname="collapsible",
        lat=2.7455962,
        lng=101.7071602,
        polylines=get_paths(),
        collapsible=True,
        zoom="3"
    )

    return render_template(
        'main.html',
        collapsible=custom_map,
        GOOGLEMAPS_KEY=request.args.get('apikey')
    )


if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)
