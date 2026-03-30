import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api/v1/game';

const gameClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const startGame = async (userId, email, videoId) => {
  try {
    const response = await gameClient.post('/start', {
      user_id: userId,
      email: email,
      video_id: videoId,
    });
    return response.data;
  } catch (error) {
    console.error('Error starting game:', error);
    throw error;
  }
};

export const playTurn = async (sessionId, answerIndex) => {
  try {
    const response = await gameClient.post('/play', {
      session_id: sessionId,
      answer_index: answerIndex,
    });
    return response.data;
  } catch (error) {
    console.error('Error playing turn:', error);
    throw error;
  }
};

export default { startGame, playTurn };
