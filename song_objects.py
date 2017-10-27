import requests
from bs4 import BeautifulSoup
import re


class SongObj(object):
    def __init__(self, song_info):
        """Saves forwarded info as object attributes. Gets lyrics for each song and saves as attribute"""
        self.artist = song_info["artist"]
        self.title = song_info["title"]
        self.rank = song_info["rank"]
        self.date = song_info["date"]
        self.lyrics = self.get_lyrics()

    def get_lyrics(self):
        try:
            url = self.create_url_for_genius(1)  # the "1" means a default url is created
            r = requests.get(url)
            r.raise_for_status()  # if this returns None the url pointed to a proper web address
        except:  # some 4xx or 5xx server error response was returned in .raise_for_status()
            try:
                url = self.create_url_for_genius(2)  # the "2" means an alternative url is created
                r = requests.get(url)
                r.raise_for_status()
            except:
                url = self.create_url_for_genius(3)  # the "3" means yet another alternative url is created
                r = requests.get(url)  # if this last url option doesn't work I give up ...
        data = r.text
        lyrics = self.read_html(data)
        return lyrics

    def create_url_for_genius(self, x=1):
        base_url = "https://genius.com/"
        url_ending = ""  # will be defined later
        regex_and = r"&"  # matches the literal "&"
        regex_punct = r"[^\w\-\s]"  # matches everything except alphanumerics, dashes and whitespaces
        regex_feat = r" Featuring.*"  # matches the word "Featuring" and any characters following it"
        regex_parenthesis = r"\s\(.*\)"  # matches parenthesis and anything inside them
        regex_dollar = r"\$"  # matches the literal "$"
        regex_exl_mark = r"(!)(\w)"  # matches an exclamation mark followed by an alphanumeric
        regex_space = r"\s"
        artist_url = re.sub(regex_feat, "", self.artist)
        artist_url = re.sub(regex_and, "and", artist_url)
        artist_url = re.sub(regex_dollar, "s", artist_url)
        artist_url = re.sub(regex_exl_mark, "i", artist_url)
        title_url = re.sub(regex_and, "and", self.title)
        title_url = re.sub(regex_exl_mark, "i", title_url)
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
            if "[" in line or (len(line) == 0) or line.startswith("Chorus") or (line.startswith("(") and
                                                                                    line.endswith(")")):
                pass  # skips empty lines and lines with meta info
            else:
                lyrics_as_list.append(line)
        lyrics = "\n".join(lyrics_as_list)
        return lyrics
