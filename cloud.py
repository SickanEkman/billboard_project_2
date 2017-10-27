import matplotlib.pyplot as plt
from wordcloud import WordCloud


def create_cloud(dict_with_song_objs, year_dict, cloud_type="year"):
    if cloud_type == "song":
        for k, v in dict_with_song_objs.items():
            text = v.lyrics.replace("\n", " ")
            cloud = WordCloud(collocations=False).generate(text)
            plt.imshow(cloud, interpolation="bilinear")
            plt.axis("off")
            #plt.show()
            filename = str(k) + ".png"
            cloud.to_file(filename)
    elif cloud_type == "year":
        counter = 1
        while counter <= len(year_dict):
            text = ""
            for k, v in dict_with_song_objs.items():
                if year_dict[str(counter)] in k:
                    text = text + "\n" + v.lyrics
            text = text.replace("\n", " ")
            cloud = WordCloud(collocations=False).generate(text)
            plt.imshow(cloud, interpolation="bilinear")
            plt.axis("off")
            #plt.show()
            filename = year_dict[str(counter)] + ".png"
            cloud.to_file(filename)
            counter += 1
