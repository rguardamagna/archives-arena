from typing import Protocol

class VideoTranscriptProvider(Protocol):
    """
    Port (Application Layer)
    Defines the contract for fetching transcripts. This allows us to
    easily swap YouTube for Vimeo or any other platform in the future,
    following the Dependency Inversion Principle.
    """
    async def get_transcript(self, video_id: str) -> str:
        ...
