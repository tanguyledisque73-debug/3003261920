#!/usr/bin/env python3
"""
Création des 8 chapitres PSC1 complets
Formation grand public - Référentiel 2024
Mise en page professionnelle SANS markdown
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

print("📚 Création des chapitres PSC1...")

psc_chapters = [
    {
        "id": "psc-ch1",
        "numero": 1,
        "titre": "Protection et alerte",
        "description": "Protéger, examiner, faire alerter ou alerter les secours appropriés",
        "icon": "ShieldAlert",
        "formation_type": "PSC",
        "fiches": [
            {
                "id": "psc-f1-1",
                "titre": "Protéger",
                "contenu": """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                        PROTÉGER
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

POURQUOI PROTÉGER ?

La protection est la PREMIÈRE action du secourisme.

Objectifs :
   → Éviter le suraccident
   → Assurer sa propre sécurité
   → Protéger la victime
   → Protéger les témoins


PRINCIPE ABSOLU

NE JAMAIS SE METTRE EN DANGER


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

RECONNAÎTRE LES DANGERS


DANGERS PERSISTANTS

→ Circulation routière
→ Incendie, fumées
→ Risque d'explosion
→ Risque d'électrocution
→ Atmosphère toxique
→ Effondrement


ÉVALUER LA SITUATION

Avant d'approcher, se poser les questions :
   → Y a-t-il un danger ?
   → Puis-je intervenir sans risque ?
   → Ai-je besoin d'aide ?


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ACTIONS DE PROTECTION


SI LE DANGER PEUT ÊTRE SUPPRIMÉ

Exemples :
   → Couper le contact d'un véhicule
   → Débrancher un appareil électrique
   → Fermer le gaz
   → Éteindre un début d'incendie (extincteur)


SI LE DANGER NE PEUT PAS ÊTRE SUPPRIMÉ

BALISER ET DÉLIMITER LA ZONE

Sur la route :
   → Allumer les feux de détresse
   → Mettre le gilet haute visibilité AVANT de sortir
   → Placer le triangle de présignalisation
      • 30 mètres en ville
      • 150 mètres sur route
      • 200 mètres sur autoroute

Empêcher l'accès :
   → Faire reculer les curieux
   → Interdire de fumer
   → Demander de l'aide


SI DANGER IMMÉDIAT ET INCONTRÔLABLE

DÉGAGEMENT D'URGENCE de la victime
   → Uniquement si danger vital immédiat
   → Traction par les chevilles ou les poignets
   → Distance minimale nécessaire

⚠ Risque d'aggravation des lésions
⚠ Uniquement en dernier recours


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CAS PARTICULIERS


ACCIDENT DE LA ROUTE

1. Se garer en sécurité
2. Mettre le gilet (AVANT de sortir)
3. Triangle de signalisation
4. Couper le contact des véhicules
5. Interdire de fumer


INCENDIE

Ne PAS pénétrer dans un lieu enfumé
Rester à 50 mètres minimum
Alerter les pompiers (18)


ÉLECTRICITÉ

Ne PAS toucher la victime
Couper le courant au disjoncteur
Si impossible : éloigner avec objet isolant (bois sec)
"""
            },
            {
                "id": "psc-f1-2",
                "titre": "Examiner",
                "contenu": """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                        EXAMINER
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

OBJECTIF

Rechercher rapidement ce qui menace immédiatement la vie de la victime.


DEUX ÉTAPES ESSENTIELLES


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. VÉRIFIER LA CONSCIENCE


PARLER FORT À LA VICTIME

"Monsieur, vous m'entendez ?"
"Madame, ouvrez les yeux !"


SI LA VICTIME RÉPOND

   → Elle est CONSCIENTE
   → Passer à l'étape suivante (recherche de dangers)


SI LA VICTIME NE RÉPOND PAS

SECOUER DOUCEMENT LES ÉPAULES

   → Si réaction : Consciente
   → Si pas de réaction : INCONSCIENTE


Si inconsciente :
   → Appeler à l'aide immédiatement
   → Passer à l'étape 2 (vérifier la respiration)


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

