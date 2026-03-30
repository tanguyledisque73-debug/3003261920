import React, { useState, useEffect } from 'react';
import { Plus, Trash2, Upload, ExternalLink, MoveUp, MoveDown } from 'lucide-react';

const API_URL = process.env.REACT_APP_BACKEND_URL;

function BannerManager({ banners: initialBanners, onChange }) {
  const [banners, setBanners] = useState(initialBanners || []);
  const [showAddModal, setShowAddModal] = useState(false);
  const [uploading, setUploading] = useState(false);

  useEffect(() => {
    loadBanners();
  }, []);

  const loadBanners = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`${API_URL}/api/admin/banners?token=${token}`);
      const data = await response.json();
      setBanners(data);
      if (onChange) onChange(data);
    } catch (error) {
      console.error('Erreur chargement bannières:', error);
    }
  };

  const uploadImage = async (file) => {
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

  const addBanner = async (bannerData) => {
    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`${API_URL}/api/admin/banner?token=${token}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(bannerData),
      });

      if (response.ok) {
        loadBanners();
        setShowAddModal(false);
      }
    } catch (error) {
      console.error('Erreur ajout bannière:', error);
    }
  };

  const deleteBanner = async (bannerId) => {
    if (!window.confirm('Supprimer cette bannière ?')) return;

    try {
      const token = localStorage.getItem('token');
      await fetch(`${API_URL}/api/admin/banner/${bannerId}?token=${token}`, {
        method: 'DELETE',
      });
      loadBanners();
    } catch (error) {
      console.error('Erreur suppression:', error);
    }
  };

  const moveUp = (index) => {
    if (index === 0) return;
    const newBanners = [...banners];
    [newBanners[index], newBanners[index - 1]] = [newBanners[index - 1], newBanners[index]];
    // Update order
    newBanners.forEach((b, i) => b.order = i);
    setBanners(newBanners);
  };

  const moveDown = (index) => {
    if (index === banners.length - 1) return;
    const newBanners = [...banners];
    [newBanners[index], newBanners[index + 1]] = [newBanners[index + 1], newBanners[index]];
    newBanners.forEach((b, i) => b.order = i);
    setBanners(newBanners);
  };

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-bold text-gray-900">Gestion des Bannières</h2>
        <button
          onClick={() => setShowAddModal(true)}
          className="flex items-center px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition"
        >
          <Plus className="w-4 h-4 mr-2" />
          Ajouter une bannière
        </button>
      </div>

      {/* Banners List */}
      <div className="space-y-4">
        {banners.length === 0 ? (
          <div className="text-center py-12 bg-gray-50 rounded-lg">
            <p className="text-gray-600">Aucune bannière. Ajoutez-en une !</p>
          </div>
        ) : (
          banners.map((banner, index) => (
            <div
              key={banner.id}
              className="flex items-center space-x-4 p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition"
            >
              <img
                src={`${API_URL}${banner.image_url}`}
                alt={banner.title}
                className="w-32 h-20 object-cover rounded"
              />
              
              <div className="flex-1">
                <h3 className="font-semibold text-gray-900">{banner.title}</h3>
                <p className="text-sm text-gray-600">Position: {banner.position}</p>
                {banner.link && (
                  <a
                    href={banner.link}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-sm text-blue-600 hover:underline flex items-center"
                  >
                    <ExternalLink className="w-3 h-3 mr-1" />
                    {banner.link}
                  </a>
                )}
              </div>

              <div className="flex items-center space-x-2">
                <button
                  onClick={() => moveUp(index)}
                  disabled={index === 0}
                  className={`p-2 rounded ${
                    index === 0
                      ? 'text-gray-300 cursor-not-allowed'
                      : 'text-gray-600 hover:bg-gray-200'
                  }`}
                >
                  <MoveUp className="w-4 h-4" />
                </button>
                
                <button
                  onClick={() => moveDown(index)}
                  disabled={index === banners.length - 1}
                  className={`p-2 rounded ${
                    index === banners.length - 1
                      ? 'text-gray-300 cursor-not-allowed'
                      : 'text-gray-600 hover:bg-gray-200'
                  }`}
                >
                  <MoveDown className="w-4 h-4" />
                </button>

                <button
                  onClick={() => deleteBanner(banner.id)}
                  className="p-2 text-red-600 hover:bg-red-50 rounded"
                >
                  <Trash2 className="w-4 h-4" />
                </button>
              </div>
            </div>
          ))
        )}
      </div>

      {/* Add Banner Modal */}
      {showAddModal && (
        <AddBannerModal
          onClose={() => setShowAddModal(false)}
          onAdd={addBanner}
          onUpload={uploadImage}
          uploading={uploading}
        />
      )}
    </div>
  );
}

function AddBannerModal({ onClose, onAdd, onUpload, uploading }) {
  const [formData, setFormData] = useState({
    title: '',
    image_url: '',
    link: '',
    position: 'home_hero',
    order: 0,
    is_active: true,
  });

  const handleFileUpload = async (e) => {
    const file = e.target.files[0];
    if (file) {
      const url = await onUpload(file);
      if (url) {
        setFormData(prev => ({ ...prev, image_url: url }));
      }
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!formData.title || !formData.image_url) {
      alert('Titre et image requis');
      return;
    }
    onAdd(formData);
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg p-6 max-w-md w-full">
        <h3 className="text-xl font-bold mb-4">Ajouter une bannière</h3>
        
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Titre *
            </label>
            <input
              type="text"
              value={formData.title}
              onChange={(e) => setFormData(prev => ({ ...prev, title: e.target.value }))}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-600 focus:border-transparent"
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Image *
            </label>
            <div className="flex space-x-2">
              <input
                type="file"
                accept="image/*"
                onChange={handleFileUpload}
                className="flex-1 px-3 py-2 border border-gray-300 rounded-lg"
                disabled={uploading}
              />
            </div>
            {uploading && <p className="text-sm text-gray-600 mt-1">Upload en cours...</p>}
            {formData.image_url && (
              <img
                src={`${API_URL}${formData.image_url}`}
                alt="Preview"
                className="mt-2 w-full h-32 object-cover rounded"
              />
            )}
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Lien (optionnel)
            </label>
            <input
              type="url"
              value={formData.link}
              onChange={(e) => setFormData(prev => ({ ...prev, link: e.target.value }))}
              placeholder="https://..."
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-600 focus:border-transparent"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Position
            </label>
            <select
              value={formData.position}
              onChange={(e) => setFormData(prev => ({ ...prev, position: e.target.value }))}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-600 focus:border-transparent"
            >
              <option value="home_hero">Hero (page d'accueil)</option>
              <option value="home_banner">Bannière (page d'accueil)</option>
              <option value="header">En-tête (toutes les pages)</option>
              <option value="chapter_top">Haut de chapitre</option>
              <option value="custom">Personnalisé</option>
            </select>
          </div>

          <div className="flex justify-end space-x-3 pt-4">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200 transition"
            >
              Annuler
            </button>
            <button
              type="submit"
              disabled={uploading}
              className="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition disabled:bg-gray-300"
            >
              Ajouter
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default BannerManager;
