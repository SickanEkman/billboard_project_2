# TAL - Text Analysis of Lyrics

TAL gets Billboard chart info and creates visual output of lyrics. The project is made as a school assignement for the course *Applyed programming for Linguists* at *Stockholm University*.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine.

### Prerequisites

* Python 3
* billboard
* requests
* BeautifulSoup from bs4
* matplotlib.pyplot
* WordCloud from wordcloud

### Installing

Terminal command:

```
git clone https://github.com/SickanEkman/billboard_project_2
```

## Built With

* [Python 3](https://docs.python.org/3/) - TAL is written in Python 3
* [billboard](https://github.com/guoguo12/billboard-charts) - Python API for accessing music charts from Billboard.com
* [requests](http://docs.python-requests.org/en/latest/index.html) - A HTTP library for Python
* [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) - Python library for projects like screen-scraping
* [matplotlib](https://matplotlib.org/) - A Python 2D plotting library
* [wordcloud](https://github.com/amueller/word_cloud) - A little word cloud generator in Python

## Running the program

You start by instantiating your Project object. Decide what time span you want to look at songs from
Billboard for, what specific chart you are interested in, and how many songs you want from each year. The program
will provide a semi-random summer month for each year during your selected time span.

### Features

class Project(first_year=2010, last_year=this_year, chart="radio-songs", num_songs=3)

| Parameters    |                                           |
|---------------|-------------------------------------------|
|first_year: int|The year you wish to start getting billbord charts for|
|last_year: int |The last year of your time period. Defaults to current year|
|chart: str     |Example "radio-hits", "hot-100", see [billboard.com](http://www.billboard.com/charts) for more|
|num_songs:int  |Number of songs you wish to see from each year|

| Methods       |                                           |
|---------------|-------------------------------------------|
|get_clouds()   |Create a word cloud for each song          |

###Examples

```
# Import third party libraries
import json
import datetime

# Import modules
import get_charts
import song_objects

# Instantiate your project
my_project = Project(first_year=2010, chart="radio-songs", num_songs=3)
# inspect json-file. Happy with song selection?

# Create word cloud for each song
my_project.get_clouds()
```

## Authors

[**SickanEkman**](https://github.com/SickanEkman)

## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT) - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* [README inspiration](https://gist.github.com/PurpleBooth/109311bb0361f32d87a2#file-readme-template-md) from [PurpleBooth](https://github.com/PurpleBooth)
* IT support from [Shortlisted](https://github.com/shortlisted)
