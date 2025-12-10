from utils import *

def main():
    youtube = auth()

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