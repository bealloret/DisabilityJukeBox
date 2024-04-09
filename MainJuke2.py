import streamlit as st
from pytube import YouTube
from pytube.exceptions import VideoUnavailable
from urllib.error import HTTPError

def load_video(video_id):
    try:
        # If video_id is just the alphanumeric ID, construct the full YouTube URL
        if 'youtube.com' not in video_id:
            video_url = f'https://www.youtube.com/watch?v={video_id}'
        else:
            video_url = video_id

        yt = YouTube(video_url)
        stream = yt.streams.filter(adaptive=True, file_extension='mp4').first()
        if stream:
            return stream.url
        else:
            return None  # No suitable stream found
    except VideoUnavailable:
        st.error("Video is unavailable")
        return None  # Video is unavailable
    except HTTPError as e:
        st.error(f"Error accessing video URL: {e}")
        return None  # Error accessing video URL
        
# Function to display questions and collect responses
def display_questions(video_index):
    st.caption("Feedback")
    rating = st.slider(f"How much do you like this song (Video {video_index + 1})?", 1, 5, key=f"rating_{video_index}")
    disability_guess = st.radio(f"One of the creators/performers of this song had a disability. Which disability do you think it was? (Song {video_index + 1})",
                                 ('mental illness', 'sensory disability: deafness', 'sensory disability: blindness', 'physical disability: amputation'), key=f"disability_{video_index}")

    return rating, disability_guess

# List of YouTube video IDs
video_ids = [
    "apBWI6xrbLY",
    "s71I_EWJk7I",
    "0qanF-91aJo",
    "gcE1avXFJb4",
    "Idsb6gk6j_U"
]

# List of artists with disabilities and Wikipedia links
artist_info = [
    "Brian Wilson was a renowned musician who despite suffering from severe mental health issues, created groundbreaking music.",
    "Ludwig van Beethoven was a visionary composer who lived with hearing loss and inspired millions.",
    "Tony Iommi was a virtuoso guitarist who continued performing despite a physical disability.",
    "Django Reinhardt was a talented guitarist who faced amputation of his fingers but found solace in music.",
    "Joaquín Rodrigo was a prolific composer who triumphed over blindness to create unforgettable melodies."
]

artist_links = [
    "https://en.wikipedia.org/wiki/Brian_Wilson",
    "https://en.wikipedia.org/wiki/Ludwig_van_Beethoven",
    "https://en.wikipedia.org/wiki/Tony_Iommi",
    "https://en.wikipedia.org/wiki/Django_Reinhardt",
    "https://en.wikipedia.org/wiki/Joaqu%C3%ADn_Rodrigo"
]

# Main Streamlit app
st.title("Disability Juke Box")
for i, video_id in enumerate(video_ids):
    st.header(f"Song {i + 1}")
    video_url = load_video(video_id)  # Load video using the video ID
    st.video(video_url)
    rating, disability_guess = display_questions(i)
    st.caption("Reveal")
    if st.button(f"Reveal Artist Info ({i + 1})"):
        st.write(artist_info[i])
        st.write(f"Read more about the artist [here]({artist_links[i]})")

