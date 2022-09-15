from googleapiclient.discovery import build
from pytube import YouTube

class Data:

    __api_key__ = 'AIzaSyBr2KnozeOvEsKAUBJpsuSCoxxzjBYtW5k'
    youtube = build('youtube', 'v3', developerKey=__api_key__)
    #youtuber_name=''
    #all_video_id_stats = []


    def get_video_stats(self, channel_id):
        try:

            all_video_id_stats = []
            request = Data.youtube.channels().list(part="snippet,contentDetails,statistics",id=channel_id)
            response = request.execute()
            data = dict(youtuber_name=response['items'][0]['snippet']['title'],
            playlist_id=response['items'][0]['contentDetails']['relatedPlaylists']['uploads'])
            playlist_id = data['playlist_id']
            youtuber_name = data['youtuber_name']

            request = Data.youtube.playlistItems().list(part='contentDetails', playlistId=playlist_id, maxResults=50)
            response = request.execute()
            video_details50 = []

            i=0
            while i < len(response['items']):

                video_details50.append(dict(video_id=response['items'][i]['contentDetails']['videoId'],
                                            video_url='https://www.youtube.com/watch?v=' +response['items'][i]['contentDetails']['videoId']))
                i=i+1

            j=0
            while j <  len(video_details50):
                all_video_id_stats.append(Data.__get_videos_stats_by_id__(video_details50[j]['video_id'],video_details50[j]['video_url'],youtuber_name))
                j=j+1
            return all_video_id_stats

        except:
            print("Error")

    def __get_videos_stats_by_id__(video_id, url,youtuber_name) :
        request = Data.youtube.videos().list(part='snippet,statistics', id=video_id)
        response = request.execute()
        for videos in response['items'] :
            video_stats = dict(Title=videos['snippet']['title'], Comment_count=videos['statistics']['commentCount'],
                           No_of_Likes=videos['statistics']['commentCount'],
                           Thumbnail=videos['snippet']['thumbnails']['default']['url'],video_id = video_id, video_url = url,Youtuber_name = youtuber_name)
            return video_stats

    def get_comments_by_id(self, video_id) :
      try:
          request = Data.youtube.commentThreads().list(part='snippet,replies', videoId=video_id)
          response = request.execute()
          comment_stack = []
          for comnts in response['items'] :
              if comnts['snippet']['totalReplyCount'] == 0 :
                  comment_data = dict(comments=comnts['snippet']['topLevelComment']['snippet']['textOriginal'],
                                    commenter_name=comnts['snippet']['topLevelComment']['snippet']['authorDisplayName'],
                                    video_id=video_id)
                  comment_stack.append(comment_data)
              else :
                  comment_data = dict(comments=comnts['snippet']['topLevelComment']['snippet']['textOriginal'],
                                    replies=Data.__get_replies__(comnts['id']),
                                    commenter_name=comnts['snippet']['topLevelComment']['snippet']['authorDisplayName'],
                                    video_id=video_id)
                  comment_stack.append(comment_data)
          return comment_stack
      except Exception as e:
          print(e)

    def __get_replies__(id) :

        request = Data.youtube.comments().list(part='snippet,id', parentId=id, maxResults=100)
        response = request.execute()
        reply1 = []
        for r in response['items'] :

            replies = dict(reply=r['snippet']['textOriginal'], response_commentor=r['snippet']['authorDisplayName'])
            reply1.append(replies)

        return reply1
