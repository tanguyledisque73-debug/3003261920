import React, { useState, useEffect } from 'react';
import { Play } from 'lucide-react';

const API_URL = process.env.REACT_APP_BACKEND_URL;

function VideoPlayer({ chapterId, ficheId, position = 'top' }) {
  const [videos, setVideos] = useState([]);

  useEffect(() => {
    if (chapterId) {
      loadVideos();
    }
  }, [chapterId, ficheId]);

  const loadVideos = async () => {
    try {
      const token = localStorage.getItem('token');
      if (!token) return;

      const response = await fetch(`${API_URL}/api/admin/videos?token=${token}`);
      const allVideos = await response.json();

      // Filter videos for this chapter/fiche
      const filtered = allVideos.filter(v => {
        if (ficheId && v.fiche_id === ficheId) return true;
        if (!ficheId && v.chapter_id === chapterId && !v.fiche_id) return true;
        return false;
      }).filter(v => v.position === position);

      setVideos(filtered);
    } catch (error) {
      console.error('Erreur chargement vidéos:', error);
    }
  };

  const renderVideo = (video) => {
    if (video.video_type === 'youtube') {
      const videoId = extractYouTubeId(video.video_url);
      return (
        <iframe
          src={`https://www.youtube.com/embed/${videoId}`}
          title={video.title}
          className="w-full h-64 md:h-96 rounded-lg"
          frameBorder="0"
          allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
          allowFullScreen
        />
      );
    }

    if (video.video_type === 'vimeo') {
      const videoId = extractVimeoId(video.video_url);
      return (
        <iframe
          src={`https://player.vimeo.com/video/${videoId}`}
          title={video.title}
          className="w-full h-64 md:h-96 rounded-lg"
          frameBorder="0"
          allow="autoplay; fullscreen; picture-in-picture"
          allowFullScreen
        />
      );
    }

    if (video.video_type === 'upload') {
      return (
        <video
          controls
          className="w-full h-64 md:h-96 rounded-lg"
          poster={video.thumbnail_url ? `${API_URL}${video.thumbnail_url}` : undefined}
        >
          <source src={`${API_URL}${video.video_url}`} type="video/mp4" />
          Votre navigateur ne supporte pas la lecture de vidéos.
        </video>
      );
    }

    return null;
  };

  if (videos.length === 0) return null;

  return (
    <div className="space-y-4 my-6">
      {videos.map((video) => (
        <div key={video.id} className="bg-gray-50 rounded-lg p-4">
          <div className="flex items-center mb-3">
            <Play className="w-5 h-5 text-red-600 mr-2" />
            <h4 className="font-semibold text-gray-900">{video.title}</h4>
          </div>
          {renderVideo(video)}
        </div>
      ))}
    </div>
  );
}

function extractYouTubeId(url) {
  const regExp = /^.*((youtu.be\/)|(v\/)|(\/u\/\w\/)|(embed\/)|(watch\?))\??v?=?([^#&?]*).*/;
  const match = url.match(regExp);
  return (match && match[7].length === 11) ? match[7] : null;
}

function extractVimeoId(url) {
  const regExp = /vimeo.*\/(\d+)/i;
  const match = url.match(regExp);
  return match ? match[1] : null;
}

export default VideoPlayer;
