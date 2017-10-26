import json
import datetime
import requests
from bs4 import BeautifulSoup
import re

import Get_charts

this_year = datetime.date.today().year

class Project(object):
    def __init__(self, first_year, chart, num_songs, last_year=this_year):
        self.first_year = first_year
        self.last_year = last_year
        self.chart_name = chart
        self.number_of_songs = num_songs
        self.year_dict, self.date_list = self.get_songs_from_billboard()
        self.dict_with_song_objs = self.create_song_objects()

    def get_songs_from_billboard(self):
        year_dict = Get_charts.create_year_data(self.first_year, self.last_year)
        date_list = Get_charts.create_date_list(year_dict)
        Get_charts.collect_charts(date_list, self.chart_name, year_dict, self.number_of_songs)
        return year_dict, date_list

    def create_song_objects(self):
        song_obj_dict = {}
        with open("chart_songs.json", "r") as fin:
            song_data = json.load(fin)
            for k, v in song_data.items():
                try:
                    name = "song_" + str(k)
                    song_obj_dict[name] = Song_obj(v)
                except AttributeError:
                    print("COULDN'T FIND LYRICS FOR THIS SONG:", v["title"], "by", v["artist"])
                    print("PRINTING LYRICS ATTR:", v.lyrics)
                    pass
        return song_obj_dict

class Song_obj():
    def __init__(self, song_info):
        self.artist = song_info["artist"]
        self.title = song_info["title"]
        self.rank = song_info["rank"]
        self.date = song_info["date"]
        self.lyrics = self.get_lyrics()

    def create_url_for_genius(self, x=1):
        regex_and = r"&"
        regex_punct = r"[^\w\-\s]"
        regex_feat = r" Featuring.*"
        regex_parenthesis = r"\s\(.*\)"
        regex_dollar = r"\$"
        regex_exl_mark = r"(!)(\w)"
        base_url = "https://genius.com/"
        artist_url = re.sub(regex_feat, "", self.artist)
        artist_url = re.sub(regex_and, "and", artist_url)
        artist_url = re.sub(regex_dollar, "s", artist_url)
        artist_url = re.sub(regex_exl_mark, "s", artist_url)
        title_url = re.sub(regex_and, "and", self.title)
        title_url = re.sub(regex_exl_mark, "and", title_url)
        if x == 1:
            url_ending = "-lyrics"
        elif x == 2:
            title_url = re.sub(regex_parenthesis, "", title_url)
            url_ending = "-lyrics"
        elif x == 3:
            title_url = re.sub(regex_parenthesis, "", title_url)
            url_ending = "-remix-lyrics"
        artist_url = re.sub(regex_punct, "", artist_url)
        artist_url = re.sub("\s", "-", artist_url)
        title_url = re.sub(regex_punct, "", title_url)
        title_url = re.sub("\s", "-", title_url)
        final_url = base_url + artist_url + "-" + title_url + url_ending
        return final_url

    def get_lyrics(self):
        try:
            url = self.create_url_for_genius(1)
            r = requests.get(url)
            r.raise_for_status()
        except:
            print("TRYING SECOND!!!!!xxxxxx")
            try:
                url = self.create_url_for_genius(2)
                r = requests.get(url)
                r.raise_for_status()
            except:
                print("TRYING THIRD!!!!!!!!!xxxxxxxxx")
                url = self.create_url_for_genius(3)
                r = requests.get(url)
        data = r.text
        soup = BeautifulSoup(data, "html.parser")
        print(url)
        lyrics_as_list = []
        small_soup = soup.find("div", class_="lyrics")
        mini_soup = small_soup.text
        mini_soup_as_list = mini_soup.split("\n")
        for line in mini_soup_as_list:
            if "[" in line or (len(line) == 0) or line.startswith("Chorus") or (line.startswith("(") and
                                                                                    line.endswith(")")):
                pass
            else:
                lyrics_as_list.append(line)
        lyrics = "\n".join(lyrics_as_list)
        print(lyrics[0:20])
        return lyrics

#BELOW IS USER INPUT, todo: remove later

first_project = Project(first_year=2017, chart="radio-songs", num_songs=5)
#print(first_project.dict_with_song_objs["song_1990_0"].url)
