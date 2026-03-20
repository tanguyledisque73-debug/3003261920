#!/usr/bin/env python3
"""
Script complet de recréation de TOUS les chapitres PSE et PSC
Mise en page professionnelle SANS markdown
Référentiel 2024
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

# Nettoyer les données existantes
print("🗑️  Nettoyage complet...")
db.chapters.delete_many({})
db.quizzes.delete_many({})
print("✅ Base nettoyée")

# ═══════════════════════════════════════════════════════════
# CHAPITRES PSE COMPLETS
# ═══════════════════════════════════════════════════════════

pse_chapters = [
    {
        "id": "pse-ch1",
        "numero": 1,
        "titre": "Rôle et attitude du secouriste",
        "description": "Protection juridique, missions du secouriste, gestion du stress et communication avec la victime",
        "icon": "Shield",
        "formation_type": "PSE",
        "fiches": [
            {
                "id": "pse-f1-1",
                "titre": "Le secouriste citoyen",
                "contenu": """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                    PROTECTION JURIDIQUE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Le citoyen qui porte secours à une personne en danger bénéficie d'une protection juridique complète.


CADRE LÉGAL

Loi n° 2020-840 du 3 juillet 2020
Protection des citoyens sauveteurs intervenant de bonne foi

Bénéfices de cette loi :
   → Immunité pénale pour les actes de secours réalisés de bonne foi
   → Protection contre les poursuites civiles en cas de dommages involontaires
   → Reconnaissance du statut de collaborateur occasionnel du service public
   → Couverture des actes effectués dans l'urgence

Exception : Cette protection ne s'applique PAS en cas de faute lourde ou intentionnelle.


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                    RÔLE DU SECOURISTE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

QUATRE MISSIONS ESSENTIELLES

1. PROTÉGER
   Assurer la sécurité de la zone d'intervention
   Éviter le suraccident
   Baliser si nécessaire

2. ALERTER
   Transmettre rapidement les informations aux secours
   Utiliser le 15 (SAMU), 18 (Pompiers) ou 112 (numéro européen)
   Donner des informations précises et complètes

3. SECOURIR
   Réaliser les gestes de premiers secours appropriés
   Agir dans la limite de ses compétences
   Utiliser le matériel disponible

4. SURVEILLER
   Maintenir une observation constante de la victime
   Réévaluer régulièrement son état
   Adapter les gestes si évolution


LIMITES D'INTERVENTION

⚠ Ne jamais se mettre en danger soi-même
⚠ Agir uniquement dans la limite de ses compétences
⚠ Demander un renfort en cas de besoin
⚠ Respecter la dignité et l'intimité de la victime
⚠ Obtenir le consentement (si victime consciente)


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                    ENTRETIEN DES COMPÉTENCES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

FORMATION CONTINUE OBLIGATOIRE

Recyclage annuel : 6 heures minimum par an
Entraînement régulier aux gestes techniques
Mise à jour selon les nouvelles recommandations
Participation aux exercices pratiques


ENGAGEMENT CITOYEN

Rejoindre une association de secourisme
Devenir réserviste de la Sécurité Civile
Utiliser les applications d'alerte citoyenne :
   → Staying Alive (arrêts cardiaques)
   → Sauv Life (premiers répondants)
Participer aux campagnes de sensibilisation


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                    GESTION DU STRESS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

RÉACTIONS NORMALES PENDANT L'INTERVENTION

   → Tachycardie (cœur qui bat vite)
   → Sudation importante
   → Mains tremblantes
   → Hyperventilation
   → Sensation d'urgence

Ces réactions sont NORMALES et permettent de mobiliser l'énergie nécessaire.


APRÈS L'INTERVENTION

Réactions attendues :
   → Fatigue physique et mentale
   → Besoin de parler de l'expérience
   → Reviviscence des images marquantes
   → Questionnements sur ses actes


SIGNES D'ALERTE NÉCESSITANT UN SOUTIEN

