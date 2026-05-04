from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter

def get_video_id(url: str) -> str:
    """Extract video ID from various YouTube URL formats."""
    if "youtu.be/" in url:
        return url.split("youtu.be/")[-1].split("?")[0]
    elif "watch?v=" in url:
        return url.split("watch?v=")[-1].split("&")[0]
    elif "youtube.com/embed/" in url:
        return url.split("embed/")[-1].split("?")[0]
    else:
        raise ValueError("Invalid YouTube URL format")

def fetch_transcript(url: str) -> dict:
    """Fetch transcript from a YouTube video."""
    video_id = get_video_id(url)
    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        formatter = TextFormatter()
        transcript_text = formatter.format_transcript(transcript_list)

        # Calculate duration
        total_duration = transcript_list[-1]['start'] + transcript_list[-1]['duration']
        minutes = int(total_duration // 60)

        return {
            "video_id": video_id,
            "transcript": transcript_text,
            "word_count": len(transcript_text.split()),
            "duration_minutes": minutes,
            "chunk_count": len(transcript_list)
        }
    except Exception as e:
        raise Exception(f"Could not fetch transcript: {str(e)}")