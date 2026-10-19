import streamlit as st
from dl_config import process_download
import os

st.set_page_config(page_title='Youtube Video Downloader', page_icon= '📹', layout='wide')
st.title('Youtube Video Downloader')
st.caption('Enter Url in sidebar and press the button')

video_url=st.sidebar.text_input('Enter video url: ')

col1, col2 = st.sidebar.columns(2)
btn_mp4 = col1.button('Get MP4')
btn_mp3 = col2.button('Get MP3')
if btn_mp4 or btn_mp3:
    if not video_url:
        st.warning('Please enter the url')
    else:
        selected_format = 'mp4' if btn_mp4 else 'mp3'
        selected_mime = 'video/mp4' if btn_mp4 else 'audio/mpeg'

        download_file_path = process_download(video_url, format_type=selected_format)
        
        if download_file_path:
            try:
                
                with open(download_file_path, 'rb') as f:
                    file_bytes = f.read()
                
                file_name = os.path.basename(download_file_path)

                st.download_button(
                    label=f'Click to download {selected_format.upper()}',
                    data=file_bytes,
                    file_name=file_name, 
                    mime=selected_mime   
                )
                
                st.success(f'Prepared {selected_format.upper()} Successfully!')
                
                #διαγραφη αρχειου απο σερβερ αφου φορτωθηκε στη μνημη
                os.remove(download_file_path)
            except Exception as e:
                st.error(f'Could not prepare the file: {e}')