import pandas as pd
import googleapiclient.discovery
import os
from flask_restful import Resource

from flask import request


class Comment(Resource):
    @staticmethod
    def get():
        url = request.args.get('url')
        return GetComment(url).get_data()


class GetComment:
    def __init__(self, url):
        self.url = url

    @staticmethod
    def get_comment(video_id, page_token=''):
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

        api_service_name = "youtube"
        api_version = "v3"
        developer_key = "AIzaSyAGCJK7EDHGgwg8eJ2GuX4C0sBEH-mLe0E"

        youtube = googleapiclient.discovery.build(
            api_service_name, api_version, developerKey=developer_key)

        vid_stats = youtube.videos().list(
            part="statistics",
            id=video_id
        ).execute()

        comment_count = vid_stats.get("items")[0].get("statistics").get("commentCount")
        if comment_count == 0:
            return [], []
        else:
            request = youtube.commentThreads().list(
                part="snippet",
                order="time",
                maxResults='100',
                pageToken=page_token,
                videoId=video_id
            )
            response = request.execute()
            try:
                next_page_token = response['nextPageToken']
            except KeyError:
                next_page_token = []
            try:
                data = pd.DataFrame(response['items'])['snippet'].apply(pd.Series)['topLevelComment'].apply(pd.Series)[
                    'snippet'].apply(pd.Series)
            except KeyError:
                data = []
            return next_page_token, data

    def transform_comment(self, video_id, video_title):
        time = 0
        result = []
        next_page_token = ''
        while True:
            if time == 0:
                next_page_token, data = self.get_comment(video_id, page_token='')
            else:
                if len(next_page_token) != 0:
                    next_page_token, data = self.get_comment(video_id, next_page_token)
                else:
                    break
            if len(data) != 0:
                result.append(data)
                print(data)
            time += 1
        video_comment = pd.concat(result)
        video_comment['Title'] = video_title
        return video_comment

    def get_data(self):
        url = self.url
        channel_id = url.split('/')[-1]
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

        api_service_name = "youtube"
        api_version = "v3"
        developer_key = "AIzaSyAGCJK7EDHGgwg8eJ2GuX4C0sBEH-mLe0E"
        # Get credentials and create an API client
        youtube = googleapiclient.discovery.build(
            api_service_name, api_version, developerKey=developer_key)

        request = youtube.search().list(
            part="snippet",
            channelId=channel_id,
            order="viewCount",
            type="video"
        )
        response = request.execute()
        # list of video_id
        video_id = list(pd.DataFrame(response['items'])['id'].apply(pd.Series)['videoId'])
        # list of title of video
        video_title = list(pd.DataFrame(response['items'])['snippet'].apply(pd.Series)['title'])
        # dict of video title and video id
        dict_video = []
        for i in range(len(video_id)):
            dict_video.append({
                'id': video_id[i],
                'title': video_title[i]
            })
        list_video_info = pd.DataFrame(dict_video)
        result = []
        for i in range(len(list_video_info)):
            vid_id = list_video_info.loc[i]['id']
            vid_title = list_video_info.loc[i]['title']
            print(vid_title)
            result.append(self.transform_comment(vid_id, vid_title))
        return pd.concat(result).to_csv()
