import json
import datetime

import get_charts
import song_objects
import cloud

this_year = datetime.date.today().year


class Project(object):
    def __init__(self, first_year=2010, last_year=this_year, chart="radio-songs", num_songs=3):
        """Gets Billboard chart info and instantiates a song object for each hit."""
        self.first_year = first_year
        self.last_year = last_year
        self.chart_name = chart
        self.number_of_songs = num_songs
        self.year_dict, self.date_list = self.get_songs_from_billboard()
        self.dict_with_song_objs = self.create_song_objects()

    def get_songs_from_billboard(self):
        """Gets charts from billboard, saves song info to one json-file. Returns dictionary with years + list with
        dates."""
        year_dict = get_charts.create_year_data(self.first_year, self.last_year)  # Example {1: 2000, 2: 2001, ...}
        date_list = get_charts.create_date_list(year_dict)  # Example {"2000-06-01", "2000-08-20", ...}
        get_charts.collect_charts(date_list, self.chart_name, self.number_of_songs)  # saves chart info as
        # json-file
        return year_dict, date_list

    def create_song_objects(self):
        """For each song in the json-file a song object is instantiated. Returns a dictionary with all song objects.
        Example: {"song_2000_0": <__main__.Song_obj...>, "song_2000_1": <__main__.Song_obj...>}"""
        song_obj_dict = {}
        with open("chart_songs.json", "r") as fin:
            song_data = json.load(fin)
            for k, v in song_data.items():
                try:
                    name = "song_" + str(k)
                    song_obj_dict[name] = song_objects.SongObj(v)  # instantiates the song object
                except AttributeError:
                    print("COULDN'T FIND LYRICS FOR THIS SONG:", v["title"], "by", v["artist"])
                    pass  # if the url didn't return a lyric no object is created for the song
        return song_obj_dict

    def get_clouds(self, cloud_type):
        """For each song object, a word cloud is generated and displayed as a picture. (In the future these word clouds
        will be joined in a timeline on a web page. You will also be able to chose if you want each song separately
        or all songs from a date joined into one cloud.) """
        cloud.create_cloud(self.dict_with_song_objs, self.year_dict, cloud_type)


# BELOW IS USER INPUT, todo: remove later

#first_project = Project(first_year=1990, num_songs=5)
#first_project.get_clouds(cloud_type="year")
