import json
import datetime
import billboard
import random
import requests
from bs4 import BeautifulSoup
import re
import matplotlib.pyplot as plt
from wordcloud import WordCloud

this_year = datetime.date.today().year

class Project(object):
    def __init__(self, first_year=2017, last_year=this_year, chart="radio-songs", num_songs=5):
        """Gets Billboard chart info and instantiates a song object for each hit."""
        self.first_year = first_year
        self.last_year = last_year
        self.chart_name = chart
        self.number_of_songs = num_songs
        self.year_dict = self.create_year_data(first_year, last_year)
        self.date_list = self.create_date_list(self.year_dict)
        self.collect_charts(self.date_list, self.chart_name, self.number_of_songs)
        self.dict_with_song_objs = self.create_song_objects()

    def create_year_data(self, first_y, last_y):
        """Creates dictionary with every relevant year as value. Example: {1:2000, 2:2001, 3:2002, ...}"""
        counter = 1
        year_dict = {}
        while first_y <= last_y:
            year_dict[str(counter)] = str(first_y)
            first_y += 1
            counter += 1
        return year_dict

    def create_date_list(self, year_dict):
        """Creates list with semi-random summer dates for every relevant year.
        Example: [2000-06-01, 2000-08-20, 2001-07-15, ...]"""
        date_list = []
        for k, v in year_dict.items():
            rand_summer_month = "%02d" % random.randint(6, 8)
            rand_day = "%02d" % random.randint(1, 30)
            rand_date = v + "-" + str(rand_summer_month) + "-" + str(rand_day)
            date_list.append(rand_date)
        return date_list

    def collect_charts(self, date_list, chart_name, number_of_songs):
        """Uses billboard API to get relevant charts. Saves data (song title, artist, rank on chart and date) to
        json-file 'chart_songs.json'. Every song saved with key: '[year]_[rank - 1]' """
        json_dict = {}
        for date in date_list:
            # print("Getting a chart")  # printing to let user know program is running
            year = date[0:4]  # Example: saves "2000" from "2000-06-01"
            song_count = 0
            chart = billboard.ChartData(chart_name, date=date)  # if no chart available - next possible date returned
            while song_count < number_of_songs:
                song = chart[song_count]
                chart_hit_dict = {"date": chart.date, "rank": song.rank, "title": song.title, "artist": song.artist}
                json_dict[year + "_" + str(song_count)] = chart_hit_dict
                song_count += 1
        with open("chart_songs.json", "w") as fout:
            fout.write(json.dumps(json_dict))
        fout.close()

    def create_song_objects(self):
        """For each song in the json-file a song object is instantiated. Returns a dictionary with all song objects.
        Example: {"song_2000_0": <__main__.Song_obj...>, "song_2000_1": <__main__.Song_obj...>}"""
        song_obj_dict = {}
        with open("chart_songs.json", "r") as fin:
            song_data = json.load(fin)
            for k, v in song_data.items():
                try:
                    name = "song_" + str(k)
                    song_obj_dict[name] = SongObj(v)  # instantiates the song object
                except AttributeError:
                    print("COULDN'T FIND LYRICS FOR THIS SONG:", v["title"], "by", v["artist"])
                    pass  # if the url didn't return a lyric no object is created for the song
        return song_obj_dict

    def get_clouds(self, cloud_type="year"):
        if cloud_type == "song":
            for k, v in self.dict_with_song_objs.items():
                text = v.lyrics.replace("\n", " ")
                cloud = WordCloud(collocations=False).generate(text)
                plt.imshow(cloud, interpolation="bilinear")
                plt.axis("off")
                # plt.show()
                filename = str(k) + ".png"
                cloud.to_file(filename)
        elif cloud_type == "year":
            counter = 1
            while counter <= len(self.year_dict):
                text = ""
                for k, v in self.dict_with_song_objs.items():
                    if self.year_dict[str(counter)] in k:
                        text = text + "\n" + v.lyrics
                text = text.replace("\n", " ")
                cloud = WordCloud(collocations=False).generate(text)
                plt.imshow(cloud, interpolation="bilinear")
                plt.axis("off")
                # plt.show()
                filename = self.year_dict[str(counter)] + ".png"
                cloud.to_file(filename)
                counter += 1
        print("\nWord clouds created - take a look in your project folder!")


