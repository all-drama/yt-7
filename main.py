import streamlit as st
from pytube import YouTube

# Function to download YouTube video
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
    resolution = st.selectbox("Select Video Resolution", resolutions)

    # Find the selected stream based on the resolution string
    selected_stream = resolution_dict.get(resolution)

    if selected_stream is not None:
        selected_stream.download()
        st.success('Done!')
        selected_resolution = resolution  # Store the selected resolution
        st.session_state.selected_resolution = selected_resolution  # Save it to session state
    else:
        st.error('Oops! Stream is not available!')

# Main code
st.title("YouTube Downloader")
url = st.text_input(label="Paste your YouTube URL")

if st.button("Download"):
    if url:
        try:
            with st.spinner("Loading..."):
                video(url)
        except Exception as e:
            st.error(e)

# Display the selected resolution after the download is completed
if 'selected_resolution' in st.session_state:
    st.write(f"Selected Resolution: {st.session_state.selected_resolution}")
