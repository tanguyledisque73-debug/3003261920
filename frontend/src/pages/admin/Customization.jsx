import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  Settings, 
  Image as ImageIcon, 
  Video, 
  Palette, 
  Type, 
  Eye,
  Save,
  RefreshCw
} from 'lucide-react';
import BannerManager from '../../components/admin/BannerManager';
import VideoManager from '../../components/admin/VideoManager';
import StyleEditor from '../../components/admin/StyleEditor';
import HomePageEditor from '../../components/admin/HomePageEditor';
import LivePreview from '../../components/admin/LivePreview';

const API_URL = process.env.REACT_APP_BACKEND_URL;

function Customization() {
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState('home');
  const [customization, setCustomization] = useState(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [showPreview, setShowPreview] = useState(false);
  const [hasChanges, setHasChanges] = useState(false);

  useEffect(() => {
    loadCustomization();
  }, []);

  const loadCustomization = async () => {
    try {
      const response = await fetch(`${API_URL}/api/customization`);
      const data = await response.json();
      setCustomization(data);
      setLoading(false);
    } catch (error) {
      console.error('Erreur chargement personnalisation:', error);
      setLoading(false);
    }
  };

  const saveCustomization = async () => {
    setSaving(true);
    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`${API_URL}/api/admin/customization?token=${token}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(customization),
      });

      if (response.ok) {
        alert('✅ Personnalisation sauvegardée avec succès !');
        setHasChanges(false);
      } else {
        alert('❌ Erreur lors de la sauvegarde');
      }
    } catch (error) {
      console.error('Erreur sauvegarde:', error);
      alert('❌ Erreur lors de la sauvegarde');
    } finally {
      setSaving(false);
    }
  };

  const updateCustomization = (section, data) => {
    setCustomization(prev => ({
      ...prev,
      [section]: data
    }));
    setHasChanges(true);
  };

  const tabs = [
    { id: 'home', label: 'Page d\'accueil', icon: Settings },
    { id: 'banners', label: 'Bannières', icon: ImageIcon },
    { id: 'videos', label: 'Vidéos', icon: Video },
    { id: 'styles', label: 'Styles & Couleurs', icon: Palette },
  ];

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="text-center">
          <RefreshCw className="w-12 h-12 animate-spin mx-auto mb-4 text-red-600" />
          <p className="text-gray-600">Chargement...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white shadow-sm border-b sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center space-x-4">
              <button
                onClick={() => navigate('/admin')}
                className="text-gray-600 hover:text-gray-900"
              >
                ← Retour
              </button>
              <h1 className="text-2xl font-bold text-gray-900">
                🎨 Personnalisation du Site
              </h1>
            </div>
            
            <div className="flex items-center space-x-3">
              <button
                onClick={() => setShowPreview(!showPreview)}
                className="flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition"
              >
                <Eye className="w-4 h-4 mr-2" />
                {showPreview ? 'Masquer' : 'Aperçu'}
              </button>
              
              <button
                onClick={saveCustomization}
                disabled={!hasChanges || saving}
                className={`flex items-center px-4 py-2 rounded-lg transition ${
                  hasChanges && !saving
                    ? 'bg-green-600 text-white hover:bg-green-700'
                    : 'bg-gray-300 text-gray-500 cursor-not-allowed'
                }`}
              >
                <Save className="w-4 h-4 mr-2" />
                {saving ? 'Sauvegarde...' : 'Sauvegarder'}
              </button>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-12 gap-6">
          {/* Sidebar Navigation */}
          <div className="col-span-3">
            <div className="bg-white rounded-lg shadow-sm p-4 space-y-2">
              {tabs.map((tab) => {
                const Icon = tab.icon;
                return (
                  <button
                    key={tab.id}
                    onClick={() => setActiveTab(tab.id)}
                    className={`w-full flex items-center px-4 py-3 rounded-lg transition ${
                      activeTab === tab.id
                        ? 'bg-red-600 text-white'
                        : 'text-gray-700 hover:bg-gray-100'
                    }`}
                  >
                    <Icon className="w-5 h-5 mr-3" />
                    {tab.label}
                  </button>
                );
              })}
            </div>

            {hasChanges && (
              <div className="mt-4 bg-yellow-50 border border-yellow-200 rounded-lg p-4">
                <p className="text-sm text-yellow-800">
                  ⚠️ Modifications non sauvegardées
                </p>
              </div>
            )}
          </div>

          {/* Main Content */}
          <div className="col-span-9">
            <div className="bg-white rounded-lg shadow-sm p-6">
              {activeTab === 'home' && (
                <HomePageEditor
                  data={customization?.home_page}
                  onChange={(data) => updateCustomization('home_page', data)}
                />
              )}
              
              {activeTab === 'banners' && (
                <BannerManager
                  banners={customization?.banners || []}
                  onChange={(data) => updateCustomization('banners', data)}
                />
              )}
              
              {activeTab === 'videos' && (
                <VideoManager />
              )}
              
              {activeTab === 'styles' && (
                <StyleEditor
                  styles={customization?.styles || {}}
                  colors={{
                    primary: customization?.primary_color,
                    secondary: customization?.secondary_color,
                    accent: customization?.accent_color,
                  }}
                  onChange={(data) => {
                    if (data.styles) {
                      updateCustomization('styles', data.styles);
                    }
                    if (data.primary_color) {
                      updateCustomization('primary_color', data.primary_color);
                    }
                    if (data.secondary_color) {
                      updateCustomization('secondary_color', data.secondary_color);
                    }
                    if (data.accent_color) {
                      updateCustomization('accent_color', data.accent_color);
                    }
                  }}
                />
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Live Preview Modal */}
      {showPreview && (
        <LivePreview
          customization={customization}
          onClose={() => setShowPreview(false)}
        />
      )}
    </div>
  );
}

export default Customization;
