import json
import datetime
import requests
from bs4 import BeautifulSoup
import re

import Get_charts

this_year = str(datetime.date.today().year)

class Project(object):
    def __init__(self):
        self.first_year = 1992
        self.last_year =  1992
        self.chart_name = "radio-songs"
        self.number_of_songs = 10
        self.year_dict, self.date_list = self.get_songs_from_billboard()
        self.dict_with_song_objs = self.create_song_objects()
#        self.first_year = int(input("What's the first year of the chart? (Ex. 1970)\n"))
#        self.last_year = int(input("What's the last year of the chart? (Ex. " + this_year + ")\n"))
#        self.chart_name = input("What is the name of the chart?\n")
#        self.number_of_songs = int(input("How many songs from each year?\n"))
        #todo: change to user input later


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
                    print("COULDN'T FIND LYRICS FOR A SONG! THIS ONE:", v["title"])
                    pass
        return song_obj_dict

class Song_obj():
    def __init__(self, song_info):
        #print("Song object created!")
        self.artist = song_info["artist"]
        self.title = song_info["title"]
        self.rank = song_info["rank"]
        self.date = song_info["date"]
        self.lyrics = self.get_lyrics()
        #print(self.lyrics)

    def create_url_for_genius(self, x=1):
        regex_and = r"&"
        regex_punct = r"[^\w\-\s]"
        regex_feat = r" Featuring.*"
        regex_parenthesis = r"\s\(.*\)"
        base_url = "https://genius.com/"
        if x == 1:
            artist_url = re.sub(regex_feat, "", self.artist)
            artist_url = re.sub(regex_and, "and", artist_url)
            artist_url = re.sub(regex_punct, "", artist_url)
            artist_url = re.sub("\s", "-", artist_url)
            #title_url = re.sub(regex_parenthesis, "", self.title)
            title_url = re.sub(regex_and, "and", self.title)
            title_url = re.sub(regex_punct, "", title_url)
            title_url = re.sub("\s", "-", title_url)
            final_url = base_url + artist_url + "-" + title_url + "-lyrics"
        elif x == 2:
            artist_url = re.sub(regex_feat, "", self.artist)
            artist_url = re.sub(regex_and, "and", artist_url)
            artist_url = re.sub(regex_punct, "", artist_url)
            artist_url = re.sub("\s", "-", artist_url)
            title_url = re.sub(regex_parenthesis, "", self.title)
            title_url = re.sub(regex_and, "and", title_url)
            title_url = re.sub(regex_punct, "", title_url)
            title_url = re.sub("\s", "-", title_url)
            final_url = base_url + artist_url + "-" + title_url + "-remix-lyrics"
        elif x == 3:
            artist_url = re.sub(regex_feat, "", self.artist)
            artist_url = re.sub(regex_and, "and", artist_url)
            artist_url = re.sub(regex_punct, "", artist_url)
            artist_url = re.sub("\s", "-", artist_url)
            title_url = re.sub(regex_parenthesis, "", self.title)
            title_url = re.sub(regex_and, "and", title_url)
            title_url = re.sub(regex_punct, "", title_url)
            title_url = re.sub("\s", "-", title_url)
            final_url = base_url + artist_url + "-" + title_url + "-lyrics"
        return final_url

    def get_lyrics(self):
        url = self.create_url_for_genius()
        try:
            r = requests.get(url)
            r.raise_for_status()
            print("FIRST ALT")
        except:
            print("FIRST EXCEPTION CATCHED")
            try:
                url = self.create_url_for_genius(2)
                r = requests.get(url)
            except:
                print("SECOND EXCEPTION CATCHED")
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
                                                                                    line.endsswith(")")):
                pass
            else:
                lyrics_as_list.append(line)
        lyrics = "\n".join(lyrics_as_list)
        return lyrics


first_project = Project()
#print(first_project.dict_with_song_objs["song_1990_0"].url)

#todo: make "Sia-Featuring-Sean-Paul-Cheap-Thrills-lyrics" into "Sia-cheap-thrills-remix-lyrics"
#todo: make "Calvin-Harris-Featuring-Rihanna-This-Is-What-You-Came-For-lyrics" into "Calvin-harris-this-is-what-you-came-for-lyrics"
#todo: make "Bruno-Mars-That's-What-I-Like-lyrics" into "Bruno-mars-thats-what-i-like-lyrics" (the ')
#todo: make "Luis-fonsi-and-daddy-yankee-featuring-justin-bieber-despacito-remix-lyrics" into "Luis-fonsi-and-daddy-yankee-despacito-remix-lyrics"
#todo: make for I Wanna Sex You Up (From "New Jack City") into "Color-me-badd-i-wanna-sex-you-up-lyrics"