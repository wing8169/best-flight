from flask import Flask, render_template, request, redirect
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map, icons
from country import *
from flask_bootstrap import Bootstrap

import io
import random
from flask import Response
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

import paths

from count_words import word_counts

app = Flask(__name__, template_folder="templates")

Bootstrap(app)

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
    custom_map = Map(
        style=(
            "height:600px;"
            "width:100%;"
            "margin-top:30px;"
            "position:relative;"
            "z-index:200;"
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

    countries_names = get_countries()
    return render_template(
        'main.html',
        collapsible=custom_map,
        GOOGLEMAPS_KEY=request.args.get('apikey'),
        options=countries_names
    )


@app.route('/plot.png')
def plot_png():
    fig = create_figure()
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')


def create_figure():
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    xs = range(100)
    ys = [random.randint(1, 50) for x in xs]
    axis.plot(xs, ys)
    return fig


# @app.route('/test')
# def chartTest():
#     fig = create_figure()
#     fig.savefig('/static/images/new_plot.png')
#     return render_template('untitled1.html', name='new_plot', url='/static/images/new_plot.png')


@app.route('/calculate_table')
def calculate_table():
    source = request.args.get('source')
    desti = request.args.get('desti')
    rslt = paths.get_paths(source, desti)
    rslt_str = "["
    for i, r in enumerate(rslt):
        rslt_str += '["'
        tmp_path_str = "->".join(r[:-1])
        tmp_cost_str = str(round(r[-1], 2))
        rslt_str += tmp_path_str
        rslt_str += '", "'
        rslt_str += tmp_cost_str
        rslt_str += '", '
        rslt_str += '"100%", "12%", "0.5"]'
        if i != len(rslt) - 1:
            rslt_str += ", "
    rslt_str += "]"
    print(rslt_str)
    return rslt_str


if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)
