from pytube import YouTube
from pathlib import Path
import video_functions

# getting the video
link = input("Paste the link here: ")

try:
    yt = YouTube(link)
except:
    print("Connection Error or wrong link")
    input("Press Enter to close")
    exit()

#preparing download directory
video_functions.prepare_df()

#title = str(yt.title)
title = video_functions.title_check(str(yt.title))


video_functions.downloading_video(link)

#merging video and audio
OUTPUT_PATH = Path(r'vid/')
video_functions.merge_va(title, OUTPUT_PATH)


print('Task Completed!')
