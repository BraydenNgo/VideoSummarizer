import streamlit as st
from googleapiclient.discovery import build
import youtube_transcript_api
import openai
from dotenv import load_dotenv
import config


def youtube_api_return_video_name(video_url, API_KEY):
    youtube = build('youtube', 'v3', developerKey=API_KEY)

    # Extract video ID from the URL
    video_id = video_url.split("v=")[1].split("&")[0]

    video_response = youtube.videos().list(part="snippet", id=video_id).execute()

    # Extract video title
    if "items" in video_response:
        video_title = video_response["items"][0]["snippet"]["title"]
        return video_title
    else:
        return "Video not found"

def youtube_get_video_transcript(video_url):
    video_transcript = ''
    # Extract video ID from the URL
    video_id = video_url.split("v=")[1].split("&")[0]
    transcript = youtube_transcript_api.YouTubeTranscriptApi.get_transcript(video_id)

    for entry in transcript:
        video_transcript += entry["text"] + ''

    return video_transcript

def chatgpt_summary(video_title, transcript):
    completion = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages = [
            {"role": "user", "content": "Given this Youtube Video with the title {} and transcript for the video{}, give \
            me a detailed summary of the video and its main points.".format(video_title, transcript)}
        ]
    )

    return completion

def main():
    st.title('Youtube Video Summarizer')
    YOUTUBE_API_KEY = config.YOUTUBE_API_KEY
    CHAT_GPT_API_KEY = config.CHAT_GPT_API_KEY

    video_transcript = ''
    load_dotenv()
    openai.api_key = CHAT_GPT_API_KEY

    user_input = st.text_area("Enter a Youtube Video URL")
    if st.button("Generate Summary"):
        if user_input:
            video_title = youtube_api_return_video_name(user_input, YOUTUBE_API_KEY)
            st.write("Youtube Video Title: {}".format(video_title))

            with st.spinner("Generating summmary..."):
                video_transcript = youtube_get_video_transcript(user_input)
                chatgpt_response = chatgpt_summary(video_title, video_transcript)["choices"][0]["message"]["content"]
                st.write("The summary of your video is...")
                st.write(chatgpt_response)
        else:
            st.warning("You must provide a Youtube URL")
    
if __name__ == "__main__":
    main()