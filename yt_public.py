# -*- coding: utf-8 -*-

# Sample Python code for youtube.commentThreads.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/code-samples#python

from multiprocessing.resource_sharer import stop
import os

from dotenv import load_dotenv 

import googleapiclient.discovery 

from utils.comments import process_comments, make_csv

from utils.videos import process_video_info, raw_video_list, has_comments, process_views_likes


load_dotenv()

api_key = os.getenv("api_key")

api_service_name = "youtube"
api_version = "v3"
youtube = googleapiclient.discovery.build(
    api_service_name, api_version, developerKey = api_key)

playlist = 'PLirAqAtl_h2r5g8xGajEwdXd3x1sZh8hC'


videoList = raw_video_list(playlist)

print(videoList)

def comment_threads(channel_ID, to_csv = False):

    comments_list = []

    request = youtube.commentThreads().list(
        part = 'id,replies,snippet', 
        order = 'relevance',
        videoId = channel_ID,
        maxResults = 200
    )
    response = request.execute()

    comments_list.extend(process_comments(response['items']))

    while response.get('nextPageToken', None) and len(comments_list) < 200:
        request = youtube.commentThreads().list(
            part = 'id,replies,snippet', 
            order = 'relevance',
            videoId = channel_ID,
            pageToken = response['nextPageToken']
        )
        response = request.execute()
        comments_list.extend(process_comments(response['items']))

    print("done")
    print(len(comments_list))

    if to_csv:
        make_csv(comments_list, channel_ID)
        
    return comments_list



def main():

    comment_csv = []
    video_csv = []

    for video in videoList:
        comment_csv.extend(comment_threads(video))
        video_csv.extend(process_views_likes(video))
    #print(video_csv)
    #print(comment_csv)
    make_csv(comment_csv, 'comments')
    make_csv(video_csv, 'videos')


if __name__ == "__main__":
    main()