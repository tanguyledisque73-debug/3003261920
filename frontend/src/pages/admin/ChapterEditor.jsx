import React, { useState, useEffect } from 'react';
import { useParams, useNavigate, useSearchParams } from 'react-router-dom';
import { 
    Plus,
    Trash2,
    Save,
    ArrowLeft,
    Image as ImageIcon,
    Video,
    FileText,
    Upload,
    Link as LinkIcon,
    Play
} from 'lucide-react';
import { Button } from '../../components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '../../components/ui/card';
import { Input } from '../../components/ui/input';
import { Label } from '../../components/ui/label';
import { Textarea } from '../../components/ui/textarea';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../../components/ui/select';
import Layout from '../../components/Layout';
import VideoUploader from '../../components/VideoUploader';
import RichTextEditor from '../../components/RichTextEditor';
import { getChapter, adminCreateChapter, adminUpdateChapter, getUser } from '../../lib/api';
import { toast } from 'sonner';
import logger from '../../utils/logger';

const AdminChapterEditor = () => {
    const { chapterId } = useParams();
    const navigate = useNavigate();
    const [searchParams] = useSearchParams();
    const user = getUser();
    const isEditing = !!chapterId;
    const defaultType = searchParams.get('type') || 'PSE';

    const [loading, setLoading] = useState(isEditing);
    const [saving, setSaving] = useState(false);
    
    const [formData, setFormData] = useState({
        numero: 1,
        titre: '',
        description: '',
        icon: 'BookOpen',
        formation_type: defaultType,
        image_url: '',
        fiches: []
    });

    useEffect(() => {
        if (!user || user.role !== 'admin') {
            navigate('/login');
            return;
        }
        if (isEditing) {
            loadChapter();
        }
    }, [chapterId]);

    const loadChapter = async () => {
        try {
            const chapter = await getChapter(chapterId);
            setFormData({
                numero: chapter.numero,
                titre: chapter.titre,
                description: chapter.description || '',
                icon: chapter.icon || 'BookOpen',
                formation_type: chapter.formation_type,
                image_url: chapter.image_url || '',
                fiches: chapter.fiches || []
            });
        } catch (error) {
            logger.logError(error, 'ChapterEditor.loadChapter');
            toast.error('Erreur lors du chargement');
        } finally {
            setLoading(false);
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        
        // Validation
        if (!formData.titre.trim()) {
            toast.error('Le titre est obligatoire');
            return;
        }

        setSaving(true);
        try {
            if (isEditing) {
                await adminUpdateChapter(chapterId, formData);
                toast.success('Chapitre modifié avec succès');
            } else {
                await adminCreateChapter(formData);
                toast.success('Chapitre créé avec succès');
            }
            navigate('/admin/chapters');
        } catch (error) {
            console.error('Erreur:', error);
            toast.error('Erreur lors de la sauvegarde');
        } finally {
            setSaving(false);
        }
    };

    const addFiche = () => {
        setFormData({
            ...formData,
            fiches: [
                ...formData.fiches,
                {
                    id: `fiche-${Date.now()}`,
                    titre: '',
                    contenu: '',
                    image_url: '',
                    video_url: ''
                }
            ]
        });
    };

    const updateFiche = (index, field, value) => {
        const newFiches = [...formData.fiches];
        newFiches[index] = { ...newFiches[index], [field]: value };
        setFormData({ ...formData, fiches: newFiches });
    };

    const deleteFiche = (index) => {
        const newFiches = formData.fiches.filter((_, i) => i !== index);
        setFormData({ ...formData, fiches: newFiches });
    };

    const iconOptions = [
        'BookOpen', 'Heart', 'Shield', 'Activity', 'AlertCircle', 
        'Droplet', 'Wind', 'Flame', 'User', 'Users', 'Bone', 'Bandage'
    ];

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
            <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8" data-testid="admin-chapter-editor">
                {/* Header */}
                <div className="mb-8">
                    <Button 
                        variant="ghost" 
                        onClick={() => navigate('/admin/chapters')}
                        className="mb-4"
                    >
                        <ArrowLeft className="w-4 h-4 mr-2" />
                        Retour aux chapitres
                    </Button>
                    <h1 className="text-3xl font-bold text-slate-900 mb-2">
                        {isEditing ? 'Modifier le chapitre' : 'Nouveau chapitre'}
                    </h1>
                    <p className="text-slate-600">
                        Gérez le contenu, les fiches, les images et les vidéos du chapitre.
                    </p>
                </div>

                <form onSubmit={handleSubmit} className="space-y-6">
                    {/* Main Info */}
                    <Card>
                        <CardHeader>
                            <CardTitle>Informations principales</CardTitle>
                        </CardHeader>
                        <CardContent className="space-y-4">
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                <div>
                                    <Label htmlFor="numero">Numéro du chapitre *</Label>
                                    <Input
                                        id="numero"
                                        type="number"
                                        min="1"
                                        value={formData.numero}
                                        onChange={(e) => setFormData({ ...formData, numero: parseInt(e.target.value) })}
                                        required
                                    />
                                </div>
                                <div>
                                    <Label htmlFor="formation_type">Type de formation *</Label>
                                    <Select 
                                        value={formData.formation_type} 
                                        onValueChange={(value) => setFormData({ ...formData, formation_type: value })}
                                        disabled={isEditing}
                                    >
                                        <SelectTrigger id="formation_type">
                                            <SelectValue />
                                        </SelectTrigger>
                                        <SelectContent>
                                            <SelectItem value="PSE">PSE - Premiers Secours en Équipe</SelectItem>
                                            <SelectItem value="PSC">PSC - Premiers Secours Citoyen</SelectItem>
                                        </SelectContent>
                                    </Select>
                                </div>
                            </div>

                            <div>
                                <Label htmlFor="titre">Titre du chapitre *</Label>
                                <Input
                                    id="titre"
                                    value={formData.titre}
                                    onChange={(e) => setFormData({ ...formData, titre: e.target.value })}
                                    placeholder="Ex: Obstruction des voies aériennes"
                                    required
                                />
                            </div>

                            <div>
                                <Label htmlFor="description">Description</Label>
                                <Textarea
                                    id="description"
                                    value={formData.description}
                                    onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                                    placeholder="Description courte du chapitre..."
                                    rows={2}
                                />
                            </div>

                            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                <div>
                                    <Label htmlFor="icon">Icône</Label>
                                    <Select 
                                        value={formData.icon} 
                                        onValueChange={(value) => setFormData({ ...formData, icon: value })}
                                    >
                                        <SelectTrigger id="icon">
                                            <SelectValue />
                                        </SelectTrigger>
                                        <SelectContent>
                                            {iconOptions.map(icon => (
                                                <SelectItem key={icon} value={icon}>{icon}</SelectItem>
                                            ))}
                                        </SelectContent>
                                    </Select>
                                </div>
                                <div>
                                    <Label htmlFor="image_url">URL de l'image du chapitre</Label>
                                    <Input
                                        id="image_url"
                                        value={formData.image_url}
                                        onChange={(e) => setFormData({ ...formData, image_url: e.target.value })}
                                        placeholder="https://..."
                                    />
                                </div>
                            </div>
                        </CardContent>
                    </Card>

                    {/* Fiches */}
                    <Card>
                        <CardHeader className="flex flex-row items-center justify-between">
                            <CardTitle>Fiches de contenu ({formData.fiches.length})</CardTitle>
                            <Button type="button" onClick={addFiche} size="sm">
                                <Plus className="w-4 h-4 mr-2" />
                                Ajouter une fiche
                            </Button>
                        </CardHeader>
                        <CardContent className="space-y-4">
                            {formData.fiches.length === 0 ? (
                                <div className="text-center py-8 text-slate-500">
                                    <FileText className="w-12 h-12 mx-auto mb-2 text-slate-300" />
                                    <p>Aucune fiche. Cliquez sur "Ajouter une fiche" pour commencer.</p>
                                </div>
                            ) : (
                                formData.fiches.map((fiche, index) => (
                                    <Card key={fiche.id} className="bg-slate-50">
                                        <CardContent className="pt-6 space-y-4">
                                            <div className="flex items-center justify-between mb-4">
                                                <h4 className="font-medium text-slate-900">Fiche {index + 1}</h4>
                                                <Button
                                                    type="button"
                                                    variant="ghost"
                                                    size="sm"
                                                    onClick={() => deleteFiche(index)}
                                                    className="text-red-600 hover:text-red-700"
                                                >
                                                    <Trash2 className="w-4 h-4" />
                                                </Button>
                                            </div>

                                            <div>
                                                <Label>Titre de la fiche *</Label>
                                                <Input
                                                    value={fiche.titre}
                                                    onChange={(e) => updateFiche(index, 'titre', e.target.value)}
                                                    placeholder="Ex: Reconnaître l'obstruction"
                                                    required
                                                />
                                            </div>

                                            <div>
                                                <Label>Contenu de la fiche *</Label>
                                                <RichTextEditor
                                                    value={fiche.contenu}
                                                    onChange={(value) => updateFiche(index, 'contenu', value)}
                                                    placeholder="Écrivez le contenu de la fiche avec mise en forme..."
                                                    height="400px"
                                                />
                                            </div>

                                            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                                <div>
                                                    <Label className="flex items-center gap-2">
                                                        <ImageIcon className="w-4 h-4" />
                                                        URL de l'image
                                                    </Label>
                                                    <Input
                                                        value={fiche.image_url || ''}
                                                        onChange={(e) => updateFiche(index, 'image_url', e.target.value)}
                                                        placeholder="https://..."
                                                    />
                                                </div>
                                            </div>
                                            
                                            {/* Video Upload/URL */}
                                            <div>
                                                <Label className="flex items-center gap-2 mb-2">
                                                    <Video className="w-4 h-4" />
                                                    Vidéo de la fiche
                                                </Label>
                                                <VideoUploader
                                                    value={fiche.video_url || ''}
                                                    onChange={(url) => updateFiche(index, 'video_url', url)}
                                                />
                                            </div>
                                        </CardContent>
                                    </Card>
                                ))
                            )}
                        </CardContent>
                    </Card>

                    {/* Actions */}
                    <div className="flex items-center justify-between">
                        <Button
                            type="button"
                            variant="outline"
                            onClick={() => navigate('/admin/chapters')}
                        >
                            Annuler
                        </Button>
                        <Button
                            type="submit"
                            disabled={saving}
                            className="bg-red-600 hover:bg-red-700"
                        >
                            <Save className="w-4 h-4 mr-2" />
                            {saving ? 'Enregistrement...' : (isEditing ? 'Enregistrer les modifications' : 'Créer le chapitre')}
                        </Button>
                    </div>
                </form>
            </div>
        </Layout>
    );
};

export default AdminChapterEditor;
