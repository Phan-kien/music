import React, { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { getSongs, uploadSong, getPlaylists, createPlaylist, addSongToPlaylist } from '../api';
import Player from '../components/Player';

const Home = () => {
  const [songs, setSongs] = useState([]);
  const [playlists, setPlaylists] = useState([]);
  const [selectedPlaylist, setSelectedPlaylist] = useState(null);
  const [newPlaylistName, setNewPlaylistName] = useState('');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [uploading, setUploading] = useState(false);
  const [likedSongs, setLikedSongs] = useState([]);
  const [currentSong, setCurrentSong] = useState(null);
  const [currentSongIndex, setCurrentSongIndex] = useState(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [editingSong, setEditingSong] = useState(null);
  const [editingPlaylist, setEditingPlaylist] = useState(null);
  const [userName, setUserName] = useState('');
  const audioRef = useRef(new Audio());
  const navigate = useNavigate();
  const [showAllSongs, setShowAllSongs] = useState(false);
  const SONGS_TO_SHOW = 5; // Number of songs to show when collapsed
  const [isShuffled, setIsShuffled] = useState(false);
  const [shuffledSongs, setShuffledSongs] = useState([]);
  const [isPlaying, setIsPlaying] = useState(false);
  const [currentTime, setCurrentTime] = useState(0);
  const [volume, setVolume] = useState(1);
  const [showMetadataModal, setShowMetadataModal] = useState(false);
  const [selectedSongForPlaylist, setSelectedSongForPlaylist] = useState(null);
  const [selectedPlaylistId, setSelectedPlaylistId] = useState('');
  const [shareLink, setShareLink] = useState('');
  const [sharedSong, setSharedSong] = useState(null);
  const [shareError, setShareError] = useState('');
  const [selectedSongMetadata, setSelectedSongMetadata] = useState(null);

  useEffect(() => {
    const token = localStorage.getItem('token');
    const storedUserName = localStorage.getItem('user_name');
    
    console.log('Stored user name:', storedUserName); // Debug log
    
    if (!token) {
      navigate('/login');
      return;
    }

    // Try to get user info from localStorage
    if (storedUserName) {
      console.log('Setting user name to:', storedUserName); // Debug log
      setUserName(storedUserName);
    } else {
      // If not in localStorage, try to get from token
      try {
        const tokenData = JSON.parse(atob(token.split('.')[1]));
        console.log('Token data:', tokenData); // Debug log
        if (tokenData.name) {
          console.log('Setting user name from token:', tokenData.name); // Debug log
          setUserName(tokenData.name);
          localStorage.setItem('user_name', tokenData.name);
        }
      } catch (err) {
        console.error('Error parsing token:', err);
      }
    }

    loadSongs();
    loadPlaylists();
    // Load liked songs from localStorage
    const savedLikedSongs = JSON.parse(localStorage.getItem('likedSongs') || '[]');
    setLikedSongs(savedLikedSongs);
  }, [navigate]);

  useEffect(() => {
    // Cleanup audio on component unmount
    return () => {
      if (audioRef.current) {
        audioRef.current.pause();
        audioRef.current.src = '';
      }
    };
  }, []);

  const loadSongs = async () => {
    try {
      const data = await getSongs();
      // Sort songs by upload date (newest first)
      const sortedSongs = data.sort((a, b) => new Date(b.upload_date) - new Date(a.upload_date));
      setSongs(sortedSongs);
    } catch (err) {
      setError('Failed to load songs');
    }
  };

  const loadPlaylists = async () => {
    try {
      const data = await getPlaylists();
      setPlaylists(data);
      // After loading playlists, update available songs
      loadSongs();
    } catch (err) {
      setError('Failed to load playlists');
    }
  };

  const handleFileUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    setUploading(true);
    setError('');
    setSuccess('');

    // Extract song information from filename
    const fileName = file.name.replace(/\.[^/.]+$/, ''); // Remove extension
    const parts = fileName.split(' - ');
    
    // Ensure we have at least title and artist
    const title = parts[0] || fileName;
    const artist = parts[1] || 'Unknown Artist';
    const genre = parts[2] || 'Unknown';
    const year = parts[3] || null;
    const album = parts[4] || 'Unknown';

    const formData = new FormData();
    formData.append('file', file);
    formData.append('title', title);
    formData.append('artist', artist);
    formData.append('genre', genre);
    formData.append('release_year', year);
    formData.append('album', album);

    try {
      const response = await uploadSong(formData);
      setSuccess('Song uploaded successfully');
      await loadSongs();
      e.target.value = '';
    } catch (err) {
      setError(err.message || 'Failed to upload song');
    } finally {
      setUploading(false);
    }
  };

  const handleCreatePlaylist = async (e) => {
    e.preventDefault();
    if (!newPlaylistName.trim()) {
      setError('Playlist name is required');
      return;
    }

    try {
      const playlist = await createPlaylist(newPlaylistName);
      setPlaylists([...playlists, playlist]);
      setNewPlaylistName('');
      setSuccess('Playlist created successfully');
    } catch (err) {
      setError(err.message);
    }
  };

  const handleAddToPlaylistClick = (song, playlistId) => {
    setSelectedSongForPlaylist(song);
    setSelectedPlaylistId(playlistId);
    setShowMetadataModal(true);
  };

  const handleConfirmAddToPlaylist = async () => {
    if (selectedSongForPlaylist && selectedPlaylistId) {
      try {
        await addSongToPlaylist(selectedPlaylistId, selectedSongForPlaylist.id);
        setSuccess('Song added to playlist successfully');
        await loadPlaylists();
      } catch (err) {
        setError(err.message);
      }
    }
    setShowMetadataModal(false);
    setSelectedSongForPlaylist(null);
    setSelectedPlaylistId('');
  };

  const handleViewPlaylist = (playlist) => {
    setSelectedPlaylist(playlist);
  };

  const handleBackToSongs = () => {
    setSelectedPlaylist(null);
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user_name');
    navigate('/login');
  };

  // Get available playlists for a song (excluding the current playlist)
  const getAvailablePlaylists = (songId) => {
    return playlists.filter(playlist => 
      !playlist.songs?.some(song => song.id === songId)
    );
  };

  // Handle like/unlike song
  const handleLikeSong = (song) => {
    const newLikedSongs = likedSongs.includes(song.id)
      ? likedSongs.filter(id => id !== song.id)
      : [...likedSongs, song.id];
    setLikedSongs(newLikedSongs);
    localStorage.setItem('likedSongs', JSON.stringify(newLikedSongs));
  };

  // Handle share song
  const handleShareSong = (song) => {
    const shareUrl = `${window.location.origin}/share/${song.id}`;
    if (navigator.share) {
      navigator.share({
        title: song.title,
        text: `Check out this song: ${song.title} by ${song.artist}`,
        url: shareUrl
      }).catch(console.error);
    } else {
      navigator.clipboard.writeText(shareUrl).then(() => {
        setSuccess('Share link copied to clipboard!');
        // Show a temporary notification
        setTimeout(() => setSuccess(''), 3000);
      }).catch(() => {
        setError('Failed to copy share link');
      });
    }
  };

  // Get liked songs
  const getLikedSongs = () => {
    return songs.filter(song => likedSongs.includes(song.id));
  };

  const handleShuffle = () => {
    if (!isShuffled) {
      // Create a copy of songs array and shuffle it
      const songsToShuffle = [...songs];
      for (let i = songsToShuffle.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [songsToShuffle[i], songsToShuffle[j]] = [songsToShuffle[j], songsToShuffle[i]];
      }
      setShuffledSongs(songsToShuffle);
    }
    setIsShuffled(!isShuffled);
  };

  const handleSongClick = async (song, index) => {
    try {
      if (currentSong?.id === song.id) {
        // If clicking the same song, toggle play/pause
        if (isPlaying) {
          audioRef.current.pause();
          setIsPlaying(false);
        } else {
          await audioRef.current.play();
          setIsPlaying(true);
        }
      } else {
        // If clicking a different song, play it
        if (audioRef.current) {
          audioRef.current.pause();
          setIsPlaying(false);
        }
        
        // Set new song
        setCurrentSong(song);
        setCurrentSongIndex(index);
        
        // Update audio source and play
        audioRef.current.src = `http://127.0.0.1:5000${song.file_path}`;
        await audioRef.current.load();
        await audioRef.current.play();
        setIsPlaying(true);
      }
    } catch (error) {
      console.error('Error playing audio:', error);
      setError('Failed to play audio. Please try again.');
      setIsPlaying(false);
    }
  };

  const handlePlayPause = async () => {
    if (!audioRef.current || !currentSong) return;

    try {
      if (isPlaying) {
        await audioRef.current.pause();
        setIsPlaying(false);
      } else {
        await audioRef.current.play();
        setIsPlaying(true);
      }
    } catch (error) {
      console.error('Error playing audio:', error);
      setError('Failed to play audio. Please try again.');
      setIsPlaying(false);
    }
  };

  const getNextSong = () => {
    if (!currentSong) return null;
    
    const currentIndex = isShuffled
      ? shuffledSongs.findIndex(song => song.id === currentSong.id)
      : songs.findIndex(song => song.id === currentSong.id);
    
    if (currentIndex === -1) return null;
    
    const nextIndex = (currentIndex + 1) % (isShuffled ? shuffledSongs.length : songs.length);
    return isShuffled ? shuffledSongs[nextIndex] : songs[nextIndex];
  };

  const getPreviousSong = () => {
    if (!currentSong) return null;
    
    const currentIndex = isShuffled
      ? shuffledSongs.findIndex(song => song.id === currentSong.id)
      : songs.findIndex(song => song.id === currentSong.id);
    
    if (currentIndex === -1) return null;
    
    const prevIndex = (currentIndex - 1 + (isShuffled ? shuffledSongs.length : songs.length)) % (isShuffled ? shuffledSongs.length : songs.length);
    return isShuffled ? shuffledSongs[prevIndex] : songs[prevIndex];
  };

  const handleNextSong = () => {
    const nextSong = getNextSong();
    if (nextSong) {
      handleSongClick(nextSong, songs.findIndex(song => song.id === nextSong.id));
    }
  };

  const handlePreviousSong = () => {
    const prevSong = getPreviousSong();
    if (prevSong) {
      handleSongClick(prevSong, songs.findIndex(song => song.id === prevSong.id));
    }
  };

  // Add audio event handlers
  useEffect(() => {
    if (audioRef.current) {
      const handleEnded = () => {
        handleNextSong();
      };

      const handleTimeUpdate = () => {
        setCurrentTime(audioRef.current.currentTime);
      };

      const handleError = (e) => {
        console.error('Audio error:', e);
        setIsPlaying(false);
        setError('Error playing audio. Please try again.');
      };

      const handlePlay = () => {
        setIsPlaying(true);
        setError(null);
      };

      const handlePause = () => {
        setIsPlaying(false);
      };

      const handleCanPlay = () => {
        setError(null);
      };

      audioRef.current.addEventListener('ended', handleEnded);
      audioRef.current.addEventListener('timeupdate', handleTimeUpdate);
      audioRef.current.addEventListener('error', handleError);
      audioRef.current.addEventListener('play', handlePlay);
      audioRef.current.addEventListener('pause', handlePause);
      audioRef.current.addEventListener('canplay', handleCanPlay);

      return () => {
        if (audioRef.current) {
          audioRef.current.removeEventListener('ended', handleEnded);
          audioRef.current.removeEventListener('timeupdate', handleTimeUpdate);
          audioRef.current.removeEventListener('error', handleError);
          audioRef.current.removeEventListener('play', handlePlay);
          audioRef.current.removeEventListener('pause', handlePause);
          audioRef.current.removeEventListener('canplay', handleCanPlay);
        }
      };
    }
  }, [currentSong]);

  // Initialize audio element
  useEffect(() => {
    if (!audioRef.current) {
      audioRef.current = new Audio();
      audioRef.current.preload = 'auto';
    }
  }, []);

  // Cleanup audio on component unmount
  useEffect(() => {
    return () => {
      if (audioRef.current) {
        audioRef.current.pause();
        audioRef.current.src = '';
        audioRef.current.load();
      }
    };
  }, []);

  // Add error message timeout
  useEffect(() => {
    if (error) {
      const timer = setTimeout(() => {
        setError(null);
      }, 3000);
      return () => clearTimeout(timer);
    }
  }, [error]);

  // Add audio controls
  const handleVolumeChange = (newVolume) => {
    setVolume(newVolume);
    if (audioRef.current) {
      audioRef.current.volume = newVolume;
    }
  };

  // Filter songs and playlists based on search query
  const filteredSongs = songs.filter(song =>
    song.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
    song.artist.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const filteredPlaylists = playlists.filter(playlist =>
    playlist.name.toLowerCase().includes(searchQuery.toLowerCase())
  );

  // Render song card with like and share buttons
  const renderSongCard = (song, index) => (
    <div
      key={song.id}
      className="bg-white rounded-lg shadow-md p-4 flex items-center justify-between hover:shadow-lg transition-shadow duration-300"
    >
      <div>
        <h3 className="font-semibold">{song.title}</h3>
        <p className="text-sm text-gray-600">{song.artist}</p>
        <button
          onClick={() => handleShowMetadata(song)}
          className="text-xs text-blue-500 hover:text-blue-600 mt-1"
        >
          Show Details
        </button>
      </div>
      <div className="flex items-center gap-2">
        <select
          onChange={(e) => handleAddToPlaylistClick(song, e.target.value)}
          className="px-2 py-1 border rounded text-sm"
          defaultValue=""
        >
          <option value="" disabled>Add to...</option>
          {getAvailablePlaylists(song.id).map((playlist) => (
            <option key={playlist.id} value={playlist.id}>
              {playlist.name}
            </option>
          ))}
        </select>
        <button
          onClick={() => handleLikeSong(song)}
          className={`p-2 rounded-full ${
            likedSongs.includes(song.id)
              ? 'text-red-500'
              : 'text-gray-400 hover:text-gray-500'
          }`}
        >
          <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill={likedSongs.includes(song.id) ? 'currentColor' : 'none'} viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
          </svg>
        </button>
        <button
          onClick={() => handleShareSong(song)}
          className="p-2 text-gray-400 hover:text-gray-500 rounded-full"
        >
          <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m0 2.684l6.632 3.316m-6.632-6l6.632-3.316m0 0a3 3 0 105.367-2.684 3 3 0 00-5.367 2.684zm0 9.316a3 3 0 105.368 2.684 3 3 0 00-5.368-2.684z" />
          </svg>
        </button>
        <button
          onClick={() => handleSongClick(song, index)}
          className="p-2 text-blue-500 hover:text-blue-600 rounded-full"
        >
          <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z" />
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        </button>
      </div>
    </div>
  );

  const handleShowMetadata = (song) => {
    setSelectedSongMetadata(song);
    setShowMetadataModal(true);
  };

  const handlePasteShareLink = async () => {
    try {
      setShareError('');
      // Extract song ID from share link
      const match = shareLink.match(/\/share\/(\d+)/);
      if (!match) {
        setShareError('Invalid share link format');
        return;
      }

      const songId = match[1];
      const response = await fetch(`http://127.0.0.1:5000/api/songs/${songId}`);
      if (!response.ok) {
        throw new Error('Failed to fetch song');
      }
      const song = await response.json();
      setSharedSong(song);
      setShareLink('');
      setSuccess('Song loaded successfully');
    } catch (err) {
      console.error('Error loading shared song:', err);
      setShareError('Failed to load shared song. Please check if the song exists.');
    }
  };

  // Add this function to format metadata display
  const formatMetadata = (song) => {
    return {
      title: song.title || 'Unknown',
      artist: song.artist || 'Unknown Artist',
      genre: song.genre || 'Unknown',
      year: song.release_year || 'Unknown',
      album: song.album || 'Unknown'
    };
  };

  return (
    <div className="container mx-auto px-4 py-8 pb-32">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold">Music App</h1>
        <div className="flex items-center gap-4">
          <div className="flex items-center gap-2">
            <div className="w-10 h-10 rounded-full bg-gray-200 overflow-hidden flex items-center justify-center">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-gray-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
              </svg>
            </div>
            <span className="text-gray-700 font-medium">{userName || 'User'}</span>
          </div>
          <button
            onClick={handleLogout}
            className="bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600"
          >
            Logout
          </button>
        </div>
      </div>

      {/* Search Section */}
      <div className="mb-8">
        <input
          type="text"
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          placeholder="Search songs and playlists..."
          className="w-full px-4 py-2 border rounded"
        />
      </div>

      {/* Upload Song and Create Playlist Section */}
      <div className="mb-8">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {/* Upload Song Section */}
          <div className="border-2 border-dashed border-gray-300 rounded-lg p-6">
            <h2 className="text-xl font-semibold mb-4">Upload Song</h2>
            <input
              type="file"
              accept="audio/*"
              onChange={handleFileUpload}
              disabled={uploading}
              className="block w-full text-sm text-gray-500
                file:mr-4 file:py-2 file:px-4
                file:rounded-full file:border-0
                file:text-sm file:font-semibold
                file:bg-blue-50 file:text-blue-700
                hover:file:bg-blue-100"
            />
            {uploading && (
              <p className="mt-2 text-sm text-gray-500">Uploading...</p>
            )}
          </div>

          {/* Create Playlist Form */}
          <div className="border-2 border-dashed border-gray-300 rounded-lg p-6">
            <h2 className="text-xl font-semibold mb-4">Create New Playlist</h2>
            <form onSubmit={handleCreatePlaylist} className="flex gap-4">
              <input
                type="text"
                value={newPlaylistName}
                onChange={(e) => setNewPlaylistName(e.target.value)}
                placeholder="Enter playlist name"
                className="flex-1 px-4 py-2 border rounded"
              />
              <button
                type="submit"
                className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
              >
                Create Playlist
              </button>
            </form>
          </div>
        </div>
      </div>

      {/* Paste Share Link Section */}
      <div className="mb-8">
        <div className="border-2 border-dashed border-gray-300 rounded-lg p-6">
          <h2 className="text-xl font-semibold mb-4">Paste Share Link</h2>
          <div className="flex gap-4">
            <input
              type="text"
              value={shareLink}
              onChange={(e) => setShareLink(e.target.value)}
              placeholder="Paste song share link here"
              className="flex-1 px-4 py-2 border rounded"
            />
            <button
              onClick={handlePasteShareLink}
              className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
            >
              Load Song
            </button>
          </div>
          {shareError && (
            <p className="mt-2 text-sm text-red-500">{shareError}</p>
          )}
        </div>
      </div>

      {/* Shared Song Section */}
      {sharedSong && (
        <div className="mb-8">
          <h2 className="text-2xl font-semibold mb-4">Shared Song</h2>
          <div className="space-y-2">
            {renderSongCard(sharedSong, -1)}
          </div>
        </div>
      )}

      {/* Liked Songs Section */}
      {likedSongs.length > 0 && (
        <div className="mb-8">
          <h2 className="text-2xl font-semibold mb-4">Liked Songs</h2>
          <div className="space-y-2">
            {getLikedSongs().map((song, index) => renderSongCard(song, index))}
          </div>
        </div>
      )}

      {/* Your Songs Section */}
      <div className="mb-8">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-2xl font-semibold">Your Songs</h2>
          {filteredSongs.length > SONGS_TO_SHOW && (
            <button
              onClick={() => setShowAllSongs(!showAllSongs)}
              className="text-blue-500 hover:text-blue-600 flex items-center gap-1"
            >
              {showAllSongs ? (
                <>
                  <span>Show Less</span>
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 15l7-7 7 7" />
                  </svg>
                </>
              ) : (
                <>
                  <span>Show All</span>
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                  </svg>
                </>
              )}
            </button>
          )}
        </div>
        <div className="space-y-2">
          {(showAllSongs ? filteredSongs : filteredSongs.slice(0, SONGS_TO_SHOW)).map((song, index) => renderSongCard(song, index))}
        </div>
      </div>

      {/* Your Playlists Section */}
      <div className="mb-8">
        <h2 className="text-2xl font-semibold mb-4">Your Playlists</h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
          {playlists.map((playlist) => (
            <div
              key={playlist.id}
              className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow duration-300"
            >
              <div className="p-4">
                <div className="flex justify-between items-center">
                  <div>
                    <h3 className="font-semibold">{playlist.name}</h3>
                    <p className="text-gray-600">{playlist.artist || 'Various Artists'}</p>
                  </div>
                  <button
                    onClick={() => handleViewPlaylist(playlist)}
                    className="bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600"
                  >
                    View Songs
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Player */}
      {currentSong && (
        <Player
          currentSong={currentSong}
          onNext={handleNextSong}
          onPrevious={handlePreviousSong}
          isPlaying={isPlaying}
          onPlayPause={handlePlayPause}
          onTimeUpdate={setCurrentTime}
          onVolumeChange={handleVolumeChange}
          volume={volume}
          onShuffle={handleShuffle}
          isShuffled={isShuffled}
        />
      )}

      {/* Playlist Songs Modal */}
      {selectedPlaylist && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4">
          <div className="bg-white rounded-lg p-6 max-w-2xl w-full max-h-[80vh] overflow-y-auto">
            <div className="flex justify-between items-center mb-4">
              <h3 className="text-xl font-semibold">{selectedPlaylist.name}</h3>
              <button
                onClick={handleBackToSongs}
                className="text-gray-500 hover:text-gray-700"
              >
                ✕
              </button>
            </div>
            <div className="space-y-2">
              {selectedPlaylist.songs && selectedPlaylist.songs.length > 0 ? (
                selectedPlaylist.songs.map((song, index) => renderSongCard(song, index))
              ) : (
                <p className="text-gray-500">No songs in this playlist</p>
              )}
            </div>
          </div>
        </div>
      )}

      {/* Metadata Modal */}
      {showMetadataModal && selectedSongMetadata && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg p-6 max-w-md w-full">
            <div className="flex justify-between items-center mb-4">
              <h3 className="text-xl font-semibold">Song Details</h3>
              <button
                onClick={() => {
                  setShowMetadataModal(false);
                  setSelectedSongMetadata(null);
                }}
                className="text-gray-500 hover:text-gray-700"
              >
                ✕
              </button>
            </div>
            <div className="space-y-3">
              {Object.entries(formatMetadata(selectedSongMetadata)).map(([key, value]) => (
                <p key={key} className="flex justify-between">
                  <span className="font-medium">
                    {key === 'title' ? 'Tên bài hát:' :
                     key === 'artist' ? 'Ca sĩ:' :
                     key === 'genre' ? 'Thể loại:' :
                     key === 'year' ? 'Năm phát hành:' :
                     'Album:'}
                  </span>
                  <span className="text-gray-700">{value}</span>
                </p>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Success/Error Messages */}
      {success && (
        <div className="fixed bottom-20 left-1/2 transform -translate-x-1/2 bg-green-500 text-white px-4 py-2 rounded shadow-lg">
          {success}
        </div>
      )}
      {error && (
        <div className="fixed bottom-20 left-1/2 transform -translate-x-1/2 bg-red-500 text-white px-4 py-2 rounded shadow-lg">
          {error}
        </div>
      )}
    </div>
  );
};

export default Home; 