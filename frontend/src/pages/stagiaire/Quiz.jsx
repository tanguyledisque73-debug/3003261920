import React, { useState, useEffect } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { 
    ArrowLeft, 
    ArrowRight, 
    CheckCircle2,
    XCircle,
    AlertCircle,
    Unlock,
    Video
} from 'lucide-react';
import { Button } from '../../components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '../../components/ui/card';
import { Progress } from '../../components/ui/progress';
import Layout from '../../components/Layout';
import { getQuizByChapter, getChapter, submitQuiz, getUser, stagiaireGetChapitres } from '../../lib/api';
import { toast } from 'sonner';

const StagiaireQuiz = () => {
    const { chapterId } = useParams();
    const navigate = useNavigate();
    const user = getUser();
    
    const [quiz, setQuiz] = useState(null);
    const [chapter, setChapter] = useState(null);
    const [loading, setLoading] = useState(true);
    const [currentQuestion, setCurrentQuestion] = useState(0);
    const [answers, setAnswers] = useState([]);
    const [selectedAnswer, setSelectedAnswer] = useState(null);
    const [showResult, setShowResult] = useState(false);
    const [result, setResult] = useState(null);
    const [submitting, setSubmitting] = useState(false);
    const [seuil, setSeuil] = useState(80);

    useEffect(() => {
        if (!user || user.role !== 'stagiaire') {
            navigate('/login');
            return;
        }
        loadData();
    }, [chapterId, user, navigate]); // Added dependencies

    const loadData = async () => {
        try {
            const [quizData, chapterData, progressData] = await Promise.all([
                getQuizByChapter(chapterId),
                getChapter(chapterId),
                stagiaireGetChapitres()
            ]);
            
            // Check if chapter is unlocked
            const chapitreInfo = progressData.chapitres?.find(c => c.id === chapterId);
            if (!chapitreInfo?.is_unlocked) {
                toast.error('Ce chapitre n\'est pas encore débloqué');
                navigate('/stagiaire');
                return;
            }
            
            setQuiz(quizData);
            setChapter(chapterData);
            setSeuil(progressData.seuil_reussite || 80);
            setAnswers(new Array(quizData.questions.length).fill(-1));
        } catch (error) {
            console.error('Erreur:', error);
            toast.error('Quiz non disponible');
        } finally {
            setLoading(false);
        }
    };

    const handleSelectAnswer = (answerIndex) => {
        setSelectedAnswer(answerIndex);
        const newAnswers = [...answers];
        newAnswers[currentQuestion] = answerIndex;
        setAnswers(newAnswers);
    };

    const handleNext = () => {
        if (currentQuestion < quiz.questions.length - 1) {
            setCurrentQuestion(currentQuestion + 1);
            setSelectedAnswer(answers[currentQuestion + 1] === -1 ? null : answers[currentQuestion + 1]);
        }
    };

    const handlePrevious = () => {
        if (currentQuestion > 0) {
            setCurrentQuestion(currentQuestion - 1);
            setSelectedAnswer(answers[currentQuestion - 1] === -1 ? null : answers[currentQuestion - 1]);
        }
    };

    const handleSubmit = async () => {
        const unanswered = answers.filter(a => a === -1).length;
        if (unanswered > 0) {
            toast.error(`Vous n'avez pas répondu à ${unanswered} question(s)`);
            return;
        }

        setSubmitting(true);
        try {
            const resultData = await submitQuiz({
                quiz_id: quiz.id,
                answers: answers
            });
            setResult(resultData);
            setShowResult(true);
            
            if (resultData.percentage >= seuil) {
                if (resultData.next_chapter_unlocked) {
                    toast.success('Chapitre suivant débloqué !');
                } else {
                    toast.success('Quiz réussi !');
                }
            } else {
                toast.error(`Score insuffisant. Il vous faut ${seuil}% minimum.`);
            }
        } catch (error) {
            console.error('Erreur:', error);
            toast.error('Erreur lors de la soumission');
        } finally {
            setSubmitting(false);
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

    if (!quiz) {
        return (
            <Layout>
                <div className="max-w-3xl mx-auto px-4 py-8 text-center">
                    <AlertCircle className="w-12 h-12 mx-auto text-slate-400 mb-4" />
                    <p className="text-slate-600 mb-4">Quiz non disponible pour ce chapitre</p>
                    <Link to={`/stagiaire/chapitre/${chapterId}`}>
                        <Button variant="outline">Retour au chapitre</Button>
                    </Link>
                </div>
            </Layout>
        );
    }

    if (showResult && result) {
        const passed = result.percentage >= seuil;
        
        return (
            <Layout>
                <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-8" data-testid="quiz-result">
                    <Card className="animate-fade-in">
                        <CardHeader className="text-center border-b border-slate-100">
                            <div className={`w-20 h-20 mx-auto rounded-full flex items-center justify-center mb-4 ${
                                passed ? 'bg-green-100' : 'bg-red-100'
                            }`}>
                                {passed ? (
                                    <CheckCircle2 className="w-10 h-10 text-green-600" />
                                ) : (
                                    <XCircle className="w-10 h-10 text-red-600" />
                                )}
                            </div>
                            <CardTitle className="text-2xl">
                                {passed ? 'Félicitations !' : 'Pas encore...'}
                            </CardTitle>
                            <p className="text-slate-600 mt-2">
                                {passed 
                                    ? 'Vous avez validé ce chapitre !' 
                                    : `Il vous faut au moins ${seuil}% pour valider.`}
                            </p>
                        </CardHeader>
                        <CardContent className="p-6">
                            {/* Score */}
                            <div className="text-center mb-8">
                                <div className={`text-5xl font-bold mb-2 ${passed ? 'text-green-600' : 'text-red-600'}`}>
                                    {result.percentage}%
                                </div>
                                <p className="text-slate-600">
                                    {result.score} bonnes réponses sur {result.total}
                                </p>
                                {result.next_chapter_unlocked && (
                                    <div className="mt-4 p-3 bg-green-50 rounded-lg inline-flex items-center gap-2 text-green-700">
                                        <Unlock className="w-5 h-5" />
                                        <span>Chapitre suivant débloqué !</span>
                                    </div>
                                )}
                            </div>

                            {/* Answers Review */}
                            <div className="space-y-4 mb-8">
                                <h3 className="font-semibold text-slate-900">Détail des réponses</h3>
                                {quiz.questions.map((question, index) => {
                                    const answerDetail = result.answers[index];
                                    return (
                                        <div 
                                            key={question.id}
                                            className={`p-4 rounded-lg border ${
                                                answerDetail?.is_correct 
                                                    ? 'border-green-200 bg-green-50' 
                                                    : 'border-red-200 bg-red-50'
                                            }`}
                                        >
                                            <div className="flex items-start gap-3">
                                                {answerDetail?.is_correct ? (
                                                    <CheckCircle2 className="w-5 h-5 text-green-600 mt-0.5 flex-shrink-0" />
                                                ) : (
                                                    <XCircle className="w-5 h-5 text-red-600 mt-0.5 flex-shrink-0" />
                                                )}
                                                <div className="flex-1">
                                                    <p className="font-medium text-slate-900 text-sm mb-2">
                                                        {question.question}
                                                    </p>
                                                    {!answerDetail?.is_correct && (
                                                        <p className="text-sm text-slate-600">
                                                            <span className="text-red-600">Votre réponse :</span> {question.options[answerDetail?.user_answer]}
                                                            <br />
                                                            <span className="text-green-600">Bonne réponse :</span> {question.options[question.correct_answer]}
                                                        </p>
                                                    )}
                                                    <p className="text-xs text-slate-500 mt-2 italic">
                                                        {question.explication}
                                                    </p>
                                                </div>
                                            </div>
                                        </div>
                                    );
                                })}
                            </div>

                            {/* Actions */}
                            <div className="flex flex-col sm:flex-row gap-3">
                                <Link to={`/stagiaire/chapitre/${chapterId}`} className="flex-1">
                                    <Button variant="outline" className="w-full">
                                        <ArrowLeft className="w-4 h-4 mr-2" />
                                        Revoir le chapitre
                                    </Button>
                                </Link>
                                {!passed && (
                                    <Button 
                                        onClick={() => {
                                            setShowResult(false);
                                            setCurrentQuestion(0);
                                            setAnswers(new Array(quiz.questions.length).fill(-1));
                                            setSelectedAnswer(null);
                                        }}
                                        variant="outline"
                                        className="flex-1"
                                    >
                                        Réessayer
                                    </Button>
                                )}
                                <Link to="/stagiaire" className="flex-1">
                                    <Button className={`w-full ${passed ? 'bg-green-600 hover:bg-green-700' : 'bg-red-600 hover:bg-red-700'}`}>
                                        {passed ? 'Continuer' : 'Tableau de bord'}
                                        <ArrowRight className="w-4 h-4 ml-2" />
                                    </Button>
                                </Link>
                            </div>
                        </CardContent>
                    </Card>
                </div>
            </Layout>
        );
    }

    const question = quiz.questions[currentQuestion];
    const progressValue = ((currentQuestion + 1) / quiz.questions.length) * 100;

    return (
        <Layout>
            <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-8" data-testid="quiz-page">
                {/* Header */}
                <div className="mb-6">
                    <Link 
                        to={`/stagiaire/chapitre/${chapterId}`}
                        className="text-sm text-slate-600 hover:text-red-600 flex items-center gap-1 mb-4"
                    >
                        <ArrowLeft className="w-4 h-4" />
                        Retour au chapitre
                    </Link>
                    <h1 className="text-2xl font-bold text-slate-900">
                        {quiz.titre}
                    </h1>
                    <p className="text-slate-600 text-sm mt-1">
                        Score minimum requis : <strong className="text-red-600">{seuil}%</strong>
                    </p>
                </div>

                {/* Video if available */}
                {quiz.video_url && currentQuestion === 0 && (
                    <Card className="mb-6 bg-slate-900">
                        <CardContent className="p-4">
                            <div className="flex items-center gap-2 text-white mb-2">
                                <Video className="w-5 h-5" />
                                <span className="font-medium">Vidéo de présentation</span>
                            </div>
                            <div className="aspect-video bg-black rounded-lg">
                                <iframe
                                    src={quiz.video_url}
                                    className="w-full h-full rounded-lg"
                                    allowFullScreen
                                />
                            </div>
                        </CardContent>
                    </Card>
                )}

                {/* Progress */}
                <div className="mb-8">
                    <div className="flex items-center justify-between text-sm text-slate-600 mb-2">
                        <span>Question {currentQuestion + 1} sur {quiz.questions.length}</span>
                        <span>{Math.round(progressValue)}%</span>
                    </div>
                    <Progress value={progressValue} className="h-2" />
                </div>

                {/* Question Card */}
                <Card className="mb-6 animate-fade-in" key={currentQuestion}>
                    <CardHeader>
                        <div className="flex items-center gap-2 mb-2">
                            <span className={`px-2 py-0.5 rounded text-xs font-medium ${
                                question.type === 'vrai_faux' 
                                    ? 'bg-blue-100 text-blue-700' 
                                    : 'bg-purple-100 text-purple-700'
                            }`}>
                                {question.type === 'vrai_faux' ? 'Vrai/Faux' : 'QCM'}
                            </span>
                        </div>
                        <CardTitle className="text-lg leading-relaxed">
                            {question.question}
                        </CardTitle>
                    </CardHeader>
                    <CardContent>
                        <div className="space-y-3">
                            {question.options.map((option, index) => (
                                <button
                                    key={`option-${currentQuestion}-${index}-${option.substring(0, 10)}`}
                                    onClick={() => handleSelectAnswer(index)}
                                    className={`w-full text-left p-4 rounded-lg border-2 transition-all ${
                                        selectedAnswer === index
                                            ? 'border-red-600 bg-red-50'
                                            : 'border-slate-200 hover:border-slate-300 hover:bg-slate-50'
                                    }`}
                                >
                                    <div className="flex items-center gap-3">
                                        <div className={`w-6 h-6 rounded-full border-2 flex items-center justify-center flex-shrink-0 ${
                                            selectedAnswer === index
                                                ? 'border-red-600 bg-red-600'
                                                : 'border-slate-300'
                                        }`}>
                                            {selectedAnswer === index && (
                                                <div className="w-2 h-2 rounded-full bg-white"></div>
                                            )}
                                        </div>
                                        <span className={selectedAnswer === index ? 'text-slate-900 font-medium' : 'text-slate-700'}>
                                            {option}
                                        </span>
                                    </div>
                                </button>
                            ))}
                        </div>
                    </CardContent>
                </Card>

                {/* Navigation */}
                <div className="flex items-center justify-between">
                    <Button
                        variant="outline"
                        onClick={handlePrevious}
                        disabled={currentQuestion === 0}
                    >
                        <ArrowLeft className="w-4 h-4 mr-2" />
                        Précédent
                    </Button>

                    <div className="hidden sm:flex items-center gap-1">
                        {quiz.questions.map((_, index) => (
                            <button
                                key={index}
                                onClick={() => {
                                    setCurrentQuestion(index);
                                    setSelectedAnswer(answers[index] === -1 ? null : answers[index]);
                                }}
                                className={`w-3 h-3 rounded-full transition-colors ${
                                    index === currentQuestion
                                        ? 'bg-red-600'
                                        : answers[index] !== -1
                                            ? 'bg-green-500'
                                            : 'bg-slate-300'
                                }`}
                            />
                        ))}
                    </div>

                    {currentQuestion === quiz.questions.length - 1 ? (
                        <Button
                            onClick={handleSubmit}
                            disabled={submitting}
                            className="bg-red-600 hover:bg-red-700"
                        >
                            {submitting ? (
                                <div className="spinner w-5 h-5 border-2 border-white/30 border-t-white"></div>
                            ) : (
                                <>
                                    Terminer
                                    <CheckCircle2 className="w-4 h-4 ml-2" />
                                </>
                            )}
                        </Button>
                    ) : (
                        <Button onClick={handleNext} disabled={selectedAnswer === null}>
                            Suivant
                            <ArrowRight className="w-4 h-4 ml-2" />
                        </Button>
                    )}
                </div>
            </div>
        </Layout>
    );
};

export default StagiaireQuiz;
