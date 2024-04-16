import streamlit as st
from pytube import YouTube
import csv
import builtins  # Import builtins module for the built-in function type

# Custom hash function for the main function
def my_hash_func(main_func):
    # Implement custom hashing logic here
    # For simplicity, let's return a hash of the function's name
    return hash(main_func.__name__)

# Function to load YouTube video
@st.cache(hash_funcs={builtins.function: my_hash_func})  # Register custom hash function
def load_video(video_url):
    yt = YouTube(video_url)
    return yt.streams.filter(adaptive=True, file_extension='mp4').first().url

# Function to display questions and collect responses
@st.cache(hash_funcs={builtins.function: my_hash_func})  # Register custom hash function
def display_questions(video_index):
    st.caption("Feedback")
    rating = st.slider(f"How much do you like this song (Video {video_index + 1})?", 1, 5, key=f"rating_{video_index}")
    disability_guess = st.radio(f"One of the creators/performers of this song had a disability. Which disability do you think it was? (Song {video_index + 1})",
                                 ('mental illness', 'sensory disability: deafness', 'sensory disability: blindness', 'physical disability: amputation'), key=f"disability_{video_index}")

    return rating, disability_guess

# Function to save responses to CSV file
@st.cache(hash_funcs={builtins.function: my_hash_func})  # Register custom hash function
def save_to_csv(filename, data):
    with open(filename, "a", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["Video", "Rating", "Disability Guess"])
        if file.tell() == 0:
            writer.writeheader()
        writer.writerow(data)

# Function to retrieve saved data from CSV file
@st.cache(hash_funcs={builtins.function: my_hash_func})  # Register custom hash function
def get_saved_data(filename):
    saved_data = []
    with open(filename, "r", newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            saved_data.append(row)
    return saved_data

# List of YouTube video URLs
video_urls = [
    "https://www.youtube.com/watch?v=apBWI6xrbLY",
    "https://www.youtube.com/watch?v=s71I_EWJk7I",
    "https://www.youtube.com/watch?v=0qanF-91aJo",
    "https://www.youtube.com/watch?v=gcE1avXFJb4",
    "https://www.youtube.com/watch?v=Idsb6gk6j_U"
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

# Display the saved data
st.subheader("Saved Data")
saved_data = get_saved_data("responses.csv")
for row in saved_data:
    st.write(row)
