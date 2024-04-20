import streamlit as st
import pandas as pd
import csv
import base64
import requests
import datetime
import matplotlib.pyplot as plt 

# Function to save responses to CSV file
def save_to_csv(filename, data):
    data["Date"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Add current date and time
    existing_data = get_saved_data(filename)
    with open(filename, "a", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["Date", "Video", "Rating", "Disability Guess"])
        if not existing_data or data not in existing_data:
            if file.tell() == 0:
                writer.writeheader()
            writer.writerow(data)


# Function to retrieve saved data from CSV file
def get_saved_data(filename):
    saved_data = []
    with open(filename, "r", newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            row_data = {
                "Date": row["Date"],  # Use row.get to handle missing "Date" column
                "Video": row["Video"],
                "Rating": row["Rating"],
                "Disability Guess": row["Disability Guess"]
            }
            saved_data.append(row_data)
    return saved_data

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
    rating = st.slider(f"How much do you like this song (Video {i + 1})?", 1, 5, key=f"rating_{i}")
    disability_guess = st.radio(f"One of the creators/performers of this song had a disability. Which disability do you think it was? (Song {i + 1})",
                                 ('mental illness', 'sensory disability: deafness', 'sensory disability: blindness', 'physical disability: amputation'), key=f"disability_{i}")
    st.write(f"### Artist Info for Song {i + 1}")
    if st.button(f"Show Artist Info for Song {i + 1}"):
        st.markdown(artist_info[i])
        st.markdown(f"[More info on Wikipedia]({artist_links[i]})")
    
     # Save responses to CSV file
    data = {
        "Date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
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

# Display a selectbox to choose the data visualization type
visualization_type = st.selectbox("Select Visualization Type", ["Table", "Graph"])

# Display data based on selected visualization type
if visualization_type == "Table":
    response = api_endpoint()
    df = pd.DataFrame(response, columns=["Date", "Video", "Rating", "Disability Guess"])  # Correct column labels
    df = df[["Video", "Date", "Rating", "Disability Guess"]]  # Reorder the columns
    st.write(df)
elif visualization_type == "Graph":
    response = api_endpoint()
    df = pd.DataFrame(response)
    rating_counts = df["Rating"].value_counts().sort_index()
    plt.bar(rating_counts.index, rating_counts.values)
    plt.xlabel("Rating")
    plt.ylabel("Count")
    plt.title("Rating Distribution")
    st.pyplot(plt)
