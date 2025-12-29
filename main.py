from utils import *
import pickle

def main():
    youtube = auth()

    # Check if there are any existing M/Y playlists
    # playlist_titles = get_valid_playlists(youtube)
    valid_playlist_titles = []

    # playlist_name = '10_25_PLEWICDO'
    # target_date = parse_target_date(playlist_name)
    target_date = date(2025, 11, 1)

    if (valid_playlist_titles):
        print(len(valid_playlist_titles))
        print(valid_playlist_titles)
    else:
        '''
        Case of no existing M/Y playlists
        Create new M/Y playlists based off all videos in the Source playlist
        '2025-11-25T18:43:57Z'
        look at all (or videos after a certain date) videos in source playlist X
        get their date, id (valid_playlist_videos) X
            add title and check for any other useful additional info
        get list of M/Y to make playlists for X
        generate playlist titles X
        create new playlist with M/Y naming convention (assume list of videos is already filtered) X
        add single video to playlist X
        populate playlist with list of valid videos ?
            - ISSUE: Quota for requests have been exceeded. 10k daily query limit. 1.8M minute, 180K per min per user
            - SOLUTION: export valid videos from source playlist as pickle for testing purposes 
        '''        
    
        valid_playlist_videos = get_valid_videos(youtube, target_date)

        
        # Save playlist video data to file for testing
        with open('valid_playlist_videos.pkl', 'wb') as f:
            pickle.dump(valid_playlist_videos, f)

  
        # Open the file in read-binary mode ('rb') and load the data
        with open('valid_playlist_videos.pkl', 'rb') as file:
            valid_playlist_videos = pickle.load(file)
        print(valid_playlist_videos)

        # playlist_titles = create_playlist_titles(valid_playlist_videos)

        # for playlist_title in playlist_titles:
        #     playlist_date = parse_target_date(playlist_title)
        #     # Filter videos whose add date is within the current playlist month date
        #     my_videos = [video for video in valid_playlist_videos if video['added_date'] >= playlist_date and video['added_date'] < playlist_date + relativedelta(months=1)]

        #     # Create new playlist
        #     playlist_result = create_playlist(youtube, f'{playlist_title}', f'Generated playlist for videos added in {playlist_date.month}/{playlist_date.year}')
        #     new_playlist_id = playlist_result['id']

        #     # Add all valid videos to playlist
        #     res = add_video_list_to_playlist(youtube, new_playlist_id, my_videos)
        #     print(res)
    

if __name__ == "__main__":
    main()