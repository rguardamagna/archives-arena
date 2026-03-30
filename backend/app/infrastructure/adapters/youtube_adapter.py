from youtube_transcript_api import YouTubeTranscriptApi
from app.application.ports.video_transcript_provider import VideoTranscriptProvider

class YoutubeTranscriptAdapter(VideoTranscriptProvider):
    """
    Adapter (Infrastructure Layer)
    Implements the VideoTranscriptProvider interface using the youtube-transcript-api.
    Uses the v1.2+ instance-based API.
    """

    async def get_transcript(self, video_id: str) -> str:
        """
        Fetches the transcript for a given YouTube video ID.
        """
        # v1.2+ requires instantiation first, then calling fetch()  
        api = YouTubeTranscriptApi()
        transcript_data = api.fetch(video_id, languages=['es', 'en'])
        
        # transcript_data is a FetchedTranscript iterable of FetchedTranscriptSnippet objects
        # Each snippet has a .text attribute
        return "\n".join([snippet.text for snippet in transcript_data])
