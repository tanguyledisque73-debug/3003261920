import React from 'react';
import { X } from 'lucide-react';

function LivePreview({ customization, onClose }) {
  return (
    <div className="fixed inset-0 bg-black bg-opacity-75 z-50 flex items-center justify-center p-4">
      <div className="bg-white rounded-lg w-full max-w-6xl h-[90vh] flex flex-col">
        {/* Header */}
        <div className="flex items-center justify-between p-4 border-b">
          <h2 className="text-xl font-bold">Aperçu en direct</h2>
          <button
            onClick={onClose}
            className="p-2 hover:bg-gray-100 rounded-full transition"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Preview Content */}
        <div className="flex-1 overflow-auto">
          <div
            className="min-h-full"
            style={{
              backgroundColor: customization?.secondary_color || '#1f2937',
            }}
          >
            {/* Hero Section */}
            <div
              className="py-20 px-8 text-white text-center"
              style={{
                backgroundColor: customization?.primary_color || '#dc2626',
              }}
            >
              <h1
                className="text-5xl font-bold mb-4"
                style={{
                  fontFamily: customization?.styles?.title?.font_family || 'Inter',
                }}
              >
                {customization?.home_page?.hero_title || 'Bienvenue'}
              </h1>
              <p className="text-2xl mb-6 opacity-90">
                {customization?.home_page?.hero_subtitle || 'Sous-titre'}
              </p>
              <p className="text-lg mb-8 opacity-80 max-w-2xl mx-auto">
                {customization?.home_page?.hero_description || 'Description'}
              </p>
              <button
                className="px-8 py-4 bg-white font-semibold rounded-lg"
                style={{
                  color: customization?.primary_color || '#dc2626',
                  fontFamily: customization?.styles?.button?.font_family || 'Inter',
                }}
              >
                {customization?.home_page?.hero_button_text || 'Commencer'}
              </button>
            </div>

            {/* Content Section */}
            <div className="py-16 px-8 bg-white">
              <div className="max-w-4xl mx-auto">
                <h2
                  className="text-3xl font-bold mb-6"
                  style={{
                    color: customization?.primary_color || '#dc2626',
                    fontFamily: customization?.styles?.subtitle?.font_family || 'Inter',
                  }}
                >
                  À propos de la formation
                </h2>
                <p
                  className="text-lg text-gray-700 leading-relaxed"
                  style={{
                    fontFamily: customization?.styles?.text?.font_family || 'Inter',
                  }}
                >
                  Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default LivePreview;