import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { 
    Users, 
    UserPlus,
    BookOpen,
    TrendingUp,
    Settings,
    ArrowRight,
    Palette
} from 'lucide-react';
import { Button } from '../../components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '../../components/ui/card';
import Layout from '../../components/Layout';
import { adminGetStats, adminGetFormateurs, getUser } from '../../lib/api';
import { toast } from 'sonner';

const AdminDashboard = () => {
    const navigate = useNavigate();
    const user = getUser();
    const [loading, setLoading] = useState(true);
    const [stats, setStats] = useState(null);
    const [formateurs, setFormateurs] = useState([]);

    useEffect(() => {
        if (!user || user.role !== 'admin') {
            navigate('/login');
            return;
        }
        loadData();
    }, []);

    const loadData = async () => {
        try {
            const [statsData, formateursData] = await Promise.all([
                adminGetStats(),
                adminGetFormateurs()
            ]);
            setStats(statsData);
            setFormateurs(formateursData);
        } catch (error) {
            console.error('Erreur:', error);
            toast.error('Erreur lors du chargement');
        } finally {
            setLoading(false);
        }
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
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8" data-testid="admin-dashboard">
                {/* Header */}
                <div className="mb-8">
                    <h1 className="text-3xl font-bold text-slate-900 mb-2">
                        Administration
                    </h1>
                    <p className="text-slate-600">
                        Bienvenue {user?.prenom}. Gérez la plateforme Secours 73.
                    </p>
                </div>

                {/* Stats */}
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
                    <Card className="card-hover">
                        <CardContent className="p-6">
                            <div className="flex items-center justify-between">
                                <div className="w-12 h-12 bg-blue-100 rounded-xl flex items-center justify-center">
                                    <UserPlus className="w-6 h-6 text-blue-600" />
                                </div>
                                <span className="text-3xl font-bold text-slate-900">{stats?.total_formateurs || 0}</span>
                            </div>
                            <p className="text-sm text-slate-600 mt-2">Formateurs</p>
                        </CardContent>
                    </Card>
                    
                    <Card className="card-hover">
                        <CardContent className="p-6">
                            <div className="flex items-center justify-between">
                                <div className="w-12 h-12 bg-green-100 rounded-xl flex items-center justify-center">
                                    <Users className="w-6 h-6 text-green-600" />
                                </div>
                                <span className="text-3xl font-bold text-slate-900">{stats?.total_stagiaires || 0}</span>
                            </div>
                            <p className="text-sm text-slate-600 mt-2">Stagiaires</p>
                        </CardContent>
                    </Card>
                    
                    <Card className="card-hover">
                        <CardContent className="p-6">
                            <div className="flex items-center justify-between">
                                <div className="w-12 h-12 bg-purple-100 rounded-xl flex items-center justify-center">
                                    <TrendingUp className="w-6 h-6 text-purple-600" />
                                </div>
                                <span className="text-3xl font-bold text-slate-900">{stats?.total_groupes || 0}</span>
                            </div>
                            <p className="text-sm text-slate-600 mt-2">Groupes</p>
                        </CardContent>
                    </Card>
                    
                    <Card className="card-hover">
                        <CardContent className="p-6">
                            <div className="flex items-center justify-between">
                                <div className="w-12 h-12 bg-yellow-100 rounded-xl flex items-center justify-center">
                                    <BookOpen className="w-6 h-6 text-yellow-600" />
                                </div>
                                <span className="text-3xl font-bold text-slate-900">{stats?.total_quiz_completés || 0}</span>
                            </div>
                            <p className="text-sm text-slate-600 mt-2">Quiz complétés</p>
                        </CardContent>
                    </Card>
                </div>

                {/* Quick Actions */}
                <div className="grid md:grid-cols-4 gap-6 mb-8">
                    <Card className="card-hover">
                        <CardContent className="p-6">
                            <div className="flex items-center justify-between">
                                <div>
                                    <h3 className="font-semibold text-slate-900 mb-1">Gestion du contenu</h3>
                                    <p className="text-sm text-slate-600">Créer, modifier chapitres, fiches, textes et images</p>
                                </div>
                                <Link to="/admin/chapters">
                                    <Button className="bg-red-600 hover:bg-red-700">
                                        Gérer
                                        <ArrowRight className="w-4 h-4 ml-2" />
                                    </Button>
                                </Link>
                            </div>
                        </CardContent>
                    </Card>
                    
                    <Card className="card-hover">
                        <CardContent className="p-6">
                            <div className="flex items-center justify-between">
                                <div>
                                    <h3 className="font-semibold text-slate-900 mb-1">Gestion des formateurs</h3>
                                    <p className="text-sm text-slate-600">Créer, modifier ou supprimer des comptes formateurs</p>
                                </div>
                                <Link to="/admin/formateurs">
                                    <Button className="bg-red-600 hover:bg-red-700">
                                        Gérer
                                        <ArrowRight className="w-4 h-4 ml-2" />
                                    </Button>
                                </Link>
                            </div>
                        </CardContent>
                    </Card>
                    
                    <Card className="card-hover">
                        <CardContent className="p-6">
                            <div className="flex items-center justify-between">
                                <div>
                                    <h3 className="font-semibold text-slate-900 mb-1">Gestion des quiz</h3>
                                    <p className="text-sm text-slate-600">Créer, modifier ou supprimer des quiz et vidéos</p>
                                </div>
                                <Link to="/admin/quizzes">
                                    <Button className="bg-red-600 hover:bg-red-700">
                                        Gérer
                                        <ArrowRight className="w-4 h-4 ml-2" />
                                    </Button>
                                </Link>
                            </div>
                        </CardContent>
                    </Card>
                    
                    <Card className="card-hover bg-gradient-to-br from-red-50 to-pink-50">
                        <CardContent className="p-6">
                            <div className="flex items-center justify-between">
                                <div>
                                    <h3 className="font-semibold text-slate-900 mb-1 flex items-center">
                                        <Palette className="w-5 h-5 mr-2 text-red-600" />
                                        Personnalisation du site
                                    </h3>
                                    <p className="text-sm text-slate-600">Couleurs, polices, bannières, vidéos</p>
                                </div>
                                <Link to="/admin/customization">
                                    <Button className="bg-red-600 hover:bg-red-700">
                                        Personnaliser
                                        <ArrowRight className="w-4 h-4 ml-2" />
                                    </Button>
                                </Link>
                            </div>
                        </CardContent>
                    </Card>
                </div>
                
                <div className="grid md:grid-cols-2 gap-6 mb-8">
                    <Card className="card-hover">
                        <CardContent className="p-6">
                            <div className="flex items-center justify-between">
                                <div>
                                    <h3 className="font-semibold text-slate-900 mb-1">Paramètres du site</h3>
                                    <p className="text-sm text-slate-600">Lien HelloAsso, images de présentation</p>
                                </div>
                                <Link to="/admin/settings">
                                    <Button className="bg-red-600 hover:bg-red-700">
                                        <Settings className="w-4 h-4 mr-2" />
                                        Gérer
                                    </Button>
                                </Link>
                            </div>
                        </CardContent>
                    </Card>
                </div>

                {/* Recent Formateurs */}
                <Card data-testid="formateurs-list">
                    <CardHeader className="flex flex-row items-center justify-between">
                        <CardTitle>Formateurs récents</CardTitle>
                        <Link to="/admin/formateurs">
                            <Button variant="ghost" size="sm">
                                Voir tous
                                <ArrowRight className="w-4 h-4 ml-1" />
                            </Button>
                        </Link>
                    </CardHeader>
                    <CardContent>
                        {formateurs.length === 0 ? (
                            <div className="empty-state py-8">
                                <Users className="w-12 h-12 mx-auto text-slate-300 mb-3" />
                                <p className="text-slate-500 mb-4">Aucun formateur</p>
                                <Link to="/admin/formateurs">
                                    <Button size="sm" className="bg-red-600 hover:bg-red-700">
                                        Créer un formateur
                                    </Button>
                                </Link>
                            </div>
                        ) : (
                            <div className="space-y-3">
                                {formateurs.slice(0, 5).map((formateur) => (
                                    <div 
                                        key={formateur.id}
                                        className="flex items-center justify-between p-4 bg-slate-50 rounded-lg"
                                    >
                                        <div>
                                            <p className="font-medium text-slate-900">
                                                {formateur.prenom} {formateur.nom}
                                            </p>
                                            <p className="text-sm text-slate-500">{formateur.email}</p>
                                        </div>
                                        <div className="text-right">
                                            <p className="text-sm font-medium text-slate-900">{formateur.nb_groupes || 0} groupes</p>
                                            <p className="text-xs text-slate-500">
                                                {formateur.must_set_password ? 'En attente' : 'Actif'}
                                            </p>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        )}
                    </CardContent>
                </Card>
            </div>
        </Layout>
    );
};

export default AdminDashboard;
