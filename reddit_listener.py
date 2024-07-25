#This script is used to colect data from the Reddit Stream API
#Import necessary packages 
import json
import praw
import pandas as pd
from datetime import datetime, timedelta
import time

#Import API config credentials
with open("config.json", "r") as jsonfile:
    data = json.load(jsonfile) # Reading the config file
    print("Config data read successful",data)
    

#Set up Praw 
reddit = praw.Reddit(
        client_id = data["client_id"],
        client_secret = data["client_secret"],
        user_agent="COM3021 Reddit Listener")


#Set the duration of the data collection to 4 hours (240 minutes)
collection_duration_minutes = 240
end_time = datetime.utcnow() + timedelta(minutes=collection_duration_minutes)

#Store data in a list of dictionaries
data_list = []

#Select the subreddits to stream data from
stream = reddit.subreddit("AskUK+AskAnAmerican").stream

for comment in stream.comments(skip_existing=True):
    #Check if the current time exceeds the end time for data collection
    if datetime.utcnow() > end_time:
        break

    print(comment.body)

    #Extract desired attributes from the data
    comment_data = {
        "author": comment.author.id if comment.author else "[deleted]",
        "id": comment.id,
        "submission": comment.link_id.split("_")[-1],
        "body": comment.body,
        "subreddit": comment.subreddit.display_name,
        "created_utc": datetime.utcfromtimestamp(comment.created_utc),
        "collected_utc": datetime.utcnow()
    }
    
    #Append the comment dictionary to the list
    data_list.append(comment_data)

    #Add sleep of 1 sec to avoid API limit
    time.sleep(1)

#Convert the data to a pandas dataframe
df = pd.DataFrame(data_list)

#Export the pandas dataframe to a csv file
df.to_csv("reddit_data.csv", index=False)

