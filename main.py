import os

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from time import sleep
from datetime import date
from dateutil import parser
from dateutil.relativedelta import relativedelta


scopes = ['https://www.googleapis.com/auth/youtube.readonly']

# Replace with your client_secret json
CLIENT_SECRETS_FILE = 'client_secret_1008844831738-32n15naetu5pcnk62tn0beno4ds4i565.apps.googleusercontent.com.json'
# Replace with your source playlist id
SOURCE_PLAYLIST_ID = 'PLEwYo0c5mGnB88HBUetQT4RNsDp9yicdO'


def auth(client_secrets_file: str):
    '''
    Authentication to Youtube
    '''
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

def format_id(id: str) -> str:
    '''
    Format id into 8 char string for M/Y playlist naming convention
    '''
    id = id.upper()
    return f'{id[:4]}{id[len(id)-4:]}'

def create_playlist_title(target_month: int, target_year: int, id: str) -> str:
    '''
    Create playlist title formatted with the proper naming convention. Example: '10_25_PLEWICDO'
    '''
    return f'{target_month}_{str(target_year)[2:]}_{format_id(id)}'

def create_playlist_titles(valid_playlist_videos: list[dict]) -> list[str]:
    '''
    Create list of playlist titles based on valid video list from the Source playlist
    '''
    # Get list of M/Y dates to make new playlists for
    my_dates = list(set([(i['added_date'].year, i['added_date'].month) for i in valid_playlist_videos]))

    # Generate playlist titles based off of dates
    return [create_playlist_title(target_month=d[1],target_year=d[0],  id=SOURCE_PLAYLIST_ID) for d in my_dates]

def is_valid_playlist(name: str) -> bool:
    '''
    Check playlist for M/Y naming convention
    '''
    if format_id(SOURCE_PLAYLIST_ID) in name:
        month = int(name[:2])
        year = int(name[3:5])
        if (month > 1 and month <= 12) and (year >= 7):
            return True
    return False

def get_playlist_list(youtube, next_page_token=''):
    '''
    Retrieve list of playlists from the current user 
    '''
    request = youtube.playlists().list(
    part='snippet',
    maxResults=50,
    mine=True,
    pageToken = next_page_token
    )
    return request.execute()



def get_playlist_videos(youtube, next_page_token=''):
    '''
    Retrieve list of playlist videos from source playlist 
    '''
    request = youtube.playlistItems().list(
        part ='snippet',
        playlistId = SOURCE_PLAYLIST_ID,
        maxResults = 50,
        pageToken = next_page_token
        )
    return request.execute()


def add_valid_playlists(response, playlist_titles: list) -> list[str]:
    '''
    Checks response object for valid playlist titles and adds to list
    '''
    for item in response['items']:
        playlist_title = item['snippet']['title']
        if is_valid_playlist(playlist_title):
            playlist_titles.append(playlist_title)
    return playlist_titles

def get_valid_playlists(youtube) -> list[str]:
    '''
    Get list of playlists from the current user that match the M/Y naming convention 
    '''
    # Initial request
    response = get_playlist_list(youtube)
      
    playlist_titles = add_valid_playlists(response, [])

    while 'nextPageToken' in response:
        next_page_token = response['nextPageToken']
        response = get_playlist_list(youtube, next_page_token)
        playlist_titles = add_valid_playlists(response, playlist_titles)
        sleep(.2)
    return playlist_titles


def parse_target_date(playlist_title: str):
    '''
    Get datetime object from playlist title
    '''
    target_month = int(playlist_title[:2])
    target_year = int(f'20{playlist_title[3:5]}')
    return date(target_year, target_month, 1)


def add_valid_playlist_videos(response, target_date, playlist_videos, found_target_date) -> tuple[dict, bool]:
    '''
    Checks response object for playlist videos added on or after the provided target date
    '''
    for item in response['items']:
        added_date = parser.isoparse(item['snippet']['publishedAt']).date()
        video_id = item['snippet']['resourceId']['videoId']
        
        if target_date:
            if added_date >= target_date:
                playlist_videos.append({'added_date': added_date, 'video_id': video_id})
            else:
                found_target_date = True
                break
        else:
            playlist_videos.append({'added_date': added_date, 'video_id': video_id})
    return (playlist_videos, found_target_date)

def get_valid_videos(youtube, target_date: date) -> list[dict]:
    '''
    Get list of video data (added_date, video_id) from the source playlist added on or after the provided target date
    '''
    response = get_playlist_videos(youtube)

    found_target_date = False

    playlist_videos, found_target_date = add_valid_playlist_videos(response, target_date, [], found_target_date)

    while 'nextPageToken' in response:
        next_page_token = response['nextPageToken']
        response = get_playlist_videos(youtube, next_page_token)
        playlist_videos, found_target_date = add_valid_playlist_videos(response, target_date, playlist_videos, found_target_date)
        
        if found_target_date:
            break
        sleep(.2)
    
    return playlist_videos



def main():
    youtube = auth(CLIENT_SECRETS_FILE)
    


    # Check if there are any existing M/Y playlists
    # playlist_titles = get_valid_playlists(youtube)
    valid_playlist_titles = []

    # playlist_name = '10_25_PLEWICDO'
    # target_date = parse_target_date(playlist_name)
    target_date = date(2025, 10, 1)

    if (valid_playlist_titles):
        print(len(valid_playlist_titles))
        print(valid_playlist_titles)
    else:
        # Case of no existing M/Y playlists
        # Create new M/Y playlists based off all videos in the Source playlist
        # '2025-11-25T18:43:57Z'
        # look at all (or videos after a certain date) videos in source playlist X
        # get their date and id (valid_playlist_videos) X
        # get list of M/Y to make playlists for X
        # generate playlist titles X
        # create new playlist with M/Y naming convention (assume list of videos is already filtered)
            # check that playlist doesn't exist
        # populate playlist with list of valid videos
    
        valid_playlist_videos = get_valid_videos(youtube, target_date)

        playlist_titles = create_playlist_titles(valid_playlist_videos)

        for playlist_title in playlist_titles:
            playlist_date = parse_target_date(playlist_title)
            # Grab videos whose add date is within the playlist date
            my_videos = [video for video in valid_playlist_videos if video['added_date'] >= playlist_date and video['added_date'] < playlist_date + relativedelta(months=1)]
            print(playlist_date)
            print(my_videos)
        
    

if __name__ == "__main__":
    main()