import matplotlib.pyplot as plt
from wordcloud import WordCloud


def create_cloud(dict_with_song_objs):
    for k,v in dict_with_song_objs.items():
        text = v.lyrics.replace("\n", " ")
        cloud = WordCloud().generate(text)
        plt.imshow(cloud, interpolation="bilinear")
        plt.axis("off")
        plt.show()
        filename = str(k) + ".png"
        cloud.to_file(filename)
