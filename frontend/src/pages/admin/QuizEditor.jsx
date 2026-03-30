import React, { useState, useEffect } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { 
    ArrowLeft,
    Plus,
    Trash2,
    Save,
    Video
} from 'lucide-react';
import { Button } from '../../components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '../../components/ui/card';
import { Input } from '../../components/ui/input';
import { Label } from '../../components/ui/label';
import { Textarea } from '../../components/ui/textarea';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../../components/ui/select';
import Layout from '../../components/Layout';
import { getQuizById, getQuizByChapter, getChapters, adminCreateQuiz, adminUpdateQuiz, getUser } from '../../lib/api';
import { toast } from 'sonner';

const AdminQuizEditor = () => {
    const { quizId } = useParams();
    const navigate = useNavigate();
    const user = getUser();
    const isEditing = Boolean(quizId);
    
    const [loading, setLoading] = useState(true);
    const [saving, setSaving] = useState(false);
    const [chapters, setChapters] = useState([]);
    const [formData, setFormData] = useState({
        chapter_id: '',
        titre: '',
        video_url: '',
        questions: []
    });

    useEffect(() => {
        if (!user || user.role !== 'admin') {
            navigate('/login');
            return;
        }
        loadData();
    }, [quizId, user, navigate]); // Added dependencies

    const loadData = async () => {
        try {
            const chaptersData = await getChapters();
            setChapters(chaptersData);
            
            if (isEditing) {
                // Get quiz by ID
                const quizData = await getQuizById(quizId);
                setFormData({
                    chapter_id: quizData.chapter_id,
                    titre: quizData.titre,
                    video_url: quizData.video_url || '',
                    questions: quizData.questions.map(q => ({
                        question: q.question,
                        type: q.type,
                        options: q.options,
                        correct_answer: q.correct_answer,
                        explication: q.explication
                    }))
                });
            }
        } catch (error) {
            console.error('Erreur:', error);
            if (isEditing) {
                toast.error('Quiz non trouvé');
            }
        } finally {
            setLoading(false);
        }
    };

    const addQuestion = () => {
        setFormData({
            ...formData,
            questions: [...formData.questions, {
                question: '',
                type: 'qcm',
                options: ['', '', '', ''],
                correct_answer: 0,
                explication: ''
            }]
        });
    };

    const removeQuestion = (index) => {
        const newQuestions = [...formData.questions];
        newQuestions.splice(index, 1);
        setFormData({ ...formData, questions: newQuestions });
    };

    const updateQuestion = (index, field, value) => {
        const newQuestions = [...formData.questions];
        newQuestions[index] = { ...newQuestions[index], [field]: value };
        setFormData({ ...formData, questions: newQuestions });
    };

    const updateOption = (questionIndex, optionIndex, value) => {
        const newQuestions = [...formData.questions];
        newQuestions[questionIndex].options[optionIndex] = value;
        setFormData({ ...formData, questions: newQuestions });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        
        if (formData.questions.length === 0) {
            toast.error('Ajoutez au moins une question');
            return;
        }

        setSaving(true);
        try {
            if (isEditing) {
                await adminUpdateQuiz(quizId, formData);
                toast.success('Quiz mis à jour');
            } else {
                await adminCreateQuiz(formData);
                toast.success('Quiz créé');
            }
            navigate('/admin/quizzes');
        } catch (error) {
            console.error('Erreur:', error);
            toast.error(error.response?.data?.detail || 'Erreur lors de l\'enregistrement');
        } finally {
            setSaving(false);
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
            <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8" data-testid="quiz-editor">
                {/* Back */}
                <Link 
                    to="/admin/quizzes"
                    className="text-sm text-slate-600 hover:text-red-600 flex items-center gap-1 mb-6"
                >
                    <ArrowLeft className="w-4 h-4" />
                    Retour aux quiz
                </Link>

                <h1 className="text-3xl font-bold text-slate-900 mb-8">
                    {isEditing ? 'Modifier le quiz' : 'Créer un quiz'}
                </h1>

                <form onSubmit={handleSubmit}>
                    {/* Basic Info */}
                    <Card className="mb-6">
                        <CardHeader>
                            <CardTitle>Informations générales</CardTitle>
                        </CardHeader>
                        <CardContent className="space-y-4">
                            <div className="grid md:grid-cols-2 gap-4">
                                <div className="space-y-2">
                                    <Label htmlFor="chapter">Chapitre associé</Label>
                                    <Select 
                                        value={formData.chapter_id}
                                        onValueChange={(value) => setFormData({...formData, chapter_id: value})}
                                        disabled={isEditing}
                                    >
                                        <SelectTrigger>
                                            <SelectValue placeholder="Sélectionner un chapitre" />
                                        </SelectTrigger>
                                        <SelectContent>
                                            {chapters.map((chapter) => (
                                                <SelectItem key={chapter.id} value={chapter.id}>
                                                    {chapter.numero}. {chapter.titre}
                                                </SelectItem>
                                            ))}
                                        </SelectContent>
                                    </Select>
                                </div>
                                <div className="space-y-2">
                                    <Label htmlFor="titre">Titre du quiz</Label>
                                    <Input
                                        id="titre"
                                        placeholder="Quiz - Nom du chapitre"
                                        value={formData.titre}
                                        onChange={(e) => setFormData({...formData, titre: e.target.value})}
                                        required
                                    />
                                </div>
                            </div>
                            
                            <div className="space-y-2">
                                <Label htmlFor="video" className="flex items-center gap-2">
                                    <Video className="w-4 h-4" />
                                    URL de la vidéo (optionnel)
                                </Label>
                                <Input
                                    id="video"
                                    placeholder="https://www.youtube.com/embed/..."
                                    value={formData.video_url}
                                    onChange={(e) => setFormData({...formData, video_url: e.target.value})}
                                />
                                <p className="text-xs text-slate-500">
                                    URL d'intégration YouTube ou autre. La vidéo sera affichée avant le quiz.
                                </p>
                            </div>
                        </CardContent>
                    </Card>

                    {/* Questions */}
                    <Card className="mb-6">
                        <CardHeader className="flex flex-row items-center justify-between">
                            <CardTitle>Questions ({formData.questions.length})</CardTitle>
                            <Button type="button" variant="outline" onClick={addQuestion}>
                                <Plus className="w-4 h-4 mr-2" />
                                Ajouter une question
                            </Button>
                        </CardHeader>
                        <CardContent>
                            {formData.questions.length === 0 ? (
                                <div className="empty-state py-8">
                                    <p className="text-slate-500 mb-4">Aucune question</p>
                                    <Button type="button" onClick={addQuestion}>
                                        <Plus className="w-4 h-4 mr-2" />
                                        Ajouter une question
                                    </Button>
                                </div>
                            ) : (
                                <div className="space-y-6">
                                    {formData.questions.map((question, qIndex) => (
                                        <div key={qIndex} className="p-4 bg-slate-50 rounded-lg">
                                            <div className="flex items-start justify-between mb-4">
                                                <span className="font-medium text-slate-900">Question {qIndex + 1}</span>
                                                <Button 
                                                    type="button" 
                                                    variant="ghost" 
                                                    size="sm"
                                                    className="text-red-600"
                                                    onClick={() => removeQuestion(qIndex)}
                                                >
                                                    <Trash2 className="w-4 h-4" />
                                                </Button>
                                            </div>
                                            
                                            <div className="space-y-4">
                                                <div className="space-y-2">
                                                    <Label>Question</Label>
                                                    <Textarea
                                                        placeholder="Posez votre question..."
                                                        value={question.question}
                                                        onChange={(e) => updateQuestion(qIndex, 'question', e.target.value)}
                                                        required
                                                    />
                                                </div>
                                                
                                                <div className="grid md:grid-cols-2 gap-4">
                                                    <div className="space-y-2">
                                                        <Label>Type</Label>
                                                        <Select 
                                                            value={question.type}
                                                            onValueChange={(value) => {
                                                                updateQuestion(qIndex, 'type', value);
                                                                if (value === 'vrai_faux') {
                                                                    updateQuestion(qIndex, 'options', ['Vrai', 'Faux']);
                                                                } else {
                                                                    updateQuestion(qIndex, 'options', ['', '', '', '']);
                                                                }
                                                            }}
                                                        >
                                                            <SelectTrigger>
                                                                <SelectValue />
                                                            </SelectTrigger>
                                                            <SelectContent>
                                                                <SelectItem value="qcm">QCM</SelectItem>
                                                                <SelectItem value="vrai_faux">Vrai/Faux</SelectItem>
                                                            </SelectContent>
                                                        </Select>
                                                    </div>
                                                    <div className="space-y-2">
                                                        <Label>Bonne réponse</Label>
                                                        <Select 
                                                            value={String(question.correct_answer)}
                                                            onValueChange={(value) => updateQuestion(qIndex, 'correct_answer', parseInt(value))}
                                                        >
                                                            <SelectTrigger>
                                                                <SelectValue />
                                                            </SelectTrigger>
                                                            <SelectContent>
                                                                {question.options.map((_, oIndex) => (
                                                                    <SelectItem key={oIndex} value={String(oIndex)}>
                                                                        Option {oIndex + 1}
                                                                    </SelectItem>
                                                                ))}
                                                            </SelectContent>
                                                        </Select>
                                                    </div>
                                                </div>
                                                
                                                <div className="space-y-2">
                                                    <Label>Options de réponse</Label>
                                                    <div className="grid md:grid-cols-2 gap-2">
                                                        {question.options.map((option, oIndex) => (
                                                            <Input
                                                                key={oIndex}
                                                                placeholder={`Option ${oIndex + 1}`}
                                                                value={option}
                                                                onChange={(e) => updateOption(qIndex, oIndex, e.target.value)}
                                                                required
                                                                disabled={question.type === 'vrai_faux'}
                                                                className={question.correct_answer === oIndex ? 'border-green-500' : ''}
                                                            />
                                                        ))}
                                                    </div>
                                                </div>
                                                
                                                <div className="space-y-2">
                                                    <Label>Explication</Label>
                                                    <Textarea
                                                        placeholder="Expliquez la bonne réponse..."
                                                        value={question.explication}
                                                        onChange={(e) => updateQuestion(qIndex, 'explication', e.target.value)}
                                                        required
                                                    />
                                                </div>
                                            </div>
                                        </div>
                                    ))}
                                </div>
                            )}
                        </CardContent>
                    </Card>

                    {/* Submit */}
                    <div className="flex gap-3">
                        <Button type="submit" className="bg-red-600 hover:bg-red-700" disabled={saving}>
                            {saving ? (
                                <div className="spinner w-5 h-5 border-2 border-white/30 border-t-white"></div>
                            ) : (
                                <>
                                    <Save className="w-4 h-4 mr-2" />
                                    {isEditing ? 'Enregistrer' : 'Créer le quiz'}
                                </>
                            )}
                        </Button>
                        <Link to="/admin/quizzes">
                            <Button type="button" variant="outline">Annuler</Button>
                        </Link>
                    </div>
                </form>
            </div>
        </Layout>
    );
};

export default AdminQuizEditor;