2. VÉRIFIER LA RESPIRATION


UNIQUEMENT SI LA VICTIME EST INCONSCIENTE


TECHNIQUE : VOS (Voir, Ouïr, Sentir)


ÉTAPES :

1. BASCULER LA TÊTE EN ARRIÈRE
   → Main sur le front
   → Tirer doucement vers l'arrière

2. ÉLEVER LE MENTON
   → 2 doigts sous le menton
   → Soulever vers le haut

3. REGARDER, ÉCOUTER, SENTIR pendant 10 secondes
   → VOIR le thorax/ventre se soulever
   → OUÏR le bruit de l'air
   → SENTIR le souffle sur la joue


RÉSULTATS


LA VICTIME RESPIRE NORMALEMENT

   → Mouvements réguliers du thorax
   → Bruit de l'air qui sort
   → Souffle perçu

   ➜ Mettre en POSITION LATÉRALE DE SÉCURITÉ
   ➜ Alerter le 15


LA VICTIME NE RESPIRE PAS ou GASPS

   → Aucun mouvement
   → Pas de bruit
   → Pas de souffle
   → OU respiration anormale (gasps)

   ➜ ARRÊT CARDIAQUE
   ➜ Alerter le 15
   ➜ Débuter IMMÉDIATEMENT la RCP


⚠ ATTENTION aux GASPS

Mouvements respiratoires lents, bruyants, inefficaces
Ce ne sont PAS des respirations normales
→ Considérer comme un ARRÊT CARDIAQUE


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

AUTRES DANGERS À RECHERCHER


SI LA VICTIME EST CONSCIENTE

Poser des questions :
   → "Où avez-vous mal ?"
   → "Que s'est-il passé ?"

Observer :
   → Saignement abondant (hémorragie)
   → Plaie grave
   → Brûlure étendue

Chaque danger nécessite une action immédiate
"""
            },
            {
                "id": "psc-f1-3",
                "titre": "Alerter les secours",
                "contenu": """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                    ALERTER LES SECOURS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

POURQUOI ALERTER ?

L'alerte permet de déclencher l'arrivée des secours adaptés le plus rapidement possible.


QUAND ALERTER ?

→ Victime inconsciente
→ Victime qui ne respire pas
→ Hémorragie
→ Douleur thoracique
→ Malaise
→ Brûlure grave
→ Traumatisme grave
→ Tout doute sur la gravité


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

NUMÉROS D'URGENCE


