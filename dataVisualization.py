# -*- coding: utf-8 -*-
"""
Created on Wed May 27 10:09:56 2015

@author: todd
"""

from pymongo import MongoClient
import matplotlib.pyplot as plt
from scipy.misc import imread

from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

import dataStatistics as ds

client = MongoClient()
db = client['big_data']

def word_list_dailymotion(mean, std):
    dailymotion = db.dailymotion
    words = ""
    for video in dailymotion.find():
        if video["views_total"] > (mean + 2 * std):
            words = words + " " + video["title"]
    return words

def word_list_yt(mean, std):
    youtube = db.youtube
    words = ""
    for video in youtube.find():
        if int(video["statistics"]["viewCount"]) > (mean + 2 * std):
            words = words + " " + video["snippet"]["title"]
    return words

def main():
    dm = ds.acquire_dailymotion()
    dmimg = imread("dmlogo.png")
    # Read the whole text.
    wc = WordCloud(mask=dmimg)
    image_colors = ImageColorGenerator(dmimg)
    wc.generate(word_list_dailymotion(ds.mean(dm[0]), ds.standard_deviation(dm[0])))
    
    
    # Open a plot of the generated image.
    plt.imshow(wc.recolor(color_func=image_colors))
    plt.axis("off")
    plt.savefig('popularWordsDM.png', bbox_inches = 'tight', dpi = 600)
    
    yt = ds.acquire_youtube()
    ytimg = imread("ytlogo.png")
    wc = WordCloud(mask=ytimg)
    image_colors = ImageColorGenerator(ytimg)
    wc.generate(word_list_yt(ds.mean(yt[0]), ds.standard_deviation(yt[0])))
    
    plt.imshow(wc.recolor(color_func = image_colors))
    plt.axis("off")
    plt.savefig('popularWordsYT.png', bbox_inches = 'tight', dpi = 600)
    
if __name__ == "__main__":
    main()