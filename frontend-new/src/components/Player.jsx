import React, { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';

const Player = ({
  currentSong,
  onNext,
  onPrevious,
  isPlaying,
  onPlayPause,
  onTimeUpdate,
  onVolumeChange,
  volume,
  onShuffle,
  isShuffled
}) => {
  const [currentTime, setCurrentTime] = useState(0);
  const [duration, setDuration] = useState(0);
  const [isLiked, setIsLiked] = useState(false);
  const audioRef = useRef(null);
  const navigate = useNavigate();
  const [showMetadata, setShowMetadata] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (currentSong) {
      // Check if song is liked
      const likedSongs = JSON.parse(localStorage.getItem('likedSongs') || '[]');
      setIsLiked(likedSongs.includes(currentSong.id));
    }
  }, [currentSong]);

  useEffect(() => {
    if (audioRef.current) {
      audioRef.current.volume = volume;
    }
  }, [volume]);

  const handleTimeUpdate = () => {
    if (audioRef.current) {
      setCurrentTime(audioRef.current.currentTime);
      setDuration(audioRef.current.duration);
      onTimeUpdate(audioRef.current.currentTime);
    }
  };

  const handleSeek = (e) => {
    const time = e.target.value;
    setCurrentTime(time);
    if (audioRef.current) {
      audioRef.current.currentTime = time;
    }
  };

  const handlePlayPauseClick = () => {
    if (audioRef.current) {
      if (isPlaying) {
        audioRef.current.pause();
      } else {
        audioRef.current.play().catch(error => {
          console.error('Error playing audio:', error);
          setError('Failed to play audio. Please try again.');
        });
      }
      onPlayPause();
    }
  };

  useEffect(() => {
    if (audioRef.current) {
      const handlePlay = () => {
        onPlayPause();
      };
      const handlePause = () => {
        onPlayPause();
      };

      audioRef.current.addEventListener('play', handlePlay);
      audioRef.current.addEventListener('pause', handlePause);

      return () => {
        audioRef.current.removeEventListener('play', handlePlay);
        audioRef.current.removeEventListener('pause', handlePause);
      };
    }
  }, [onPlayPause]);

  const formatTime = (time) => {
    if (isNaN(time)) return '0:00';
    const minutes = Math.floor(time / 60);
    const seconds = Math.floor(time % 60);
    return `${minutes}:${seconds.toString().padStart(2, '0')}`;
  };

  const handleLike = () => {
    if (!currentSong) return;
    
    const likedSongs = JSON.parse(localStorage.getItem('likedSongs') || '[]');
    if (isLiked) {
      const newLikedSongs = likedSongs.filter(id => id !== currentSong.id);
      localStorage.setItem('likedSongs', JSON.stringify(newLikedSongs));
    } else {
      likedSongs.push(currentSong.id);
      localStorage.setItem('likedSongs', JSON.stringify(likedSongs));
    }
    setIsLiked(!isLiked);
  };

  const handleShare = () => {
    if (!currentSong) return;
    
    const shareUrl = `${window.location.origin}/share/${currentSong.id}`;
    if (navigator.share) {
      navigator.share({
        title: currentSong.title,
        text: `Check out this song: ${currentSong.title} by ${currentSong.artist}`,
        url: shareUrl
      }).catch(console.error);
    } else {
      navigator.clipboard.writeText(shareUrl)
        .then(() => {
          alert('Link copied to clipboard!');
        })
        .catch(err => {
          console.error('Failed to copy link:', err);
        });
    }
  };

  return (
    <div className="fixed bottom-0 left-0 right-0 bg-white border-t shadow-lg p-4">
      <audio
        ref={audioRef}
        src={currentSong ? `http://127.0.0.1:5000${currentSong.file_path}` : ''}
        onTimeUpdate={handleTimeUpdate}
        onEnded={onNext}
        onLoadedMetadata={() => setDuration(audioRef.current?.duration || 0)}
        onError={() => setError('Failed to load audio file')}
        preload="metadata"
      />
      
      <div className="container mx-auto flex items-center justify-between">
        {/* Song Info */}
        <div className="flex items-center space-x-4">
          <div>
            <h3 className="font-semibold">{currentSong?.title}</h3>
            <p className="text-sm text-gray-600">{currentSong?.artist}</p>
            <button
              onClick={() => setShowMetadata(!showMetadata)}
              className="text-xs text-blue-500 hover:text-blue-600 mt-1"
            >
              {showMetadata ? 'Hide Details' : 'Show Details'}
            </button>
            {showMetadata && (
              <div className="text-xs text-gray-500 mt-2 space-y-1">
                <p><span className="font-medium">Tên bài hát:</span> {currentSong?.title}</p>
                <p><span className="font-medium">Ca sĩ:</span> {currentSong?.artist}</p>
                <p><span className="font-medium">Thể loại:</span> {currentSong?.genre || 'Unknown'}</p>
                <p><span className="font-medium">Thời lượng:</span> {formatTime(duration)}</p>
                <p><span className="font-medium">Năm phát hành:</span> {currentSong?.release_year || 'Unknown'}</p>
                <p><span className="font-medium">Album:</span> {currentSong?.album || 'Unknown'}</p>
              </div>
            )}
          </div>
        </div>

        {/* Player Controls */}
        <div className="flex flex-col items-center w-1/3">
          <div className="flex items-center gap-4 mb-2">
            <button
              onClick={onShuffle}
              className={`p-2 rounded-full ${isShuffled ? 'text-blue-500' : 'text-gray-400'}`}
            >
              <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
              </svg>
            </button>
            <button
              onClick={onPrevious}
              className="p-2 text-gray-400 hover:text-gray-500 rounded-full"
            >
              <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 19l-7-7 7-7m8 14l-7-7 7-7" />
              </svg>
            </button>
            <button
              onClick={handlePlayPauseClick}
              className="p-3 bg-blue-500 text-white rounded-full hover:bg-blue-600"
            >
              {isPlaying ? (
                <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 9v6m4-6v6m7-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              ) : (
                <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z" />
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              )}
            </button>
            <button
              onClick={onNext}
              className="p-2 text-gray-400 hover:text-gray-500 rounded-full"
            >
              <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 5l7 7-7 7M5 5l7 7-7 7" />
              </svg>
            </button>
          </div>
          
          {/* Progress Bar */}
          <div className="w-full flex items-center gap-2">
            <span className="text-sm text-gray-500">{formatTime(currentTime)}</span>
            <input
              type="range"
              min="0"
              max={duration || 0}
              value={currentTime}
              onChange={handleSeek}
              className="w-full h-1 bg-gray-200 rounded-lg appearance-none cursor-pointer"
            />
            <span className="text-sm text-gray-500">{formatTime(duration)}</span>
          </div>
        </div>

        {/* Volume Control */}
        <div className="flex items-center gap-2 w-1/3 justify-end">
          <button
            onClick={handleLike}
            className={`p-2 rounded-full hover:bg-gray-100 ${isLiked ? 'text-red-500' : 'text-gray-600'}`}
          >
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill={isLiked ? 'currentColor' : 'none'} viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
            </svg>
          </button>
          <button
            onClick={handleShare}
            className="p-2 rounded-full hover:bg-gray-100 text-gray-600"
          >
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m0 2.684l6.632 3.316m-6.632-6l6.632-3.316m0 0a3 3 0 105.367-2.684 3 3 0 00-5.367 2.684zm0 9.316a3 3 0 105.368 2.684 3 3 0 00-5.368-2.684z" />
            </svg>
          </button>
          <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15.536 8.464a5 5 0 010 7.072m2.828-9.9a9 9 0 010 12.728M5.586 15.536a5 5 0 001.414 1.414m2.828-9.9a9 9 0 012.728-2.728" />
          </svg>
          <input
            type="range"
            min="0"
            max="1"
            step="0.1"
            value={volume}
            onChange={(e) => onVolumeChange(parseFloat(e.target.value))}
            className="w-24 h-1 bg-gray-200 rounded-lg appearance-none cursor-pointer"
          />
        </div>
      </div>

      {/* Error Message */}
      {error && (
        <div className="fixed bottom-20 left-1/2 transform -translate-x-1/2 bg-red-500 text-white px-4 py-2 rounded shadow-lg">
          {error}
        </div>
      )}
    </div>
  );
};

export default Player; 