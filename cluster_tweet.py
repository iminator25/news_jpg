import sys
from PIL import Image
import tweepy
import os
import shutil
import keys
import math

class createCluster():
    name_number = 0
    new_height = 350

    def __init__(self, urls, r, g, b):
        self.urls = urls
        self.background = (r, g, b)
        self.images = list(map(Image.open, self.urls))
        self.img_length = len(self.images)
        self.count = 0
        self.imgs_per_row = 3

    def resizeImages(self):
        index = 0
        for im in self.images:
            new_width = (createCluster.new_height*im.width)//im.height
            im = im.resize((new_width,createCluster.new_height), Image.ANTIALIAS)
            im.save(self.urls[index], "JPEG")
            self.images = list(map(Image.open, self.urls))
            index += 1
        print(self.img_length)

    def createCluster(self):
        width_per_row = []
        temp = 0

        for im in self.images:
            temp += im.width
            self.count += 1
            if self.count == self.imgs_per_row:
                width_per_row.append(temp)
                temp = 0
                self.count = 0
        self.count = 0

        total_width = max(width_per_row)
        max_height = math.ceil(self.img_length/self.imgs_per_row) * createCluster.new_height

        new_im = Image.new('RGB', (total_width, max_height), self.background)
        x_offset = 0
        y_coord = 0

        for im in self.images:
            if self.count > self.imgs_per_row - 1:
                y_coord += createCluster.new_height
                x_offset = 0
                self.count = 0
            new_im.paste(im, (x_offset,y_coord))
            x_offset += im.size[0]
            im.close()
            self.count += 1

        self.path_to_image = '%d.jpg' % createCluster.name_number
        new_im.save(self.path_to_image)
        createCluster.name_number += 1
        return self.path_to_image

class TweetIt:

    def __init__(self, img, headline):
        self.img = img
        self.headline = headline

    def authorize(self):
        auth = tweepy.OAuthHandler(keys.twitCAPI, keys.twitCAPISecret)
        auth.set_access_token(keys.twitAccess, keys.twitAccessSecret)
        self.api = tweepy.API(auth)

    def tweet(self):
        self.api.update_with_media(self.img, status=self.headline)



for entry in headline_image.masterList:
    print(entry['urls'])
    newCluster = createCluster(entry['urls'], 0, 0, 0)
    newCluster.resizeImages()
    path = newCluster.createCluster()

    newTweet = TweetIt(path, "\"" + entry['title'] + "\"" + " -" + entry['source'] + " " + "(" + entry['source_url'] + ")")
    newTweet.authorize()
    newTweet.tweet()
    os.remove(path)
    # shutil.rmtree('/Users/calebcarithers/Documents/news_jpg/static/Resources/Images')

