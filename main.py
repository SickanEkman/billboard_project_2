import json
import datetime

import get_charts
import song_objects
import cloud

this_year = datetime.date.today().year


class Project(object):
    def __init__(self, first_year=2015, last_year=this_year, chart="radio-songs", num_songs=3):
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
        will be joined in a time line on a web page. You will also be able to chose if you want each song separately
        or all songs from a date joined into one cloud.) """
        cloud.create_cloud(self.dict_with_song_objs, self.year_dict, cloud_type)


def run_program():
    while True:
        print("\nMENU:")
        choice = input("Hit 'd' for new project with default parameters\n"
                       "Hit 'n' for new project with parameters specified by you\n"
                       "Hit 'q' to exit\n")
        if choice == "d":
            new_project = Project()
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
        elif choice == "n":
            a = int(input("First year: "))
            b = int(input("Last year: "))
            if a > b:
                print("\nFirst year can't be later than last year. Try again!")
                run_program()
            elif a > this_year or b > this_year:
                print("\nUnfortunately I can't get charts from the future. Try again!")
                run_program()
            else:
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
