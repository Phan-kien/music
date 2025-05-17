import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { getSongById } from '../api';

const SharedSong = () => {
  const { songId } = useParams();
  const navigate = useNavigate();
  const [song, setSong] = useState(null);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(true);
  const [notification, setNotification] = useState('');

  useEffect(() => {
    const fetchSong = async () => {
      try {
        const data = await getSongById(songId);
        setSong(data);
      } catch (err) {
        setError('Failed to load song. The song may have been removed or is no longer available.');
      } finally {
        setLoading(false);
      }
    };

    fetchSong();
  }, [songId]);

  const handleShare = () => {
    navigator.clipboard.writeText(window.location.href)
      .then(() => {
        setNotification('Link copied to clipboard!');
        setTimeout(() => setNotification(''), 3000);
      })
      .catch(() => {
        setError('Failed to copy link');
      });
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-100">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  if (error || !song) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-100">
        <div className="text-center bg-white p-8 rounded-lg shadow-lg max-w-md">
          <h1 className="text-2xl font-bold text-red-500 mb-4">Error</h1>
          <p className="text-gray-600 mb-6">{error || 'Song not found'}</p>
          <button
            onClick={() => navigate('/')}
            className="bg-blue-500 text-white px-6 py-2 rounded hover:bg-blue-600 transition-colors"
          >
            Go to Home
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-100 py-12">
      <div className="max-w-2xl mx-auto bg-white rounded-lg shadow-lg overflow-hidden">
        <div className="p-8">
          <div className="flex items-center space-x-6 mb-8">
            <div className="w-32 h-32 bg-gray-200 rounded-lg overflow-hidden">
              <img
                src={song.album_art || 'https://via.placeholder.com/128'}
                alt={song.title}
                className="w-full h-full object-cover"
              />
            </div>
            <div>
              <h1 className="text-3xl font-bold mb-2">{song.title}</h1>
              <p className="text-xl text-gray-600 mb-4">{song.artist}</p>
              <div className="text-sm text-gray-500 space-y-1">
                {song.genre && <p>Genre: {song.genre}</p>}
                {song.release_year && <p>Year: {song.release_year}</p>}
                {song.album && <p>Album: {song.album}</p>}
              </div>
            </div>
          </div>

          <div className="space-y-4">
            <audio
              controls
              className="w-full"
              src={`http://127.0.0.1:5000${song.file_path}`}
              onError={() => setError('Failed to load audio file')}
            >
              Your browser does not support the audio element.
            </audio>

            <div className="flex justify-between items-center">
              <button
                onClick={() => navigate('/')}
                className="text-blue-500 hover:text-blue-600 transition-colors"
              >
                ← Back to Home
              </button>
              <button
                onClick={handleShare}
                className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 transition-colors"
              >
                Share
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Notification */}
      {notification && (
        <div className="fixed bottom-4 left-1/2 transform -translate-x-1/2 bg-green-500 text-white px-6 py-3 rounded-lg shadow-lg">
          {notification}
        </div>
      )}
    </div>
  );
};

export default SharedSong; 