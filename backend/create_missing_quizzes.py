"""
Script pour créer les quiz manquants pour tous les chapitres
"""
import asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

# Quiz data for missing chapters
MISSING_QUIZZES = [
    {
        "id": "quiz-ch3",
        "chapter_id": "ch3",
        "titre": "Quiz - Protection et sécurité",
        "video_url": None,
        "questions": [
            {
                "id": "q3-1",
                "question": "Quelle est la priorité lors de l'arrivée sur les lieux d'un accident?",
                "type": "qcm",
                "options": ["Secourir la victime", "Protéger la zone", "Alerter les secours", "Faire un bilan"],
                "correct_answer": 1,
                "explication": "La priorité est toujours PROTÉGER avant de secourir ou d'alerter."
            },
            {
                "id": "q3-2",
                "question": "Le port des gants est obligatoire pour tout contact avec une victime.",
                "type": "vrai_faux",
                "options": ["Vrai", "Faux"],
                "correct_answer": 0,
                "explication": "Les gants protègent contre les agents infectieux et doivent être portés systématiquement."
            },
            {
                "id": "q3-3",
                "question": "Dans quel cas utilise-t-on un triangle de présignalisation?",
                "type": "qcm",
                "options": ["Accident en ville", "Accident sur route", "Accident domestique", "Jamais"],
                "correct_answer": 1,
                "explication": "Le triangle de présignalisation est utilisé sur les routes pour signaler un danger."
            },
            {
                "id": "q3-4",
                "question": "Quelle distance minimale faut-il respecter pour placer le triangle de présignalisation?",
                "type": "qcm",
                "options": ["10 mètres", "30 mètres", "100 mètres", "200 mètres"],
                "correct_answer": 2,
                "explication": "Le triangle doit être placé à au moins 100 mètres avant l'accident sur route."
            },
            {
                "id": "q3-5",
                "question": "On peut déplacer une victime si elle est en danger immédiat.",
                "type": "vrai_faux",
                "options": ["Vrai", "Faux"],
                "correct_answer": 0,
                "explication": "Si la victime est en danger immédiat (incendie, explosion...), il faut la dégager rapidement."
            }
        ]
    },
    {
        "id": "quiz-ch4",
        "chapter_id": "ch4",
        "titre": "Quiz - Hygiène et asepsie",
        "video_url": None,
        "questions": [
            {
                "id": "q4-1",
                "question": "Quelle est la durée minimale pour un lavage des mains efficace?",
                "type": "qcm",
                "options": ["10 secondes", "30 secondes", "1 minute", "3 minutes"],
                "correct_answer": 1,
                "explication": "Un lavage des mains efficace doit durer au moins 30 secondes."
            },
            {
                "id": "q4-2",
                "question": "La friction hydro-alcoolique remplace le lavage des mains.",
                "type": "vrai_faux",
                "options": ["Vrai", "Faux"],
                "correct_answer": 1,
                "explication": "La SHA ne remplace pas le lavage si les mains sont visiblement souillées."
            },
            {
                "id": "q4-3",
                "question": "Que signifie l'acronyme DASRI?",
                "type": "qcm",
                "options": ["Déchets d'Activités de Soins à Risques Infectieux", "Dispositifs d'Aide aux Soins", "Danger Accidents Soins Risques", "Détection Alerte Soins"],
                "correct_answer": 0,
                "explication": "DASRI = Déchets d'Activités de Soins à Risques Infectieux (aiguilles, compresses souillées...)."
            },
            {
                "id": "q4-4",
                "question": "Les gants peuvent être réutilisés après désinfection.",
                "type": "vrai_faux",
                "options": ["Vrai", "Faux"],
                "correct_answer": 1,
                "explication": "Les gants à usage unique doivent être jetés après chaque utilisation."
            },
            {
                "id": "q4-5",
                "question": "Quelle est la bonne technique pour retirer des gants contaminés?",
                "type": "qcm",
                "options": ["Tirer par le bout des doigts", "Pincer l'extérieur et retourner", "Les couper", "Utiliser du désinfectant"],
                "correct_answer": 1,
                "explication": "On retire le premier gant en pinçant l'extérieur, puis on glisse les doigts sous le second."
            }
        ]
    },
    {
        "id": "quiz-ch6",
        "chapter_id": "ch6",
        "titre": "Quiz - Malaises et affections spécifiques",
        "video_url": None,
        "questions": [
            {
                "id": "q6-1",
                "question": "Quelle est la position d'attente pour une victime consciente présentant un malaise?",
                "type": "qcm",
                "options": ["Allongée sur le dos", "Position demi-assise", "Position latérale de sécurité", "Debout"],
                "correct_answer": 1,
                "explication": "La position demi-assise est recommandée pour une victime consciente en malaise."
            },
            {
                "id": "q6-2",
                "question": "Un diabétique en hypoglycémie peut être conscient.",
                "type": "vrai_faux",
                "options": ["Vrai", "Faux"],
                "correct_answer": 0,
                "explication": "L'hypoglycémie peut se manifester par des sueurs, tremblements, confusion tout en restant conscient."
            },
            {
                "id": "q6-3",
                "question": "Que faire face à une victime diabétique consciente en hypoglycémie?",
                "type": "qcm",
                "options": ["Donner de l'eau", "Donner du sucre", "Donner de l'insuline", "Ne rien donner"],
                "correct_answer": 1,
                "explication": "On donne du sucre rapide (morceau de sucre, jus de fruit) si la victime est consciente."
            },
            {
                "id": "q6-4",
                "question": "Les signes d'un AVC peuvent inclure une asymétrie du visage.",
                "type": "vrai_faux",
                "options": ["Vrai", "Faux"],
                "correct_answer": 0,
                "explication": "L'asymétrie faciale est un signe typique d'AVC (bouche qui tombe, paupière tombante)."
            },
            {
                "id": "q6-5",
                "question": "Quelle est la conduite à tenir face à une crise d'épilepsie?",
                "type": "qcm",
                "options": ["Maintenir la victime", "Protéger la tête", "Mettre un objet dans la bouche", "Donner à boire"],
                "correct_answer": 1,
                "explication": "On protège la tête contre les chocs et on laisse la crise se dérouler sans intervenir."
            }
        ]
    },
    {
        "id": "quiz-ch7",
        "chapter_id": "ch7",
        "titre": "Quiz - Atteintes circonstancielles",
        "video_url": None,
        "questions": [
            {
                "id": "q7-1",
                "question": "Quelle est la température corporelle normale?",
                "type": "qcm",
                "options": ["35°C", "37°C", "39°C", "40°C"],
                "correct_answer": 1,
                "explication": "La température normale du corps humain est d'environ 37°C."
            },
            {
                "id": "q7-2",
                "question": "L'hypothermie est définie par une température inférieure à 35°C.",
                "type": "vrai_faux",
                "options": ["Vrai", "Faux"],
                "correct_answer": 0,
                "explication": "En dessous de 35°C, on parle d'hypothermie."
            },
            {
                "id": "q7-3",
                "question": "Que faire face à une victime en hypothermie?",
                "type": "qcm",
                "options": ["Réchauffer rapidement", "Frictionner vigoureusement", "Réchauffer progressivement", "Donner de l'alcool"],
                "correct_answer": 2,
                "explication": "On réchauffe progressivement avec des couvertures, jamais brutalement."
            },
            {
                "id": "q7-4",
                "question": "Un coup de chaleur peut survenir sans exposition directe au soleil.",
                "type": "vrai_faux",
                "options": ["Vrai", "Faux"],
                "correct_answer": 0,
                "explication": "Le coup de chaleur peut survenir dans un environnement chaud et humide, même à l'ombre."
            },
            {
                "id": "q7-5",
                "question": "Quelle est la priorité face à une noyade?",
                "type": "qcm",
                "options": ["Sécher la victime", "Réchauffer", "Libérer les voies aériennes", "Faire vomir"],
                "correct_answer": 2,
                "explication": "La priorité est de libérer les voies aériennes et vérifier la respiration."
            }
        ]
    },
    {
        "id": "quiz-ch8",
        "chapter_id": "ch8",
        "titre": "Quiz - Traumatismes",
        "video_url": None,
        "questions": [
            {
                "id": "q8-1",
                "question": "Que signifie PLS?",
                "type": "qcm",
                "options": ["Position Latérale Simple", "Position Latérale de Sécurité", "Procédure de Libération Simple", "Protection Latérale Systématique"],
                "correct_answer": 1,
                "explication": "PLS = Position Latérale de Sécurité."
            },
            {
                "id": "q8-2",
                "question": "On peut retirer un casque de moto à une victime traumatisée.",
                "type": "vrai_faux",
                "options": ["Vrai", "Faux"],
                "correct_answer": 1,
                "explication": "Le casque ne doit être retiré que par des secouristes formés, sauf si nécessaire pour assurer la respiration."
            },
            {
                "id": "q8-3",
                "question": "Face à une fracture ouverte, que faire en priorité?",
                "type": "qcm",
                "options": ["Réduire la fracture", "Arrêter l'hémorragie", "Immobiliser", "Désinfecter"],
                "correct_answer": 1,
                "explication": "La priorité est d'arrêter l'hémorragie avant l'immobilisation."
            },
            {
                "id": "q8-4",
                "question": "Une entorse nécessite toujours une immobilisation.",
                "type": "vrai_faux",
                "options": ["Vrai", "Faux"],
                "correct_answer": 0,
                "explication": "Toute entorse doit être immobilisée pour éviter l'aggravation."
            },
            {
                "id": "q8-5",
                "question": "Quelle est la règle du 'PAS BOUGER'?",
                "type": "qcm",
                "options": ["Ne jamais mobiliser", "Mobiliser uniquement si danger", "Mobiliser après bilan", "Attendre les pompiers"],
                "correct_answer": 1,
                "explication": "On ne mobilise une victime traumatisée que si elle est en danger immédiat."
            }
        ]
    },
    {
        "id": "quiz-ch9",
        "chapter_id": "ch9",
        "titre": "Quiz - Souffrance psychique",
        "video_url": None,
        "questions": [
            {
                "id": "q9-1",
                "question": "Quelle est l'attitude à adopter face à une victime en détresse psychologique?",
                "type": "qcm",
                "options": ["Minimiser ses émotions", "Écouter avec empathie", "Isoler la victime", "Ignorer les signes"],
                "correct_answer": 1,
                "explication": "L'écoute active et empathique est essentielle pour accompagner la détresse."
            },
            {
                "id": "q9-2",
                "question": "Une crise d'angoisse peut provoquer des symptômes physiques.",
                "type": "vrai_faux",
                "options": ["Vrai", "Faux"],
                "correct_answer": 0,
                "explication": "La crise d'angoisse peut causer oppression thoracique, palpitations, sueurs, etc."
            },
            {
                "id": "q9-3",
                "question": "Face à une personne suicidaire, que faire?",
                "type": "qcm",
                "options": ["La laisser seule", "Ne pas aborder le sujet", "Écouter et alerter", "Minimiser ses idées"],
                "correct_answer": 2,
                "explication": "Il faut écouter sans jugement et alerter les services compétents."
            },
            {
                "id": "q9-4",
                "question": "Le stress post-traumatique peut survenir immédiatement après l'événement.",
                "type": "vrai_faux",
                "options": ["Vrai", "Faux"],
                "correct_answer": 1,
                "explication": "Le stress post-traumatique apparaît généralement plusieurs jours ou semaines après."
            },
            {
                "id": "q9-5",
                "question": "Quelle est la meilleure façon de communiquer avec une personne agitée?",
                "type": "qcm",
                "options": ["Parler fort", "Rester calme et posé", "S'approcher rapidement", "Menacer"],
                "correct_answer": 1,
                "explication": "Un ton calme, posé et des gestes lents aident à apaiser une personne agitée."
            }
        ]
    },
    {
        "id": "quiz-ch10",
        "chapter_id": "ch10",
        "titre": "Quiz - Relevage et brancardage",
        "video_url": None,
        "questions": [
            {
                "id": "q10-1",
                "question": "Combien de personnes minimum faut-il pour porter un brancard?",
                "type": "qcm",
                "options": ["1 personne", "2 personnes", "3 personnes", "4 personnes"],
                "correct_answer": 3,
                "explication": "Un brancard nécessite au minimum 4 porteurs pour garantir la sécurité."
            },
            {
                "id": "q10-2",
                "question": "Le chef de brancard se place toujours aux pieds de la victime.",
                "type": "vrai_faux",
                "options": ["Vrai", "Faux"],
                "correct_answer": 1,
                "explication": "Le chef de brancard se place à la tête pour surveiller la victime."
            },
            {
                "id": "q10-3",
                "question": "Quelle technique utilise-t-on pour soulever une victime du sol?",
                "type": "qcm",
                "options": ["Le dos rond", "Les bras tendus", "Les jambes pliées", "En se penchant"],
                "correct_answer": 2,
                "explication": "On plie les jambes et garde le dos droit pour préserver son dos."
            },
            {
                "id": "q10-4",
                "question": "On peut brancarder une victime tête en avant dans les escaliers.",
                "type": "vrai_faux",
                "options": ["Vrai", "Faux"],
                "correct_answer": 1,
                "explication": "Dans les escaliers, la victime doit toujours être pieds en avant en descente."
            },
            {
                "id": "q10-5",
                "question": "Quelle est la position d'un brancard pendant le transport?",
                "type": "qcm",
                "options": ["Horizontal toujours", "Tête haute", "Pieds hauts", "Selon la pathologie"],
                "correct_answer": 3,
                "explication": "La position dépend de la pathologie: tête haute pour détresse respiratoire, pieds hauts pour choc..."
            }
        ]
    },
    {
        "id": "quiz-ch11",
        "chapter_id": "ch11",
        "titre": "Quiz - Situations particulières",
        "video_url": None,
        "questions": [
            {
                "id": "q11-1",
                "question": "Quelle est la particularité de la réanimation chez le nourrisson?",
                "type": "qcm",
                "options": ["Pas de RCP", "RCP avec 2 doigts", "Même technique qu'adulte", "Uniquement bouche-à-bouche"],
                "correct_answer": 1,
                "explication": "Chez le nourrisson, on utilise 2 doigts pour les compressions thoraciques."
            },
            {
                "id": "q11-2",
                "question": "Une femme enceinte en détresse doit être installée sur le côté gauche.",
                "type": "vrai_faux",
                "options": ["Vrai", "Faux"],
                "correct_answer": 0,
                "explication": "Le décubitus latéral gauche évite la compression de la veine cave par l'utérus."
            },
            {
                "id": "q11-3",
                "question": "À partir de quel âge utilise-t-on les électrodes adultes du DAE?",
                "type": "qcm",
                "options": ["1 an", "5 ans", "8 ans", "12 ans"],
                "correct_answer": 2,
                "explication": "On utilise les électrodes adultes à partir de 8 ans ou 25 kg."
            },
            {
                "id": "q11-4",
                "question": "La manœuvre de Heimlich est adaptée chez la femme enceinte.",
                "type": "vrai_faux",
                "options": ["Vrai", "Faux"],
                "correct_answer": 1,
                "explication": "Chez la femme enceinte, on pratique des compressions thoraciques à la place."
            },
            {
                "id": "q11-5",
                "question": "Quelle est la fréquence de compressions thoraciques chez l'enfant?",
                "type": "qcm",
                "options": ["60-80/min", "100-120/min", "140-160/min", "180/min"],
                "correct_answer": 1,
                "explication": "La fréquence reste 100-120/min, identique à l'adulte."
            }
        ]
    },
    {
        "id": "quiz-ch12",
        "chapter_id": "ch12",
        "titre": "Quiz - Divers",
        "video_url": None,
        "questions": [
            {
                "id": "q12-1",
                "question": "Quel est le numéro d'appel d'urgence européen?",
                "type": "qcm",
                "options": ["15", "17", "18", "112"],
                "correct_answer": 3,
                "explication": "Le 112 est le numéro d'urgence européen valable dans tous les pays de l'UE."
            },
            {
                "id": "q12-2",
                "question": "Le SAMU correspond au numéro 15.",
                "type": "vrai_faux",
                "options": ["Vrai", "Faux"],
                "correct_answer": 0,
                "explication": "Le 15 est le numéro du SAMU (Service d'Aide Médicale Urgente)."
            },
            {
                "id": "q12-3",
                "question": "Que signifie l'acronyme SMUR?",
                "type": "qcm",
                "options": ["Service Mobile d'Urgence et Réanimation", "Secours Médicaux Urgents Rapides", "Soins Médicaux Urgence Régionale", "Système Médical Unique Régional"],
                "correct_answer": 0,
                "explication": "SMUR = Service Mobile d'Urgence et de Réanimation."
            },
            {
                "id": "q12-4",
                "question": "Un défibrillateur automatisé externe peut être utilisé par toute personne.",
                "type": "vrai_faux",
                "options": ["Vrai", "Faux"],
                "correct_answer": 0,
                "explication": "Le DAE est conçu pour être utilisé par le grand public, sans formation spécifique."
            },
            {
                "id": "q12-5",
                "question": "Quelle information est prioritaire lors d'un appel d'urgence?",
                "type": "qcm",
                "options": ["Nom de la victime", "Localisation précise", "Antécédents médicaux", "Âge exact"],
                "correct_answer": 1,
                "explication": "La localisation précise permet aux secours de se rendre rapidement sur les lieux."
            }
        ]
    }
]

