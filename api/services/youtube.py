import requests
import os

def get_live_stream_details(channel_id):
    api_key = os.getenv("YOUTUBE_API_KEY")
    
    search_url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&channelId={channel_id}&eventType=live&type=video&key={api_key}"
    search_response = requests.get(search_url)
    search_data = search_response.json()
    
    if not search_data.get("items"):
        return None, None

    video_id = search_data["items"][0]["id"]["videoId"]

    details_url = f"https://www.googleapis.com/youtube/v3/videos?part=liveStreamingDetails&id={video_id}&key={api_key}"
    details_response = requests.get(details_url)
    details_data = details_response.json()
    
    try:
        start_time = details_data["items"][0]["liveStreamingDetails"]["actualStartTime"]
        return video_id, start_time
    except KeyError:
        return None, None