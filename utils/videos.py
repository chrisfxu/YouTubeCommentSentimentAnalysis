# -*- coding: utf-8 -*-

# Sample Python code for youtube.playlistItems.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/code-samples#python

import os
from traceback import print_tb

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

from dotenv import load_dotenv 
load_dotenv()
api_key = os.getenv("api_key")

playlistID = 'PLirAqAtl_h2r5g8xGajEwdXd3x1sZh8hC'


scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

api_service_name = "youtube"
api_version = "v3"

youtube = googleapiclient.discovery.build(
api_service_name, api_version, developerKey = api_key)

video_list = []

def has_comments(videoID):

    request = youtube.videos().list(
    part="id, statistics",
    id=videoID
    )
    response = request.execute()
    #print(response['items'][0]['statistics'].get('commentCount', '0'))
    if response['items'][0]['statistics'].get('commentCount', "0") != "0":
        return True 

def process_views_likes(videoID):

    data = []
    if has_comments(videoID):
        request = youtube.videos().list(
            part = "id, statistics",

            id = videoID
        )
        response = request.execute()
        video = {}
        video['id'] = response['items'][0]['id']
        video['viewCount'] = response['items'][0]['statistics']['viewCount']
        video['likeCount'] = response['items'][0]['statistics']['likeCount']
        data.append(video)
        
        return data 



def process_video_info(response_items):

    videos= []

    for res in response_items:

        snippet = res['snippet']
        videoID = snippet['resourceId']['videoId']
        if has_comments(videoID) and (len(video_list) + len(videos)) < 150:
            videos.append(videoID)
        #has_comments(videoID)

    return videos 

def raw_video_list(playlist_ID):

    request = youtube.playlistItems().list(
    part="id, snippet",
    playlistId=playlist_ID)

    response = request.execute()

    video_list.extend(process_video_info(response['items']))


    while response.get('nextPageToken', None) and len(video_list) < 150:
        request = youtube.playlistItems().list(
            part = 'id,snippet', 
            playlistId="PLirAqAtl_h2r5g8xGajEwdXd3x1sZh8hC",
            pageToken = response['nextPageToken']
        )
        response = request.execute()
        video_list.extend(process_video_info(response['items']))

    print(video_list)
    #print(len(video_list))

    return video_list


def main():

    raw_video_list(playlistID)

if __name__ == "__main__":
    main()