# PSC Quizzes
PSC_QUIZZES = [
    {
        "id": "quiz-psc-ch1",
        "chapter_id": "psc-ch1",
        "titre": "Quiz - Protection et alerte",
        "video_url": None,
        "questions": [
            {
                "id": "qpsc1-1",
                "question": "Avant de porter secours, que faut-il faire en premier?",
                "type": "qcm",
                "options": ["Appeler les secours", "Protéger la zone", "Examiner la victime", "Faire un massage cardiaque"],
                "correct_answer": 1,
                "explication": "La protection est toujours la première étape pour éviter le sur-accident."
            },
            {
                "id": "qpsc1-2",
                "question": "Le numéro 112 fonctionne uniquement en France.",
                "type": "vrai_faux",
                "options": ["Vrai", "Faux"],
                "correct_answer": 1,
                "explication": "Le 112 est le numéro d'urgence européen, valable dans toute l'Union Européenne."
            },
            {
                "id": "qpsc1-3",
                "question": "Que doit-on préciser en priorité lors d'un appel aux secours?",
                "type": "qcm",
                "options": ["Le nom de la victime", "L'adresse exacte", "Son âge", "Ses antécédents"],
                "correct_answer": 1,
                "explication": "L'adresse exacte permet aux secours d'arriver rapidement."
            },
            {
                "id": "qpsc1-4",
                "question": "On peut raccrocher dès que les secours ont compris la situation.",
                "type": "vrai_faux",
                "options": ["Vrai", "Faux"],
                "correct_answer": 1,
                "explication": "On ne raccroche jamais en premier, c'est le régulateur qui met fin à l'appel."
            },
            {
                "id": "qpsc1-5",
                "question": "Dans quelle situation doit-on déplacer une victime?",
                "type": "qcm",
                "options": ["Jamais", "Si danger immédiat", "Pour la mettre en PLS", "Pour la réchauffer"],
                "correct_answer": 1,
                "explication": "On ne déplace une victime qu'en cas de danger vital immédiat (incendie, explosion...)."
            }
        ]
    },
    {
        "id": "quiz-psc-ch2",
        "chapter_id": "psc-ch2",
        "titre": "Quiz - Obstruction des voies aériennes",
        "video_url": None,
        "questions": [
            {
                "id": "qpsc2-1",
                "question": "Quelle est la première technique face à un étouffement total?",
                "type": "qcm",
                "options": ["Claques dans le dos", "Heimlich", "Bouche-à-bouche", "Position allongée"],
                "correct_answer": 0,
                "explication": "On commence par 5 claques vigoureuses dans le dos entre les omoplates."
            },
            {
                "id": "qpsc2-2",
                "question": "Les compressions abdominales sont interdites chez la femme enceinte.",
                "type": "vrai_faux",
                "options": ["Vrai", "Faux"],
                "correct_answer": 0,
                "explication": "Chez la femme enceinte et le nourrisson, on pratique des compressions thoraciques."
            },
            {
                "id": "qpsc2-3",
                "question": "Comment reconnaître une obstruction totale?",
                "type": "qcm",
                "options": ["La victime tousse", "La victime parle", "La victime ne peut plus parler ni tousser", "La victime respire bruyamment"],
                "correct_answer": 2,
                "explication": "L'obstruction totale : impossibilité de parler, tousser ou respirer."
            },
            {
                "id": "qpsc2-4",
                "question": "Si la victime devient inconsciente pendant un étouffement, on commence la RCP.",
                "type": "vrai_faux",
                "options": ["Vrai", "Faux"],
                "correct_answer": 0,
                "explication": "Si perte de conscience, on débute immédiatement la réanimation cardio-pulmonaire."
            },
            {
                "id": "qpsc2-5",
                "question": "Combien de claques dans le dos avant de passer aux compressions abdominales?",
                "type": "qcm",
                "options": ["3", "5", "10", "15"],
                "correct_answer": 1,
                "explication": "On alterne 5 claques dans le dos et 5 compressions abdominales."
            }
        ]
    },
    {
        "id": "quiz-psc-ch3",
        "chapter_id": "psc-ch3",
        "titre": "Quiz - Hémorragies externes",
        "video_url": None,
        "questions": [
            {
                "id": "qpsc3-1",
                "question": "Quelle est la technique de base pour arrêter une hémorragie?",
                "type": "qcm",
                "options": ["Garrot", "Compression directe", "Élévation du membre", "Point de compression"],
                "correct_answer": 1,
                "explication": "La compression directe sur la plaie est la technique de première intention."
            },
            {
                "id": "qpsc3-2",
                "question": "Un garrot peut être desserré pour vérifier l'arrêt du saignement.",
                "type": "vrai_faux",
                "options": ["Vrai", "Faux"],
                "correct_answer": 1,
                "explication": "Un garrot ne doit JAMAIS être desserré une fois mis en place."
            },
            {
                "id": "qpsc3-3",
                "question": "Où place-t-on un garrot?",
                "type": "qcm",
                "options": ["Sur la plaie", "Au-dessus de la plaie", "En-dessous de la plaie", "N'importe où"],
                "correct_answer": 1,
                "explication": "Le garrot se place toujours au-dessus de la plaie, entre le cœur et la blessure."
            },
            {
                "id": "qpsc3-4",
                "question": "Une hémorragie du nez nécessite toujours un appel aux secours.",
                "type": "vrai_faux",
                "options": ["Vrai", "Faux"],
                "correct_answer": 1,
                "explication": "Un saignement de nez simple ne nécessite pas forcément les secours, sauf s'il persiste plus de 10 minutes."
            },
            {
                "id": "qpsc3-5",
                "question": "Quelle position adopter face à un saignement de nez?",
                "type": "qcm",
                "options": ["Tête en arrière", "Allongé", "Tête penchée en avant", "Debout"],
                "correct_answer": 2,
                "explication": "On se penche en avant pour éviter d'avaler le sang et on comprime les narines."
            }
        ]
    },
    {
        "id": "quiz-psc-ch4",
        "chapter_id": "psc-ch4",
        "titre": "Quiz - Perte de connaissance",
        "video_url": None,
        "questions": [
            {
                "id": "qpsc4-1",
                "question": "Comment vérifier si une victime est consciente?",
                "type": "qcm",
                "options": ["La secouer fortement", "Lui parler et la stimuler doucement", "Lui donner une gifle", "Attendre"],
                "correct_answer": 1,
                "explication": "On parle fort et on stimule doucement les épaules pour vérifier la conscience."
            },
            {
                "id": "qpsc4-2",
                "question": "Une victime inconsciente qui respire doit être mise en PLS.",
                "type": "vrai_faux",
                "options": ["Vrai", "Faux"],
                "correct_answer": 0,
                "explication": "La Position Latérale de Sécurité maintient les voies aériennes libres."
            },
            {
                "id": "qpsc4-3",
                "question": "Combien de temps maximum pour vérifier la respiration?",
                "type": "qcm",
                "options": ["5 secondes", "10 secondes", "20 secondes", "1 minute"],
                "correct_answer": 1,
                "explication": "On vérifie la respiration pendant 10 secondes maximum."
            },
            {
                "id": "qpsc4-4",
                "question": "En PLS, la victime est placée sur le côté droit uniquement.",
                "type": "vrai_faux",
                "options": ["Vrai", "Faux"],
                "correct_answer": 1,
                "explication": "On peut placer la victime sur le côté gauche ou droit selon la situation."
            },
            {
                "id": "qpsc4-5",
                "question": "Que faire si la victime vomit en PLS?",
                "type": "qcm",
                "options": ["La remettre sur le dos", "La laisser en PLS", "La redresser", "L'allonger à plat"],
                "correct_answer": 1,
                "explication": "La PLS permet justement l'évacuation des vomissements sans risque d'étouffement."
            }
        ]
    },
    {
        "id": "quiz-psc-ch5",
        "chapter_id": "psc-ch5",
        "titre": "Quiz - Arrêt cardiaque et défibrillateur",
        "video_url": None,
        "questions": [
            {
                "id": "qpsc5-1",
                "question": "Comment reconnaître un arrêt cardiaque?",
                "type": "qcm",
                "options": ["Victime qui crie", "Victime inconsciente qui ne respire pas", "Victime qui tousse", "Victime qui saigne"],
                "correct_answer": 1,
                "explication": "L'arrêt cardiaque : victime inconsciente + absence de respiration normale."
            },
            {
                "id": "qpsc5-2",
                "question": "On commence toujours par 5 insufflations avant les compressions.",
                "type": "vrai_faux",
                "options": ["Vrai", "Faux"],
                "correct_answer": 1,
                "explication": "Chez l'adulte, on commence immédiatement par 30 compressions thoraciques."
            },
            {
                "id": "qpsc5-3",
                "question": "Quelle est la fréquence des compressions thoraciques?",
                "type": "qcm",
                "options": ["60/min", "100-120/min", "150/min", "200/min"],
                "correct_answer": 1,
                "explication": "La fréquence recommandée est de 100 à 120 compressions par minute."
            },
            {
                "id": "qpsc5-4",
                "question": "On peut utiliser un défibrillateur sans formation.",
                "type": "vrai_faux",
                "options": ["Vrai", "Faux"],
                "correct_answer": 0,
                "explication": "Le DAE guide l'utilisateur par messages vocaux, aucune formation obligatoire."
            },
            {
                "id": "qpsc5-5",
                "question": "Quel est le rapport compressions/insufflations?",
                "type": "qcm",
                "options": ["15/2", "30/2", "20/2", "25/2"],
                "correct_answer": 1,
                "explication": "Le rapport est de 30 compressions pour 2 insufflations."
            }
        ]
    },
    {
        "id": "quiz-psc-ch6",
        "chapter_id": "psc-ch6",
        "titre": "Quiz - Malaises",
        "video_url": None,
        "questions": [
            {
                "id": "qpsc6-1",
                "question": "Quelle position pour une victime consciente en malaise?",
                "type": "qcm",
                "options": ["Allongée sur le dos", "Position demi-assise", "Debout", "À genoux"],
                "correct_answer": 1,
                "explication": "La position demi-assise permet à la victime de respirer confortablement."
            },
            {
                "id": "qpsc6-2",
                "question": "On peut donner à boire à une victime en malaise.",
                "type": "vrai_faux",
                "options": ["Vrai", "Faux"],
                "correct_answer": 1,
                "explication": "On ne donne rien à boire ni à manger en attendant les secours."
            },
            {
                "id": "qpsc6-3",
                "question": "Quels signes caractérisent un malaise cardiaque?",
                "type": "qcm",
                "options": ["Maux de tête", "Douleur thoracique intense", "Fièvre", "Éternuements"],
                "correct_answer": 1,
                "explication": "La douleur thoracique intense, en étau, est typique de l'infarctus."
            },
            {
                "id": "qpsc6-4",
                "question": "Un diabétique peut avoir un malaise par excès de sucre uniquement.",
                "type": "vrai_faux",
                "options": ["Vrai", "Faux"],
                "correct_answer": 1,
                "explication": "Le malaise diabétique peut être dû à l'hypoglycémie (manque) ou hyperglycémie (excès)."
            },
            {
                "id": "qpsc6-5",
                "question": "Face à un malaise, que faire en priorité?",
                "type": "qcm",
                "options": ["Donner des médicaments", "Mettre au repos et alerter", "Faire marcher", "Donner de l'eau"],
                "correct_answer": 1,
                "explication": "On met la victime au repos, on alerte et on surveille en attendant les secours."
            }
        ]
    },
    {
        "id": "quiz-psc-ch7",
        "chapter_id": "psc-ch7",
        "titre": "Quiz - Plaies et traumatismes",
        "video_url": None,
        "questions": [
            {
                "id": "qpsc7-1",
                "question": "Comment protéger une plaie simple?",
                "type": "qcm",
                "options": ["La nettoyer avec de l'alcool", "La rincer à l'eau et savon puis couvrir", "Ne rien faire", "Mettre du coton"],
                "correct_answer": 1,
                "explication": "On nettoie à l'eau et au savon puis on couvre avec un pansement propre."
            },
            {
                "id": "qpsc7-2",
                "question": "On doit retirer un objet fiché dans une plaie.",
                "type": "vrai_faux",
                "options": ["Vrai", "Faux"],
                "correct_answer": 1,
                "explication": "On ne retire JAMAIS un objet fiché, il limite le saignement."
            },
            {
                "id": "qpsc7-3",
                "question": "Face à une brûlure, quelle est la première action?",
                "type": "qcm",
                "options": ["Mettre de la glace", "Arroser d'eau froide 5 minutes", "Percer les cloques", "Mettre du beurre"],
                "correct_answer": 1,
                "explication": "On arrose à l'eau froide (15-25°C) pendant au moins 5 minutes."
            },
            {
                "id": "qpsc7-4",
                "question": "Une fracture fermée ne nécessite pas d'immobilisation.",
                "type": "vrai_faux",
                "options": ["Vrai", "Faux"],
                "correct_answer": 1,
                "explication": "Toute suspicion de fracture doit être immobilisée."
            },
            {
                "id": "qpsc7-5",
                "question": "Comment immobiliser un membre traumatisé?",
                "type": "qcm",
                "options": ["Dans la position trouvée", "En le redressant", "En le pliant", "N'importe comment"],
                "correct_answer": 0,
                "explication": "On immobilise toujours dans la position trouvée, sans bouger le membre."
            }
        ]
    },
    {
        "id": "quiz-psc-ch8",
        "chapter_id": "psc-ch8",
        "titre": "Quiz - Brûlures",
        "video_url": None,
        "questions": [
            {
                "id": "qpsc8-1",
                "question": "Quelle est la première action face à une brûlure thermique?",
                "type": "qcm",
                "options": ["Percer les cloques", "Arroser d'eau froide", "Mettre de la glace", "Appliquer une crème"],
                "correct_answer": 1,
                "explication": "On refroidit immédiatement à l'eau froide (15-25°C) pendant au moins 5 minutes."
            },
            {
                "id": "qpsc8-2",
                "question": "On peut mettre de la glace directement sur une brûlure.",
                "type": "vrai_faux",
                "options": ["Vrai", "Faux"],
                "correct_answer": 1,
                "explication": "La glace aggrave les lésions. On utilise de l'eau froide mais pas glacée."
            },
            {
                "id": "qpsc8-3",
                "question": "Que faire face à une brûlure chimique?",
                "type": "qcm",
                "options": ["Attendre", "Rincer abondamment à l'eau", "Mettre un pansement", "Frotter"],
                "correct_answer": 1,
                "explication": "On rince abondamment à l'eau pendant au moins 20 minutes après avoir retiré les vêtements."
            },
            {
                "id": "qpsc8-4",
                "question": "Les cloques d'une brûlure doivent être percées.",
                "type": "vrai_faux",
                "options": ["Vrai", "Faux"],
                "correct_answer": 1,
                "explication": "On ne perce JAMAIS les cloques, elles protègent contre l'infection."
            },
            {
                "id": "qpsc8-5",
                "question": "Une brûlure grave nécessite:",
                "type": "qcm",
                "options": ["Un pansement sec", "Eau froide puis pansement stérile", "Crème grasse", "Rien"],
                "correct_answer": 1,
                "explication": "On refroidit, puis on couvre avec un pansement stérile et on alerte."
            }
        ]
    },
    {
        "id": "quiz-bnssa-1",
        "chapter_id": "bnssa-1",
        "titre": "Quiz - BNSSA Introduction",
        "video_url": None,
        "questions": [
            {
                "id": "qbnssa1-1",
                "question": "Que signifie BNSSA?",
                "type": "qcm",
                "options": ["Brevet National de Sauvetage Sportif Aquatique", "Brevet National de Secourisme Sauvetage Aquatique", "Brevet National de Surveillant de Sécurité Aquatique", "Brevet National de Sauvetage et Secours Aquatique"],
                "correct_answer": 3,
                "explication": "BNSSA = Brevet National de Sauvetage et de Secourisme Aquatique."
            },
            {
                "id": "qbnssa1-2",
                "question": "Le BNSSA permet de surveiller seul une piscine publique.",
                "type": "vrai_faux",
                "options": ["Vrai", "Faux"],
                "correct_answer": 1,
                "explication": "Le BNSSA ne permet pas la surveillance seule, il faut être titulaire du BEESAN."
            },
            {
                "id": "qbnssa1-3",
                "question": "Quelle est la durée de validité du BNSSA?",
                "type": "qcm",
                "options": ["1 an", "3 ans", "5 ans", "10 ans"],
                "correct_answer": 2,
                "explication": "Le BNSSA est valable 5 ans et nécessite un recyclage continu."
            },
            {
                "id": "qbnssa1-4",
                "question": "Le BNSSA inclut une formation aux premiers secours.",
                "type": "vrai_faux",
                "options": ["Vrai", "Faux"],
                "correct_answer": 0,
                "explication": "Le BNSSA comprend le PSE1 (Premiers Secours en Équipe niveau 1)."
            },
            {
                "id": "qbnssa1-5",
                "question": "À partir de quel âge peut-on passer le BNSSA?",
                "type": "qcm",
                "options": ["16 ans", "17 ans", "18 ans", "21 ans"],
                "correct_answer": 1,
                "explication": "Le BNSSA peut être passé à partir de 17 ans."
            }
        ]
    }
]

async def main():
    client = AsyncIOMotorClient(os.environ.get('MONGO_URL'))
    db = client[os.environ.get('DB_NAME', 'secours73')]
    
    all_quizzes = MISSING_QUIZZES + PSC_QUIZZES
    
    print(f"Création de {len(all_quizzes)} quiz...")
    
    for quiz in all_quizzes:
        await db.quizzes.insert_one(quiz)
        print(f"✅ Créé: {quiz['titre']}")
    
    print(f"\n✅ {len(all_quizzes)} quiz créés avec succès!")
    
    # Vérifier le total
    total = await db.quizzes.count_documents({})
    print(f"\n📊 Total quiz en base: {total}")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(main())
