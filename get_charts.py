import json
import billboard

import random


def create_year_data(first_year, last_year):
    """Creates dictionary with every (user chosen) year as value. Example: {1:2000, 2:2001, 3:2002, ...}"""
    counter = 1
    year_dict = {}
    while first_year <= last_year:
        year_dict[str(counter)] = str(first_year)
        first_year += 1
        counter += 1
    return year_dict


def create_date_list(year_dict):
    """Creates list with semi-random summer dates for every (user chosen) year.
    Example: [2000-06-01, 2000-08-20, 2001-07-15, ...]"""
    date_list = []
    for k, v in year_dict.items():
        rand_summer_month = "%02d" % random.randint(6, 8)
        rand_day = "%02d" % random.randint(1, 30)
        rand_date = v + "-" + str(rand_summer_month) + "-" + str(rand_day)
        date_list.append(rand_date)
    return date_list


def collect_charts(date_list, chart_name, number_of_songs):
    """Uses billboard API to get (user chosen) charts. Saves data (song title, artist, rank on chart and date) to
    json-file 'chart_songs.json'. Every song saved with key: '[year]_[rank - 1]' """
    json_dict = {}
    for date in date_list:
        print("Getting a chart")  # only printing to let user know program is running
        year = date[0:4]  # Example: saves "2000" from "2000-06-01"
        song_count = 0
        chart = billboard.ChartData(chart_name, date=date)  # if no chart available for date it gets next possible date
        while song_count < number_of_songs:
            song = chart[song_count]
            chart_hit_dict = {"date": chart.date, "rank": song.rank, "title": song.title, "artist": song.artist}
            json_dict[year + "_" + str(song_count)] = chart_hit_dict
            song_count += 1
    with open("chart_songs.json", "w") as fout:
        fout.write(json.dumps(json_dict))
    fout.close()
