import React, { useState } from 'react';
import { Palette, Type } from 'lucide-react';

function StyleEditor({ styles, colors, onChange }) {
  const [localColors, setLocalColors] = useState(colors || {});
  const [localStyles, setLocalStyles] = useState(styles || {});

  const handleColorChange = (key, value) => {
    const newColors = { ...localColors, [key]: value };
    setLocalColors(newColors);
    onChange({ [key]: value });
  };

  const fonts = [
    'Inter',
    'Roboto',
    'Open Sans',
    'Montserrat',
    'Lato',
    'Poppins',
    'Raleway',
  ];

  const elements = [
    { id: 'title', label: 'Titres (H1, H2)' },
    { id: 'subtitle', label: 'Sous-titres' },
    { id: 'text', label: 'Texte normal' },
    { id: 'button', label: 'Boutons' },
    { id: 'menu', label: 'Menu navigation' },
  ];

  return (
    <div>
      <h2 className="text-2xl font-bold text-gray-900 mb-6">Styles & Couleurs</h2>

      {/* Couleurs principales */}
      <div className="mb-8">
        <h3 className="text-lg font-semibold mb-4 flex items-center">
          <Palette className="w-5 h-5 mr-2" />
          Couleurs principales
        </h3>
        <div className="grid grid-cols-3 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Couleur principale
            </label>
            <div className="flex items-center space-x-2">
              <input
                type="color"
                value={localColors.primary || '#dc2626'}
                onChange={(e) => handleColorChange('primary_color', e.target.value)}
                className="w-16 h-10 rounded cursor-pointer"
              />
              <input
                type="text"
                value={localColors.primary || '#dc2626'}
                onChange={(e) => handleColorChange('primary_color', e.target.value)}
                className="flex-1 px-3 py-2 border rounded"
              />
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Couleur secondaire
            </label>
            <div className="flex items-center space-x-2">
              <input
                type="color"
                value={localColors.secondary || '#1f2937'}
                onChange={(e) => handleColorChange('secondary_color', e.target.value)}
                className="w-16 h-10 rounded cursor-pointer"
              />
              <input
                type="text"
                value={localColors.secondary || '#1f2937'}
                onChange={(e) => handleColorChange('secondary_color', e.target.value)}
                className="flex-1 px-3 py-2 border rounded"
              />
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Couleur accent
            </label>
            <div className="flex items-center space-x-2">
              <input
                type="color"
                value={localColors.accent || '#3b82f6'}
                onChange={(e) => handleColorChange('accent_color', e.target.value)}
                className="w-16 h-10 rounded cursor-pointer"
              />
              <input
                type="text"
                value={localColors.accent || '#3b82f6'}
                onChange={(e) => handleColorChange('accent_color', e.target.value)}
                className="flex-1 px-3 py-2 border rounded"
              />
            </div>
          </div>
        </div>
      </div>

      {/* Polices par élément */}
      <div>
        <h3 className="text-lg font-semibold mb-4 flex items-center">
          <Type className="w-5 h-5 mr-2" />
          Polices par élément
        </h3>
        <div className="space-y-4">
          {elements.map(element => (
            <div key={element.id} className="bg-gray-50 p-4 rounded-lg">
              <h4 className="font-medium mb-3">{element.label}</h4>
              <div className="grid grid-cols-4 gap-3">
                <div>
                  <label className="text-xs text-gray-600">Police</label>
                  <select
                    value={localStyles[element.id]?.font_family || 'Inter'}
                    onChange={(e) => {
                      const newStyles = {
                        ...localStyles,
                        [element.id]: { ...localStyles[element.id], font_family: e.target.value }
                      };
                      setLocalStyles(newStyles);
                      onChange({ styles: newStyles });
                    }}
                    className="w-full px-2 py-1 border rounded text-sm"
                  >
                    {fonts.map(font => (
                      <option key={font} value={font}>{font}</option>
                    ))}
                  </select>
                </div>

                <div>
                  <label className="text-xs text-gray-600">Taille</label>
                  <select
                    value={localStyles[element.id]?.font_size || 'medium'}
                    onChange={(e) => {
                      const newStyles = {
                        ...localStyles,
                        [element.id]: { ...localStyles[element.id], font_size: e.target.value }
                      };
                      setLocalStyles(newStyles);
                      onChange({ styles: newStyles });
                    }}
                    className="w-full px-2 py-1 border rounded text-sm"
                  >
                    <option value="small">Petit</option>
                    <option value="medium">Moyen</option>
                    <option value="large">Grand</option>
                  </select>
                </div>

                <div>
                  <label className="text-xs text-gray-600">Style</label>
                  <select
                    value={localStyles[element.id]?.font_weight || 'normal'}
                    onChange={(e) => {
                      const newStyles = {
                        ...localStyles,
                        [element.id]: { ...localStyles[element.id], font_weight: e.target.value }
                      };
                      setLocalStyles(newStyles);
                      onChange({ styles: newStyles });
                    }}
                    className="w-full px-2 py-1 border rounded text-sm"
                  >
                    <option value="normal">Normal</option>
                    <option value="bold">Gras</option>
                  </select>
                </div>

                <div>
                  <label className="text-xs text-gray-600">Alignement</label>
                  <select
                    value={localStyles[element.id]?.text_align || 'left'}
                    onChange={(e) => {
                      const newStyles = {
                        ...localStyles,
                        [element.id]: { ...localStyles[element.id], text_align: e.target.value }
                      };
                      setLocalStyles(newStyles);
                      onChange({ styles: newStyles });
                    }}
                    className="w-full px-2 py-1 border rounded text-sm"
                  >
                    <option value="left">Gauche</option>
                    <option value="center">Centre</option>
                    <option value="right">Droite</option>
                  </select>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default StyleEditor;