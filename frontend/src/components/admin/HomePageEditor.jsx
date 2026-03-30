import React, { useState } from 'react';

function HomePageEditor({ data, onChange }) {
  const [formData, setFormData] = useState(data || {
    hero_title: '',
    hero_subtitle: '',
    hero_description: '',
    hero_button_text: '',
    hero_button_link: '',
  });

  const handleChange = (field, value) => {
    const newData = { ...formData, [field]: value };
    setFormData(newData);
    onChange(newData);
  };

  return (
    <div>
      <h2 className="text-2xl font-bold text-gray-900 mb-6">Page d'accueil</h2>

      <div className="space-y-6">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Titre principal (H1)
          </label>
          <input
            type="text"
            value={formData.hero_title}
            onChange={(e) => handleChange('hero_title', e.target.value)}
            placeholder="Bienvenue sur FAOD-SECOURS73"
            className="w-full px-4 py-3 border border-gray-300 rounded-lg text-lg focus:ring-2 focus:ring-red-600"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Sous-titre
          </label>
          <input
            type="text"
            value={formData.hero_subtitle}
            onChange={(e) => handleChange('hero_subtitle', e.target.value)}
            placeholder="Formation professionnelle aux premiers secours"
            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-600"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Description
          </label>
          <textarea
            value={formData.hero_description}
            onChange={(e) => handleChange('hero_description', e.target.value)}
            placeholder="Plateforme de formation en ligne pour les secouristes"
            rows={4}
            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-600"
          />
        </div>

        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Texte du bouton
            </label>
            <input
              type="text"
              value={formData.hero_button_text}
              onChange={(e) => handleChange('hero_button_text', e.target.value)}
              placeholder="Commencer"
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-600"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Lien du bouton
            </label>
            <input
              type="text"
              value={formData.hero_button_link}
              onChange={(e) => handleChange('hero_button_link', e.target.value)}
              placeholder="/login"
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-600"
            />
          </div>
        </div>

        {/* Aperçu */}
        <div className="mt-8 p-6 bg-gradient-to-r from-red-600 to-red-800 rounded-lg text-white">
          <h3 className="text-sm font-medium mb-4 opacity-75">Aperçu</h3>
          <h1 className="text-4xl font-bold mb-3">{formData.hero_title || 'Titre principal'}</h1>
          <p className="text-xl mb-4 opacity-90">{formData.hero_subtitle || 'Sous-titre'}</p>
          <p className="mb-6 opacity-80">{formData.hero_description || 'Description'}</p>
          <button className="px-6 py-3 bg-white text-red-600 font-semibold rounded-lg">
            {formData.hero_button_text || 'Bouton'}
          </button>
        </div>
      </div>
    </div>
  );
}

export default HomePageEditor;