"""
Download Tweet and Media Content Functions
"""

from typing import List, Dict
from datetime import datetime
import os, signal

#from .tweetDB import TweetDB
from  pathlib import Path
from newspaper import Article
import requests
import youtube_dl
import twint


URL_DENIED_LIST = ['https://twitter.com']

def scrape_tweets(
    keyword: str,
    mongo_database: TweetDB,
    since: datetime = None,
    until: datetime = None,
    tweet_user: str = '',

):
    """
    Scrape tDownload tweets and insert in mongo_database

    The keyword search can be formated as:
       'key1 OR key2 AND key3'
    """

    c= twint.Config()
    c.MongoDBurl = mongo_database._server_url
    c.MongoDBdb = mongo_database._database
    c.MongoDBcollection = mongo_database._collection
    c.MongoDB = True
    c.Username = tweet_user if tweet_user else None
    c.Since = datetime.strftime(since, "%Y-%m-%d %H:%M:%S") if since else None  # '2021-09-06 21:00:00 -0300'
    c.Until = datetime.strftime(until, "%Y-%m-%d %H:%M:%S") if until else None #'2021-09-07 00:00:00 -0300'
    c.Search = keyword

    twint.run.Search(c)


def check_url(url):
    """
    Check if url is useful and does not contain
    malicious content.
    We also remove twitter links since it will be already
    adressed by youtube-dl or request
    """
    # Denied List

    for urld in URL_DENIED_LIST:
        if urld in url:
            return False
    return True


def follow_tweet_cited_article(tweet: Dict,
                      mongo_database: TweetDB,
                      base_dir: str,
                      scrap_urls: bool = True,
                      download_media: bool = True):
    """
    Follow the tweets associated urls and save all associated media urls into mongo_database

    Args:
        tweets <dict>:
            tweet docuement
        mongo_database <TweetDB>:
            TweetDB object that the function will perform its operation
    """

    urls_media = dict()
    # Get only non-malicious urls
     
    urls = tweet['_source']['urls'] if tweet['_source'].get('urls') else []
    urls = [url for url in urls if check_url(url)]
    
    if scrap_urls is True:
        for url in urls:
            try:
                urls_media[url] = dict()
    
                article = Article(url)
                article.download()
                article.parse()
    
                # Keep only links, discard raw images.
                urls_media[url]["images"] = [img for img in article.images if img.startswith("https://") or  img.startswith("http://")]
                urls_media[url]["videos"] = list(article.movies)
                urls_media[url]["text"] = article.text
                urls_media[url]["top_image"] = article.top_image if a.has_top_image() else ""
    
            except Exception as e:
                #print(e)
                pass
    
        # Update MongoDB with media from URLs
        if urls_media:
            update_info = {"_source.urls_article_content":urls_media}
            tweet_id = tweet['_source']['id']
            mongo_database.update_tweet(tweet_id, update_info)

    if download_media is True:
        for url_id, url in enumerate(urls):
            print(url_id, url)
            save_dir_base = f"{base_dir}/{tweet['_source']['language']}/{tweet['_source']['id']}/cited_article/{url_id:03d}"

            #images
            print(save_dir_base)
            save_dir = Path(save_dir_base) / Path("images")
            os.makedirs(save_dir, exist_ok=True)

            url_content = tweet["_source"]["urls_article_content"][url]

            if "images" in url_content.keys():
                images = url_content["images"]
                for img in images:
                    filename = os.path.basename(img)
                    savepath = Path(save_dir) / Path(filename)
                    savepath = str(savepath)
                
                    # Download image if not exists
                    if (os.path.isfile(savepath) is False):
                        open(savepath, "wb").write(requests.get(url).content)

            #videos
            save_dir = Path(save_dir_base) / Path("videos")
            os.makedirs(save_dir, exist_ok=True)

            if "videos" in url_content.keys():
                videos = url_content["videos"]
                for link in videos:
                    _youtube_download(link, save_dir)

            #text
            if "text" in url_content.keys():
                text_url = url_content["text"]
                if text_url is not None:
                    savepath = Path(save_dir_base) / Path("text_url.txt")
                    savepath = str(savepath)
    
                    with open(savepath, "w") as text_file:
                        text_file.write(text_url)

            #top_image
            if "top_image" in url_content.keys():
                top_image = url_content["top_image"]
                if top_image is not None:
                    filename = os.path.basename(top_image)
                    savepath = Path(save_dir_base) / Path(filename)
                    savepath = str(savepath)
    
                    # Download image if not exists
                    if (os.path.isfile(savepath) is False):
                        open(savepath, "wb").write(requests.get(url).content)


#########################################################
#                Youtube DL handler                     #
#########################################################
class YTQuietLogger(object):
    """
    Class to make the logger quiet
    """
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        pass


