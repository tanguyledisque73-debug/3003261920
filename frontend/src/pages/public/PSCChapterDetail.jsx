import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { 
    ArrowLeft, 
    ArrowRight, 
    BookOpen, 
    FileText,
    ChevronRight,
    AlertCircle,
    Heart
} from 'lucide-react';
import { Button } from '../../components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '../../components/ui/card';
import { ScrollArea } from '../../components/ui/scroll-area';
import Layout from '../../components/Layout';
import { getChapter } from '../../lib/api';
import { toast } from 'sonner';
import VideoPlayer from '../../components/VideoPlayer';

const PSCChapterDetail = () => {
    const { chapterId } = useParams();
    const [chapter, setChapter] = useState(null);
    const [loading, setLoading] = useState(true);
    const [activeFiche, setActiveFiche] = useState(0);

    useEffect(() => {
        loadData();
    }, [chapterId]);

    const loadData = async () => {
        try {
            const chapterData = await getChapter(chapterId);
            setChapter(chapterData);
        } catch (error) {
            console.error('Erreur:', error);
            toast.error('Erreur lors du chargement');
        } finally {
            setLoading(false);
        }
    };

    const renderContent = (htmlContent) => {
        if (!htmlContent) return null;
        
        // Si le contenu contient des balises HTML (éditeur riche)
        if (htmlContent.includes('<p>') || htmlContent.includes('<h1>') || htmlContent.includes('<div>')) {
            return (
                <div 
                    className="prose prose-slate max-w-none rich-text-content"
                    dangerouslySetInnerHTML={{ __html: htmlContent }}
                />
            );
        }
        
        const lines = htmlContent.split('\n');
        return lines.map((line, index) => {
            // Headers (##)
            if (line.startsWith('## ')) {
                return (
                    <h2 key={index} className="text-2xl font-bold text-slate-900 mt-8 mb-4">
                        {line.replace(/^## /, '')}
                    </h2>
                );
            }
            
            // Subheaders (###)
            if (line.startsWith('### ')) {
                return (
                    <h3 key={index} className="text-xl font-semibold text-slate-900 mt-6 mb-3">
                        {line.replace(/^### /, '')}
                    </h3>
                );
            }
            
            // Sub-subheaders (####)
            if (line.startsWith('#### ')) {
                return (
                    <h4 key={index} className="text-lg font-semibold text-slate-900 mt-4 mb-2">
                        {line.replace(/^#### /, '')}
                    </h4>
                );
            }
            
            // Bold text
            if (line.startsWith('**') && line.endsWith('**')) {
                return (
                    <p key={index} className="font-semibold text-slate-900 mt-4 mb-2">
                        {line.replace(/\*\*/g, '')}
                    </p>
                );
            }
            
            // Inline bold
            if (line.includes('**')) {
                const parts = line.split(/\*\*(.*?)\*\*/g);
                return (
                    <p key={index} className="mb-2 text-slate-700 leading-relaxed">
                        {parts.map((part, i) => 
                            i % 2 === 1 ? <strong key={i} className="font-semibold text-slate-900">{part}</strong> : part
                        )}
                    </p>
                );
            }
            
            // Bullet lists
            if (line.startsWith('- ') || line.startsWith('* ')) {
                return (
                    <li key={index} className="ml-6 mb-1 text-slate-700 list-disc">
                        {line.substring(2)}
                    </li>
                );
            }
            
            // Numbered lists
            if (/^\d+\./.test(line)) {
                return (
                    <li key={index} className="ml-6 mb-1 text-slate-700 list-decimal">
                        {line.replace(/^\d+\.\s*/, '')}
                    </li>
                );
            }
            
            // Horizontal lines
            if (line.trim() === '---') {
                return <hr key={index} className="my-6 border-slate-200" />;
            }
            
            // Empty lines
            if (line.trim() === '') {
                return <br key={index} />;
            }
            
            // Regular paragraphs
            return (
                <p key={index} className="mb-2 text-slate-700 leading-relaxed">
                    {line}
                </p>
            );
        });
    };

    if (loading) {
        return (
            <Layout>
                <div className="flex items-center justify-center min-h-[60vh]">
                    <div className="spinner"></div>
                </div>
            </Layout>
        );
    }

    if (!chapter) {
        return (
            <Layout>
                <div className="max-w-7xl mx-auto px-4 py-8 text-center">
                    <p className="text-slate-600">Chapitre non trouvé</p>
                    <Link to="/psc" className="mt-4 inline-block">
                        <Button variant="outline">Retour aux chapitres PSC</Button>
                    </Link>
                </div>
            </Layout>
        );
    }

    const currentFiche = chapter.fiches?.[activeFiche];

    return (
        <Layout>
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8" data-testid="psc-chapter-detail">
                {/* Disclaimer Banner */}
                <div className="max-w-4xl mx-auto mb-6 bg-amber-50 border border-amber-200 rounded-xl p-4">
                    <div className="flex items-start gap-3">
                        <AlertCircle className="w-5 h-5 text-amber-600 flex-shrink-0 mt-0.5" />
                        <div>
                            <p className="text-sm font-medium text-amber-800 mb-1">Plateforme de révision uniquement</p>
                            <p className="text-sm text-amber-700">
                                Ce contenu ne remplace pas une formation officielle PSC1 en centre agréé.
                            </p>
                        </div>
                    </div>
                </div>

                {/* Breadcrumb */}
                <div className="flex items-center gap-2 text-sm text-slate-600 mb-6">
                    <Link to="/" className="hover:text-green-600 transition-colors">
                        Accueil
                    </Link>
                    <ChevronRight className="w-4 h-4" />
                    <Link to="/psc" className="hover:text-green-600 transition-colors">
                        PSC - Premiers Secours Citoyen
                    </Link>
                    <ChevronRight className="w-4 h-4" />
                    <span className="text-slate-900 font-medium">{chapter.titre}</span>
                </div>

                {/* Header */}
                <div className="flex flex-col md:flex-row md:items-start md:justify-between gap-4 mb-8">
                    <div className="flex-1">
                        <div className="flex items-center gap-3 mb-3">
                            <div className="w-12 h-12 bg-green-100 rounded-xl flex items-center justify-center">
                                <Heart className="w-6 h-6 text-green-600" />
                            </div>
                            <div>
                                <span className="text-sm font-medium text-green-600">Chapitre {chapter.numero}</span>
                                <h1 className="text-3xl font-bold text-slate-900">
                                    {chapter.titre}
                                </h1>
                            </div>
                        </div>
                        <p className="text-slate-600">
                            {chapter.description}
                        </p>
                    </div>
                </div>

                {/* Content */}
                <div className="grid lg:grid-cols-4 gap-8">
                    {/* Sidebar */}
                    <div className="lg:col-span-1">
                        <Card className="sticky top-24" data-testid="fiches-sidebar">
                            <CardHeader className="pb-3">
                                <CardTitle className="text-sm font-medium text-slate-600 flex items-center gap-2">
                                    <FileText className="w-4 h-4" />
                                    Fiches ({chapter.fiches?.length || 0})
                                </CardTitle>
                            </CardHeader>
                            <CardContent className="p-0">
                                <ScrollArea className="h-[400px]">
                                    <div className="px-4 pb-4 space-y-1">
                                        {chapter.fiches?.map((fiche, index) => (
                                            <button
                                                key={fiche.id}
                                                onClick={() => setActiveFiche(index)}
                                                className={`w-full text-left px-3 py-2 rounded-lg text-sm transition-colors ${
                                                    activeFiche === index
                                                        ? 'bg-green-100 text-green-700 font-medium'
                                                        : 'text-slate-600 hover:bg-slate-100'
                                                }`}
                                                data-testid={`fiche-btn-${index}`}
                                            >
                                                {fiche.titre}
                                            </button>
                                        ))}
                                    </div>
                                </ScrollArea>
                            </CardContent>
                        </Card>
                    </div>

                    {/* Main Content */}
                    <div className="lg:col-span-3">
                        {/* Vidéos en haut du chapitre */}
                        <VideoPlayer 
                            chapterId={chapterId} 
                            position="top" 
                        />
                        
                        <Card data-testid="fiche-content">
                            {currentFiche?.image_url && (
                                <div className="w-full h-64 overflow-hidden rounded-t-lg">
                                    <img 
                                        src={currentFiche.image_url} 
                                        alt={currentFiche.titre}
                                        className="w-full h-full object-cover"
                                    />
                                </div>
                            )}
                            <CardHeader className="border-b border-slate-100">
                                <CardTitle className="text-xl">
                                    {currentFiche?.titre}
                                </CardTitle>
                            </CardHeader>
                            <CardContent className="p-6">
                                {/* Vidéos de la fiche */}
                                <VideoPlayer 
                                    chapterId={chapterId}
                                    ficheId={currentFiche?.id}
                                    position="top" 
                                />
                                
                                <div className="prose prose-slate max-w-none">
                                    {renderContent(currentFiche?.contenu || '')}
                                </div>
                                
                                {/* Vidéos en bas de la fiche */}
                                <VideoPlayer 
                                    chapterId={chapterId}
                                    ficheId={currentFiche?.id}
                                    position="bottom" 
                                />
                            </CardContent>
                        </Card>

                        {/* Navigation */}
                        <div className="flex items-center justify-between mt-6">
                            <Button
                                variant="outline"
                                onClick={() => setActiveFiche(Math.max(0, activeFiche - 1))}
                                disabled={activeFiche === 0}
                            >
                                <ArrowLeft className="w-4 h-4 mr-2" />
                                Précédent
                            </Button>
                            
                            <span className="text-sm text-slate-500">
                                Fiche {activeFiche + 1} sur {chapter.fiches?.length || 0}
                            </span>
                            
                            {activeFiche < (chapter.fiches?.length || 0) - 1 ? (
                                <Button
                                    variant="outline"
                                    onClick={() => setActiveFiche(activeFiche + 1)}
                                >
                                    Suivant
                                    <ArrowRight className="w-4 h-4 ml-2" />
                                </Button>
                            ) : (
                                <Link to="/psc">
                                    <Button variant="outline">
                                        Retour aux chapitres
                                        <ArrowRight className="w-4 h-4 ml-2" />
                                    </Button>
                                </Link>
                            )}
                        </div>
                    </div>
                </div>
            </div>
        </Layout>
    );
};

export default PSCChapterDetail;
