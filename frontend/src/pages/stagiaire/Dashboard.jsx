import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { 
    BookOpen, 
    CheckCircle2, 
    Trophy, 
    TrendingUp, 
    ArrowRight,
    Lock,
    Unlock,
    Star,
    Award
} from 'lucide-react';
import { Button } from '../../components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '../../components/ui/card';
import { Progress } from '../../components/ui/progress';
import Layout from '../../components/Layout';
import { stagiaireGetProgress, stagiaireGetChapitres, getUser, getCertificateStatus, generateCertificate } from '../../lib/api';
import { toast } from 'sonner';
import { CertificateBanner, CertificatePDF, CertificateProgress } from '../../components/Certificate';

const StagiaireDashboard = () => {
    const navigate = useNavigate();
    const user = getUser();
    const [loading, setLoading] = useState(true);
    const [progressData, setProgressData] = useState(null);
    const [chapitres, setChapitres] = useState([]);
    const [seuil, setSeuil] = useState(80);
    const [certificateStatus, setCertificateStatus] = useState(null);
    const [showCertificate, setShowCertificate] = useState(false);
    const [certificateData, setCertificateData] = useState(null);

    useEffect(() => {
        if (!user || user.role !== 'stagiaire') {
            navigate('/login');
            return;
        }
        loadData();
    }, [user, navigate]); // Added dependencies

    const loadData = async () => {
        try {
            const [progress, chapitresData, certStatus] = await Promise.all([
                stagiaireGetProgress(),
                stagiaireGetChapitres(),
                getCertificateStatus()
            ]);
            setProgressData(progress);
            setChapitres(chapitresData.chapitres || []);
            setSeuil(chapitresData.seuil_reussite || 80);
            setCertificateStatus(certStatus);
        } catch (error) {
            console.error('Erreur:', error);
            toast.error('Erreur lors du chargement des données');
        } finally {
            setLoading(false);
        }
    };

    const handleViewCertificate = async () => {
        try {
            const result = await generateCertificate();
            setCertificateData(result.certificate_data);
            setShowCertificate(true);
        } catch (error) {
            toast.error(error.response?.data?.detail || 'Erreur lors de la génération du certificat');
        }
    };

    const totalChapitres = chapitres.length;
    const completedChapitres = progressData?.progress?.chapitres_completes?.length || 0;
    const progressPercentage = totalChapitres > 0 ? (completedChapitres / totalChapitres) * 100 : 0;

    const getScoreColor = (score) => {
        if (score >= 80) return 'text-green-600 bg-green-100';
        if (score >= 60) return 'text-yellow-600 bg-yellow-100';
        return 'text-red-600 bg-red-100';
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

    return (
        <Layout>
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8" data-testid="stagiaire-dashboard">
                {/* Certificate Banner - Show when earned */}
                {certificateStatus?.earned && (
                    <CertificateBanner onViewCertificate={handleViewCertificate} />
                )}

                {/* Certificate Modal */}
                {showCertificate && certificateData && (
                    <CertificatePDF 
                        certificateData={certificateData}
                        onClose={() => setShowCertificate(false)}
                    />
                )}

                {/* Header */}
                <div className="mb-8">
                    <h1 className="text-3xl font-bold text-slate-900 mb-2">
                        Bonjour, {user?.prenom} !
                    </h1>
                    <p className="text-slate-600">
                        {progressData?.groupe ? (
                            <>Groupe : <strong>{progressData.groupe.nom}</strong> • Seuil de réussite : <strong>{seuil}%</strong></>
                        ) : (
                            'Suivez votre progression dans la formation'
                        )}
                    </p>
                </div>

                {/* Stats Cards */}
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8 stagger-children">
                    <Card className="card-hover" data-testid="stat-progress">
                        <CardContent className="p-6">
                            <div className="flex items-center justify-between mb-4">
                                <div className="w-12 h-12 bg-red-100 rounded-xl flex items-center justify-center">
                                    <TrendingUp className="w-6 h-6 text-red-600" />
                                </div>
                                <span className="text-3xl font-bold text-slate-900">
                                    {Math.round(progressPercentage)}%
                                </span>
                            </div>
                            <p className="text-sm text-slate-600">Progression globale</p>
                            <Progress value={progressPercentage} className="mt-2 h-2" />
                        </CardContent>
                    </Card>

                    <Card className="card-hover" data-testid="stat-chapters">
                        <CardContent className="p-6">
                            <div className="flex items-center justify-between mb-4">
                                <div className="w-12 h-12 bg-blue-100 rounded-xl flex items-center justify-center">
                                    <BookOpen className="w-6 h-6 text-blue-600" />
                                </div>
                                <span className="text-3xl font-bold text-slate-900">
                                    {completedChapitres}/{totalChapitres}
                                </span>
                            </div>
                            <p className="text-sm text-slate-600">Chapitres validés</p>
                        </CardContent>
                    </Card>

                    <Card className="card-hover" data-testid="stat-quizzes">
                        <CardContent className="p-6">
                            <div className="flex items-center justify-between mb-4">
                                <div className="w-12 h-12 bg-green-100 rounded-xl flex items-center justify-center">
                                    <CheckCircle2 className="w-6 h-6 text-green-600" />
                                </div>
                                <span className="text-3xl font-bold text-slate-900">
                                    {progressData?.quizzes_completed || 0}
                                </span>
                            </div>
                            <p className="text-sm text-slate-600">Quiz réalisés</p>
                        </CardContent>
                    </Card>

                    <Card className="card-hover" data-testid="stat-score">
                        <CardContent className="p-6">
                            <div className="flex items-center justify-between mb-4">
                                <div className="w-12 h-12 bg-yellow-100 rounded-xl flex items-center justify-center">
                                    <Trophy className="w-6 h-6 text-yellow-600" />
                                </div>
                                <span className="text-3xl font-bold text-slate-900">
                                    {Math.round(progressData?.average_score || 0)}%
                                </span>
                            </div>
                            <p className="text-sm text-slate-600">Score moyen</p>
                        </CardContent>
                    </Card>
                </div>

                {/* Chapitres */}
                <Card data-testid="chapitres-list">
                    <CardHeader className="flex flex-row items-center justify-between">
                        <CardTitle className="text-lg">Votre parcours de formation</CardTitle>
                        <Link to="/stagiaire/chapitres">
                            <Button variant="ghost" size="sm">
                                Voir tout
                                <ArrowRight className="w-4 h-4 ml-1" />
                            </Button>
                        </Link>
                    </CardHeader>
                    <CardContent>
                        {chapitres.length === 0 ? (
                            <div className="empty-state py-8">
                                <BookOpen className="w-12 h-12 mx-auto text-slate-300 mb-3" />
                                <p className="text-slate-500">Aucun chapitre configuré pour votre groupe</p>
                            </div>
                        ) : (
                            <div className="space-y-3">
                                {chapitres.map((chapter, index) => (
                                    <div 
                                        key={chapter.id}
                                        className={`flex items-center justify-between p-4 rounded-lg border transition-colors ${
                                            chapter.is_unlocked 
                                                ? chapter.is_completed 
                                                    ? 'bg-green-50 border-green-200' 
                                                    : 'bg-white border-slate-200 hover:border-red-200'
                                                : 'bg-slate-50 border-slate-200 opacity-60'
                                        }`}
                                    >
                                        <div className="flex items-center gap-4">
                                            <div className={`w-10 h-10 rounded-lg flex items-center justify-center ${
                                                chapter.is_completed 
                                                    ? 'bg-green-100 text-green-600'
                                                    : chapter.is_unlocked 
                                                        ? 'bg-red-100 text-red-600'
                                                        : 'bg-slate-200 text-slate-400'
                                            }`}>
                                                {chapter.is_completed ? (
                                                    <CheckCircle2 className="w-5 h-5" />
                                                ) : chapter.is_unlocked ? (
                                                    <Unlock className="w-5 h-5" />
                                                ) : (
                                                    <Lock className="w-5 h-5" />
                                                )}
                                            </div>
                                            <div>
                                                <p className="font-medium text-slate-900">
                                                    {index + 1}. {chapter.titre}
                                                </p>
                                                <p className="text-xs text-slate-500">
                                                    {chapter.fiches?.length || 0} fiches
                                                </p>
                                            </div>
                                        </div>
                                        
                                        {chapter.is_unlocked && (
                                            <Link to={`/stagiaire/chapitre/${chapter.id}`}>
                                                <Button 
                                                    size="sm" 
                                                    variant={chapter.is_completed ? 'outline' : 'default'}
                                                    className={!chapter.is_completed ? 'bg-red-600 hover:bg-red-700' : ''}
                                                >
                                                    {chapter.is_completed ? 'Revoir' : 'Continuer'}
                                                </Button>
                                            </Link>
                                        )}
                                    </div>
                                ))}
                            </div>
                        )}
                    </CardContent>
                </Card>

                {/* Recent Results */}
                {progressData?.quiz_results?.length > 0 && (
                    <Card className="mt-6" data-testid="recent-results">
                        <CardHeader>
                            <CardTitle className="text-lg">Derniers résultats</CardTitle>
                        </CardHeader>
                        <CardContent>
                            <div className="space-y-3">
                                {progressData.quiz_results.slice(0, 5).map((result) => (
                                    <div 
                                        key={result.id}
                                        className="flex items-center justify-between p-3 bg-slate-50 rounded-lg"
                                    >
                                        <div className="flex items-center gap-3">
                                            <div className={`w-8 h-8 rounded-lg flex items-center justify-center ${getScoreColor(result.percentage)}`}>
                                                <Star className="w-4 h-4" />
                                            </div>
                                            <div>
                                                <p className="text-sm font-medium text-slate-900">
                                                    {chapitres.find(c => c.id === result.chapter_id)?.titre || 'Quiz'}
                                                </p>
                                                <p className="text-xs text-slate-500">
                                                    {new Date(result.completed_at).toLocaleDateString('fr-FR')}
                                                </p>
                                            </div>
                                        </div>
                                        <span className={`font-bold ${result.percentage >= seuil ? 'text-green-600' : 'text-red-600'}`}>
                                            {result.percentage}%
                                        </span>
                                    </div>
                                ))}
                            </div>
                        </CardContent>
                    </Card>
                )}
            </div>
        </Layout>
    );
};

export default StagiaireDashboard;
