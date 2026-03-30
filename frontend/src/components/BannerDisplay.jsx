import React, { useState, useEffect } from 'react';
import { ChevronLeft, ChevronRight } from 'lucide-react';

const API_URL = process.env.REACT_APP_BACKEND_URL;

function BannerDisplay({ position = 'home_hero' }) {
  const [banners, setBanners] = useState([]);
  const [currentIndex, setCurrentIndex] = useState(0);

  useEffect(() => {
    loadBanners();
  }, [position]);

  const loadBanners = async () => {
    try {
      const response = await fetch(`${API_URL}/api/customization`);
      const data = await response.json();
      
      const filteredBanners = (data.banners || [])
        .filter(b => b.position === position && b.is_active)
        .sort((a, b) => a.order - b.order);
      
      setBanners(filteredBanners);
    } catch (error) {
      console.error('Erreur chargement bannières:', error);
    }
  };

  const nextBanner = () => {
    setCurrentIndex((prev) => (prev + 1) % banners.length);
  };

  const prevBanner = () => {
    setCurrentIndex((prev) => (prev - 1 + banners.length) % banners.length);
  };

  if (banners.length === 0) return null;

  const currentBanner = banners[currentIndex];

  return (
    <div className="relative w-full overflow-hidden rounded-lg">
      {currentBanner.link ? (
        <a href={currentBanner.link} target="_blank" rel="noopener noreferrer">
          <img
            src={`${API_URL}${currentBanner.image_url}`}
            alt={currentBanner.title}
            className="w-full h-auto object-cover"
          />
        </a>
      ) : (
        <img
          src={`${API_URL}${currentBanner.image_url}`}
          alt={currentBanner.title}
          className="w-full h-auto object-cover"
        />
      )}

      {banners.length > 1 && (
        <>
          <button
            onClick={prevBanner}
            className="absolute left-4 top-1/2 -translate-y-1/2 bg-white/80 hover:bg-white p-2 rounded-full shadow-lg transition"
          >
            <ChevronLeft className="w-6 h-6 text-gray-800" />
          </button>
          <button
            onClick={nextBanner}
            className="absolute right-4 top-1/2 -translate-y-1/2 bg-white/80 hover:bg-white p-2 rounded-full shadow-lg transition"
          >
            <ChevronRight className="w-6 h-6 text-gray-800" />
          </button>

          {/* Dots */}
          <div className="absolute bottom-4 left-1/2 -translate-x-1/2 flex space-x-2">
            {banners.map((_, index) => (
              <button
                key={index}
                onClick={() => setCurrentIndex(index)}
                className={`w-2 h-2 rounded-full transition ${
                  index === currentIndex ? 'bg-white w-8' : 'bg-white/60'
                }`}
              />
            ))}
          </div>
        </>
      )}
    </div>
  );
}

export default BannerDisplay;
