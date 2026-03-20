#!/usr/bin/env python3
"""
Création des quiz PSE chapitres 7 à 12
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

print("📝 Création des quiz PSE 7-12...")

quizzes = [
    {
        "id": str(uuid4()),
        "chapter_id": "pse-ch7",
        "titre": "Quiz - Traumatismes",
        "formation_type": "PSE",
        "questions": [
            {
                "id": str(uuid4()),
                "question": "Quel est le principe de base face à un traumatisme ?",
                "options": [
                    "Mobiliser pour examiner",
                    "Ne pas mobiliser",
                    "Remettre en place",
                    "Faire marcher la victime"
                ],
                "correct_answer": 1
            },
            {
                "id": str(uuid4()),
                "question": "Comment immobilise-t-on un membre traumatisé ?",
                "options": [
                    "En le redressant",
                    "Dans la position où il se trouve",
                    "En le pliant à 90°",
                    "En l'étirant"
                ],
                "correct_answer": 1
            },
            {
                "id": str(uuid4()),
                "question": "Que faire face à un traumatisme du rachis ?",
                "options": [
                    "Mobiliser doucement",
                    "Ne pas mobiliser et maintenir la tête",
                    "Mettre en PLS",
                    "Faire asseoir la victime"
                ],
                "correct_answer": 1
            },
            {
                "id": str(uuid4()),
                "question": "Qu'est-ce qu'une fracture ouverte ?",
                "options": [
                    "Une fracture visible à la radio",
                    "Une fracture avec plaie en regard",
                    "Une fracture multiple",
                    "Une fracture ancienne"
                ],
                "correct_answer": 1
            },
            {
                "id": str(uuid4()),
                "question": "Que faire en cas de suspicion de traumatisme crânien ?",
                "options": [
                    "Donner à boire",
                    "Alerter le 15 et surveiller la conscience",
                    "Faire vomir",
                    "Mettre de la glace sur la tête"
                ],
                "correct_answer": 1
            }
        ]
    },
    {
        "id": str(uuid4()),
        "chapter_id": "pse-ch8",
        "titre": "Quiz - Plaies et brûlures",
        "formation_type": "PSE",
        "questions": [
            {
                "id": str(uuid4()),
                "question": "Qu'est-ce qu'une plaie grave ?",
                "options": [
                    "Toute plaie qui saigne",
                    "Une plaie étendue, profonde ou sur zone à risque",
                    "Une plaie qui fait mal",
                    "Une plaie ancienne"
                ],
                "correct_answer": 1
            },
            {
                "id": str(uuid4()),
                "question": "Combien de temps doit-on refroidir une brûlure ?",
                "options": [
                    "1 minute",
                    "5 minutes minimum",
                    "10 secondes",
                    "30 minutes"
                ],
                "correct_answer": 1
            },
            {
                "id": str(uuid4()),
                "question": "Que faire face à une brûlure chimique ?",
                "options": [
                    "Mettre de la pommade",
                    "Arroser abondamment à l'eau 20 minutes",
                    "Sécher avec un linge",
                    "Ne rien faire"
                ],
                "correct_answer": 1
            },
            {
                "id": str(uuid4()),
                "question": "Comment reconnaît-on une brûlure du 3ᵉ degré ?",
                "options": [
                    "Rougeur et douleur intense",
                    "Cloques",
                    "Peau blanche ou noire, peu de douleur",
                    "Légère rougeur"
                ],
                "correct_answer": 2
            },
            {
                "id": str(uuid4()),
                "question": "Que ne doit-on JAMAIS faire sur une brûlure ?",
                "options": [
                    "Refroidir à l'eau",
                    "Percer les cloques ou mettre du beurre",
                    "Protéger avec un linge propre",
                    "Alerter les secours"
                ],
                "correct_answer": 1
            }
        ]
    },
    {
        "id": str(uuid4()),
        "chapter_id": "pse-ch9",
        "titre": "Quiz - Arrêt cardiaque et défibrillation",
        "formation_type": "PSE",
        "questions": [
            {
                "id": str(uuid4()),
                "question": "Quels sont les deux signes d'un arrêt cardiaque ?",
                "options": [
                    "Douleur thoracique et sueurs",
                    "Inconscience et absence de respiration",
                    "Pâleur et pouls rapide",
                    "Fièvre et confusion"
                ],
                "correct_answer": 1
            },
            {
                "id": str(uuid4()),
                "question": "Quelle est la séquence de RCP adulte ?",
                "options": [
                    "15 compressions / 2 insufflations",
                    "30 compressions / 2 insufflations",
                    "100 compressions / 5 insufflations",
                    "5 compressions / 1 insufflation"
                ],
                "correct_answer": 1
            },
            {
                "id": str(uuid4()),
                "question": "À quelle profondeur doit-on comprimer le thorax d'un adulte ?",
                "options": [
                    "1 à 2 cm",
                    "3 à 4 cm",
                    "5 à 6 cm",
                    "10 cm"
                ],
                "correct_answer": 2
            },
            {
                "id": str(uuid4()),
                "question": "Que doit-on faire dès l'arrivée du DAE ?",
                "options": [
                    "Arrêter la RCP et attendre",
                    "Mettre en marche, coller les électrodes et suivre les instructions",
                    "Continuer la RCP sans utiliser le DAE",
                    "Éteindre le DAE après le choc"
                ],
                "correct_answer": 1
            },
            {
                "id": str(uuid4()),
                "question": "Quand doit-on reprendre la RCP après un choc du DAE ?",
                "options": [
                    "Attendre 5 minutes",
                    "Immédiatement",
                    "Seulement si le DAE le demande",
                    "Jamais"
                ],
                "correct_answer": 1
            }
        ]
    },
    {
        "id": str(uuid4()),
        "chapter_id": "pse-ch10",
        "titre": "Quiz - Oxygénothérapie",
        "formation_type": "PSE",
        "questions": [
            {
                "id": str(uuid4()),
                "question": "Quel est le débit d'oxygène pour l'inhalation ?",
                "options": [
                    "1 à 3 L/min",
                    "3 à 15 L/min",
                    "20 à 25 L/min",
                    "30 L/min"
                ],
                "correct_answer": 1
            },
            {
                "id": str(uuid4()),
                "question": "Quel dispositif utilise-t-on pour l'insufflation en ventilation artificielle ?",
                "options": [
                    "Masque haute concentration",
                    "Lunettes à oxygène",
                    "Ballon auto-remplisseur à valve unidirectionnelle (BAVU)",
                    "Inhalateur"
                ],
                "correct_answer": 2
            },
            {
                "id": str(uuid4()),
                "question": "Quelle précaution prendre avec une bouteille d'oxygène ?",
                "options": [
                    "La coucher au sol",
                    "L'éloigner de toute source de chaleur et ne pas fumer",
                    "La secouer avant utilisation",
                    "L'ouvrir complètement"
                ],
                "correct_answer": 1
            },
            {
                "id": str(uuid4()),
                "question": "Quand utilise-t-on l'oxygénothérapie ?",
                "options": [
                    "Uniquement en cas d'arrêt cardiaque",
                    "Pour toute détresse respiratoire ou circulatoire",
                    "Jamais",
                    "Seulement sur prescription médicale"
                ],
                "correct_answer": 1
            }
        ]
    },
    {
        "id": str(uuid4()),
        "chapter_id": "pse-ch11",
        "titre": "Quiz - Relevage et brancardage",
        "formation_type": "PSE",
        "questions": [
            {
                "id": str(uuid4()),
                "question": "Combien de secouristes minimum pour porter un brancard ?",
                "options": [
                    "1",
                    "2",
                    "3",
                    "4"
                ],
                "correct_answer": 2
            },
            {
                "id": str(uuid4()),
                "question": "Quel est le principe de base du relevage ?",
                "options": [
                    "Aller vite",
                    "Coordination et communication",
                    "Porter seul si possible",
                    "Tirer la victime"
                ],
                "correct_answer": 1
            },
            {
                "id": str(uuid4()),
                "question": "Quelle technique utiliser pour relever une victime suspecte de traumatisme du rachis ?",
                "options": [
                    "La pont néerlandais",
                    "Relevage à 2 secouristes",
                    "Plan dur avec maintien de l'axe tête-cou-tronc",
                    "Position assise"
                ],
                "correct_answer": 2
            },
            {
                "id": str(uuid4()),
                "question": "Dans quel sens doit-on porter un brancard dans un escalier en montant ?",
                "options": [
                    "Tête en haut",
                    "Pieds en haut",
                    "Sur le côté",
                    "Peu importe"
                ],
                "correct_answer": 0
            },
            {
                "id": str(uuid4()),
                "question": "Que doit-on vérifier avant de soulever un brancard ?",
                "options": [
                    "Que la victime soit attachée et que tous soient prêts",
                    "Rien",
                    "Seulement le poids",
                    "La météo"
                ],
                "correct_answer": 0
            }
        ]
    },
    {
        "id": str(uuid4()),
        "chapter_id": "pse-ch12",
        "titre": "Quiz - Situations particulières",
        "formation_type": "PSE",
        "questions": [
            {
                "id": str(uuid4()),
                "question": "Comment aborder une victime agitée ou agressive ?",
                "options": [
                    "La maîtriser de force",
                    "Rester calme, à distance de sécurité, parler doucement",
                    "L'ignorer",
                    "Appeler la police uniquement"
                ],
                "correct_answer": 1
            },
            {
                "id": str(uuid4()),
                "question": "Que faire face à une victime qui refuse les soins ?",
                "options": [
                    "Forcer les soins",
                    "Respecter son choix si elle est consciente et lucide, mais alerter si danger vital",
                    "Partir immédiatement",
                    "Appeler la police"
                ],
                "correct_answer": 1
            },
            {
                "id": str(uuid4()),
                "question": "Quelle position pour une femme enceinte en détresse ?",
                "options": [
                    "Sur le dos strictement",
                    "Sur le côté gauche de préférence",
                    "Sur le ventre",
                    "Debout"
                ],
                "correct_answer": 1
            },
            {
                "id": str(uuid4()),
                "question": "Comment adapter la RCP chez un nourrisson ?",
                "options": [
                    "Avec 2 mains",
                    "Avec 2 doigts et bouche à bouche-nez",
                    "Pas de RCP possible",
                    "Uniquement des insufflations"
                ],
                "correct_answer": 1
            },
            {
                "id": str(uuid4()),
                "question": "Que faire en cas d'accouchement inopiné ?",
                "options": [
                    "Paniquer",
                    "Rester calme, alerter le 15, accompagner l'accouchement, réchauffer le bébé",
                    "Transporter immédiatement",
                    "Empêcher l'accouchement"
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

print(f"\n🎉 Quiz PSE 7-12 créés")
print(f"📊 Total quiz: {db.quizzes.count_documents({})}")

client.close()
