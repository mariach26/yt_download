import streamlit as st
import yt_dlp 
import os


def process_download(url,output_path='downloads', format_type='mp4'):
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    if '&list=' in url:
        url = url.split('&list=')[0]

    final_filepath=None
    #mp3 settings
    if format_type=='mp3': 
        ydl_opts={
            'format': 'bestvideo+bestaudio/best',
            'outtmpl': f'{output_path}/%(title)s.%(ext)s',
            'noplaylist': True,
            'writedescription': False,
            #'noprogress': False,
            'playlist_items': '1',
            'quiet': True,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],

        }
        spinner_msg = 'Downloading the audio and converting to MP3...'
        #video mp4 settings
    else:
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best', # Καλύτερο για να βγει σίγουρα MP4
            'outtmpl': f'{output_path}/%(title)s.%(ext)s',
            'noplaylist': True,
            'playlist_items': '1',
            'noplaylist': True,
            'quiet': True,
        }
        spinner_msg = 'Downloading the video...'

    try:
        st.info(f"Currently given URL: {url}") #shows url
        with st.spinner('Downloading..'): #downloads
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info_dict=ydl.extract_info(url, download=True) #metadata from url
                final_filepath= ydl.prepare_filename(info_dict) #gives final filepath

                if format_type == 'mp3':
                    final_filepath = os.path.splitext(final_filepath)[0] + '.mp3'

        st.success("Download complete on the server.")
        return final_filepath
    except yt_dlp.utils.DownloadError as de:
        st.error(de)
        return None
    except Exception as e:
        st.error(e)
        return None