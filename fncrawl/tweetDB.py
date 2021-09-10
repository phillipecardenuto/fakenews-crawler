"""
Interface with Mongo DB
"""
from typing import Dict
import pymongo
from pymongo import MongoClient

TWEET_ESSENCIAL_FIELDS = [ '_id', '_source' ]
TWEET_ESSENCUAK_SOURCE_FIELDS = ['id','conversation_id', 'created_at',
                                'date', 'timezone', 'tweet', 'language',
                                 'user_id_str', 'username', 'name', 'link',
                                 'retweet', 'date_formated']
class TweetDB(object):



    def __init__(self,
                 host: str,
                 port: str,
                 database: str,
                 collection: str,
                 username: str ='',
                 password: str =''
                 ):
        """
        Interface with a MongoDB databaset to store and load
        tweet documents
        Args:
            host <str>: hostname
            port <str>: port
            database <str>: MongoDB database
            collection <str>: Collection of MongoDB database
            username <str> (optional)
            password <str> (optional)
        """

        self.host = host
        self.port = port
        self.usernam = username
        self.password = password
        self.database = database
        self.collection = collection

        self.__connectDB()

    def __connectDB(self):
        """
        Connect to MongoDB client and select the database and collection from this client
        """
        # Coonect to Client
        if self.username:
            self.client = MongoClient(f"mongodb://{self.username}:{self.password}@{self.host}:{self.port}/")
        else:
            self.client = MongoClient(f"mongodb://{self.host}:{self.port}/",
                                           serverSelectionTimeoutMS = 2000)

        # Check if client is connected
        try:
            self.client.serverInfo()

        except pymongo.errors.ServerSelectionTimeoutError as err:

            print(f"Could not connect ot server using client: {self.client}")
            raise(err)


        # Get collection from client
        self.tweetDB = eval(f"self.client.{self.database}")
        self.tweetDB = self.tweetDB[self.collection]

        return self.tweetDB


    def update_tweet(self,
                     tweet_id: str,
                     update_info: Dict):
        """
        Update a tweet document from MongoDB with the info of 'update_info'

        tweet_id <str>
        """

        self.tweetDB.update({"_id": f"{tweet_id}_raw_"}, {"$set": update_info})


    def insert_tweet(self,
                     tweet_id: str,
                     update_info: Dict):
        """
        Insert  a tweet document from MongoDB with the info of 'update_info'
        tweet_id <str>
        """

        self.__assert_tweet_fields(update_info)
        self.tweetDB.update({"_id": f"{tweet_id}_raw_"}, {"$set": update_info})


    def remove_tweet(self,
                    tweet_id: str
                     ):
        """
        Removes a tweet document with id equal 'tweet_id'.
        """

        self.tweetDB.delete_one({"_id": f"{tweet_id}_raw_"})

    def get_tweet_by_id(self,
                        tweet_id: str
                        ):
        """
        Retrieves a tweet document, if exists, from the MongoDB database
        If none tweet was found, returns None
        """

        asw = self.tweetDB.find_one({"_id": f"{tweet_id}_raw_"}, {'_source':1})

        if asw:
            return asw.get('_source')

        return asw

    def __assert_tweet_fields(self, tweet):

        for field in TWEET_ESSENCIAL_FIELDS:
            assert  field in tweet.keys(), f"{field} is not present in tweet document"

        for field in TWEET_ESSENCUAK_SOURCE_FIELDS:
            assert  field in tweet['_source'].keys(), f"{field} is not present in '_source' tweet document"

