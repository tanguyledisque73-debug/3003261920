#!/usr/bin/env python3
"""
Création des quiz PSE chapitres 1 à 6
4-5 questions par chapitre
"""
from pymongo import MongoClient
import os
from dotenv import load_dotenv
from pathlib import Path
from uuid import uuid4

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / 'backend' / '.env')

mongo_url = os.environ['MONGO_URL']
client = MongoClient(mongo_url)
db = client[os.environ['DB_NAME']]

print("📝 Création des quiz PSE 1-6...")

quizzes = [
    {
        "id": str(uuid4()),
        "chapter_id": "pse-ch1",
        "titre": "Quiz - Rôles et responsabilités du secouriste",
        "formation_type": "PSE",
        "questions": [
            {
                "id": str(uuid4()),
                "question": "Quel est le rôle principal d'un équipier secouriste PSE ?",
                "options": [
                    "Remplacer les médecins",
                    "Assurer les premiers secours en équipe",
                    "Transporter uniquement les blessés",
                    "Faire des diagnostics médicaux"
                ],
                "correct_answer": 1
            },
            {
                "id": str(uuid4()),
                "question": "Que signifie le principe PAS ?",
                "options": [
                    "Prévenir, Alerter, Soigner",
                    "Protéger, Alerter, Secourir",
                    "Protéger, Animer, Surveiller",
                    "Prévenir, Annoncer, Sauver"
                ],
                "correct_answer": 1
            },
            {
                "id": str(uuid4()),
                "question": "Quelle est la première action à effectuer sur une intervention ?",
                "options": [
                    "Examiner la victime",
                    "Alerter les secours",
                    "Protéger la zone",
                    "Faire un massage cardiaque"
                ],
                "correct_answer": 2
            },
            {
                "id": str(uuid4()),
                "question": "Un secouriste peut-il être poursuivi s'il commet une erreur en portant secours ?",
                "options": [
                    "Oui, toujours",
                    "Non, jamais",
                    "Oui, uniquement en cas de faute grave ou intentionnelle",
                    "Seulement s'il n'est pas diplômé"
                ],
                "correct_answer": 2
            },
            {
                "id": str(uuid4()),
                "question": "Que doit faire un secouriste face à une situation qui dépasse ses compétences ?",
                "options": [
                    "Improviser une solution",
                    "Ne rien faire",
                    "Alerter et demander un renfort médical",
                    "Transporter immédiatement la victime"
                ],
                "correct_answer": 2
            }
        ]
    },
    {
        "id": str(uuid4()),
        "chapter_id": "pse-ch2",
        "titre": "Quiz - Hygiène et asepsie",
        "formation_type": "PSE",
        "questions": [
            {
                "id": str(uuid4()),
                "question": "Quelle est la méthode la plus efficace pour se laver les mains ?",
                "options": [
                    "Rinçage rapide à l'eau",
                    "Friction avec solution hydro-alcoolique",
                    "Essuyage avec un mouchoir",
                    "Trempage dans l'eau"
                ],
                "correct_answer": 1
            },
            {
                "id": str(uuid4()),
                "question": "Quand doit-on porter des gants ?",
                "options": [
                    "Uniquement en hiver",
                    "Seulement en cas d'hémorragie",
                    "Lors de tout contact avec du sang ou des liquides biologiques",
                    "Jamais, c'est inutile"
                ],
                "correct_answer": 2
            },
            {
                "id": str(uuid4()),
                "question": "Que signifie DASRI ?",
                "options": [
                    "Déchet À Sortir Rapidement Ici",
                    "Déchets d'Activités de Soins à Risques Infectieux",
                    "Danger Sanitaire Risque Immédiat",
                    "Dispositif d'Alerte Sanitaire et de Récupération d'Instruments"
                ],
                "correct_answer": 1
            },
            {
                "id": str(uuid4()),
                "question": "Comment éliminer une aiguille usagée ?",
                "options": [
                    "La jeter à la poubelle normale",
                    "La mettre dans un collecteur DASRI",
                    "La recapuchonner puis la jeter",
                    "La donner à la victime"
                ],
                "correct_answer": 1
            }
        ]
    },
    {
        "id": str(uuid4()),
        "chapter_id": "pse-ch3",
        "titre": "Quiz - Bilan et surveillance",
        "formation_type": "PSE",
        "questions": [
            {
                "id": str(uuid4()),
                "question": "Que signifie le bilan circonstanciel ?",
                "options": [
                    "L'état de santé de la victime",
                    "Les circonstances de l'accident",
                    "Les antécédents médicaux",
                    "Les constantes vitales"
                ],
                "correct_answer": 1
            },
            {
                "id": str(uuid4()),
                "question": "Quelle est la fréquence respiratoire normale d'un adulte au repos ?",
                "options": [
                    "5 à 10 par minute",
                    "12 à 20 par minute",
                    "25 à 35 par minute",
                    "40 à 50 par minute"
                ],
                "correct_answer": 1
            },
            {
                "id": str(uuid4()),
                "question": "Comment mesure-t-on le pouls radial ?",
                "options": [
                    "Au niveau du cou",
                    "Au niveau du poignet",
                    "Au niveau de la cheville",
                    "Au niveau du coude"
                ],
                "correct_answer": 1
            },
            {
                "id": str(uuid4()),
                "question": "Que signifie SAMPLE dans le bilan complémentaire ?",
                "options": [
                    "Un échantillon de sang",
                    "Symptômes, Allergies, Médicaments, Passé, Last meal, Événement",
                    "Un protocole de secours",
                    "Un type de traumatisme"
                ],
                "correct_answer": 1
            },
            {
                "id": str(uuid4()),
                "question": "À quelle fréquence doit-on surveiller une victime ?",
                "options": [
                    "Une seule fois au début",
                    "Toutes les heures",
                    "Régulièrement jusqu'à l'arrivée des secours",
                    "Uniquement si elle se plaint"
                ],
                "correct_answer": 2
            }
        ]
    },
    {
        "id": str(uuid4()),
        "chapter_id": "pse-ch4",
        "titre": "Quiz - Obstruction des voies aériennes",
        "formation_type": "PSE",
        "questions": [
            {
                "id": str(uuid4()),
                "question": "Comment reconnaît-on une obstruction totale ?",
                "options": [
                    "La victime tousse fort",
                    "La victime ne peut plus parler ni tousser",
                    "La victime respire bruyamment",
                    "La victime parle difficilement"
                ],
                "correct_answer": 1
            },
            {
                "id": str(uuid4()),
                "question": "Que faire en cas d'obstruction partielle ?",
                "options": [
                    "Donner des claques dans le dos",
                    "Faire des compressions abdominales",
                    "Encourager à tousser",
                    "Mettre en PLS"
                ],
                "correct_answer": 2
            },
            {
                "id": str(uuid4()),
                "question": "Combien de claques dans le dos avant les compressions abdominales ?",
                "options": [
                    "3 claques",
                    "5 claques",
                    "10 claques",
                    "Jusqu'à expulsion"
                ],
                "correct_answer": 1
            },
            {
                "id": str(uuid4()),
                "question": "Où se place le poing pour la manœuvre de Heimlich ?",
                "options": [
                    "Sur le sternum",
                    "Entre le nombril et le sternum",
                    "Sur les côtes",
                    "Dans le dos"
                ],
                "correct_answer": 1
            },
            {
                "id": str(uuid4()),
                "question": "Que faire si la victime perd connaissance pendant la désobstruction ?",
                "options": [
                    "Continuer les claques dans le dos",
                    "Débuter la RCP",
                    "La mettre en PLS",
                    "Attendre qu'elle se réveille"
                ],
                "correct_answer": 1
            }
        ]
    },
    {
        "id": str(uuid4()),
        "chapter_id": "pse-ch5",
        "titre": "Quiz - Hémorragies",
        "formation_type": "PSE",
        "questions": [
            {
                "id": str(uuid4()),
                "question": "Quelle est la première action face à une hémorragie externe ?",
                "options": [
                    "Alerter les secours",
                    "Compression directe",
                    "Allonger la victime",
                    "Donner à boire"
                ],
                "correct_answer": 1
            },
            {
                "id": str(uuid4()),
                "question": "Combien de temps doit-on maintenir une compression manuelle ?",
                "options": [
                    "2 minutes",
                    "5 minutes",
                    "Jusqu'à l'arrivée des secours",
                    "Jusqu'à ce que ça arrête de saigner puis relâcher"
                ],
                "correct_answer": 2
            },
            {
                "id": str(uuid4()),
                "question": "Que faire si un corps étranger est enfoncé dans une plaie qui saigne ?",
                "options": [
                    "Retirer l'objet immédiatement",
                    "Comprimer de chaque côté sans retirer l'objet",
                    "Tirer doucement sur l'objet",
                    "Ne rien faire"
                ],
                "correct_answer": 1
            },
            {
                "id": str(uuid4()),
                "question": "Quels sont les signes d'un état de choc hémorragique ?",
                "options": [
                    "Rougeur et chaleur",
                    "Pâleur, sueurs froides, pouls rapide",
                    "Fièvre et maux de tête",
                    "Respiration lente"
                ],
                "correct_answer": 1
            },
            {
                "id": str(uuid4()),
                "question": "Quand utilise-t-on un garrot tourniquet ?",
                "options": [
                    "Dès qu'il y a un saignement",
                    "Uniquement en dernier recours si compression impossible",
                    "Toujours en premier",
                    "Jamais"
                ],
                "correct_answer": 1
            }
        ]
    },
    {
        "id": str(uuid4()),
        "chapter_id": "pse-ch6",
        "titre": "Quiz - Inconscience et PLS",
        "formation_type": "PSE",
        "questions": [
            {
                "id": str(uuid4()),
                "question": "Quels sont les deux critères pour définir l'inconscience ?",
                "options": [
                    "Ne parle pas et ne bouge pas",
                    "Ne répond pas et respire",
                    "Ne répond pas et ne réagit pas",
                    "Yeux fermés et respiration lente"
                ],
                "correct_answer": 2
            },
            {
                "id": str(uuid4()),
                "question": "Pourquoi met-on une victime inconsciente en PLS ?",
                "options": [
                    "Pour la réchauffer",
                    "Pour libérer les voies aériennes",
                    "Pour faciliter le transport",
                    "Pour la réveiller"
                ],
                "correct_answer": 1
            },
            {
                "id": str(uuid4()),
                "question": "À quelle fréquence doit-on surveiller la respiration d'une victime en PLS ?",
                "options": [
                    "Une seule fois",
                    "Toutes les 10 minutes",
                    "Toutes les minutes",
                    "Uniquement si elle bouge"
                ],
                "correct_answer": 2
            },
            {
                "id": str(uuid4()),
                "question": "Que faire si une victime en PLS arrête de respirer ?",
                "options": [
                    "Appeler les secours",
                    "La secouer pour la réveiller",
                    "La remettre sur le dos et débuter la RCP",
                    "Attendre qu'elle reprenne d'elle-même"
                ],
                "correct_answer": 2
            },
            {
                "id": str(uuid4()),
                "question": "Quelle est la position de la bouche en PLS ?",
                "options": [
                    "Fermée",
                    "Ouverte vers le sol",
                    "Ouverte vers le ciel",
                    "Peu importe"
                ],
                "correct_answer": 1
            }
        ]
    }
]

# Insertion des quiz
for quiz in quizzes:
    db.quizzes.insert_one(quiz)
    chapter = db.chapters.find_one({"id": quiz["chapter_id"]}, {"_id": 0})
    print(f"  ✅ Quiz créé pour Ch{chapter['numero']}: {chapter['titre']} ({len(quiz['questions'])} questions)")

print(f"\n🎉 Quiz PSE 1-6 créés")
print(f"📊 Total quiz: {db.quizzes.count_documents({})}")

client.close()
