import random
import streamlit as st
from pytube import YouTube, Playlist, Channel
import os

# Function for some random animations
def random_celeb():
    return random.choice([st.balloons()])

# Function to download YouTube single videos
def video(url):
    video_caller = YouTube(url)
    st.info(video_caller.title, icon="ℹ️")

    # Get available video streams
    streams = video_caller.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc()

    # Create a dictionary to store resolution and corresponding streams
    resolution_dict = {}
    for stream in streams:
        resolution = f"{stream.resolution} ({stream.mime_type.split('/')[1]})"
        resolution_dict[resolution] = stream

    # Get the available resolutions
    resolutions = list(resolution_dict.keys())

    # Display resolution options
    selected_stream_resolution = st.selectbox("Select Video Resolution", resolutions, key="resolution_selectbox")

    # Find the selected stream based on the resolution string
    selected_stream = resolution_dict.get(selected_stream_resolution)

    if selected_stream is not None:
        selected_stream.download()
        st.success('Done!')
        with open(selected_stream.default_filename, 'rb') as file:
            st.download_button('Download Video', file, file_name=selected_stream.default_filename + '.mp4')
    else:
        st.error('Oops! Stream is not available!')

# Function for downloading YouTube playlist
def playlist(url):
    playlist_obj = Playlist(url)
    st.info('Number of videos in playlist: %s' % len(playlist_obj.video_urls), icon="ℹ️")
    for video in playlist_obj.videos:
        x = video.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
        if x is not None:
            x.download()
            st.success('Done!')
            with open(selected_stream.default_filename, 'rb') as file:
                st.download_button('Download Video', file, file_name=x.default_filename + '.mp4')

# Function for downloading YouTube channel
def channel(url):
    channel_videos = Channel(url)
    st.info(f'Downloading videos by: {channel_videos.channel_name}', icon="ℹ️")
    for video in channel_videos.videos:
        z = video.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
        if z is not None:
            z.download()
            st.success('Done!')
            with open(selected_stream.default_filename, 'rb') as file:
                st.download_button('Download Channel', file, file_name=z.default_filename + '.mp4')

# Integration of all above-defined functions
st.title("YouTube Downloader")
url = st.text_input(label="Paste your YouTube URL")
selected_resolution = st.empty()  # Placeholder to store selected resolution

if st.button("Download"):
    if url:
        try:
            with st.spinner("Loading..."):
                if 'playlist' in url:
                    playlist(url)
                elif 'channel' in url:
                    channel(url)
                else:
                    video(url)
            
            selected_resolution.text("")  # Clear the selected resolution
            random_celeb()
        except Exception as e:
            st.error(e)
else:
    # Retrieve the selected resolution from the hidden input field after the page refreshes
    if selected_resolution.text() != "":
        st.session_state.selected_resolution = selected_resolution.text()
# Integration of all above-defined functions

# Integration of all above-defined functions
st.title("YouTube Downloader")
url = st.text_input(label="Paste your YouTube URL")
selected_resolution = st.empty()  # Placeholder to store selected resolution

if st.button("Download"):
    if url:
        try:
            with st.spinner("Loading..."):
                if 'playlist' in url:
                    playlist(url)
                elif 'channel' in url:
                    channel(url)
                else:
                    video(url)

            selected_resolution.empty()  # Clear the selected resolution
            random_celeb()
        except Exception as e:
            st.error(e)
else:
    # Retrieve the selected resolution from the hidden input field after the page refreshes
    if 'selected_resolution' in st.session_state:
        selected_resolution.write(st.session_state.selected_resolution)

# After the page refreshes, display the selected resolution if it exists in session state
if 'selected_resolution' in st.session_state:
    selected_resolution.write(st.session_state.selected_resolution)
