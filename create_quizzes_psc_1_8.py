#!/usr/bin/env python3
"""
Création des quiz PSC chapitres 1 à 8
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

print("📝 Création des quiz PSC 1-8...")

quizzes = [
    {
        "id": str(uuid4()),
        "chapter_id": "psc-ch1",
        "titre": "Quiz - Protection et alerte",
        "formation_type": "PSC",
        "questions": [
            {
                "id": str(uuid4()),
                "question": "Quelle est la première action en secourisme ?",
                "options": [
                    "Examiner la victime",
                    "Protéger",
                    "Alerter",
                    "Secourir"
                ],
                "correct_answer": 1
            },
            {
                "id": str(uuid4()),
                "question": "À quelle distance doit-on placer le triangle de signalisation sur autoroute ?",
                "options": [
                    "30 mètres",
                    "100 mètres",
                    "200 mètres",
                    "500 mètres"
                ],
                "correct_answer": 2
            },
            {
                "id": str(uuid4()),
                "question": "Quel numéro appeler pour le SAMU ?",
                "options": [
                    "17",
                    "18",
                    "15",
                    "112"
                ],
                "correct_answer": 2
            },
            {
                "id": str(uuid4()),
                "question": "Que signifie VOS dans l'examen de la victime ?",
                "options": [
                    "Vérifier, Observer, Signaler",
                    "Voir, Ouïr, Sentir",
                    "Ventiler, Oxygéner, Surveiller",
                    "Vitesse, Orientation, Santé"
                ],
                "correct_answer": 1
            },
            {
                "id": str(uuid4()),
                "question": "Doit-on raccrocher en premier lors d'un appel d'urgence ?",
                "options": [
                    "Oui, dès qu'on a donné l'adresse",
                    "Non, attendre que le régulateur le dise",
                    "Peu importe",
                    "Oui, après 2 minutes"
                ],
                "correct_answer": 1
            }
        ]
    },
    {
        "id": str(uuid4()),
        "chapter_id": "psc-ch2",
        "titre": "Quiz - Obstruction des voies aériennes",
        "formation_type": "PSC",
        "questions": [
            {
                "id": str(uuid4()),
                "question": "Quel est le signe d'une obstruction totale ?",
                "options": [
                    "La personne tousse fort",
                    "La personne ne peut plus parler ni tousser",
                    "La personne parle difficilement",
                    "La personne respire bruyamment"
                ],
                "correct_answer": 1
            },
            {
                "id": str(uuid4()),
                "question": "Que faire en cas d'obstruction partielle ?",
                "options": [
                    "Claques dans le dos",
                    "Compressions abdominales",
                    "Encourager à tousser",
                    "Mettre en PLS"
                ],
                "correct_answer": 2
            },
            {
                "id": str(uuid4()),
                "question": "Où place-t-on le poing pour la manœuvre de Heimlich ?",
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
                "question": "Combien de claques dans le dos avant de passer aux compressions ?",
                "options": [
                    "3",
                    "5",
                    "10",
                    "15"
                ],
                "correct_answer": 1
            },
            {
                "id": str(uuid4()),
                "question": "Que faire chez un nourrisson qui s'étouffe ?",
                "options": [
                    "Compressions abdominales",
                    "Claques dans le dos et compressions thoraciques",
                    "Le secouer",
                    "Le mettre tête en bas"
                ],
                "correct_answer": 1
            }
        ]
    },
    {
        "id": str(uuid4()),
        "chapter_id": "psc-ch3",
        "titre": "Quiz - Hémorragies externes",
        "formation_type": "PSC",
        "questions": [
            {
                "id": str(uuid4()),
                "question": "Que faire en priorité face à une hémorragie ?",
                "options": [
                    "Alerter le 15",
                    "Compression directe immédiate",
                    "Allonger la victime",
                    "Chercher des gants"
                ],
                "correct_answer": 1
            },
            {
                "id": str(uuid4()),
                "question": "Combien de temps maintenir la compression ?",
                "options": [
                    "2 minutes",
                    "5 minutes",
                    "Jusqu'à l'arrivée des secours sans relâcher",
                    "Jusqu'à ce que ça arrête puis relâcher"
                ],
                "correct_answer": 2
            },
            {
                "id": str(uuid4()),
                "question": "Que faire si un objet est enfoncé dans la plaie ?",
                "options": [
                    "Le retirer immédiatement",
                    "Comprimer de chaque côté sans le retirer",
                    "Le pousser plus profond",
                    "Tirer doucement"
                ],
                "correct_answer": 1
            },
            {
                "id": str(uuid4()),
                "question": "Quels sont les signes du choc hémorragique ?",
                "options": [
                    "Fièvre et maux de tête",
                    "Pâleur, sueurs froides, pouls rapide",
                    "Rougeur et chaleur",
                    "Somnolence"
                ],
                "correct_answer": 1
            }
        ]
    },
    {
        "id": str(uuid4()),
        "chapter_id": "psc-ch4",
        "titre": "Quiz - Perte de connaissance",
        "formation_type": "PSC",
        "questions": [
            {
                "id": str(uuid4()),
                "question": "Comment reconnaît-on qu'une personne est inconsciente ?",
                "options": [
                    "Elle ne parle pas",
                    "Elle ne répond pas et ne réagit pas",
                    "Elle a les yeux fermés",
                    "Elle respire lentement"
                ],
                "correct_answer": 1
            },
            {
                "id": str(uuid4()),
                "question": "Pourquoi mettre une personne inconsciente en PLS ?",
                "options": [
                    "Pour la réchauffer",
                    "Pour libérer les voies aériennes et éviter l'étouffement",
                    "Pour la transporter",
                    "Pour la réveiller"
                ],
                "correct_answer": 1
            },
            {
                "id": str(uuid4()),
                "question": "À quelle fréquence surveiller la respiration en PLS ?",
                "options": [
                    "Une fois",
                    "Toutes les 5 minutes",
                    "Toutes les minutes",
                    "Toutes les 30 minutes"
                ],
                "correct_answer": 2
            },
            {
                "id": str(uuid4()),
                "question": "Si la personne en PLS arrête de respirer, que faire ?",
                "options": [
                    "Continuer la PLS",
                    "La secouer",
                    "La remettre sur le dos et débuter la RCP",
                    "Attendre"
                ],
                "correct_answer": 2
            },
            {
                "id": str(uuid4()),
                "question": "Comment doit être la bouche en PLS ?",
                "options": [
                    "Fermée",
                    "Ouverte vers le sol",
                    "Ouverte vers le ciel",
                    "Peu importe"
                ],
                "correct_answer": 1
            }
        ]
    },
    {
        "id": str(uuid4()),
        "chapter_id": "psc-ch5",
        "titre": "Quiz - Arrêt cardiaque et DAE",
        "formation_type": "PSC",
        "questions": [
            {
                "id": str(uuid4()),
                "question": "Quels sont les 2 signes de l'arrêt cardiaque ?",
                "options": [
                    "Douleur et sueurs",
                    "Inconscience et absence de respiration",
                    "Pâleur et pouls faible",
                    "Fièvre et confusion"
                ],
                "correct_answer": 1
            },
            {
                "id": str(uuid4()),
                "question": "Quelle est la séquence de RCP ?",
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
                "question": "À quelle profondeur comprimer le thorax adulte ?",
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
                "question": "Quand reprendre la RCP après un choc du DAE ?",
                "options": [
                    "Attendre 5 minutes",
                    "Immédiatement",
                    "Uniquement si le DAE le demande",
                    "Jamais"
                ],
                "correct_answer": 1
            },
            {
                "id": str(uuid4()),
                "question": "Que faire si la victime reprend connaissance avec le DAE branché ?",
                "options": [
                    "Éteindre le DAE",
                    "Retirer les électrodes",
                    "Laisser le DAE allumé et électrodes en place, mettre en PLS",
                    "Continuer la RCP"
                ],
                "correct_answer": 2
            }
        ]
    },
    {
        "id": str(uuid4()),
        "chapter_id": "psc-ch6",
        "titre": "Quiz - Malaises",
        "formation_type": "PSC",
        "questions": [
            {
                "id": str(uuid4()),
                "question": "Comment reconnaît-on un malaise cardiaque ?",
                "options": [
                    "Maux de tête",
                    "Douleur thoracique en étau, irradiant au bras gauche",
                    "Fièvre",
                    "Douleur au ventre"
                ],
                "correct_answer": 1
            },
            {
                "id": str(uuid4()),
                "question": "Que signifie le test VITE pour l'AVC ?",
                "options": [
                    "Vitesse d'intervention",
                    "Visage paralysé, Impossibilité de bouger un bras, Trouble de la parole, Extrême urgence",
                    "Vérifier, Interroger, Tester, Évaluer",
                    "Ventiler, Immobiliser, Transporter, Examiner"
                ],
                "correct_answer": 1
            },
            {
                "id": str(uuid4()),
                "question": "Quelle position pour un malaise avec douleur thoracique ?",
                "options": [
                    "Allongée jambes surélevées",
                    "Demi-assise",
                    "Sur le ventre",
                    "Debout"
                ],
                "correct_answer": 1
            },
            {
                "id": str(uuid4()),
                "question": "Que faire si une personne diabétique fait une hypoglycémie ?",
                "options": [
                    "Lui donner de l'insuline",
                    "Resucrer (3 sucres, jus de fruit)",
                    "La faire courir",
                    "Lui donner de l'eau"
                ],
                "correct_answer": 1
            },
            {
                "id": str(uuid4()),
                "question": "Que ne doit-on PAS faire lors d'une crise d'épilepsie ?",
                "options": [
                    "Protéger la tête",
                    "Maintenir de force ou mettre quelque chose dans la bouche",
                    "Écarter les objets dangereux",
                    "Chronométrer"
                ],
                "correct_answer": 1
            }
        ]
    },
    {
        "id": str(uuid4()),
        "chapter_id": "psc-ch7",
        "titre": "Quiz - Plaies et traumatismes",
        "formation_type": "PSC",
        "questions": [
            {
                "id": str(uuid4()),
                "question": "Qu'est-ce qu'une plaie grave ?",
                "options": [
                    "Toute plaie qui saigne",
                    "Plaie étendue, profonde ou sur zone à risque",
                    "Plaie qui fait mal",
                    "Plaie ancienne"
                ],
                "correct_answer": 1
            },
            {
                "id": str(uuid4()),
                "question": "Quel est le principe face à un traumatisme d'un membre ?",
                "options": [
                    "Mobiliser pour examiner",
                    "Ne pas mobiliser",
                    "Remettre en place",
                    "Faire marcher"
                ],
                "correct_answer": 1
            },
            {
                "id": str(uuid4()),
                "question": "Que faire en cas de traumatisme du dos ou du cou ?",
                "options": [
                    "Mobiliser doucement",
                    "Ne pas bouger, maintenir la tête, alerter 15",
                    "Mettre en PLS",
                    "Faire asseoir"
                ],
                "correct_answer": 1
            },
            {
                "id": str(uuid4()),
                "question": "Comment traiter une entorse bénigne ?",
                "options": [
                    "Mettre du chaud",
                    "Glace, repos, surélévation",
                    "Faire bouger",
                    "Masser fort"
                ],
                "correct_answer": 1
            }
        ]
    },
    {
        "id": str(uuid4()),
        "chapter_id": "psc-ch8",
        "titre": "Quiz - Brûlures",
        "formation_type": "PSC",
        "questions": [
            {
                "id": str(uuid4()),
                "question": "Combien de temps refroidir une brûlure à l'eau ?",
                "options": [
                    "1 minute",
                    "5 minutes minimum",
                    "30 secondes",
                    "20 minutes"
                ],
                "correct_answer": 1
            },
            {
                "id": str(uuid4()),
                "question": "Comment reconnaît-on une brûlure du 3ᵉ degré ?",
                "options": [
                    "Rougeur et douleur",
                    "Cloques",
                    "Peau blanche ou noire, peu de douleur",
                    "Légère rougeur"
                ],
                "correct_answer": 2
            },
            {
                "id": str(uuid4()),
                "question": "Que faire face à une brûlure chimique ?",
                "options": [
                    "Mettre de la pommade",
                    "Arroser abondamment 20 minutes",
                    "Sécher",
                    "Ne rien faire"
                ],
                "correct_answer": 1
            },
            {
                "id": str(uuid4()),
                "question": "Que ne doit-on JAMAIS faire sur une brûlure ?",
                "options": [
                    "Refroidir",
                    "Percer les cloques ou mettre du beurre",
                    "Alerter",
                    "Protéger"
                ],
                "correct_answer": 1
            },
            {
                "id": str(uuid4()),
                "question": "Une brûlure électrique est-elle toujours grave ?",
                "options": [
                    "Non, jamais",
                    "Oui, toujours",
                    "Seulement si elle fait mal",
                    "Seulement si elle est étendue"
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

print(f"\n🎉 Quiz PSC 1-8 créés")
print(f"📊 Total quiz: {db.quizzes.count_documents({})}")

client.close()
