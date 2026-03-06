import re
from datetime import datetime, timezone, timedelta
from api.services.youtube import get_live_stream_details
from api.services.discord import send_discord_webhook

def handle_clip_request(user, msg, channel_id):
    offset = 0
    title = msg
    match = re.search(r'(.*?)\s*-\s*(\d+)$', msg)
    if match:
        title = match.group(1).strip()
        offset = int(match.group(2))

    video_id, start_time_str = get_live_stream_details(channel_id)
    if not video_id or not start_time_str:
        return {"message": f"@{user} Error: No active live stream found for this channel."}

    start_time = datetime.fromisoformat(start_time_str.replace('Z', '+00:00'))
    now = datetime.now(timezone.utc)
    
    total_seconds = int((now - start_time).total_seconds()) - offset
    
    if total_seconds < 0:
        total_seconds = 0
        
    formatted_time = str(timedelta(seconds=total_seconds))
    
    url = f"https://youtu.be/{video_id}?t={total_seconds}"
    payload = {
        "username": "Stream Highlights Bot",
        "embeds": [{
            "title": "🎬 New Highlight Captured!",
            "color": 16711680,
            "fields": [
                {"name": "📝 Note", "value": title, "inline": False},
                {"name": "🔗 Link", "value": f"[▶️ Watch the Clip Here]({url})", "inline": False},
                {"name": "⏱️ Stream Time", "value": f"`{formatted_time}`", "inline": True},
                {"name": "👤 Clipped By", "value": f"`{user}`", "inline": True}
            ]
        }]
    }

    success = send_discord_webhook(payload)
    if success:
        return {"message": f"@{user} Clip logged successfully at {formatted_time}!"}
    else:
        return {"message": f"@{user} Error: Failed to send clip to Discord."}