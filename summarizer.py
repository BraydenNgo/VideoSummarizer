import streamlit as st
from googleapiclient.discovery import build
import youtube_transcript_api
import os
import openai
import requests
from dotenv import load_dotenv


API_KEY = ''
CHAT_KEY = ''
video_transcript = ''

load_dotenv()
openai.api_key = CHAT_KEY

youtube = build('youtube', 'v3', developerKey=API_KEY)

st.title('Youtube Video Summarizer')
user_input = st.text_area("Enter a Youtube Video URL")
st.button("Generate Summary")
st.write("Video Submitted:", user_input)


video_url = "https://www.youtube.com/watch?v=ASXavjitZCQ"

# Extract video ID from the URL
video_id = video_url.split("v=")[1].split("&")[0]

# Retrieve transcript using the youtube-transcript-api
transcript = youtube_transcript_api.YouTubeTranscriptApi.get_transcript(video_id)

video_response = youtube.videos().list(part="snippet", id=video_id).execute()

# Extract video title
if "items" in video_response:
    video_title = video_response["items"][0]["snippet"]["title"]
    st.write("Video Title:", video_title)
else:
    st.write("Video not found")


# Print the transcript
for entry in transcript:
    video_transcript += entry["text"] + ''
#st.write(video_transcript)

completion_ = openai.ChatCompletion.create(
    model = "gpt-3.5-turbo",
    messages = [
        {"role": "user", "content": "Given this Youtube Video with the title {} and transcript for the video{}, give \
          me a detailed summary of the video and its main points.".format(video_title, transcript)}
    ]
)

st.write("The summary of your video is...")
st.write(completion_["choices"][0]["message"]["content"])