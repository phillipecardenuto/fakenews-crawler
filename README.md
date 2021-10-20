# fakenews-crawler
A Crawler for downloading Twitter and Newspaper Data

# Quick Run

### Install the requirements of the lib in a python 3.6+ environment

We recommend using a virtual environment for this (e.g., [anaconda](https://www.anaconda.com/products/individual))

``` bash
pip install -r requirements.txt
```

The library also requires `exiftool`. A workaround to avoid `root` permission to install this module is installing it with conda:

```
conda install -c conda-forge exiftool
```

After this, you should be ready to use the fakenews-crawler without problems.

## Scrapping the data

### 1 -  Setting up the database

The library uses MongoDB to organize and store the tweets.
As a more praticle way to install MongoDB, we recommend using docker.

*WARNING: The instructions bellow are just a quick run for researching and developing, if you are going to use these databases in a production environment make sure to increase databases security by adding passwords and others security layers.*

Visit [docker-library MongoDB](https://github.com/docker-library/docs/blob/master/mongo/README.md#what-is-mongodb)  or MongoDB tutorials (e.g., [Tutorial by Leon Fang](https://medium.com/@leonfeng/set-up-a-secured-mongodb-container-e895807054bd)) for more information about security.

```bash
# Warninig: we are not adding any authentication layer to the database
<<<<<<< HEAD
docker run -d  --name tweetMongoDB -p 27017:27017 mongo
=======
docker run -d  --name tweetMongoDB -p <port>:27017 mongo
>>>>>>> dev
```

### 2 - Scraping the tweets
The scape function allow the user to input target keywords (e.g., "COVID-19") and frame the search within a 
timeframe (e.g., since:2019, until: 2021).

```
from fncrawl.tweetDB import TweetDB
from fncrawl.mediaDownload import scrape_tweets
from datetime import datetime

# connect to the collection 'test' of 'testDB' database from a local MongoDB server
tweet_database = TweetDB(host="localhost", port="27017", database='testDB',collection='test')

# start scaping tweets with keywords = "COVID19", since 2019
since = datetime.strptime('March 10, 2019', "%B %d, %Y")
scrape_tweets(keyword='COVID19', mongo_database=tweet_database, since=since)
```

After executing the code above, a log of the downloaded tweets will appear, showing each download tweet text.



### 3 - Download tweet related media
The library supports downloading all images and videos content embedded in the tweet as well as all associated
urls from image or videos cited  in the tweet body text.

```
TODO insert functions
```

### 4 - Following the tweet cited newspaper/blog article.
As a special feature, the library also allows one to follow all newspaper/blog article cited in a tweet text 
updating the tweet database with the article's text and media content.
This feature enables one to check if the cited article is consistent with the tweet text and 
to check whether the citated article is a source of misinformation.


```
TODO add how to upload the database with the article info
```

```
TODO show the function that download the article media.
```


## Database structure

```
{'_id': <tweet_id>_raw_,
 '_index': <string> # name of the crawler's tool ,
 '_sourc-- Todo insert image of the database scheme
74
e': {
      'id': <tweet_id>,
      'conversation_id': <conversation_id>, # Thread tweet id
      'created_at': <string>, # time tweet was created STRING FORMAT
      'date': <string>, # date of the tweet STRING FORMAT
      'date_formated': <datetime>, # date of the tweet datetime FORMAT
      'timezone': <string>, # STRING FORMAT
      'place': {
                    'coordinates': [<float>, <float>], # User coordinate while tweeting
                    'type': <string> # Type of coordinate
               },
      'tweet': <string>, # Tweet body text
      'language': <string>, # tweet text language
      'hashtags': [],
      'cashtags': [],
      'user_id_str': <tweet_user_id>, # String
      'username': <string>, # Username
      'name': <string>, # name
      'link': <string>, # Link to original tweet
      'retweet': <bool> # Is retweet?
      'nlikes': <int>, # Number of like at time of collection
      'nreplies': <int>, # Number of replies at time of collection
      'nretweets': <string>, # number of retweets
      'quote_url': <string>, # URL to the quote tweet
                             # ICYM: quote_tweet --> ReTweet that allows you to embed your own comments above the original tweet
      'video': <1 or 0>, # 1 - Has video, 0 - Hasn't video
      'search': <string>, # Keyword used while querying the tweet
      'urls': <list>, # List of urls cited in the tweet body text,
      'urls_article_content': {
            <url_1>:
                  {'text': <string> # Text found on 'url_1'
                   'images': [<string>] # List of image urls found on 'url_1'
                   'videos': [<string] # List of videos urls found on 'url_1'
                  }
      }
   }
}

```



