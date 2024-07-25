#This script sends the reddit comments obtained from the reddit API through a network socket on 127.0.0.1 port 5590

#Import necessary packages 
import json
import socket
import praw
from praw.models.reddit.subreddit import SubredditStream


class RedditProducer(SubredditStream):
    def __init__(self, subreddit, socket):
        super().__init__(subreddit)
        self.socket = socket
        
    def run(self):
        #This code iterates through the comments in the chosen subreddits and extracts the chosen fields.
        for comment in self.comments(skip_existing=False):
            #print(dir(comment))
            print("Sending data")
            #Extracting the body, subreddit and created_utc fields
            body = comment.body
            subreddit = comment.subreddit.display_name
            created_utc = comment.created_utc
            data = {
            "body": body,
            "subreddit": subreddit,
            "created_utc": created_utc
            }
            #Sending data in JSON format
            self.socket.send((repr(data) + '\n').encode('utf-8'))



if __name__ == '__main__':
    #Loading API credentials from the config file
    with open("config.json", "r") as jsonfile:
        data = json.load(jsonfile)  
        # print("Config data read successful", data)

    reddit = praw.Reddit(
            client_id=data["client_id"],
            client_secret=data["client_secret"],
            user_agent="COM3021 Reddit Producer"
    )
    #Define server details
    host = '127.0.0.1'
    port = 5590
    address = (host, port)

    #Initializing the socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(address)
    server_socket.listen(5)

    print("Listening for client...")

    conn, address = server_socket.accept()
    #Accepting client connection
    print("Connected to Client at " + str(address))

    #Define subreddits to get data from
    subreddits = reddit.subreddit("AskUK+AskAnAmerican")
    stream = RedditProducer(subreddits, conn)
    #Initialise streaming
    stream.run()