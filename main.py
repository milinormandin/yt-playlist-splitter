# -*- coding: utf-8 -*-

# Sample Python code for youtube.channels.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/code-samples#python

import os

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

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

def main():
    youtube = auth(CLIENT_SECRETS_FILE)
    request = youtube.playlistItems().list(
        part ='snippet',
        playlistId = SOURCE_PLAYLIST_ID
        maxResults = 5 # todo: change to 50
    )
    response = request.execute()

    print(response)

if __name__ == "__main__":
    main()