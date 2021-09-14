# fakenews-crawler
A Crawler for downloading Twitter and Newpaper Data

# Quick Run

### Install the requirements of the lib in a python 3.6+ enviroment

``` bash
$ pip install -r requirements.txt
```

## Setting up the database

*WARNING: The instructions bellow are just a quick run for researching and developing, if you are going to use these databases in a production environment make sure to increase databases security by adding passwords and security layers.*

Visit [docker-library MongoDB](https://github.com/docker-library/docs/blob/master/mongo/README.md#what-is-mongodb)  or MongoDB tutorials (e.g., [Tutorial by Leon Fang](https://medium.com/@leonfeng/set-up-a-secured-mongodb-container-e895807054bd)) for more information about security.

#### 1 - Initialize MongoDB

```bash
# Warninig: we are not adding any authentication layer to the database
docker run -d  --name tweetMongoDB -p 27017:27017 mongo
```

### 2 - Scraping the tweets
The scape function allow the user to input a target keyword (e.g., "COVID-19") and frame the search withing a 
timeline (e.g., since:2019, until: 2021).

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

-- Todo insert image of the database scheme

```
{'_id': <tweet_id>_raw_,
 '_index': <name_of_crawler>,
 '_source': {'id': <tweet_id>,
  'conversation_id': <conversation_id>, # Thread tweet id
  'created_at': <datetime>, # time tweet was created STRING FORMAT
  'date': <datetime>, # date of the tweet STRING FORMAT
  'timezone': <timezone>, # STRING FORMAT
  'place': <tweet's country>,
  'tweet': <tweet text>, # STRING
  'language': <tweet text language>, # String
  'hashtags': [],
  'cashtags': [],
  'user_id_str': <tweet_user_id>, # String
  'username': <tweet_user_name>, # String
  'name': <name>, # String
  'link': <link to original tweet>, # String
  'retweet': <reweet> # Bool
  'nlikes': <number of like at time of collection>, # INT
  'nreplies': <number of replies at time of collection>, # INT
  'nretweets': <number of retweets>, # 'quote_url': '',
  'video': <has embedded video>, # 1 or 0
  'search': <query search>, # String keyword used to query the tweet
  'urls': <list of urls cited in the tweet body text>, # List of strings,
  'urls_article_content': {
        <url_1>:
              {'text': <article text> # Text found on 'url_1'
               'images': [<img_urls>] # List of image urls found on 'url_1'
               'videos': [<videos_urls] # List of videos urls found on 'url_1'
              }
        }   
   }
}

```



