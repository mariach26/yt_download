import streamlit as st
from dl_config import download_yt_video
import os

st.set_page_config(page_title='Youtube Video Downloader', page_icon= '📹', layout='wide')
st.title('Youtube Video Downloader')
st.caption('Enter Url in sidebar and press the button')

video_url=st.sidebar.text_input('Enter video url: ')

button=st.sidebar.button('Start download')
if video_url and button:
    download_file_path=download_yt_video(video_url)
    if download_file_path:
        try:
            with open(download_file_path,'rb') as f:
                video_bytes=f.read()
            
            file_name=os.path.basename(download_file_path)

            st.download_button(
                label='Click to download the video' ,
                data=video_bytes,
                file_name="video.mp4",
                mime='video/mp4'
            )
            st.success('Downloaded Video Successfully')
            os.remove(download_file_path)
        except Exception as e:
            st.error(f'Could prepare the file {e}')
else:
    st.warning('Please enter the url')
    