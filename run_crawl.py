from fncrawl import *
from datetime import datetime

"""
Missing Parallel fuction for download media from articles
"""
"""
# Test scrape_tweets
tweetDB = TweetDB(
                 host = 'localhost',
                 port = '5013',
                 database = 'socialTrack',
                 collection = 'tweets-7Sep',
)
"""
"""
tweetDB = TweetDB(
                 host = 'localhost',
                 port = '5013',
                 database = 'socialTrack',
                 collection = 'tweets-8-11-Sep',
)
"""
tweetDB = TweetDB(
                 host = 'localhost',
                 port = '5013',
                 database = 'socialTrack',
                 collection = 'tweets-12Sep',
)
"""
# follow tweet parallel
from tqdm.contrib.concurrent import process_map, thread_map
tweets = list(tweetDB.tweetDB.find({
                "_source.language":{'$in': ['pt','en','es']}
} ))
database_info = {
    'host' : 'localhost',
    'port' : '5013',
    'database' : 'socialTrack',
    'collection' : 'tweets-12Sep',
}
pcall_follow_cited_articles(tweets, tweetDB)
"""

# download tweets photos
"""
from tqdm import tqdm
tweets = list(tweetDB.tweetDB.find({}))
for tweet in tqdm(tweets):
    download_tweet_photos(tweet,"test")
"""

# download tweets photos in parallel
"""
from tqdm.contrib.concurrent import process_map
tweets = list(tweetDB.tweetDB.find({
                "_source.language":{'$in': ['pt','en','es']}
}))

save_path = "/home/dejavu/datasets/social-tracker-events/collections/7Setembro/media_12"
tweets = [ (t, save_path) for t in tweets]
process_map (pcall_download_tweet_photos,
             tweets,chunksize=1)
"""


# download tweets media from url 
"""
from tqdm import tqdm
tweets = list(tweetDB.tweetDB.find({}))
for tweet in tqdm(tweets):
    download_tweet_videos_from_urls(tweet,"test")
"""


# download tweets photos in parallel
"""
from tqdm.contrib.concurrent import process_map
tweets = list(tweetDB.tweetDB.find({
                "_source.language":{'$in': ['pt','en','es']}
        }))

save_path = "/home/dejavu/datasets/social-tracker-events/collections/7Setembro/media_12"
tweets = [ (t, save_path) for t in tweets]
process_map (pcall_download_tweet_media_from_urls,
             tweets,
             max_workers=20)
"""


# download tweets videos using links
"""
from tqdm import tqdm
tweets = list(tweetDB.tweetDB.find({}))
for tweet in tqdm(tweets):
    download_tweet_videos_from_link(tweet,"test")
    """


"""
# download tweets photos in parallel
from tqdm.contrib.concurrent import process_map
tweets = list(tweetDB.tweetDB.find({}))
tweets = [ (t, "test") for t in tweets]
save_path = "/home/dejavu/datasets/social-tracker-events/collections/7Setembro/media_12"
tweets = [ (t, save_path) for t in tweets]
process_map (pcall_download_tweet_videos_from_link,
             tweets, chunksize=1, max_workers=10)
"""

# download media from metioned tweets articles
"""
from tqdm import tqdm
tweets = list(tweetDB.tweetDB.find({}))
for tweet in tqdm(tweets):
    download_media_from_article_urls(tweet,"test")
"""
from tqdm.contrib.concurrent import process_map
tweets = list(tweetDB.tweetDB.find({
                "_source.language":{'$in': ['pt','en','es']}
        }))
save_path = "/home/dejavu/datasets/social-tracker-events/collections/7Setembro/media_l2"
tweets = [ (t, save_path) for t in tweets]
process_map (pcall_download_media_from_article_urls,
             tweets, chunksize=1)