15 - SAMU (SERVICE D'AIDE MÉDICALE URGENTE)
   → Problèmes médicaux
   → Malaises, douleurs
   → Urgences vitales


18 - SAPEURS-POMPIERS
   → Incendie
   → Accidents
   → Personnes en danger


112 - NUMÉRO D'URGENCE EUROPÉEN
   → Fonctionne dans toute l'Europe
   → Accessible même sans crédit
   → Accessible même sans réseau (autre opérateur)


114 - URGENCE PAR SMS
   → Pour personnes sourdes ou malentendantes
   → Envoyer un SMS au 114


NUMÉROS SPÉCIFIQUES

17 - Police / Gendarmerie
   → Agression, vol, délit


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

QUI DOIT ALERTER ?


SI VOUS ÊTES SEUL

   → Alerter AVANT de faire les gestes de secours
   → Exception : Arrêt cardiaque enfant (RCP 1 min PUIS alerte)


SI VOUS ÊTES PLUSIEURS

   → Désigner une personne précisément
   → "Vous, en rouge, appelez le 15"
   → Pendant ce temps : commencer les gestes


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

COMMENT ALERTER ?


MESSAGE D'ALERTE - 5 POINTS ESSENTIELS


1. SE PRÉSENTER

"Je m'appelle [nom], j'appelle de [lieu]"


2. LOCALISER PRÉCISÉMENT

   → Adresse complète
   → Commune
   → Points de repère
   → Code postal
   → Étage, porte, code d'accès


3. DÉCRIRE LA SITUATION

   → Nombre de victimes
   → Ce qui s'est passé (chute, malaise, accident...)
   → Dangers persistants


4. DÉCRIRE L'ÉTAT DE LA VICTIME

   → Consciente ou inconsciente
   → Respire ou non
   → Saignement
   → Douleur
   → Signes visibles


5. DÉCRIRE LES GESTES EFFECTUÉS

   → "Je l'ai mise sur le côté"
   → "Je comprime la plaie"
   → "Je fais un massage cardiaque"


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

RÈGLES IMPORTANTES


RÉPONDRE AUX QUESTIONS

Les secours posent des questions
Répondre calmement et précisément


SUIVRE LES CONSIGNES

Le régulateur peut donner des conseils
Écouter et appliquer


NE JAMAIS RACCROCHER EN PREMIER

Attendre que le régulateur dise de raccrocher


RESTER JOIGNABLE

Laisser son téléphone allumé
Les secours peuvent rappeler pour localisation


GUIDER LES SECOURS

   → Envoyer quelqu'un à leur rencontre
   → Allumer les lumières
   → Dégager l'accès
   → Tenir les chiens


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CAS PARTICULIERS


AUTOROUTE

Appeler depuis une borne d'appel d'urgence (tous les 2 km)
La localisation est automatique
Sinon : 112 depuis le téléphone


MONTAGNE / ZONE ISOLÉE

112 (capte mieux que les autres numéros)
Indiquer coordonnées GPS si possible
Décrire l'environnement


LIEU PUBLIC (GARE, CENTRE COMMERCIAL)

Prévenir aussi le personnel de sécurité sur place
Ils ont du matériel (DAE, trousse de secours)
"""
            }
        ]
    },
    {
        "id": "psc-ch2",
        "numero": 2,
        "titre": "Obstruction des voies aériennes",
        "description": "Reconnaître une obstruction, claques dans le dos, compressions abdominales (Heimlich)",
        "icon": "Wind",
        "formation_type": "PSC",
        "fiches": [
            {
                "id": "psc-f2-1",
                "titre": "Reconnaître l'obstruction",
                "contenu": """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
            OBSTRUCTION DES VOIES AÉRIENNES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

DÉFINITION

Un corps étranger (aliment, objet) bloque les voies respiratoires et empêche la respiration.


SITUATION TYPIQUE

   → Pendant un repas
   → La personne porte la main à la gorge
   → Ne peut plus parler ni respirer


CAUSES FRÉQUENTES

→ Fausse route alimentaire (viande, os, arête)
→ Bonbon, chewing-gum
→ Petit objet (jouet chez l'enfant)


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

DEUX TYPES D'OBSTRUCTION


OBSTRUCTION PARTIELLE


SIGNES

La victime :
   ✓ TOUSSE vigoureusement
   ✓ Peut parler (même difficilement)
   ✓ Respire bruyamment (sifflement)
   ✓ Est consciente


CONDUITE À TENIR

1. ENCOURAGER À TOUSSER

   "Toussez fort !"

   La toux est le moyen le plus efficace d'expulser le corps étranger


2. NE RIEN FAIRE D'AUTRE

   Ne pas donner de claques dans le dos
   Ne pas faire de compressions abdominales


3. RESTER AVEC LA PERSONNE

   Surveiller l'évolution


4. ALERTER LE 15

   Si la toux devient inefficace
   Si la personne s'épuise
   Si passage en obstruction totale


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

OBSTRUCTION TOTALE


SIGNES

La victime :
   ✗ NE PEUT PLUS PARLER
   ✗ NE PEUT PLUS TOUSSER
   ✗ NE PEUT PLUS ÉMETTRE DE SON
   ✓ Fait le signe universel (mains à la gorge)
   ✓ Bouche ouverte
   ✓ Visage qui devient rouge puis bleu (cyanose)
   ✓ Agitation, panique


URGENCE VITALE ABSOLUE

Agir IMMÉDIATEMENT
Sans oxygène, perte de connaissance en 1 minute
Arrêt cardiaque en quelques minutes


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

QUESTIONS À POSER


"Vous étouffez ?"

Si la personne ne peut pas parler mais fait oui de la tête :
   → OBSTRUCTION TOTALE
   → AGIR IMMÉDIATEMENT
"""
            },
            {
                "id": "psc-f2-2",
                "titre": "Désobstruction adulte et enfant",
                "contenu": """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        DÉSOBSTRUCTION ADULTE ET ENFANT (> 1 an)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SÉQUENCE EN ALTERNANCE


ALTERNER :
   → 5 claques dans le dos
   → 5 compressions abdominales
   → Jusqu'à expulsion du corps étranger ou perte de connaissance


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

TECHNIQUE 1 : CLAQUES DANS LE DOS


POSITION

1. Se placer SUR LE CÔTÉ et légèrement en arrière de la victime

2. Soutenir le thorax d'une main
   → Main à plat sur le sternum

3. Pencher la victime EN AVANT
   → Tête plus basse que le thorax
   → Si possible : 90° (tronc horizontal)


GESTE

1. Donner 5 CLAQUES VIGOUREUSES entre les omoplates
   → Avec le talon de la main
   → De bas en haut
   → Sèches et franches

2. Vérifier après CHAQUE claque
   → Le corps étranger est-il sorti ?
   → Si oui : ARRÊTER
   → Si non : Continuer jusqu'à 5 claques


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

TECHNIQUE 2 : COMPRESSIONS ABDOMINALES
(Manœuvre de HEIMLICH)


UNIQUEMENT SI LES CLAQUES ONT ÉCHOUÉ


POSITION

1. Se placer DERRIÈRE la victime

2. Passer les bras autour de la taille

3. Placer un POING FERMÉ
   → Entre le nombril et le sternum
   → Au creux de l'estomac
   → Pouce contre l'abdomen

4. Placer l'autre main PAR-DESSUS le poing


GESTE

1. Tirer franchement EN ARRIÈRE et VERS LE HAUT
   → Mouvement sec
   → En "J"

2. Répéter 5 FOIS

3. Vérifier après chaque compression
   → Corps étranger expulsé ?


⚠ Ne pas appuyer sur les côtes


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ALTERNANCE


SI LES 5 COMPRESSIONS N'ONT PAS FONCTIONNÉ

RECOMMENCER :
   → 5 claques dans le dos
   → 5 compressions abdominales
   → 5 claques dans le dos
   → 5 compressions abdominales
   → Continuer jusqu'à expulsion ou perte de connaissance


DEMANDER DE L'AIDE

Faire alerter le 15 pendant que vous agissez


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SI LA VICTIME PERD CONNAISSANCE


1. ACCOMPAGNER LA CHUTE
   → L'allonger au sol délicatement

2. ALERTER LE 15 (si pas déjà fait)

3. DÉBUTER LA RCP
   → 30 compressions thoraciques
   → Regarder dans la bouche
   → Retirer le corps étranger SI VISIBLE
   → 2 insufflations
   → Continuer 30/2

Les compressions thoraciques peuvent expulser le corps étranger


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CAS PARTICULIERS


FEMME ENCEINTE (dernier trimestre)

REMPLACER les compressions abdominales par :
   → COMPRESSIONS THORACIQUES
   → Mains au milieu du sternum
   → Même technique mais sur le thorax


PERSONNE OBÈSE

Si impossible d'entourer la taille :
   → COMPRESSIONS THORACIQUES
   → Sur le sternum


NOURRISSON (< 1 an)

Technique différente (voir fiche dédiée)


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

APRÈS EXPULSION DU CORPS ÉTRANGER


1. Faire cracher le corps étranger

2. Installer la victime confortablement

3. ALERTER LE 15 systématiquement
   → Même si la personne va bien
   → Les compressions abdominales peuvent causer des lésions internes

4. Surveiller jusqu'à l'arrivée des secours
"""
            },
            {
                "id": "psc-f2-3",
                "titre": "Désobstruction nourrisson",
                "contenu": """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
            DÉSOBSTRUCTION NOURRISSON (< 1 an)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PARTICULARITÉ

⚠ PAS de compressions abdominales chez le nourrisson
⚠ Uniquement claques dans le dos + compressions thoraciques


ALTERNER :
   → 5 claques dans le dos
   → 5 compressions thoraciques


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

TECHNIQUE 1 : CLAQUES DANS LE DOS


POSITION

1. S'ASSEOIR

2. Placer le nourrisson À PLAT VENTRE
   → Sur l'avant-bras
   → Avant-bras posé sur la cuisse

3. Maintenir la tête du nourrisson
   → Main sous la mâchoire
   → Tête légèrement plus BASSE que le tronc

4. Attention : Soutenir fermement


GESTE

1. Donner 5 CLAQUES entre les omoplates
   → Avec le talon de la main
   → Geste ferme mais adapté à l'âge

2. Vérifier après chaque claque


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

TECHNIQUE 2 : COMPRESSIONS THORACIQUES


SI LES CLAQUES ONT ÉCHOUÉ


POSITION

1. RETOURNER le nourrisson SUR LE DOS
   → Sur l'autre avant-bras
   → Toujours avant-bras sur la cuisse

2. Tête légèrement plus BASSE que le tronc

3. Soutenir la nuque et la tête


GESTE

1. Placer 2 DOIGTS au centre du thorax
   → Au milieu du sternum
   → Index et majeur

2. Effectuer 5 COMPRESSIONS
   → Enfoncer le thorax d'environ 1/3 de son épaisseur
   → Comme pour un massage cardiaque
   → Mais plus lentement

3. Vérifier après chaque compression


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ALTERNANCE

RECOMMENCER :
   → 5 claques dans le dos
   → 5 compressions thoraciques
   → Continuer jusqu'à expulsion ou perte de connaissance


ALERTER LE 15

Faire alerter pendant que vous agissez


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SI LE NOURRISSON PERD CONNAISSANCE


1. Allonger sur une surface dure

2. Alerter le 15 (si pas déjà fait)

3. RCP nourrisson
   → 30 compressions (2 doigts)
   → Regarder dans la bouche
   → Retirer corps étranger si visible
   → 2 insufflations (bouche à bouche-nez)
   → Continuer


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

APRÈS EXPULSION


Même si le nourrisson va bien :

ALERTER LE 15 SYSTÉMATIQUEMENT
   → Examen médical obligatoire
   → S'assurer qu'il n'y a pas de lésion


SURVEILLER en attendant les secours
"""
            }
        ]
    },
    {
        "id": "psc-ch3",
        "numero": 3,
        "titre": "Hémorragies externes",
        "description": "Reconnaître une hémorragie, compression directe, point de compression à distance",
        "icon": "Droplet",
        "formation_type": "PSC",
        "fiches": [
            {
                "id": "psc-f3-1",
                "titre": "Reconnaître une hémorragie",
                "contenu": """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                HÉMORRAGIE EXTERNE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

DÉFINITION

Saignement abondant, visible, qui s'écoule et ne s'arrête pas spontanément.


URGENCE VITALE

Une hémorragie non contrôlée peut entraîner la mort en quelques minutes.


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

RECONNAÎTRE


SIGNES ÉVIDENTS

→ Saignement abondant qui coule
→ Flaque de sang qui s'agrandit
→ Vêtements imbibés de sang
→ Écoulement continu


⚠ Ne pas confondre avec :
   → Saignement de nez (moins grave)
   → Petite plaie qui saigne peu


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SIGNES DE GRAVITÉ


SIGNES DE CHOC HÉMORRAGIQUE

→ Pâleur importante
→ Sueurs froides
→ Respiration rapide
→ Pouls rapide et faible
→ Angoisse
→ Soif
→ Confusion, faiblesse


Ces signes montrent que la victime a perdu beaucoup de sang
"""
            },
            {
                "id": "psc-f3-2",
                "titre": "Arrêter l'hémorragie",
                "contenu": """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                ARRÊTER L'HÉMORRAGIE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PRIORITÉ ABSOLUE

ARRÊTER LE SAIGNEMENT immédiatement


PRINCIPE

COMPRESSION DIRECTE sur la plaie


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

TECHNIQUE DE COMPRESSION DIRECTE


1. SE PROTÉGER

   → Mettre des GANTS si disponibles
   → Si pas de gants : utiliser un sac plastique, linge
   → En dernier recours : mains nues (urgence vitale)


2. COMPRIMER FORTEMENT

   → Appuyer DIRECTEMENT sur la plaie
   → Avec la PAUME DE LA MAIN
   → Utiliser un linge propre, mouchoir, vêtement
   → Si rien : main directement

   PRESSION FORTE ET CONTINUE


3. ALLONGER LA VICTIME

   → Position allongée sur le dos
   → Jambes surélevées si possible (pas de douleur)


4. FAIRE ALERTER LE 15

   → Désigner quelqu'un pour appeler
   → Si seul : appeler en haut-parleur tout en comprimant


5. MAINTENIR LA COMPRESSION

   → Sans relâcher
   → Pendant 10, 15, 20 minutes ou plus
   → Jusqu'à l'arrivée des secours

   ⚠ Ne JAMAIS relâcher pour "voir si ça saigne encore"


SI VOS MAINS FATIGUENT

   → Demander un relais
   → Transition SANS relâcher la pression


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

APRÈS ARRÊT DU SAIGNEMENT


1. Couvrir la victime
   → Couverture, veste
   → Éviter le refroidissement

2. Rassurer
   → Parler calmement
   → "Les secours arrivent"

3. Surveiller
   → Conscience
   → Respiration

4. Ne rien donner à boire


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CAS PARTICULIERS


CORPS ÉTRANGER ENFONCÉ DANS LA PLAIE

   ✗ NE PAS RETIRER l'objet
   ✓ Comprimer de CHAQUE CÔTÉ de l'objet
   ✓ Stabiliser l'objet (caler avec compresses)


OBJET SECTIONNÉ (doigt, main, etc.)

   ✓ Comprimer la plaie
   ✓ Récupérer le membre sectionné
   ✓ L'envelopper dans linge propre
   ✓ Le placer dans sac plastique
   ✓ Le conserver au frais (PAS directement sur glace)
   ✓ L'amener aux secours


SAIGNEMENT DE NEZ ABONDANT

   Position assise, tête penchée EN AVANT
   Pincer les narines 10 minutes
   Si échec ou récidive : Alerter 15
"""
            }
        ]
    },
    {
        "id": "psc-ch4",
        "numero": 4,
        "titre": "Perte de connaissance",
        "description": "Reconnaître l'inconscience, libérer les voies aériennes, Position Latérale de Sécurité",
        "icon": "UserX",
        "formation_type": "PSC",
        "fiches": [
            {
                "id": "psc-f4-1",
                "titre": "Reconnaître l'inconscience",
                "contenu": """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                    PERTE DE CONNAISSANCE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

DÉFINITION

Une personne inconsciente ne répond pas et ne réagit pas, mais RESPIRE.


DANGER

Une personne inconsciente allongée sur le dos risque :
   → Chute de la langue en arrière → étouffement
   → Inhalation de vomissures → étouffement
   → Arrêt respiratoire → arrêt cardiaque


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

RECONNAÎTRE


VÉRIFIER LA CONSCIENCE

1. PARLER FORT
   "Monsieur, vous m'entendez ?"
   "Madame, ouvrez les yeux !"

2. SECOUER DOUCEMENT LES ÉPAULES
   Stimulation douce


SI PAS DE RÉACTION

   → La personne est INCONSCIENTE


APPELER À L'AIDE IMMÉDIATEMENT

   "À l'aide !"
   "Quelqu'un peut m'aider ?"


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

VÉRIFIER LA RESPIRATION


TECHNIQUE VOS : Voir, Ouïr, Sentir


1. BASCULER LA TÊTE EN ARRIÈRE
   → Main sur le front
   → Tirer doucement vers l'arrière

2. ÉLEVER LE MENTON
   → 2 doigts sous le menton
   → Soulever vers le haut

3. REGARDER, ÉCOUTER, SENTIR pendant 10 secondes
   → VOIR le ventre/thorax se soulever
   → OUÏR le bruit de l'air
   → SENTIR le souffle sur la joue


DEUX SITUATIONS POSSIBLES


LA VICTIME RESPIRE

   → Mouvements réguliers du thorax
   → Air qui sort

   ➜ Mettre en POSITION LATÉRALE DE SÉCURITÉ
   ➜ Alerter le 15
   ➜ Surveiller


LA VICTIME NE RESPIRE PAS

   → Aucun mouvement
   → Pas d'air

   ➜ ARRÊT CARDIAQUE
   ➜ Alerter le 15
   ➜ RCP immédiate
"""
            },
            {
                "id": "psc-f4-2",
                "titre": "Position Latérale de Sécurité",
                "contenu": """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        POSITION LATÉRALE DE SÉCURITÉ (PLS)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

OBJECTIF

Maintenir les voies aériennes libres pour que la victime inconsciente puisse respirer sans risque d'étouffement.


AVANTAGES DE LA PLS

→ La langue ne peut pas tomber en arrière
→ Les liquides (salive, vomissures) s'écoulent par la bouche
→ La victime peut respirer librement


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

TECHNIQUE - 5 ÉTAPES


PRÉPARATION

→ Victime allongée sur le dos
→ Retirer les lunettes si présentes
→ S'agenouiller à côté de la victime


ÉTAPE 1 : PRÉPARER LE BRAS

Placer le bras côté sauveteur à ANGLE DROIT
   → Coude plié
   → Paume de la main vers le HAUT


ÉTAPE 2 : PLACER LA MAIN OPPOSÉE

Saisir la main opposée de la victime
Placer le DOS de cette main contre sa JOUE
   → Du côté du sauveteur
Maintenir la main plaquée contre la joue


ÉTAPE 3 : REPLIER LA JAMBE OPPOSÉE

Attraper la jambe opposée
Plier le GENOU
Pied au sol à côté de l'autre genou


ÉTAPE 4 : FAIRE ROULER

Tirer sur le genou vers soi
La victime roule sur le côté
Ajuster la jambe du dessus
   → Genou à 90° (angle droit)
   → Stabilise la position


ÉTAPE 5 : AJUSTER LA TÊTE

Ouvrir la bouche de la victime
   → Avec le pouce
   → Bouche dirigée vers le SOL

Vérifier que la respiration est libre


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

APRÈS LA MISE EN PLS


1. ALERTER LE 15

Si pas encore fait


2. COUVRIR

Couverture, veste
Éviter l'hypothermie


3. SURVEILLER LA RESPIRATION

   → TOUTES LES MINUTES
   → Regarder le ventre bouger
   → Écouter les bruits respiratoires


SI LA VICTIME ARRÊTE DE RESPIRER

   → Remettre SUR LE DOS
   → Débuter la RCP


4. SI VOMISSEMENTS

Laisser s'écouler par la bouche
Nettoyer avec un doigt (utiliser un gant ou linge)


5. RASSURER

Si la victime se réveille :
   → Expliquer calmement la situation
   → L'empêcher de se lever brusquement
   → Attendre les secours


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ERREURS À ÉVITER

✗ Laisser la victime sur le dos (risque d'étouffement)
✗ Ne pas surveiller la respiration
✗ Donner à boire à une personne inconsciente
✗ La laisser seule


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CAS PARTICULIERS


FEMME ENCEINTE (> 6 mois)

Préférer le CÔTÉ GAUCHE
   → Évite la compression de la veine cave


TRAUMATISME SUSPECT

PLS seulement si nécessaire
   → Si vomissements
   → Si impossible de surveiller la respiration
Retournement prudent
"""
            }
        ]
    }
]

# Insertion des 4 premiers chapitres PSC
for ch in psc_chapters:
    db.chapters.insert_one(ch)
    print(f"  ✅ Ch{ch['numero']}: {ch['titre']}")

print(f"\n🎉 4 premiers chapitres PSC créés")
print(f"📊 Total chapitres: PSE={db.chapters.count_documents({'formation_type': 'PSE'})} | PSC={db.chapters.count_documents({'formation_type': 'PSC'})}")

client.close()
