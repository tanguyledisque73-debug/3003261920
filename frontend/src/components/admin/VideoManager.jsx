import React, { useState, useEffect } from 'react';
import { Plus, Trash2, Video as VideoIcon, Upload, Link as LinkIcon } from 'lucide-react';

const API_URL = process.env.REACT_APP_BACKEND_URL;

function VideoManager() {
  const [videos, setVideos] = useState([]);
  const [chapters, setChapters] = useState([]);
  const [showAddModal, setShowAddModal] = useState(false);
  const [uploading, setUploading] = useState(false);

  useEffect(() => {
    loadVideos();
    loadChapters();
  }, []);

  const loadVideos = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`${API_URL}/api/admin/videos?token=${token}`);
      const data = await response.json();
      setVideos(data);
    } catch (error) {
      console.error('Erreur chargement vidéos:', error);
    }
  };

  const loadChapters = async () => {
    try {
      const response = await fetch(`${API_URL}/api/chapters`);
      const data = await response.json();
      setChapters(data);
    } catch (error) {
      console.error('Erreur chargement chapitres:', error);
    }
  };

  const addVideo = async (videoData) => {
    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`${API_URL}/api/admin/video?token=${token}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(videoData),
      });

      if (response.ok) {
        loadVideos();
        setShowAddModal(false);
      }
    } catch (error) {
      console.error('Erreur ajout vidéo:', error);
    }
  };

  const deleteVideo = async (videoId) => {
    if (!window.confirm('Supprimer cette vidéo ?')) return;

    try {
      const token = localStorage.getItem('token');
      await fetch(`${API_URL}/api/admin/video/${videoId}?token=${token}`, {
        method: 'DELETE',
      });
      loadVideos();
    } catch (error) {
      console.error('Erreur suppression:', error);
    }
  };

  const uploadVideo = async (file) => {
    setUploading(true);
    try {
      const token = localStorage.getItem('token');
      const formData = new FormData();
      formData.append('file', file);

      const response = await fetch(`${API_URL}/api/admin/upload-media?token=${token}`, {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();
      return data.url;
    } catch (error) {
      console.error('Erreur upload:', error);
      alert('Erreur lors de l\'upload');
      return null;
    } finally {
      setUploading(false);
    }
  };

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-bold text-gray-900">Gestion des Vidéos</h2>
        <button
          onClick={() => setShowAddModal(true)}
          className="flex items-center px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition"
        >
          <Plus className="w-4 h-4 mr-2" />
          Ajouter une vidéo
        </button>
      </div>

      {/* Videos Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {videos.length === 0 ? (
          <div className="col-span-2 text-center py-12 bg-gray-50 rounded-lg">
            <VideoIcon className="w-12 h-12 mx-auto text-gray-400 mb-4" />
            <p className="text-gray-600">Aucune vidéo. Ajoutez-en une !</p>
          </div>
        ) : (
          videos.map((video) => (
            <div key={video.id} className="bg-gray-50 rounded-lg p-4 hover:bg-gray-100 transition">
              {video.video_type === 'upload' && video.video_url ? (
                <video
                  src={`${API_URL}${video.video_url}`}
                  controls
                  className="w-full h-40 object-cover rounded mb-3"
                />
              ) : (
                <div className="w-full h-40 bg-gray-200 rounded mb-3 flex items-center justify-center">
                  <VideoIcon className="w-12 h-12 text-gray-400" />
                </div>
              )}
              
              <h3 className="font-semibold text-gray-900 mb-1">{video.title}</h3>
              <p className="text-sm text-gray-600 mb-2">
                Type: {video.video_type === 'upload' ? 'Upload' : video.video_type.toUpperCase()}
              </p>
              
              {video.chapter_id && (
                <p className="text-sm text-gray-600 mb-2">
                  Chapitre: {chapters.find(c => c.id === video.chapter_id)?.titre || 'N/A'}
                </p>
              )}

              <button
                onClick={() => deleteVideo(video.id)}
                className="w-full mt-2 flex items-center justify-center px-3 py-2 bg-red-100 text-red-600 rounded hover:bg-red-200 transition"
              >
                <Trash2 className="w-4 h-4 mr-2" />
                Supprimer
              </button>
            </div>
          ))
        )}
      </div>

      {showAddModal && (
        <AddVideoModal
          onClose={() => setShowAddModal(false)}
          onAdd={addVideo}
          onUpload={uploadVideo}
          uploading={uploading}
          chapters={chapters}
        />
      )}
    </div>
  );
}

function AddVideoModal({ onClose, onAdd, onUpload, uploading, chapters }) {
  const [videoType, setVideoType] = useState('youtube');
  const [formData, setFormData] = useState({
    title: '',
    video_type: 'youtube',
    video_url: '',
    chapter_id: '',
    fiche_id: '',
    position: 'top',
  });

  const handleFileUpload = async (e) => {
    const file = e.target.files[0];
    if (file) {
      const url = await onUpload(file);
      if (url) {
        setFormData(prev => ({ ...prev, video_url: url, video_type: 'upload' }));
      }
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!formData.title || !formData.video_url) {
      alert('Titre et vidéo requis');
      return;
    }
    onAdd(formData);
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg p-6 max-w-md w-full max-h-[90vh] overflow-y-auto">
        <h3 className="text-xl font-bold mb-4">Ajouter une vidéo</h3>
        
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Type de vidéo
            </label>
            <div className="flex space-x-2">
              <button
                type="button"
                onClick={() => {
                  setVideoType('youtube');
                  setFormData(prev => ({ ...prev, video_type: 'youtube' }));
                }}
                className={`flex-1 py-2 rounded ${
                  videoType === 'youtube'
                    ? 'bg-red-600 text-white'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                YouTube
              </button>
              <button
                type="button"
                onClick={() => {
                  setVideoType('vimeo');
                  setFormData(prev => ({ ...prev, video_type: 'vimeo' }));
                }}
                className={`flex-1 py-2 rounded ${
                  videoType === 'vimeo'
                    ? 'bg-red-600 text-white'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                Vimeo
              </button>
              <button
                type="button"
                onClick={() => setVideoType('upload')}
                className={`flex-1 py-2 rounded ${
                  videoType === 'upload'
                    ? 'bg-red-600 text-white'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                Upload
              </button>
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Titre *
            </label>
            <input
              type="text"
              value={formData.title}
              onChange={(e) => setFormData(prev => ({ ...prev, title: e.target.value }))}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg"
              required
            />
          </div>

          {videoType === 'upload' ? (
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Fichier vidéo *
              </label>
              <input
                type="file"
                accept="video/*"
                onChange={handleFileUpload}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                disabled={uploading}
              />
              {uploading && <p className="text-sm text-gray-600 mt-1">Upload en cours...</p>}
            </div>
          ) : (
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                URL {videoType.toUpperCase()} *
              </label>
              <input
                type="url"
                value={formData.video_url}
                onChange={(e) => setFormData(prev => ({ ...prev, video_url: e.target.value }))}
                placeholder={`https://${videoType}.com/...`}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                required
              />
            </div>
          )}

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Chapitre (optionnel)
            </label>
            <select
              value={formData.chapter_id}
              onChange={(e) => setFormData(prev => ({ ...prev, chapter_id: e.target.value }))}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg"
            >
              <option value="">Aucun chapitre</option>
              {chapters.map(ch => (
                <option key={ch.id} value={ch.id}>
                  {ch.formation_type} - Ch{ch.numero}: {ch.titre}
                </option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Position
            </label>
            <select
              value={formData.position}
              onChange={(e) => setFormData(prev => ({ ...prev, position: e.target.value }))}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg"
            >
              <option value="top">Début du chapitre</option>
              <option value="inline">Dans le contenu</option>
              <option value="bottom">Fin du chapitre</option>
            </select>
          </div>

          <div className="flex justify-end space-x-3 pt-4">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200"
            >
              Annuler
            </button>
            <button
              type="submit"
              disabled={uploading}
              className="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 disabled:bg-gray-300"
            >
              Ajouter
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default VideoManager;
