Objectives:
- Split existing youtube playlist into mini playlists based on the month/year (M/Y) the video was added to the playlist
- M/Y playlists are updated based on updates to the Source playlist
- Example: 
  - Input: Source Playlist
    - Video A (Added 10/1/25)
    - Video B  (Added 10/7/25)
    - Video C (Added 11/12/25)
  - Output:
    - Playlist A 10/25
      - Video A
      - Video B
    - Playlist B 11/25
      - Video C
- Before creating a new playlist, check:
  - Are there are any existing M/Y playlists?:
    - If YES:
      - Get the latest M/Y playlist
      - Are all videos from the latest M/Y in the Source playlist present in the latest M/Y playlist?
        - If YES:
          - Are there are any videos in the Source playlist that have been added after the latest M/Y?
            - If YES:
              - Create new playlists based off all videos added after the latest M/Y in the Source playlist
              - END
            - If NO:
              - END
        - If NO:
          - Add videos added in the latest M/Y from the Source playlist that are not found in the latest M/Y playlist
          - Are there are any videos in the Source playlist that have been added after the latest M/Y?
            - If YES:
              - Create new playlists based off all videos added after the latest M/Y in the Source playlist
              - END
            - If NO:
              - END
    - If NO:
      - Create new M/Y playlists based off all videos in the Source playlist
      - END

Pre-requisites:
  1. Set up your project and credentials: [https://developers.google.com/youtube/v3/quickstart/python#step_1_set_up_your_project_and_credentials]
  2. Add client_secrets .json file to the project folder