def handler_timeout(cls, signum):
    """ just a timeout handler :) """
    raise Exception()

def save_desc(dictMeta, directory):
    """
    Save the description of a video using the Json from yt-dl
    in 'directory'
    """
    if dictMeta.get('description'):
        desc_file = os.path.join(directory, 'description.txt')
        with open(desc_file, 'w') as f:
            f.write(dictMeta.get('description'))

def _youtube_download(link: str,
                     directory: str,
                      max_duration: int = 300):
    """
    Youtube-DL download

    Save media from link at directory with name <id>.<ext>
    The id will be retrived automatically from the link
     """

    try:

        # set Timeout alarm
        signal.signal(signal.SIGALRM, handler_timeout)
        signal.alarm(10*60)


        output = os.path.join(directory,'%(id)s.%(ext)s')

        ydl_opts = {'outtmpl': output,
                   'socket_timeout': 60,
                   'quiet': True,
                   'logger': YTQuietLogger(), # Silence Yt-dl errors
                   'match_filter': youtube_dl.utils.match_filter_func("!is_live")} # Avoid live streams

        # Get Video duration
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                dictMeta = ydl.extract_info(link, download=False)

        # Download playlists, asserting that each downloaded video has lt 'max_duration'
        if dictMeta.get('_type'):
            if dictMeta['_type'] == 'playlist':
                items = [item+1 for item, entry in enumerate(dictMeta['entries']) if entry['duration'] < max_duration]
                ydl_opts['playlist_items'] = ", ".join([str(i) for i in items])
                if items:
                    os.makedirs(directory, exist_ok=True)
                    # Download Video
                    youtube_dl.YoutubeDL(ydl_opts).download([link])

                    # Save Video Description
                    save_desc(dictMeta, directory)

        # Download videos that aren't playlist and have duration lt 'duration'
        elif dictMeta.get('duration'):

            if dictMeta['duration'] < max_duration:

                # Create dir if not exists
                os.makedirs(directory, exist_ok=True)

                # Download Video
                youtube_dl.YoutubeDL(ydl_opts).download([link])

                # Save Video Description, if exists
                save_desc(dictMeta, directory)

    except Exception as e:
        print(e)
        pass

    finally:
        # Disarm Timeutl alarm
        signal.alarm(0)


def download_tweet_videos_from_link(tweet: Dict,
                         save_dir: str,
                         max_duration: int  = 300):
    """
    Download videos content from a tweet using youtube-dl
    If the tweet has a image in its 'links', it also might be download and saved in "save_dir"

    Args:
        tweet: Tweet document in dict format
        save_dir: Path to output directory
        max_duration: Maximum video duration (in seconds) allowed to save the video.
                      This argument avoids download long videos.
    """

    link =  tweet['_source']['link']

    save_dir = f"{save_dir}/{tweet['_source']['language']}/{tweet['_source']['id']}/videos/link/"

    # Download Images and Videos using youtube_dl
    _youtube_download(link, save_dir, max_duration)


def download_tweet_videos_from_urls(tweet: Dict,
                         save_dir: str,
                         max_duration: int  = 300):
    """
    Download associated url videos cited in tweet text using youtube-dl
    Args:
        tweet: Tweet document in dict format
        save_dir: Path to output directory
        max_duration: Maximum video duration (in seconds) allowed to save the video.
                      This argument avoids download long videos.
    """
    if tweet['_source'].get('urls') is None:
        return

    urls = tweet['_source']['urls'] if tweet['_source'].get('urls') else []
    urls = [url for url in urls if check_url(url)]
    
    for url_id, url in enumerate(urls):

        save_dir = f"{save_dir}/{tweet['_source']['language']}/{tweet['_source']['id']}/videos/{url_id:03d}"

        # Download Images and Videos using youtube_dl
        _youtube_download(url, save_dir, max_duration)


#########################################################
#                Requests   handler                     #
#########################################################

def download_tweet_photos(tweet: Dict,
                          save_dir:str,
                          overwrite: bool = False):
    """
    Download photos from tweet

    """

    if tweet['_source'].get('photos') is None:
        return

    # Fix Save Dir
    save_dir = f"{save_dir}/{tweet['_source']['language']}/{tweet['_source']['id']}/images"

    for url in tweet['_source'].get('photos'):
        filename = os.path.basename(url)
        # Create dir if not exists
        os.makedirs(save_dir, exist_ok=True)

        # Include filename to savepath
        savepath = Path(save_dir) / Path(filename)
        savepath = str(savepath)

        # Download image if not exists
        if (os.path.isfile(savepath) is False) or overwrite:
            open(savepath, "wb").write(requests.get(url).content)



