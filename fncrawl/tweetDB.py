"""
Interface with Mongo DB
"""
from typing import Dict
import pymongo
from pymongo import MongoClient

TWEET_ESSENCIAL_FIELDS = [ '_id', '_source' ]
TWEET_ESSENCIAL_SOURCE_FIELDS = ['id','conversation_id', 'created_at',
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

        self._host = host
        self._port = port
        self._username = username
        self._password = password
        self._database = database
        self._collection = collection

        self.__connectDB()

    def __connectDB(self):
        """
        Connect to MongoDB client and select the database and collection from this client
        """
        # Coonect to Client
        if self._username:
            self._server_url = f"mongodb://{self._username}:{self._password}@{self._host}:{self._port}/"
        else:
            self._server_url = f"mongodb://{self._host}:{self._port}/"

        self._client = MongoClient(self._server_url, serverSelectionTimeoutMS = 2000)

        # Check if client is connected
        try:
            self._client.server_info()

        except pymongo.errors.ServerSelectionTimeoutError as err:

            print(f"Could not connect ot server using client: {self.client}")
            raise(err)


        # Get collection from client
        self.tweetDB = eval(f"self._client.{self._database}")
        self.tweetDB = self.tweetDB[self._collection]

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
                     tweet_doc: Dict):
        """
        Insert  a tweet document from MongoDB with the info of 'update_info'
        tweet_id <str>
        Assert that tweet_doc has all essential fields of a regular tweet

        FIELDS = [ '_id', '_source' ]
        _SOURCE_FIELDS = ['id','conversation_id', 'created_at',
                                'date', 'timezone', 'tweet', 'language',
                                 'user_id_str', 'username', 'name', 'link',
                                 'retweet', 'date_formated']
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

        for field in TWEET_ESSENCIAL_SOURCE_FIELDS:
            assert  field in tweet['_source'].keys(), f"{field} is not present in filed '_source'"