⚠ Troubles du sommeil persistants (plus d'une semaine)
⚠ Irritabilité ou changements d'humeur inhabituels
⚠ Flash-backs récurrents et intrusifs
⚠ Évitement des situations rappelant l'intervention
⚠ Symptômes physiques inexpliqués
⚠ Isolement social

EN CAS DE BESOIN : Contacter le numéro d'aide psychologique de votre association ou consulter un professionnel.


TECHNIQUES DE GESTION

Avant l'intervention :
   → Respiration contrôlée (inspiration 4 sec, expiration 6 sec)
   → Visualisation positive
   → Rappel des procédures

Pendant :
   → Se concentrer sur les gestes techniques
   → Communication avec l'équipe
   → Rester factuel

Après :
   → Débriefing collectif
   → Partage d'expérience avec les pairs
   → Repos suffisant
"""
            },
            {
                "id": "pse-f1-2",
                "titre": "Les 5 principes d'action",
                "contenu": """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                LES CINQ PRINCIPES FONDAMENTAUX
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


PRINCIPE 1 : RESPECTER L'HYGIÈNE ET LA SÉCURITÉ

Protection personnelle obligatoire :
   → Port de gants à usage unique (latex ou nitrile)
   → Masque de protection si risque de projection
   → Lunettes de protection si nécessaire
   → Surblouse si contact avec liquides biologiques

Hygiène des mains :
   → Lavage à l'eau et au savon (30 secondes minimum)
   → Solution hydro-alcoolique si mains non souillées
   → Avant ET après chaque intervention

Condition physique :
   → Maintenir une bonne forme physique
   → Respecter les techniques de manutention
   → Ne pas intervenir si état incompatible (fatigue extrême, alcool)


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PRINCIPE 2 : NE PAS NUIRE

"PRIMUM NON NOCERE"
D'abord ne pas nuire


Règles d'or :
   → Ne pas aggraver l'état de la victime
   → Ne pas déplacer une victime traumatisée (sauf danger vital immédiat)
   → Ne pas retirer un corps étranger enfoncé
   → Ne pas donner à boire à une victime inconsciente
   → Ne pas donner de médicaments (sauf consigne médicale)

En cas de doute : Demander conseil au SAMU (15)


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PRINCIPE 3 : MAÎTRISER LES TECHNIQUES

Formation initiale complète et validée
Entraînement régulier et répété
Respect strict des protocoles et procédures
Actualisation permanente des connaissances

⚠ N'appliquer QUE les gestes pour lesquels vous êtes formé et entraîné.


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PRINCIPE 4 : ADAPTER SES ACTIONS

Chaque intervention est unique :
   → Environnement différent
   → Victimes différentes
   → Moyens disponibles variables
   → Contraintes spécifiques

Le secouriste doit :
   → Analyser rapidement la situation
   → Adapter les gestes aux circonstances
   → Improviser avec discernement si nécessaire
   → Garder son calme et sa lucidité


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PRINCIPE 5 : COLLABORER AVEC LES AUTRES ÉQUIPES

Travail en équipe :
   → Communication claire et précise
   → Transmission complète des informations
   → Continuité des soins assurée
   → Respect de la hiérarchie opérationnelle

Lors de l'arrivée des renforts :
   → Présenter un bilan clair
   → Mentionner les gestes déjà effectués
   → Rester disponible pour aider
   → Ne pas partir sans autorisation
"""
            },
            {
                "id": "pse-f1-3",
                "titre": "Communication avec la victime",
                "contenu": """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                    PREMIERS CONTACTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SE PRÉSENTER CLAIREMENT

Approche recommandée :
   "Bonjour, je suis secouriste. Je vais vous aider."

Étapes du premier contact :
   1. Annoncer son rôle et son intention d'aider
   2. Demander l'autorisation d'intervenir (si victime consciente)
   3. Rassurer par une présence calme et posée
   4. Expliquer ce que l'on va faire


ÉTABLIR LE CONTACT

Position du secouriste :
   → Se placer à hauteur de la victime (ne pas dominer)
   → Maintenir un contact visuel rassurant
   → Adopter une posture ouverte et non menaçante
   → Se tenir à une distance respectueuse (50-80 cm)

Attitude :
   → Voix posée et rassurante
   → Débit de parole modéré
   → Écoute active des réponses
   → Empathie sans familiarité excessive


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                COMMUNICATION VERBALE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PRINCIPES

Phrases courtes et simples
Vocabulaire accessible (éviter le jargon médical)
Ton calme et rassurant
Questions ouvertes pour recueillir l'information


CE QU'IL FAUT DIRE

✓ "Je vais vous examiner"
✓ "Les secours sont en route"
✓ "Vous êtes en sécurité maintenant"
✓ "Je reste avec vous"
✓ "Pouvez-vous me dire ce qui s'est passé ?"
✓ Expliquer chaque geste AVANT de le faire


CE QU'IL FAUT ÉVITER

✗ "Tout va bien se passer" (promesse impossible à tenir)
✗ "Ce n'est rien" (minimisation de la souffrance)
✗ "Ne vous inquiétez pas" (la personne EST inquiète)
✗ Jugements sur la situation ou le comportement
✗ Silence total prolongé (source d'angoisse)
✗ Discussions personnelles non pertinentes


ADAPTATION DU LANGAGE

Enfant :
   → Vocabulaire simple et ludique
   → Ton doux et rassurant
   → Impliquer un parent si possible

Personne âgée :
   → Parler clairement (sans crier)
   → Laisser le temps de répondre
   → Vouvoiement respectueux

Personne ne parlant pas français :
   → Phrases très simples
   → Gestuelle explicite
   → Utiliser un traducteur si disponible (app smartphone)


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                COMMUNICATION NON-VERBALE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LANGAGE DU CORPS

Posture ouverte et accueillante
Gestes calmes et mesurés
Contact physique professionnel et rassurant :
   → Main sur l'épaule
   → Maintien de la main (avec consentement)
Respect de l'espace personnel


EXPRESSION FACIALE

Visage détendu et concentré
Regard bienveillant
Sourire rassurant (adapté à la situation)
Éviter les mimiques d'inquiétude ou de dégoût


GESTION DES ÉMOTIONS

Maîtrise de ses propres émotions
Empathie SANS fusion émotionnelle
Patience face à l'agressivité ou la peur :
   → Ne pas le prendre personnellement
   → Comprendre que c'est une réaction au stress
Professionnalisme constant

La victime observe TOUT : votre attitude influence son état émotionnel.
"""
            }
        ]
    },
    {
        "id": "pse-ch2",
        "numero": 2,
        "titre": "Les bilans",
        "description": "Bilan circonstanciel, primaire, secondaire et complémentaire selon la méthode SAMPLE",
        "icon": "ClipboardList",
        "formation_type": "PSE",
        "fiches": [
            {
                "id": "pse-f2-1",
                "titre": "Bilan circonstanciel",
                "contenu": """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
            BILAN CIRCONSTANCIEL (BC)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

OBJECTIF

Évaluer la situation GLOBALE avant d'agir sur la victime.

Durée : 10 à 30 secondes


QUATRE ÉLÉMENTS À OBSERVER


1. LES DANGERS

Dangers présents ou potentiels :
   → Circulation routière
   → Incendie, fumées, explosion
   → Électricité (fils, appareils)
   → Produits chimiques, gaz
   → Effondrement de structure
   → Agression en cours

Question clé : Puis-je intervenir EN SÉCURITÉ ?


2. LE MÉCANISME

Accident :
   → Chute de quelle hauteur ?
   → Collision à quelle vitesse ?
   → Objet contondant ou pénétrant ?
   → Projection, écrasement ?

Malaise :
   → Survenue brutale ou progressive ?
   → Pendant un effort ou au repos ?
   → Perte de connaissance ?


3. LE NOMBRE DE VICTIMES

Une seule victime :
   → Intervention classique

Plusieurs victimes :
   → Demander des renforts IMMÉDIATEMENT
   → Noter le nombre approximatif
   → Repérer les urgences vitales
   → Organiser un triage si nécessaire


4. L'ENVIRONNEMENT

Accessibilité :
   → Voie carrossable ou chemin ?
   → Étage (avec ou sans ascenseur) ?
   → Espace confiné ?

Conditions :
   → Température extérieure
   → Météo (pluie, neige, vent)
   → Luminosité

Témoins :
   → Personnes ayant vu l'événement
   → Proches de la victime


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

DÉCISIONS IMMÉDIATES

Protéger la zone si danger
Baliser si nécessaire
Demander des renforts (18, 15, 112)
Mettre des gants avant tout contact
"""
            },
            {
                "id": "pse-f2-2",
                "titre": "Bilan primaire",
                "contenu": """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
              BILAN PRIMAIRE (BP)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

OBJECTIF

Identifier et traiter les URGENCES VITALES en moins de 90 secondes.


SÉQUENCE D'ÉVALUATION


ÉTAPE 1 : CONSCIENCE

Approche :
   "Monsieur, vous m'entendez ?"
   "Madame, ouvrez les yeux !"
   
Stimulation progressive :
   → Verbale (parler fort)
   → Tactile (secouer légèrement les épaules)
   → Douloureuse (pincement trapèze si nécessaire)

Score EVDA :
   E = Éveillé (yeux ouverts spontanément)
   V = Réagit à la Voix
   D = Réagit à la Douleur
   A = Aucune réaction


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ÉTAPE 2 : RESPIRATION

SI VICTIME CONSCIENTE :
   Observer les mouvements du thorax
   Compter pendant 15 secondes puis multiplier par 4
   
SI VICTIME INCONSCIENTE :
   1. Basculer prudemment la tête en arrière
   2. Élever le menton
   3. Approcher la joue de la bouche et regarder le thorax
   4. Pendant 10 secondes : VOS
      → Voir le thorax se soulever
      → Ouïr le bruit de l'air
      → Sentir le souffle sur la joue


Fréquence respiratoire normale :
   Adulte : 12 à 20 cycles par minute
   Enfant : 20 à 30 cycles par minute
   Nourrisson : 30 à 40 cycles par minute


SIGNES DE DÉTRESSE RESPIRATOIRE

⚠ Fréquence anormale (< 10 ou > 30 chez l'adulte)
⚠ Tirage intercostal ou sus-sternal
⚠ Battement des ailes du nez
⚠ Cyanose (coloration bleutée lèvres/extrémités)
⚠ Sueurs profuses
⚠ Angoisse, impossibilité de parler


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ÉTAPE 3 : CIRCULATION

Recherche du pouls carotidien :
   → 2 doigts (index + majeur) dans la gouttière carotidienne
   → Pendant 10 secondes maximum
   → Ne pas appuyer trop fort

Recherche d'hémorragie externe :
   → Balayage visuel rapide
   → Inspection sous les vêtements si suspicion

Signes de choc :
   → Pâleur importante
   → Sueurs froides
   → Marbrures cutanées
   → Pouls rapide et faible


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ACTIONS IMMÉDIATES SELON RÉSULTATS


┌─────────────────────────────────────────────────┐
│  SITUATION            │  ACTION IMMÉDIATE       │
├───────────────────────┼─────────────────────────┤
│  Arrêt cardiaque      │  RCP + DAE              │
│  Obstruction totale   │  Claques + Heimlich     │
│  Hémorragie externe   │  Compression directe    │
│  Inconscient respire  │  PLS                    │
│  Détresse respiratoire│  Position demi-assise   │
│  Choc                 │  Allonger, jambes levées│
└─────────────────────────────────────────────────┘


Toute urgence vitale DOIT être traitée AVANT de poursuivre le bilan.
"""
            },
            {
                "id": "pse-f2-3",
                "titre": "Bilan secondaire et SAMPLE",
                "contenu": """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
           BILAN SECONDAIRE (BS)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

OBJECTIF

Recherche COMPLÈTE des lésions de la tête aux pieds.

Réalisé APRÈS avoir traité les urgences vitales.


EXAMEN SYSTÉMATIQUE


TÊTE ET COU

Inspection :
   → Plaies, bosses, déformations
   → Saignements nez/oreilles
   → Écoulement de liquide clair (LCR)

Pupilles :
   → Taille (myosis / mydriase)
   → Réactivité à la lumière
   → Symétrie

Rachis cervical :
   → Douleur à la palpation
   → Déformation


THORAX

Palpation douce :
   → Douleur
   → Déformation, enfoncement
   → Ecchymoses

Observation :
   → Mouvement respiratoire symétrique
   → Emphysème sous-cutané (crépitation)


ABDOMEN

Inspection :
   → Distension
   → Ecchymoses
   → Plaies

Palpation des 4 quadrants :
   → Douleur localisée ou diffuse
   → Défense abdominale (contraction réflexe)
   → Plaie pénétrante


BASSIN ET MEMBRES

Bassin :
   → Pression douce sur les crêtes iliaques
   → Douleur = suspicion de fracture

Membres supérieurs et inférieurs :
   → Déformation, gonflement
   → Plaies
   → Motricité : "Serrez mes doigts, poussez contre ma main"
   → Sensibilité : "Sentez-vous que je vous touche ?"
   → Pouls distaux (radial, pédieux)


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
           BILAN COMPLÉMENTAIRE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

INTERROGATOIRE : MÉTHODE SAMPLE


S = SIGNES ET SYMPTÔMES

"Que ressentez-vous actuellement ?"
"Où avez-vous mal ?"
"Décrivez-moi votre douleur"
"Sur une échelle de 0 à 10, évaluez votre douleur"


A = ALLERGIES

"Êtes-vous allergique à quelque chose ?"
   → Médicaments
   → Aliments
   → Latex, piqûres d'insectes
   → Autres allergies connues


M = MÉDICAMENTS

"Prenez-vous des médicaments ?"
"Lesquels et depuis quand ?"
"Avez-vous pris votre traitement aujourd'hui ?"

Médicaments importants à noter :
   → Anticoagulants (Kardégic, Préviscan, Eliquis)
   → Antidiabétiques (insuline, Metformine)
   → Cardio (bêtabloquants, antiarythmiques)
   → Corticoïdes au long cours


P = PASSÉ MÉDICAL (ANTÉCÉDENTS)

"Avez-vous des problèmes de santé connus ?"
   → Maladies cardiovasculaires
   → Diabète
   → Asthme, BPCO
   → Épilepsie
   → Cancers

"Avez-vous été opéré ?"
   → Quelles interventions ?
   → Quand ?


L = LAST MEAL (DERNIER REPAS)

"Quand avez-vous mangé pour la dernière fois ?"
"Qu'avez-vous mangé ?"
"Avez-vous bu de l'alcool ?"

Important pour :
   → Risque d'anesthésie
   → Hypoglycémie
   → Intoxication alimentaire


E = ÉVÉNEMENTS

"Que faisiez-vous quand c'est arrivé ?"
"Comment cela s'est-il produit ?"
"Avez-vous ressenti des signes avant-coureurs ?"


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PARAMÈTRES VITAUX À MESURER

Pression artérielle (tensiomètre)
Fréquence cardiaque (pouls ou scope)
Fréquence respiratoire (comptage)
Saturation en oxygène (oxymètre de pouls)
Température corporelle (thermomètre)
Glycémie capillaire (lecteur glycémie)


SURVEILLANCE

Réévaluer toutes les 5 à 10 minutes
Noter l'évolution
Transmettre les changements au régulateur
"""
            }
        ]
    }
]

print("\n📚 Insertion des chapitres PSE...")
for ch in pse_chapters:
    db.chapters.insert_one(ch)
    print(f"  ✅ {ch['titre']}")

print(f"\n🎉 {len(pse_chapters)} chapitres PSE créés avec succès")
print(f"📊 Total dans la base : {db.chapters.count_documents({})} chapitres")

client.close()
