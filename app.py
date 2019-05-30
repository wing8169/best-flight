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
import matplotlib.pyplot as plt
import numpy as np

import time
import paths

from count_words import sentiment_results

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


def create_figure():
    countries_names = get_countries()
    # Draw bar chart
    # get number of groups
    groups = len(countries_names) - 1
    # get number of words for each country
    normal_words = []
    stop_words = []
    country_tmp = []
    for country in countries_names:
        if country == "Malaysia - Kuala Lumpur (KUL)":
            continue
        country_tmp.append(country[country.index("(")+1: country.index(")")])
        normal_words.append(sentiment_results[country]["positive"] +
                            sentiment_results[country]["negative"] + sentiment_results[country]["neutral"])
        stop_words.append(sentiment_results[country]["stop_words"])
    normal_words = tuple(normal_words)  # put in frequency data
    stop_words = tuple(stop_words)
    y_pos = np.arange(groups)
    bar_width = 0.35

    rects1 = plt.bar(y_pos, normal_words, bar_width, alpha=0.8,
                     color='lightblue', label='Normal Words')
    rects2 = plt.bar(y_pos + bar_width, stop_words, bar_width,
                     alpha=0.8, color='blue', label='Stop Words')

    plt.xticks(y_pos + bar_width, tuple(country_tmp))
    plt.xlabel('Country')
    plt.ylabel('Frequency of words')
    plt.title('Frequency of type of words')
    plt.legend()  # show the label
    plt.savefig("static/images/barchart.png")
    plt.clf()
    # Draw country pie chart
    for country in countries_names:
        if country == "Malaysia - Kuala Lumpur (KUL)":
            continue
        labels = ['Neural Words', 'Negative Words', 'Positive Words']
        frequency = [
            sentiment_results[country]["neutral_pct"],
            sentiment_results[country]["negative_pct"],
            sentiment_results[country]["positive_pct"],
        ]
        color = ['lightcyan', 'powderblue', '#7df293']
        explode = (0.1, 0, 0.05)
        plt.pie(frequency, labels=labels, colors=color,
                startangle=90, explode=explode, autopct='%0.2f%%', shadow=True)
        plt.axis('equal')
        plt.title('Sentiment Analysis for ' + country)
        plt.savefig("static/images/" + country + ".png")
        plt.clf()


create_figure()


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


def calculate_average_sentiment(c):
    rslt = 0
    for c1 in c:
        if c1 == "Malaysia - Kuala Lumpur (KUL)":
            continue
        rslt += sentiment_results[c1]["sentiment"]
    return round(rslt / len(c), 2)


def get_score(distance, shortest, longest, sentiment):
    score = ((longest - distance)*70 / (longest-shortest)) + \
        ((sentiment + 100)*30/200)
    return round(score, 2)


def get_prob(score, total_score):
    prob_dist = score / total_score
    return round(prob_dist, 2)


@app.route('/calculate_table')
def calculate_table():
    # start find path
    source = request.args.get('source')
    desti = request.args.get('desti')
    rslt = paths.get_paths(source, desti)
    # end find path
    # start find distances
    shortest_distance = round(get_distance(source, desti), 2)
    longest_distance_list = max(rslt, key=lambda x: x[-1])
    longest_distance = round(longest_distance_list[-1], 2)
    # end find distances
    # start find probability distribution
    # end find probability distribution
    rslt_str = []
    total_score = 0
    for i, r in enumerate(rslt):
        # start find sentiment
        current_sentiment = calculate_average_sentiment(r[:-1])
        # end find sentiment
        # start find score
        score = get_score(
            round(r[-1], 2), shortest_distance, longest_distance, current_sentiment)
        # end find score
        # start find total score
        total_score += score
        # end find total_score
        rslt_str_small = []
        tmp_path_str = "->".join(r[:-1])
        tmp_cost_str = str(round(r[-1], 2))
        rslt_str_small.append(tmp_path_str)
        rslt_str_small.append(tmp_cost_str)
        rslt_str_small.append(str(current_sentiment) + "%")
        rslt_str_small.append(str(score) + "%")
        rslt_str_small.append("0.5")
        rslt_str.append(rslt_str_small)
    for i1, r1 in enumerate(rslt):
        rslt_str[i1][-1] = str(get_prob(float(rslt_str[i1]
                                              [-2][:-1]), total_score))
    rslt_str.sort(key=lambda x: float(x[-2][:-1]), reverse=True)
    return str(rslt_str).replace("'", '"')


@app.route('/get_pct')
def get_pct():
    # start find path
    c = request.args.get('country')
    pct_list = {
        "id": c[:4],
        "pct": [
            sentiment_results[c]["positive_pct"],
            sentiment_results[c]["positive"],
            sentiment_results[c]["negative_pct"],
            sentiment_results[c]["negative"],
            sentiment_results[c]["neutral_pct"],
            sentiment_results[c]["neutral"],
        ]
    }
    return str(pct_list).replace("'", '"')


if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)
