import streamlit as st
import pandas as pd
import csv
import base64
import requests

# Function to save responses to CSV file
def save_to_csv(filename, data):
    with open(filename, "a", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["Video", "Rating", "Disability Guess"])
        if file.tell() == 0:
            writer.writeheader()
        writer.writerow(data)

# Function to retrieve saved data from CSV file
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
    rating = st.slider(f"How much do you like this song (Video {i + 1})?", 1, 5, key=f"rating_{i}")
    disability_guess = st.radio(f"One of the creators/performers of this song had a disability. Which disability do you think it was? (Song {i + 1})",
                                 ('mental illness', 'sensory disability: deafness', 'sensory disability: blindness', 'physical disability: amputation'), key=f"disability_{i}")
    
    # Save responses to CSV file
    data = {
        "Video": f"Video {i + 1}",
        "Rating": rating,
        "Disability Guess": disability_guess
    }
    save_to_csv("responses.csv", data)

# Define API endpoint
@st.cache
def api_endpoint():
    saved_data = get_saved_data("responses.csv")
    return saved_data

# Display a button to trigger data retrieval via API
if st.button("Get Data via API"):
    response = api_endpoint()
    st.write(pd.DataFrame(response))  # Convert to DataFrame for better display

