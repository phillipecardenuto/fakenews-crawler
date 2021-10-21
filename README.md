# fakenews-crawler
A Crawler for downloading Twitter and Newspaper related data

# Quick Run

### Install the requirements of the lib in a python 3.6+ environment

We recommend using a virtual environment for this (e.g., [anaconda](https://www.anaconda.com/products/individual))

``` bash
pip install -r requirements.txt
```

The library also requires `exiftool`. A workaround to avoid `root` permission is installing it with conda:

```
conda install -c conda-forge exiftool
```

After this, you should be ready to use the fakenews-crawler without problems :)

## Scrapping the data

### 1 -  Setting up the database

The library uses MongoDB to organize and store the tweets.
As a more praticle way to install MongoDB, we recommend using docker.

*WARNING: The instructions bellow are just a quick run for researching and developing, if you are going to use these databases in a production environment make sure to increase databases security by adding passwords and others security layers.*

Visit [docker-library MongoDB](https://github.com/docker-library/docs/blob/master/mongo/README.md#what-is-mongodb)  or MongoDB tutorials (e.g., [Tutorial by Leon Fang](https://medium.com/@leonfeng/set-up-a-secured-mongodb-container-e895807054bd)) for more information about security.

```bash
# Warninig: we are not adding any authentication layer to the database
docker run -d  --name tweetMongoDB -p <port>:27017 mongo:4.4.6
```

### 2 - Scraping the tweets
The scape function allow the user to input target keywords (e.g., "COVID-19") and frame the search within a 
timeframe (e.g., since:2019, until: 2021).

```python
from fncrawl.tweetDB import TweetDB
from fncrawl.mediaDownload import scrape_tweets
from datetime import datetime

# connect to the collection 'test' of 'testDB' database from a local MongoDB server
# Same port used in docker must be set to the next command
tweet_database = TweetDB(host="localhost", port=<port>, database='testDB',collection='test')

# start scaping tweets with keywords = "COVID19", since 2019
since = datetime.strptime('March 10, 2019', "%B %d, %Y")
scrape_tweets(keyword='COVID19', mongo_database=tweet_database, since=since)
```

After executing the code above, a log of the downloaded tweets will appear, showing each download tweet text.

### 3 - Download media from the tweet body
Download images and videos content embedded in the tweet (shown in the tweet body) 

#### 3.1 Tweet Photos/Images (shown in the tweet body)

**3.1.1 Download Photos/Images Sequentially**

```python
from fncrawl.tweetDB import TweetDB
from tqdm import tqdm

# connect to the collection 'test' of 'testDB' database from a local MongoDB server
# Same port used in docker must be set to the next command
tweet_database = TweetDB(host="localhost", port=<port>, database='testDB',collection='test')

# Select all tweets from the database
tweets = list(tweet_database.tweetDB.find({}))

# For each tweet found, download the photos/images present in its body and save it to <savepath>
savepath = <savepath>
for tweet in tqdm(tweets):
    download_tweet_photos(tweet, savepath)
```

**3.1.2 Download Photos/Images Parallel**

```python
from fncrawl.tweetDB import TweetDB
from fncrawl import pcall_download_tweet_photos
from tqdm.contrib.concurrent import process_map


# connect to the collection 'test' of 'testDB' database from a local MongoDB server
# Same port used in docker must be set to the next command
tweet_database = TweetDB(host="localhost", port=<port>, database='testDB',collection='test')

# Select all tweets from the database
tweets = list(tweet_database.tweetDB.find({}))

# For each tweet found, parallel download the photos/images present in its body and save it to <savepath>
savepath = <savepath>
tweets = [ (t, savepath) for t in tweets]
# call parallel function
process_map (pcall_download_tweet_photos,
             tweets, chunksize=1)
```

#### 3.2 Tweet Videos (shown in the tweet body)

**3.2.1 Download Videos Sequentially**

```python
from fncrawl.tweetDB import TweetDB
from tqdm import tqdm

# connect to the collection 'test' of 'testDB' database from a local MongoDB server
# Same port used in docker must be set to the next command
tweet_database = TweetDB(host="localhost", port=<port>, database='testDB',collection='test')

# Select all tweets from the database
tweets = list(tweet_database.tweetDB.find({}))

# For each tweet found, download the video presented in its body and save it to <savepath>
savepath = <savepath>
for tweet in tqdm(tweets):
    download_tweet_videos_from_link(tweet, savepath)
```

**3.2.2 Download Videos Parallel**

```python
from fncrawl.tweetDB import TweetDB
from fncrawl import pcall_download_tweet_videos_from_link
from tqdm.contrib.concurrent import process_map

# connect to the collection 'test' of 'testDB' database from a local MongoDB server
# Same port used in docker must be set to the next command
tweet_database = TweetDB(host="localhost", port=<port>, database='testDB',collection='test')

# Select all tweets from the database
tweets = list(tweet_database.tweetDB.find({}))

# For each tweet found, parallel download the video presented in its body and save it to <savepath>
savepath = <savepath>
tweets = [ (t, savepath) for t in tweets]
# call parallel function
process_map (pcall_download_tweet_videos_from_link,
             tweets, chunksize=1)
```

#### 3.3 Tweet Media URLs content (cited in the tweet body text)

**Download all related media from the URLs within the tweet body text**

**3.3.1 Sequentially**

```python
from fncrawl.tweetDB import TweetDB
from tqdm import tqdm

# connect to the collection 'test' of 'testDB' database from a local MongoDB server
# Same port used in docker must be set to the next command
tweet_database = TweetDB(host="localhost", port=port, database='testDB',collection='test')

# Select all tweets from the database
tweets = list(tweet_database.tweetDB.find({}))

# For each tweet found, download cited media to <savepath>
savepath = <savepath>
for tweet in tqdm(tweets):
    download_tweet_media_from_urls(tweet, savepath)
```

**3.3.2 Parallel**

```python
from fncrawl.tweetDB import TweetDB
from fncrawl import pcall_download_tweet_media_from_urls
from tqdm.contrib.concurrent import process_map

# connect to the collection 'test' of 'testDB' database from a local MongoDB server
# Same port used in docker must be set to the next command
tweet_database = TweetDB(host="localhost", port=<port>, database='testDB',collection='test')

# Select all tweets from the database
tweets = list(tweet_database.tweetDB.find({}))

# For each tweet found, download cited media to <savepath>
savepath = <savepath>
tweets = [ (t, savepath) for t in tweets]
# call parallel function
process_map (pcall_download_tweet_media_from_urls,
             tweets, chunksize=1)
```



### 4 - Follow Newspaper and Blog articles cited in the Tweet and download their content

As a special feature, the library also allows one to follow all newspaper/blog article cited in a tweet text 
updating the tweet database with the article's text and media content.

This feature enables one to check if the cited article is consistent with the tweet text and 
to check whether the cited article is a source of misinformation.

**Follow articles and save their metadata content in the database**

```python
from fncrawl.tweetDB import TweetDB
from fncrawl import pcall_follow_cited_articles,
from tqdm.contrib.concurrent import process_map

# connect to the collection 'test' of 'testDB' database from a local MongoDB server
# Same port used in docker must be set to the next command
tweet_database = TweetDB(host="localhost", port=<port>, database='testDB',collection='test')

# Select all tweets from the database
tweets = list(tweet_database.tweetDB.find({}))

#For all tweets in the database, parellel follow all cited article from the tweet and scrape their content
pcall_follow_cited_articles(tweets, tweet_database)
```
**Download the articles assets based in their collected metadata**

```python
from fncrawl.tweetDB import TweetDB
from fncrawl import  pcall_download_media_from_article_urls
from tqdm.contrib.concurrent import process_map

# After collecting the articles content
# download their related media into <savepath>
savepath = <savepath>
tweets = [ (t, savepath) for t in tweets]
# call parallel function
process_map (pcall_download_media_from_article_urls,
             tweets, chunksize=1 )
```

# Database structure

### Tweet Metadata scheme

All scrapped tweets follows the [twint](https://github.com/twintproject/twint) document-based scheme, added by a field that explicit indicates the presence of a external News/Blog article URL, which is cited within the tweet body.

**Document-based Tweet Scheme**

```python
{'_id': <tweet_id>_raw_,**Document-based Tweet Scheme**
 '_index': <string> # name of the crawler's tool ,
 '_source': {
      'id': <tweet_id>,
      'conversation_id': <conversation_id>, # Thread tweet id
      'created_at': <string>, # time tweet was created
      'date': <string>, # date of the tweet
      'date_formated': <datetime>, # date of the tweet datetime FORMAT
      'timezone': <string>,
      'place': {
                    'coordinates': [<float>, <float>], # User coordinate while tweeting
                    'type': <string> # Type of coordinate
               },
      'tweet': <string>, # Tweet body text
      'language': <string>, # tweet text language
      'hashtags': [],
      'cashtags': [],
      'user_id_str': <string>, # user id 
      'username': <string>, # Username
      'name': <string>, # name
      'link': <string>, # Link to original tweet
      'retweet': <bool> # Is retweet?tweet_database
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
```



### Tweet Media Database

After downloading the tweets assets, you will find the media content of the Tweets organized as:

```bash
<savepath> # base directory of the media database (input savepath)
  └──<language> # language of the tweet (e.g., 'en' for english)
	      └── <tweet_id> # tweet id typically is a number (e.g., '1450915222089261059')
		      ├── cited_article # directory of all media related to URLs cited in the tweet body text
		      │      └── <link_id>  # link id related to the cited URL (e.g., '0' )
		      │            └── images
		      │            │     └── <image_file> 
		      │            └── videos
		      │            │     └── <video_file> 
		      │            │
		      │            └── <top_image_file> # Image that correspond to the article's thumbnail
		      │            └── text_url.txt # text of the article
		      └── images
		      │     └── <image_file>  # Image embedded in the tweet body
		      └── videos
		            └── <video_file>  # Video embedded in the tweet body

```



##### AUTHORS

Phillipe Cardenuto and José Nascimento,

```
		                     UNICAMP (University of Campinas) RECOD.AI
```

*If you find any bug, please do not hesitate to create a new issue*
