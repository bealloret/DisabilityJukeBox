import streamlit as st
from pytube import YouTube
import csv


# Function to load YouTube video
def load_video(video_url):
    yt = YouTube(video_url)
    return yt.streams.filter(adaptive=True, file_extension='mp4').first().url

# Function to display questions and collect responses
def display_questions(video_index):
    st.caption("Feedback")
    rating = st.slider(f"How much do you like this song (Video {video_index + 1})?", 1, 5, key=f"rating_{video_index}")
    disability_guess = st.radio(f"One of the creators/performers of this song had a disability. Which disability do you think it was? (Song {video_index + 1})",
                                 ('mental illness', 'sensory disability: deafness', 'sensory disability: blindness', 'physical disability: amputation'), key=f"disability_{video_index}")

    return rating, disability_guess

# Function to save responses to CSV file
def save_to_csv(filename, data):
    with open(filename, "a", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["Video", "Rating", "Disability Guess"])
        if file.tell() == 0:
            writer.writeheader()
        writer.writerow(data)


# List of YouTube video URLs
video_urls = [
    "https://www.youtube.com/watch?v=apBWI6xrbLY",
    "https://www.youtube.com/watch?v=s71I_EWJk7I",
    "https://www.youtube.com/watch?v=0qanF-91aJo",
    "https://www.youtube.com/watch?v=gcE1avXFJb4",
    "https://www.youtube.com/watch?v=Idsb6gk6j_U"
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
for i, video_url in enumerate(video_urls):
    st.header(f"Song {i + 1}")
    st.video(video_url)  # Display video
    rating, disability_guess = display_questions(i)
    st.caption("Reveal")
    if st.button(f"Reveal Artist Info ({i + 1})"):
        st.write(artist_info[i])
        st.write(f"Read more about the artist [here]({artist_links[i]})")
        
    # Save responses to CSV file
    data = {
        "Video": f"Video {i + 1}",
        "Rating": rating,
        "Disability Guess": disability_guess
    }
    save_to_csv("responses.csv", data)
