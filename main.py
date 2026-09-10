import asyncio
import os
import json
from mcp.server.fastmcp import FastMCP
import yt_dlp

# মিউজিক সার্ভার ইনিশিয়ালাইজ করা
mcp = FastMCP("Cloud-Music-Server")

@mcp.tool()
def play_music_from_youtube(song_name: str) -> str:
    """
    YouTube থেকে যেকোনো গান সার্চ করে সেটির ডিরেক্ট অডিও স্ট্রিম লিংক বের করার টুল।
    চ্যাটবট এই লিংকের মাধ্যমে সরাসরি গান প্লে করবে।
    """
    if not song_name:
        return "দয়া করে গানের নাম বলুন।"
        
    ydl_opts = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'quiet': True,
        'default_search': 'ytsearch',
        'nocheckcertificate': True
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            search_result = ydl.extract_info(f"ytsearch:{song_name}", download=False)
            if 'entries' in search_result and len(search_result['entries']) > 0:
                video_data = search_result['entries'][0]
                audio_url = video_data['url']
                return audio_url
            else:
                return "দুঃখিত, এই নামে কোনো গান খুঁজে পাওয়া যায়নি।"
        except Exception as e:
            return f"গানটি লোড করতে সমস্যা হয়েছে: {str(e)}"

if __name__ == "__main__":
    # Render-এর ফ্রি পোর্টের সাথে সামঞ্জস্য রেখে সরাসরি WebSocket ট্রান্সপোর্ট চালু করা
    port = int(os.environ.get("PORT", 10000))
    mcp.run(transport="websocket", host="0.0.0.0", port=port)
