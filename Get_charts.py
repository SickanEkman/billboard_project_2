import json
import billboard

import random

def create_year_data(first_year, last_year):
    counter = 1
    year_dict = {}
    while first_year <= last_year:
        year_dict[str(counter)] = str(first_year)
        first_year += 1
        counter += 1
    return year_dict

def create_date_list(year_dict):
    date_list = []
    for k,v in year_dict.items():
        rand_summer_month = "%02d" % random.randint(6, 8)
        rand_day = "%02d" % random.randint(1, 30)
        rand_date = v + "-" + str(rand_summer_month) + "-" + str(rand_day)
        date_list.append(rand_date)
    return date_list

def collect_charts(date_list, chart_name, year_dict, number_of_songs):
    """Creates the json-file 'chart_top_songs_by_year.json'
    which contains a json formatted database with songs"""
    json_dict = {}
    for date in date_list:
        print("Getting a chart") #only printing to let user know it's running
        year = date[0:4]
        song_count = 0
        chart = billboard.ChartData(chart_name, date=date) #get top list for that year
        while song_count < number_of_songs:
            song = chart[song_count]  # s = one song from the chart
            chart_hit_dict = {"date": chart.date, "rank": song.rank, "title": song.title, "artist": song.artist}
            json_dict[year + "_" + str(song_count)] = chart_hit_dict
            song_count += 1
    with open("chart_songs.json", "w") as fout:
        fout.write(json.dumps(json_dict))
    fout.close()