class SongObj(object):
    def __init__(self, song_info):
        """Saves argument info as class attributes. Gets lyrics for each song and saves as class attribute"""
        self.artist = song_info["artist"]
        self.title = song_info["title"]
        self.rank = song_info["rank"]
        self.date = song_info["date"]
        self.lyrics = self.get_lyrics()

    def get_lyrics(self):
        url = self.create_url_for_genius(1)
        try:
            r = requests.get(url)
            r.raise_for_status()
        except requests.exceptions.HTTPError:
            url = self.create_url_for_genius(2)
            try:
                r = requests.get(url)
                r.raise_for_status()
            except requests.exceptions.HTTPError:
                url = self.create_url_for_genius(3)
                r = requests.get(url)  # if this last url option doesn't work I give up ...
        data = r.text
        lyrics = self.read_html(data)
        return lyrics

    def create_url_for_genius(self, x=1):
        base_url = "https://genius.com/"
        url_ending = ""  # will be defined in if-else clauses
        regex_and = r"&"  # matches the literal "&"
        regex_punct = r"[^\w\-\s]"  # matches everything except alphanumerics, dashes and whitespaces
        regex_feat = r" Featuring.*"  # matches the word "Featuring" and any characters following it"
        regex_parenthesis = r"\s\(.*\)"  # matches parenthesis and anything inside them
        regex_dollar = r"\$"  # matches the literal "$"
        regex_exl_mark = r"(!)(\w)"  # matches an exclamation mark followed by an alphanumeric
        regex_space = r"\s"  # matches whitespace
        artist_url = re.sub(regex_feat, "", self.artist)
        artist_url = re.sub(regex_and, "and", artist_url)
        artist_url = re.sub(regex_dollar, "s", artist_url)
        artist_url = re.sub(regex_exl_mark, r"i\2", artist_url)
        title_url = re.sub(regex_and, "and", self.title)
        title_url = re.sub(regex_exl_mark, r"i\2", title_url)  # change first group to "i" and keep second group
        if x == 1:
            url_ending = "-lyrics"
        elif x == 2:
            title_url = re.sub(regex_parenthesis, "", title_url)
            url_ending = "-lyrics"
        elif x == 3:
            title_url = re.sub(regex_parenthesis, "", title_url)
            url_ending = "-remix-lyrics"
        artist_url = re.sub(regex_punct, "", artist_url)
        artist_url = re.sub(regex_space, "-", artist_url)
        title_url = re.sub(regex_punct, "", title_url)
        title_url = re.sub(regex_space, "-", title_url)
        final_url = base_url + artist_url + "-" + title_url + url_ending
        return final_url

    def read_html(self, data):
        soup = BeautifulSoup(data, "html.parser")  # gets the HTML doc
        lyrics_as_list = []
        small_soup = soup.find("div", class_="lyrics")  # finds the right part of the HTML code
        mini_soup = small_soup.text  # reads only what's between the brackets
        mini_soup_as_list = mini_soup.split("\n")
        for line in mini_soup_as_list:
            if "[" in line or (len(line) == 0) or line.startswith("Chorus"):
                pass  # skips empty lines and lines with meta info
            elif line.startswith("(") and line.endswith(")"):  # breaking up conditions for readability
                pass  # skips more lines with meta info
            else:
                lyrics_as_list.append(line)
        lyrics = "\n".join(lyrics_as_list)
        return lyrics


def run_program():
    while True:
        print("\nMENU:")
        choice = input("Hit 'd' for new project with default parameters\n"
                       "Hit 'n' for new project with parameters specified by you\n"
                       "Hit 'q' to exit\n")
        if choice == "d" or choice == "n":
            if choice == "d":
                new_project = Project()
            elif choice == "n":
                a = int(input("First year: "))
                b = int(input("Last year: "))
                if a > b:
                    print("\nFirst year can't be later than last year. Try again!")
                    a = int(input("First year: "))
                    b = int(input("Last year: "))
                elif a > this_year or b > this_year:
                    print("\nUnfortunately I can't get charts from the future. Try again!")
                    a = int(input("First year: "))
                    b = int(input("Last year: "))
                c = input("Chart name: ")
                d = int(input("Number of songs for each year: "))
                new_project = Project(first_year=a, last_year=b, chart=c, num_songs=d)
            print("\nTake a look at the json-file created in the project folder. Happy with the song selection?")
            print("MENU:")
            choice2 = input("Hit 's' to create a word cloud for each SONG\n"
                            "Hit 'y' to create a word cloud for each YEAR\n"
                            "Hit 'b' to start over from the beginning\n"
                            "Hit 'q' to exit\n")
            if choice2 == "s":
                new_project.get_clouds(cloud_type="song")
            elif choice2 == "y":
                new_project.get_clouds(cloud_type="year")
            elif choice2 == "q":
                print("Goodbye!")
                quit()
            else:
                run_program()
        elif choice == "q":
            print("Goodbye!")
            quit()
        else:
            print("\nI didn't get that, try again.")
            run_program()

if __name__ == "__main__":
    run_program()
