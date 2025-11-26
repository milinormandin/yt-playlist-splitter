import os

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from time import sleep

scopes = ['https://www.googleapis.com/auth/youtube.readonly']
# Replace with your client_secret json
CLIENT_SECRETS_FILE = 'client_secret_1008844831738-32n15naetu5pcnk62tn0beno4ds4i565.apps.googleusercontent.com.json'
# Replace with your source playlist id
SOURCE_PLAYLIST_ID = 'PLEwYo0c5mGnB88HBUetQT4RNsDp9yicdO'

# Authentication to Youtube
def auth(client_secrets_file: str):
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"

    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    credentials = flow.run_local_server()
    return googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)

# Retrieve list of playlists from the current user 
def get_playlist_list(youtube, next_page_token=''):
    request = youtube.playlists().list(
    part='snippet',
    maxResults=50,
    mine=True,
    pageToken = next_page_token
    )
    return request.execute()



def main():
    youtube = auth(CLIENT_SECRETS_FILE)
    # request = youtube.playlistItems().list(
    #     part ='snippet',
    #     playlistId = SOURCE_PLAYLIST_ID
    #     maxResults = 5 # todo: change to 50
    # )

    # Check all playlist titles
    # Check all plalist titles for naming convention
    # Get list of all playlists with naming convention

    # Initial request
    response = get_playlist_list(youtube)
    
    playlist_titles = []
    
    for item in response['items']:
        playlist_titles.append(item['snippet']['title'])

    while 'nextPageToken' in response:
        next_page_token = response['nextPageToken']
        response = get_playlist_list(youtube, next_page_token)
        for item in response['items']:
            playlist_titles.append(item['snippet']['title'])
        sleep(.2)

    print(len(playlist_titles))
    print(playlist_titles)
    
    # print(response)
# 'PLEwYo0c5mGnB88HBUetQT4RNsDp9yicdO'
if __name__ == "__main__":
    main()