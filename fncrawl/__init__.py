# -*- coding: utf-8 -*-
__title__ = 'fakenews-crawler'
__author__ = 'Joao Phillipe Cardenuto, Jose Nascimento'
__license__ = 'MIT'
__copyright__ = 'Copyright 2021, J.N., J.P.C.'


from .tweetDB import TweetDB
from .mediaDownload import (scrape_tweets,
                            check_file,
                            follow_tweet_cited_article,
                            pcall_follow_cited_articles,
                            # Tweets photos
                            download_tweet_photos,
                            pcall_download_tweet_photos,

                            # Tweet Videos using URL
                            download_tweet_videos_from_urls,
                            pcall_download_tweet_videos_from_urls,

                            # Tweet Videos using links
                            download_tweet_videos_from_link,
                            pcall_download_tweet_videos_from_link,

                            # Tweet media from articles urls
                            download_media_from_article_urls,
                            pcall_download_media_from_article_urls

                           )
