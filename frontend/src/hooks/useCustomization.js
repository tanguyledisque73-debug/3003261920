import { useState, useEffect } from 'react';

const API_URL = process.env.REACT_APP_BACKEND_URL;

export function useCustomization() {
  const [customization, setCustomization] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadCustomization();
  }, []);

  const loadCustomization = async () => {
    try {
      const response = await fetch(`${API_URL}/api/customization`);
      const data = await response.json();
      setCustomization(data);
      
      // Appliquer les styles globaux
      applyGlobalStyles(data);
      
      setLoading(false);
    } catch (error) {
      console.error('Erreur chargement personnalisation:', error);
      setLoading(false);
    }
  };

  const applyGlobalStyles = (data) => {
    if (!data) return;

    const root = document.documentElement;

    // Appliquer les couleurs
    if (data.primary_color) {
      root.style.setProperty('--color-primary', data.primary_color);
    }
    if (data.secondary_color) {
      root.style.setProperty('--color-secondary', data.secondary_color);
    }
    if (data.accent_color) {
      root.style.setProperty('--color-accent', data.accent_color);
    }

    // Appliquer les polices
    if (data.styles) {
      Object.entries(data.styles).forEach(([element, style]) => {
        if (style.font_family) {
          root.style.setProperty(`--font-${element}`, style.font_family);
        }
      });
    }
  };

  return { customization, loading, reload: loadCustomization };
}

export function getStyleForElement(customization, elementType) {
  if (!customization?.styles?.[elementType]) return {};

  const style = customization.styles[elementType];
  const result = {};

  if (style.font_family) result.fontFamily = style.font_family;
  if (style.color) result.color = style.color;
  if (style.text_align) result.textAlign = style.text_align;
  
  if (style.font_size) {
    const sizes = {
      small: '0.875rem',
      medium: '1rem',
      large: '1.25rem'
    };
    result.fontSize = sizes[style.font_size] || sizes.medium;
  }

  if (style.font_weight) {
    result.fontWeight = style.font_weight === 'bold' ? '700' : '400';
  }

  if (style.font_style) {
    result.fontStyle = style.font_style;
  }

  return result;
}
