import requests
import datetime
from google_images_download import google_images_download
from random import randint
import string
import keys

#Get the current date
now = datetime.datetime.now().date()

# Data structure for headlines || masterList = [{'source':'news source', 'title':'headline title',
# 'source_url':'the sauce', 'urls': [all downloaded image paths]}]
masterList = []

# Get headlines
url = ('https://newsapi.org/v2/top-headlines?'
       'country=us&pageSize=1&'
       'apiKey=' + keys.newsAPIkey)
response = requests.get(url)

# Add headlines to masterList in structure specified on lines 12 & 13
for thing in response.json()['articles']:
    headLine = thing['title']
    masterList.append({'source':thing['source']['name'], 'title':str(headLine[:headLine.rfind("-")]), 'source_url':thing['url']})

# Get images for each word in headline
response = google_images_download.googleimagesdownload()

# Parameters & initializer for downloading
imageLimit = 3
imageFileNumber = 0
counter = 0

# For each dictionary in the list add list of downloaded image paths
for item in masterList:
    urlList = []
    # Iterate through headline without punctuation
    for word in item['title'].translate(str.maketrans('', '', string.punctuation)).split():
        arguments = {"keywords": word, "limit": imageLimit,
                     "print_urls": False,
                     "output_directory": "static/Resources/Images/%s/%d" % (now, imageFileNumber),
                     'format': 'jpg'}
        paths = response.download(arguments)  # store paths from response

        try:
            randToChoose = randint(0, imageLimit-1)  # choose random image as the one to add to url list
            urlList.append(paths[0][word][randToChoose])
        except IndexError:  # if image does not download try again
            paths = response.download(arguments)
            randToChoose = randint(0, imageLimit - 1)
            urlList.append(paths[0][word][randToChoose])

    masterList[counter]['urls'] = urlList
    imageFileNumber += 1
    counter += 1

    print(masterList[0]['urls'])
