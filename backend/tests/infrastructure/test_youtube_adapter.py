import pytest
from unittest.mock import patch, MagicMock
from app.infrastructure.adapters.youtube_adapter import YoutubeTranscriptAdapter

@patch('app.infrastructure.adapters.youtube_adapter.YouTubeTranscriptApi')
def test_get_transcript_success(mock_youtube_api_class):
    # Arrange
    video_id = "test_video_id"
    
    # v1.2+ returns FetchedTranscriptSnippet objects with a .text attribute
    snippet1 = MagicMock()
    snippet1.text = "Hello world"
    snippet2 = MagicMock()
    snippet2.text = "Welcome to the course"
    
    # The adapter instantiates the class, then calls .fetch() on the instance
    mock_instance = mock_youtube_api_class.return_value
    mock_instance.fetch.return_value = [snippet1, snippet2]

    adapter = YoutubeTranscriptAdapter()
    
    # Act
    result = adapter.get_transcript(video_id)
    
    # Assert
    expected_text = "Hello world\nWelcome to the course"
    assert result == expected_text
    mock_instance.fetch.assert_called_once_with(video_id, languages=['es', 'en'])
