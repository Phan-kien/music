import axios from 'axios';

const API_URL = 'http://localhost:5000/api';

// Create axios instance with default config
const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add request interceptor to add token to all requests
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Add response interceptor to handle 401 errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export const register = async (userData) => {
  try {
    const response = await api.post('/register', {
      username: userData.username,
      email: userData.email,
      password: userData.password
    });
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'Registration failed');
  }
};

export const login = async (userData) => {
  try {
    const response = await api.post('/login', userData);
    const { token } = response.data;
    localStorage.setItem('token', token);
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'Login failed');
  }
};

export const uploadSong = async (formData) => {
  try {
    const response = await api.post('/songs/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'Upload failed');
  }
};

export const getSongs = async () => {
  try {
    const response = await api.get('/songs');
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'Failed to fetch songs');
  }
};

export const createPlaylist = async (name) => {
  try {
    const response = await api.post('/playlists', { name });
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'Failed to create playlist');
  }
};

export const getPlaylists = async () => {
  try {
    const response = await api.get('/playlists');
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'Failed to fetch playlists');
  }
};

export const addSongToPlaylist = async (playlistId, songId) => {
  try {
    const response = await api.post(`/playlists/${playlistId}/songs`, { song_id: songId });
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'Failed to add song to playlist');
  }
};

export const getSongById = async (songId) => {
  const response = await fetch(`${API_URL}/songs/${songId}`, {
    headers: {
      'Authorization': `Bearer ${localStorage.getItem('token')}`
    }
  });
  if (!response.ok) {
    throw new Error('Failed to get song');
  }
  return response.json();
}; 