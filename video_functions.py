from moviepy.editor import *
from pathlib import Path
from pytube import YouTube

def title_check(input_title):
    '''Removes characters that can cause issues from the title.
    Most of them are characters that cannot be used when naming files on windows '''

    F_SYMBOLS = ['\\', r'/', '\n', r'*', r'.', r'"', 
                r'[', r']', r':', r';', r'|', r',', 
                r'<', r'>', r'?'] #forbidden symbols
    output_title = str(input_title)
    R_SYMBOL = '・' #character which replaces the forbidden symbols

    character_number = 0
    while character_number <= len(F_SYMBOLS) - 1:
        output_title = output_title.replace(F_SYMBOLS[character_number], R_SYMBOL)
        character_number = character_number + 1 

    return output_title



def merge_va(output_name, output_path):
    '''Merges audio and video streams'''

    #getting file paths
    SAVE_PATH = Path(r'vid/prepare')
    OUTPUT = Path(output_path, output_name + '.mp4')

    vid = sorted(SAVE_PATH.glob('video.*'))
    aud = sorted(SAVE_PATH.glob('audio.*'))

    #merging them
    output_video = VideoFileClip(filename:=str(vid[0]), audio:=False)
    output_video.audio = AudioFileClip(str(aud[0]))

    #converting and outputing the file
    output_video.write_videofile(str(OUTPUT))

    #removing partial files
    file_list = sorted(SAVE_PATH.glob('*.*'))

    element = 0
    while element < len(file_list):
        p_file = file_list[element]
        Path(p_file).unlink(missing_ok=True)
        element = element + 1


def downloading_video(link):
    '''Function to download both video and audio streams in the highest available quality '''

    SAVE_PATH = Path(r'vid/prepare')

    try:
        yt = YouTube(link)
    except:
        print("Connection Error or wrong link")
        input("Press Enter to close")
        exit()

    #downloading the video
    video = yt.streams.order_by('resolution')
    video = video.desc()
    video = video.first()

    try:
        # downloading the video
        video.download(outputpath:=SAVE_PATH, filename:="video")
    except:
        print("Error while downloading video")
        input("Press Enter to close")
        exit()


    #getting audio
    audio = yt.streams.filter(only_audio=True)
    audio = audio.order_by('abr')
    audio = audio.desc()
    audio = audio.first()

    try:
        audio.download(outputpath:=SAVE_PATH, filename="audio")
        pass
    except:
        print ('Error while downloading audio')
        input("Press Enter to close")
        exit()


def prepare_df():
    '''Used to check if download folder exists and if contains any files 
    that can cause issues'''

    #checking if the vid folder is there, and if not creating it
    if Path('vid/').is_dir() == False:
        os.mkdir('vid/prepare')
    
    #checking the leftover files etc. 
    if Path('vid/prepare').is_dir() == True:
        SAVE_PATH = Path('vid/prepare')
        vid = sorted(SAVE_PATH.glob('video.*'))
        aud = sorted(SAVE_PATH.glob('audio.*'))

        #removing files that can screw up v/a merge
        v_file = len(vid) - 1
        a_file = len(aud) - 1
        while len(vid) > 0:
            Path(vid[v_file]).unlink()
            vid = sorted(SAVE_PATH.glob('video.*'))
            v_file = v_file - 1
        while len(aud) > 0: 
            Path(aud[a_file]).unlink()
            aud = sorted(SAVE_PATH.glob('audio.*'))
            a_file = a_file - 1




if __name__ == "__main__":
    
   prepare_df()
