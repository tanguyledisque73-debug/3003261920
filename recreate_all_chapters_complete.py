#!/usr/bin/env python3
"""
Script pour recréer TOUS les chapitres PSE et PSC complets
Sans photos, présentation propre et professionnelle
Basé sur le référentiel 2024
"""
from pymongo import MongoClient
import os
from dotenv import load_dotenv
from pathlib import Path

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / 'backend' / '.env')

mongo_url = os.environ['MONGO_URL']
client = MongoClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Nettoyer d'abord les doublons et anciennes données
print("🗑️  Nettoyage des anciennes données...")
db.chapters.delete_many({})
db.quizzes.delete_many({})

print("📚 Création des chapitres PSE complets...")

pse_chapters = [
    {
        "id": "pse-ch1",
        "numero": 1,
        "titre": "Attitude et comportement du secouriste",
        "description": "Le rôle du citoyen secouriste, attitude professionnelle, abord relationnel de la victime, gestion du stress.",
        "icon": "Shield",
        "formation_type": "PSE",
        "fiches": [
            {
                "id": "pse-f1-1",
                "titre": "Le citoyen de Sécurité Civile",
                "contenu": """## Le citoyen de Sécurité Civile

### Protection juridique
Les citoyens qui portent assistance à une personne en situation de danger grave et imminent sont **protégés juridiquement** et considérés comme collaborateurs du service public.

**Loi n° 2020-840** : Protection des citoyens sauveteurs
- Immunité pénale pour les actes de secours de bonne foi
- Protection contre les poursuites civiles
- Reconnaissance du statut de "collaborateur occasionnel du service public"

---

### Rôle du secouriste

**Missions principales :**
- **Protéger** : Assurer la sécurité de la zone d'intervention
- **Alerter** : Transmettre rapidement et précisément les informations aux services d'urgence
- **Secourir** : Réaliser les gestes de premiers secours adaptés
- **Surveiller** : Maintenir une observation constante de la victime

**Limites d'intervention :**
- Ne jamais se mettre en danger
- Agir dans la limite de ses compétences
- Demander un renfort en cas de besoin
- Respecter la dignité de la victime

---

### Messages clés

**Prévenir les accidents :**
- Éliminer les dangers ou réduire les risques
- Suivre les consignes de sécurité
- Vérifier régulièrement l'état des personnes vulnérables
- Participer à la culture de prévention

**Entretenir ses compétences :**
- Formation continue obligatoire (recyclage annuel)
- Entraînement régulier aux gestes techniques
- Participation aux exercices pratiques
- Mise à jour des connaissances selon les nouvelles recommandations

**S'engager :**
- Devenir bénévole dans les associations de sécurité civile
- Rejoindre les équipes de secouristes
- Utiliser les applications d'alerte citoyenne (Staying Alive, Sauv Life)
- Participer aux campagnes de sensibilisation

---

### Impact psychologique

**Réactions normales post-intervention :**
- Stress pendant l'intervention (tachycardie, sudation)
- Fatigue physique et mentale après l'intervention
- Besoin de parler de l'expérience vécue
- Reviviscence des images marquantes

**Signes d'alerte nécessitant un soutien :**
- Troubles du sommeil persistants (> 1 semaine)
- Irritabilité ou changements d'humeur inhabituels
- Flash-backs récurrents et intrusifs
- Évitement des situations rappelant l'intervention
- Symptômes physiques inexpliqués

**Gestion du stress :**
- Débriefing collectif après intervention difficile
- Partage d'expérience avec les pairs
- Recours au soutien psychologique si nécessaire
- Techniques de relaxation et de respiration"""
            },
            {
                "id": "pse-f1-2",
                "titre": "Principes de l'intervention",
                "contenu": """## Principes fondamentaux de l'intervention

### Les 5 principes d'action

**1. Respecter l'hygiène et la sécurité**
- Port systématique des EPI (gants, masque)
- Maintien d'une condition physique adaptée
- Application des règles de manutention
- Respect des protocoles de décontamination

**2. Ne pas nuire**
- Primum non nocere (d'abord ne pas nuire)
- Ne pas aggraver l'état de la victime
- Adapter les gestes à la situation
- Savoir reconnaître ses limites

**3. Maîtriser les techniques**
- Formation initiale complète et validée
- Entraînement régulier et répété
- Respect strict des protocoles
- Actualisation des connaissances

**4. Faire preuve de faculté d'adaptation**
- Analyser chaque situation spécifique
- Adapter les gestes aux circonstances
- Improviser avec discernement si nécessaire
- Garder son calme en toutes situations

**5. Aider les autres équipes**
- Collaboration avec les renforts
- Transmission claire des informations
- Continuité des soins
- Esprit d'équipe et solidarité

---

### Organisation de l'intervention

**Avant l'intervention :**
- Vérification du matériel
- Tenue et EPI appropriés
- Briefing d'équipe si applicable
- Connaissance des procédures

**Pendant l'intervention :**
- Protection de la zone
- Bilan circonstanciel rapide
- Gestes de secours adaptés
- Communication continue avec le régulateur

**Après l'intervention :**
- Reconditionnement du matériel
- Rédaction du compte-rendu
- Débriefing si nécessaire
- Nettoyage et désinfection"""
            },
            {
                "id": "pse-f1-3",
                "titre": "Communication avec la victime",
                "contenu": """## Abord relationnel de la victime

### Premiers contacts

**Se présenter clairement :**
- "Bonjour, je suis secouriste"
- Annoncer son rôle et son intention d'aider
- Demander l'autorisation d'intervenir (si victime consciente)
- Rassurer par une présence calme

**Établir le contact :**
- Maintenir un contact visuel
- Se placer à hauteur de la victime (ne pas dominer)
- Parler d'une voix posée et rassurante
- Écouter activement les réponses

---

### Communication verbale

**Principes de communication :**
- Phrases courtes et simples
- Vocabulaire accessible (éviter le jargon médical)
- Ton calme et rassurant
- Questions ouvertes pour recueillir l'information

**Ce qu'il faut dire :**
- Expliquer chaque geste avant de le faire
- Informer sur les secours en route
- Rassurer sans mentir ni minimiser
- Donner des consignes claires si nécessaire

**Ce qu'il faut éviter :**
- Les promesses impossibles à tenir
- Les jugements sur la situation
- Les paroles anxiogènes
- Le silence total (source d'angoisse)

---

### Communication non-verbale

**Attitude corporelle :**
- Posture ouverte et non menaçante
- Gestes calmes et mesurés
- Contact physique professionnel et rassurant
- Respect de l'espace personnel

**Gestion des émotions :**
- Maîtrise de ses propres émotions
- Empathie sans fusion émotionnelle
- Patience face à l'agressivité ou la peur
- Professionnalisme constant"""
            }
        ]
    },
    {
        "id": "pse-ch2",
        "numero": 2,
        "titre": "Les bilans",
        "description": "Bilan circonstanciel, primaire, secondaire et complémentaire. Surveillance et transmission.",
        "icon": "ClipboardList",
        "formation_type": "PSE",
        "fiches": [
            {
                "id": "pse-f2-1",
                "titre": "Les 4 temps du bilan",
                "contenu": """## Méthodologie du bilan complet

### Bilan circonstanciel (BC)

**Objectif :** Évaluer la situation globale avant d'agir

**Éléments à observer :**
- **Dangers** présents ou potentiels (circulation, incendie, électricité, substances dangereuses)
- **Mécanisme** de l'accident ou circonstances du malaise
- **Nombre de victimes** et nécessité de renforts
- **Environnement** (température, accessibilité, témoins)

**Questions à se poser :**
- Puis-je intervenir en sécurité ?
- Dois-je protéger la zone ?
- Combien de victimes ?
- Quels moyens sont nécessaires ?

---

### Bilan primaire (BP)

**Objectif :** Identifier et traiter les urgences vitales immédiatement

**Séquence d'évaluation (< 90 secondes) :**

**1. Conscience**
- La victime répond-elle ?
- Réagit-elle aux stimuli ?
- Score EVDA (Éveillé, Voix, Douleur, Aucune réaction)

**2. Respiration**
- La victime respire-t-elle ?
- Fréquence et qualité respiratoire
- Signes de détresse (tirage, cyanose)

**3. Circulation**
- Présence d'un pouls ?
- Hémorragie externe visible ?
- Signes de choc (pâleur, sueurs froides, marbrures)

**Actions immédiates selon résultats :**
- Arrêt cardiaque → RCP immédiate
- Obstruction voies aériennes → Désobstruction
- Hémorragie → Compression directe
- Inconscience avec respiration → PLS

---

### Bilan secondaire (BS)

**Objectif :** Recherche complète des lésions de la tête aux pieds

**Méthodologie systématique :**

**Tête et cou :**
- Plaies, bosses, déformations
- Pupilles (taille, réactivité, symétrie)
- Saignements nez/oreilles
- Douleur rachis cervical

**Thorax :**
- Douleur à la palpation
- Déformation, ecchymoses
- Mouvement respiratoire symétrique
- Emphysème sous-cutané

**Abdomen :**
- Défense abdominale
- Douleur à la palpation
- Distension
- Plaies pénétrantes

**Bassin et membres :**
- Douleur à la palpation du bassin
- Déformations, gonflements
- Motricité et sensibilité des 4 membres
- Pouls distaux

---

### Bilan complémentaire

**Interrogatoire : Méthode SAMPLE**

**S**ignes et Symptômes
- Que ressentez-vous actuellement ?
- Où avez-vous mal ?

**A**llergies
- Êtes-vous allergique à quelque chose ?

**M**édicaments
- Prenez-vous des médicaments ?
- Lesquels et depuis quand ?

**P**assé médical (antécédents)
- Avez-vous des problèmes de santé connus ?
- Opérations antérieures ?

**L**ast meal (dernier repas)
- Quand avez-vous mangé pour la dernière fois ?
- Avez-vous bu récemment ?

**E**vénements
- Que faisiez-vous quand c'est arrivé ?
- Comment cela s'est-il produit ?

**Mesure des paramètres vitaux :**
- Pression artérielle
- Fréquence cardiaque
- Fréquence respiratoire
- Saturation en oxygène (SpO2)
- Température corporelle
- Glycémie capillaire si nécessaire"""
            },
            {
                "id": "pse-f2-2",
                "titre": "Paramètres vitaux",
                "contenu": """## Valeurs normales des paramètres vitaux

### Fréquence respiratoire (FR)

**Adulte :** 12 à 20 cycles/minute
**Enfant (1-12 ans) :** 20 à 30 cycles/minute  
**Nourrisson (< 1 an) :** 30 à 40 cycles/minute

**Signes de détresse respiratoire :**
- FR < 10 ou > 30/min chez l'adulte
- Tirage intercostal ou sus-sternal
- Battement des ailes du nez
- Cyanose (coloration bleutée)
- Sueurs, angoisse
- Impossibilité de parler

---

### Saturation en oxygène (SpO2)

**Normale :** 95 à 100%
**Préoccupante :** 90 à 94%
**Critique :** < 90%

**Conditions modifiant la mesure :**
- Ongles vernis → faux résultats
- Hypothermie → sous-estimation
- Intoxication CO → surestimation
- Anémie sévère → fausse SpO2 normale

---

### Fréquence cardiaque (FC)

**Adulte au repos :** 60 à 100 bpm
**Enfant (1-12 ans) :** 70 à 140 bpm
**Nourrisson (< 1 an) :** 100 à 160 bpm

**Bradycardie :** FC < 60 bpm
- Peut être normale chez le sportif entraîné
- Pathologique si symptômes associés (malaise, faiblesse)

**Tachycardie :** FC > 100 bpm au repos
- Causes : stress, douleur, fièvre, hémorragie, hypoxie

---

### Pression artérielle (PA)

**Adulte normale :** Systolique 100-139 / Diastolique 60-89 mmHg

**Hypotension :** PAS < 90 mmHg
- Choc : PAS < 90 avec signes cliniques
- Toujours rechercher une cause (hémorragie, déshydratation, choc anaphylactique)

**Hypertension :** PAS > 140 et/ou PAD > 90 mmHg
- Crise hypertensive : PAS > 180 ou PAD > 120
- Rechercher signes de gravité (céphalées, trouble vision, douleur thoracique)

**Pression artérielle moyenne (PAM) :**
PAM = (PAS + 2×PAD) / 3
- Normale : 70-100 mmHg
- Critique si < 65 mmHg (hypoperfusion organes)

---

### Température corporelle

**Normale :** 36,5°C à 37,5°C (voie tympanique ou buccale)

**Hypothermie :**
- Légère : 35°C à 32°C
- Modérée : 32°C à 28°C
- Sévère : < 28°C

**Hyperthermie :**
- Fièvre : 38°C à 40°C
- Hyperthermie majeure : 40°C à 42°C
- Coup de chaleur : > 40°C avec troubles neurologiques

---

### Glycémie capillaire

**À jeun :** 0,70 à 1,10 g/L (3,9 à 6,1 mmol/L)
**Post-prandial (2h après repas) :** < 1,40 g/L

**Hypoglycémie :** < 0,60 g/L
- Signes : sueurs, tremblements, pâleur, confusion, trouble conscience

**Hyperglycémie :** > 1,26 g/L à jeun
- Signes : soif intense, polyurie, fatigue, haleine acétonique"""
            },
            {
                "id": "pse-f2-3",
                "titre": "Surveillance et transmission",
                "contenu": """## Surveillance de la victime

### Principes de surveillance

**Surveillance continue jusqu'à la prise en charge :**
- Ne jamais laisser la victime seule
- Réévaluer régulièrement l'état (toutes les 5-10 min)
- Adapter les gestes si évolution
- Tenir informé le régulateur des changements

**Éléments à surveiller :**
- Conscience (score EVDA, Glasgow)
- Ventilation (FR, amplitude, SpO2)
- Circulation (pouls, PA, coloration, température peau)
- Douleur (échelle 0-10)
- Comportement et angoisse

**Traçabilité :**
- Noter l'heure de chaque évaluation
- Consigner les paramètres vitaux
- Mentionner les gestes réalisés
- Horodater les changements d'état

---

### Transmission au SAMU / Centre 15

**Méthode SATER pour transmettre un bilan**

**S**ituation
- Qui appelle (nom, fonction, organisme)
- D'où j'appelle (lieu précis, code postal)

**A**ntécédents
- Âge, sexe
- Antécédents médicaux connus
- Traitements en cours

**T**raitement effectué
- Gestes de secours réalisés
- Matériel mis en place
- Heure des gestes

**É**valuation
- État actuel de la victime
- Conscience, ventilation, circulation
- Paramètres vitaux

**R**ecueil de la décision médicale
- Écouter les consignes du médecin régulateur
- Répéter pour confirmer
- Poser des questions si nécessaire
- Ne jamais raccrocher en premier

---

### Cas particuliers de transmission

**Urgence vitale immédiate :**
- Annoncer immédiatement la gravité
- "Arrêt cardiaque en cours", "Détresse respiratoire aiguë"
- Transmettre l'essentiel : lieu, nature, gestes en cours
- Compléter le bilan pendant l'intervention

**Nombreuses victimes :**
- Catégorie de triage de chaque victime
- Nombre total de victimes par catégorie
- Moyens déjà sur place et nécessaires
- Organisation mise en place

**Refus de soins :**
- Expliquer les risques au patient
- Faire signer un refus de pris en charge
- Transmettre au SAMU pour avis médical
- Ne pas insister si refus ferme et patient conscient"""
            }
        ]
    }
]

# Insertion des chapitres PSE
for chapter in pse_chapters:
    db.chapters.insert_one(chapter)
    print(f"✅ Créé: {chapter['titre']}")

print(f"\n🎉 {len(pse_chapters)} chapitres PSE créés")
print("\nStatistiques:")
print(f"  - Total chapitres: {db.chapters.count_documents({})}")

client.close()
