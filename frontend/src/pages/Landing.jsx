import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { 
    Heart, 
    ArrowRight,
    Shield,
    Waves,
    Lock,
    Unlock,
    AlertCircle,
    HandHeart,
    ExternalLink
} from 'lucide-react';
import { Button } from '../components/ui/button';
import Layout from '../components/Layout';
import { seedDatabase, getUser, getSiteSettings } from '../lib/api';
import { useCustomization, getStyleForElement } from '../hooks/useCustomization';
import BannerDisplay from '../components/BannerDisplay';

const Landing = () => {
    const user = getUser();
    const [settings, setSettings] = useState({ helloasso_url: '', helloasso_enabled: false });
    const { customization, loading } = useCustomization();

    useEffect(() => {
        const initApp = async () => {
            try {
                await seedDatabase();
                const siteSettings = await getSiteSettings();
                setSettings(siteSettings);
            } catch (error) {
                console.error('Erreur:', error);
            }
        };
        initApp();
    }, []);

    const getDashboardLink = () => {
        if (!user) return '/login';
        switch (user.role) {
            case 'admin': return '/admin';
            case 'formateur': return '/formateur';
            case 'stagiaire': return '/stagiaire';
            case 'visiteur': return '/visiteur';
            default: return '/';
        }
    };

    const formations = [
        {
            id: 'pse',
            title: 'PSE - Premiers Secours en Équipe',
            description: 'Plateforme de formation ouverte à distance pour les premiers secours. Progression guidée, quiz interactifs et suivi personnalisé par votre formateur.',
            icon: Shield,
            color: 'red',
            access: 'Sur inscription avec code groupe',
            link: '/pse-info',
            hasFreeTrial: true
        },
        {
            id: 'psc',
            title: 'PSC - Premiers Secours Citoyen',
            description: 'Plateforme de révision des gestes qui sauvent. Elle ne remplace en aucun cas une formation en centre de formation.',
            icon: Heart,
            color: 'green',
            access: 'Accès gratuit sans inscription',
            link: '/psc',
            disclaimer: true
        },
        {
            id: 'bnssa',
            title: 'BNSSA - Sauvetage Aquatique',
            description: 'Plateforme de formation ouverte à distance pour le sauvetage aquatique. Progression guidée, quiz interactifs et suivi personnalisé par votre formateur.',
            icon: Waves,
            color: 'blue',
            access: 'Sur autorisation formateur',
            link: '/bnssa-info'
        }
    ];

    // Obtenir les styles personnalisés
    const heroTitleStyle = customization ? getStyleForElement(customization, 'hero_title') : {};
    const heroSubtitleStyle = customization ? getStyleForElement(customization, 'hero_subtitle') : {};
    const sectionTitleStyle = customization ? getStyleForElement(customization, 'section_title') : {};

    return (
        <Layout>
            {/* Hero Section - Personnalisable */}
            <section className="hero-gradient py-16 md:py-24 relative overflow-hidden" data-testid="hero-section">
                <div className="absolute inset-0 mountain-pattern opacity-50"></div>
                
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative">
                    {/* Bannière Hero */}
                    <BannerDisplay position="home_hero" />
                    
                    <div className="text-center animate-fade-in mt-8">
                        <div className="flex items-center justify-center mb-6">
                            <img 
                                src="/images/logo-secours73.png" 
                                alt="Secours Alpes 73" 
                                className="h-24 w-auto"
                            />
                        </div>
                        
                        <h1 
                            className="text-4xl md:text-5xl lg:text-6xl font-bold tracking-tight mb-6"
                            style={{
                                ...heroTitleStyle,
                                color: heroTitleStyle.color || (customization?.primary_color || '#0f172a')
                            }}
                        >
                            {customization?.hero_title || 'Formez-vous aux premiers secours'}
                        </h1>
                        
                        {customization?.hero_subtitle && (
                            <p 
                                className="text-lg md:text-xl mb-8 max-w-3xl mx-auto"
                                style={heroSubtitleStyle}
                            >
                                {customization.hero_subtitle}
                            </p>
                        )}
                        
                        {user && (
                            <div className="mt-8">
                                <Link to={getDashboardLink()}>
                                    <Button 
                                        size="lg" 
                                        className="bg-red-600 hover:bg-red-700 btn-active"
                                        data-testid="cta-dashboard"
                                    >
                                        Accéder à mon espace
                                        <ArrowRight className="w-5 h-5 ml-2" />
                                    </Button>
                                </Link>
                            </div>
                        )}
                    </div>
                </div>
            </section>

            {/* Nous soutenir Section */}
            <section className="py-12 bg-gradient-to-r from-red-50 to-orange-50" data-testid="support-section">
                <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="flex flex-col md:flex-row items-center justify-between gap-6 bg-white rounded-2xl p-8 shadow-sm border border-red-100">
                        <div className="flex items-center gap-4">
                            <div className="w-14 h-14 bg-red-100 rounded-xl flex items-center justify-center flex-shrink-0">
                                <HandHeart className="w-7 h-7 text-red-600" />
                            </div>
                            <div>
                                <h2 className="text-xl font-bold text-slate-900 mb-1">
                                    Nous soutenir
                                </h2>
                                <p className="text-slate-600 text-sm">
                                    Aidez-nous à former plus de secouristes et à sauver des vies
                                </p>
                            </div>
                        </div>
                        {settings.helloasso_enabled && settings.helloasso_url ? (
                            <a 
                                href={settings.helloasso_url} 
                                target="_blank" 
                                rel="noopener noreferrer"
                                className="flex-shrink-0"
                            >
                                <Button className="bg-red-600 hover:bg-red-700" data-testid="donate-btn">
                                    Faire un don
                                    <ExternalLink className="w-4 h-4 ml-2" />
                                </Button>
                            </a>
                        ) : (
                            <Button 
                                variant="outline" 
                                className="flex-shrink-0"
                                disabled
                                data-testid="donate-btn-disabled"
                            >
                                Bientôt disponible
                            </Button>
                        )}
                    </div>
                </div>
            </section>

            {/* Formations Section - Les 3 onglets */}
            <section className="py-16 md:py-24 bg-white" data-testid="formations-section">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="text-center mb-12">
                        <h2 
                            className="text-3xl md:text-4xl font-bold mb-4"
                            style={sectionTitleStyle}
                        >
                            Nos formations
                        </h2>
                        <p className="text-lg text-slate-600 max-w-2xl mx-auto">
                            Choisissez la formation adaptée à vos besoins
                        </p>
                    </div>
                    
                    <div className="grid md:grid-cols-3 gap-8 stagger-children">
                        {formations.map((formation) => (
                            <div 
                                key={formation.id}
                                className={`bg-white border-2 rounded-2xl p-8 card-hover ${
                                    formation.color === 'red' ? 'border-red-200 hover:border-red-400' :
                                    formation.color === 'green' ? 'border-green-200 hover:border-green-400' :
                                    'border-blue-200 hover:border-blue-400'
                                }`}
                            >
                                <div className={`w-14 h-14 rounded-xl flex items-center justify-center mb-6 ${
                                    formation.color === 'red' ? 'bg-red-100' :
                                    formation.color === 'green' ? 'bg-green-100' :
                                    'bg-blue-100'
                                }`}>
                                    <formation.icon className={`w-7 h-7 ${
                                        formation.color === 'red' ? 'text-red-600' :
                                        formation.color === 'green' ? 'text-green-600' :
                                        'text-blue-600'
                                    }`} />
                                </div>
                                <h3 className="text-xl font-semibold text-slate-900 mb-3">
                                    {formation.title}
                                </h3>
                                <p className="text-slate-600 mb-4 text-sm leading-relaxed">
                                    {formation.description}
                                </p>
                                
                                {formation.disclaimer && (
                                    <div className="flex items-start gap-2 p-3 bg-amber-50 border border-amber-200 rounded-lg mb-4">
                                        <AlertCircle className="w-4 h-4 text-amber-600 flex-shrink-0 mt-0.5" />
                                        <p className="text-xs text-amber-700">
                                            Cette plateforme ne remplace pas une formation en centre agréé.
                                        </p>
                                    </div>
                                )}
                                
                                <div className={`flex items-center gap-2 text-sm mb-4 ${
                                    formation.color === 'green' ? 'text-green-600' : 'text-slate-500'
                                }`}>
                                    {formation.color === 'green' ? (
                                        <Unlock className="w-4 h-4" />
                                    ) : (
                                        <Lock className="w-4 h-4" />
                                    )}
                                    {formation.access}
                                </div>
                                <Link to={formation.link}>
                                    <Button 
                                        variant={formation.color === 'green' ? 'default' : 'outline'}
                                        className={formation.color === 'green' ? 'bg-green-600 hover:bg-green-700 w-full' : 'w-full'}
                                    >
                                        {formation.color === 'green' ? 'Accéder gratuitement' : 'En savoir plus'}
                                    </Button>
                                </Link>
                            </div>
                        ))}
                    </div>
                </div>
            </section>

            {/* Footer CTA */}
            <section className="py-12 bg-slate-900" data-testid="cta-section">
                <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
                    <p className="text-sm text-slate-400">
                        Développé par <strong className="text-white">Secours Alpes 73</strong> - Association habilitée pour la formation aux premiers secours
                    </p>
                </div>
            </section>
        </Layout>
    );
};

export default Landing;
