#!/usr/bin/env python3
"""
PSE Chapitres 3 à 6 - Protection, Hygiène, Urgences vitales, Malaises
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

pse_chapters_3_6 = [
    {
        "id": "pse-ch3",
        "numero": 3,
        "titre": "Protection et sécurité",
        "description": "Principes de protection, dangers spécifiques, balisage et sécurisation de zone",
        "icon": "ShieldAlert",
        "formation_type": "PSE",
        "fiches": [
            {
                "id": "pse-f3-1",
                "titre": "La protection",
                "contenu": """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                    PRINCIPE DE PROTECTION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

RÈGLE ABSOLUE

La protection est la PREMIÈRE action avant toute intervention.

Objectifs :
   → Éviter le suraccident
   → Protéger le secouriste
   → Protéger la victime
   → Protéger les tiers


TROIS NIVEAUX DE PROTECTION


1. PROTECTION DU SECOURISTE

Le secouriste NE DOIT JAMAIS se mettre en danger.

Équipements de Protection Individuelle (EPI) obligatoires :
   → Gants à usage unique
   → Gilet haute visibilité
   → Chaussures de sécurité
   → Casque (si risque de chute d'objets)
   → Masque de protection respiratoire (si nécessaire)


2. PROTECTION DE LA ZONE

Signaler et baliser la zone d'intervention :
   → Triangle de présignalisation (30m en ville, 150m sur route)
   → Cônes ou ruban de balisage
   → Feux de détresse
   → Gyrophare si véhicule de secours

Supprimer ou isoler les dangers :
   → Couper le contact d'un véhicule
   → Fermer l'arrivée de gaz
   → Éloigner les produits dangereux
   → Interdire de fumer


3. PROTECTION DE LA VICTIME

En présence d'un danger persistant NON maîtrisable :
   → Dégagement d'urgence de la victime
   → Techniques : traction par les chevilles, traction par les poignets
   → UNIQUEMENT si danger vital immédiat et imminent

Protection contre les intempéries :
   → Couverture isothermique
   → Abri contre la pluie
   → Protection du soleil


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                    DANGERS SPÉCIFIQUES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CIRCULATION ROUTIÈRE

Mesures de protection :
   1. Garer le véhicule en sécurité (feux de détresse)
   2. Port du gilet haute visibilité AVANT de sortir
   3. Placer le triangle de présignalisation
   4. Baliser la zone (cônes si disponibles)
   5. Faire éloigner les curieux

Distance de sécurité du triangle :
   → En ville : 30 mètres
   → Sur route : 150 mètres
   → Sur autoroute : 200 mètres + appel au 18


INCENDIE

Conduite à tenir :
   → Ne PAS pénétrer dans un lieu enfumé sans protection
   → Rester à distance de sécurité (50 mètres minimum)
   → Alerter les pompiers (18 ou 112)
   → Utiliser un extincteur uniquement si :
      • Feu de petite taille
      • Vous êtes formé
      • Vous avez une issue de secours dégagée

Si victime avec vêtements en feu :
   → L'empêcher de courir
   → La faire rouler au sol
   → Étouffer les flammes (couverture, terre)


ÉLECTRICITÉ

Risques :
   → Électrocution
   → Électrisation
   → Brûlures internes graves

Conduite à tenir :
   → NE JAMAIS toucher la victime tant que le courant n'est pas coupé
   → Couper le courant au disjoncteur
   → Si impossible : éloigner la victime avec un objet isolant (bois sec)
   → Haute tension : rester à 20 mètres minimum, alerter EDF

⚠ L'eau conduit l'électricité : ne jamais arroser avec de l'eau


PRODUITS CHIMIQUES

Dangers :
   → Inhalation de vapeurs toxiques
   → Contact cutané (brûlures chimiques)
   → Ingestion

Protection :
   → Port de gants adaptés
   → Masque à cartouche si vapeurs
   → Lunettes de protection
   → Ne pas inhaler les vapeurs

Distance de sécurité : 100 mètres minimum

Alerter immédiatement les pompiers (18)


GAZ

Types de gaz :
   → Gaz naturel (odeur caractéristique ajoutée)
   → GPL (propane, butane)
   → Gaz toxiques (CO, H2S, etc.)

Conduite à tenir :
   → Évacuer la zone
   → Ne pas provoquer d'étincelle (interrupteur, téléphone)
   → Aérer si possible (ouvrir portes et fenêtres à distance)
   → Ne pas fumer
   → Appeler les pompiers depuis l'extérieur


EFFONDREMENT

Dangers :
   → Chute de débris
   → Effondrement secondaire
   → Gaz, électricité

Conduite à tenir :
   → Ne pas s'aventurer sous une structure instable
   → Attendre les équipes spécialisées (GRIMP)
   → Établir un périmètre de sécurité
   → Empêcher l'accès
"""
            },
            {
                "id": "pse-f3-2",
                "titre": "Dégagement d'urgence",
                "contenu": """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                DÉGAGEMENT D'URGENCE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PRINCIPE

Le dégagement d'urgence est une manœuvre EXCEPTIONNELLE réalisée UNIQUEMENT en présence d'un danger VITAL, IMMÉDIAT et NON CONTRÔLABLE.


QUAND DÉGAGER ?

Danger vital imminent :
   → Incendie ou explosion imminente
   → Effondrement en cours
   → Gaz toxique
   → Noyade en cours

⚠ DANGER : Cette manœuvre peut aggraver un traumatisme du rachis


QUAND NE PAS DÉGAGER ?

✗ Victime traumatisée en zone sécurisée
✗ Possibilité de supprimer le danger autrement
✗ Arrivée imminente de moyens spécialisés
✗ Danger maîtrisable


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

TECHNIQUES DE DÉGAGEMENT


TRACTION PAR LES CHEVILLES

Position :
   1. Saisir fermement les deux chevilles
   2. Se positionner dans l'axe du corps
   3. Reculer en tirant

Avantages : Rapide, maintien relatif de l'axe
Inconvénients : Difficile sur longue distance


TRACTION PAR LES POIGNETS

Position :
   1. Passer derrière la victime
   2. Glisser les mains sous les aisselles
   3. Saisir les poignets croisés sur la poitrine
   4. Se relever et reculer en tirant

Avantages : Bonne prise, contrôle de la tête
Inconvénients : Demande plus de force


TRACTION PAR LES VÊTEMENTS

En dernier recours :
   Saisir le col de la veste ou le haut du vêtement
   Attention à ne pas étrangler la victime


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

POINTS CLÉS

Distance minimale : Dégager sur la distance STRICTEMENT nécessaire

Axe du corps : Maintenir l'alignement tête-cou-tronc autant que possible

Rapidité : Effectuer le geste rapidement mais sans brutalité

Bilan immédiat : Réaliser un bilan primaire dès que la victime est en sécurité
"""
            }
        ]
    },
    {
        "id": "pse-ch4",
        "numero": 4,
        "titre": "Hygiène et asepsie",
        "description": "Hygiène des mains, utilisation des EPI, prévention des infections, gestion des déchets",
        "icon": "Droplets",
        "formation_type": "PSE",
        "fiches": [
            {
                "id": "pse-f4-1",
                "titre": "Hygiène des mains",
                "contenu": """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                    LAVAGE DES MAINS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

POURQUOI ?

Les mains sont le PRINCIPAL vecteur de transmission des infections.

80% des infections sont transmises par les mains.


QUAND SE LAVER LES MAINS ?


AVANT :
   → Chaque intervention
   → Contact avec une victime
   → Manipulation de matériel stérile
   → Prise de repas


APRÈS :
   → Contact avec une victime
   → Contact avec du sang ou liquides biologiques
   → Retrait des gants
   → Utilisation des toilettes
   → Intervention terminée


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

TECHNIQUE DE LAVAGE À L'EAU ET AU SAVON

Durée totale : 30 à 60 secondes minimum


ÉTAPES :

1. Mouiller les mains à l'eau tiède

2. Appliquer du savon liquide (une pression)

3. Frictionner méthodiquement :
   → Paume contre paume
   → Dos de la main
   → Espaces interdigitaux
   → Dos des doigts
   → Pouces
   → Poignets
   → Ongles (avec brosse si très sales)

4. Rincer abondamment à l'eau courante

5. Sécher avec un essuie-mains à usage unique

6. Fermer le robinet avec l'essuie-mains (pas avec les mains propres)


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

FRICTION HYDRO-ALCOOLIQUE (SHA)

QUAND L'UTILISER ?

✓ Mains visiblement propres
✓ Pas d'accès à un point d'eau
✓ Entre deux interventions rapprochées
✓ Complément au lavage des mains


QUAND NE PAS L'UTILISER ?

✗ Mains visiblement souillées
✗ Contact avec du sang ou liquides biologiques
✗ Après utilisation des toilettes
✗ Avant de manger


TECHNIQUE :

Durée : 30 secondes minimum jusqu'à séchage complet

1. Appliquer une dose de SHA dans le creux de la main

2. Frictionner selon la même technique que le lavage :
   → Paumes
   → Dos des mains
   → Espaces interdigitaux
   → Dos des doigts
   → Pouces
   → Poignets

3. Continuer jusqu'à séchage complet

4. Ne pas essuyer, ne pas rincer


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

RÈGLES D'OR

Ongles courts et propres (pas de vernis)
Pas de bijoux aux mains et poignets (alliance simple tolérée)
Pas de faux ongles
Manches courtes ou retroussées
"""
            },
            {
                "id": "pse-f4-2",
                "titre": "Équipements de protection individuelle",
                "contenu": """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
            ÉQUIPEMENTS DE PROTECTION INDIVIDUELLE (EPI)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


LES GANTS


TYPES DE GANTS :

Gants d'examen (latex, nitrile, vinyle) :
   → Usage unique
   → Protection contre les liquides biologiques
   → À usage unique

Gants de protection (épais) :
   → Manipulation d'objets tranchants
   → Désincarcération
   → Réutilisables après nettoyage


QUAND PORTER DES GANTS ?

TOUJOURS lors de :
   → Contact avec du sang
   → Contact avec tous liquides biologiques (salive, urines, selles, vomissures)
   → Contact avec une peau lésée
   → Manipulation de matériel souillé
   → Toucher des muqueuses


TECHNIQUE DE PORT :

1. Se laver les mains AVANT de mettre les gants

2. Mettre les gants sans toucher l'extérieur

3. Changer les gants :
   → Entre chaque victime
   → Si déchirés ou souillés
   → Après contact avec une surface contaminée

4. Retrait des gants contaminés :
   → Pincer le premier gant par l'extérieur au niveau du poignet
   → Retirer en le retournant
   → Glisser les doigts sous le second gant (côté peau)
   → Retirer en retournant par-dessus le premier
   → Jeter dans un sac DASRI

5. Se laver les mains APRÈS le retrait


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

MASQUES DE PROTECTION


TYPES DE MASQUES :

Masque chirurgical :
   → Protège la victime des projections du secouriste
   → Durée : 3 à 4 heures maximum

Masque FFP2 :
   → Protège le secouriste des agents infectieux aéroportés
   → Tuberculose, COVID-19, grippe
   → Durée : 8 heures maximum
   → Doit être ajusté (test d'étanchéité)


QUAND PORTER UN MASQUE ?

→ Suspicion de maladie infectieuse respiratoire
→ Ventilation au BAVU (masque + lunettes)
→ Victime qui tousse ou éternue
→ Gestes invasifs (aspiration)


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LUNETTES DE PROTECTION

QUAND LES PORTER ?

→ Risque de projection de sang ou liquides biologiques
→ Ventilation au BAVU
→ Aspiration de sécrétions
→ Accouchement


AUTRES EPI

Surblouse ou tablier :
   → Contact prolongé avec liquides biologiques
   → Accouchement

Surchaussures :
   → Milieu très contaminé
   → Rarement nécessaires en secourisme


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PRINCIPES GÉNÉRAUX

Les EPI doivent être :
   → Facilement accessibles
   → En nombre suffisant
   → Aux bonnes tailles
   → Vérifiés régulièrement (dates de péremption)

Ordre de retrait des EPI (du plus contaminé au moins contaminé) :
   1. Gants
   2. Surblouse/tablier
   3. Lunettes
   4. Masque
   5. Lavage des mains
"""
            },
            {
                "id": "pse-f4-3",
                "titre": "Gestion des déchets",
                "contenu": """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                GESTION DES DÉCHETS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CATÉGORIES DE DÉCHETS


DASRI (Déchets d'Activités de Soins à Risques Infectieux)

Conteneur : Boîte jaune rigide

Déchets à y jeter :
   → Aiguilles, seringues
   → Lames de bistouri
   → Tout objet piquant ou tranchant souillé
   → Compresses imbibées de sang
   → Pansements souillés
   → Gants souillés de sang

⚠ Ne JAMAIS recapuchonner une aiguille


DASRI MOUS

Conteneur : Sac jaune

Déchets à y jeter :
   → Matériel souillé non piquant
   → Tubulures
   → Masques usagés
   → Champs opératoires
   → Protection de défibrillateur


DÉCHETS MÉNAGERS

Conteneur : Sac noir

Déchets à y jeter :
   → Emballages non souillés
   → Gants propres non utilisés
   → Matériel d'emballage


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

RÈGLES DE TRI

Le tri s'effectue au plus près du soin
Ne jamais remplir un conteneur DASRI à plus de 3/4
Fermer immédiatement le conteneur une fois plein
Ne jamais transvaser des déchets
En cas de doute : considérer comme DASRI


TRAÇABILITÉ

Les conteneurs DASRI doivent être étiquetés :
   → Date
   → Service
   → Nom du responsable


ÉLIMINATION

Les DASRI sont incinérés dans des filières spécialisées
Ne jamais jeter de DASRI dans une poubelle ordinaire
Circuit : Conteneur → Collecte spécialisée → Incinération
"""
            }
        ]
    },
    {
        "id": "pse-ch5",
        "numero": 5,
        "titre": "Urgences vitales",
        "description": "Arrêt cardiaque, obstruction des voies aériennes, hémorragies, inconscience",
        "icon": "Heart",
        "formation_type": "PSE",
        "fiches": [
            {
                "id": "pse-f5-1",
                "titre": "Arrêt cardiaque",
                "contenu": """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                    ARRÊT CARDIAQUE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

DÉFINITION

L'arrêt cardiaque (AC) est l'interruption brutale et soudaine de la circulation sanguine.

En France : 50 000 arrêts cardiaques par an
Taux de survie : 5 à 7% (peut atteindre 30% si RCP précoce + DAE)


SIGNES DE RECONNAISSANCE

La victime :
   → Ne répond pas
   → Ne réagit pas aux stimulations
   → Ne respire pas ou respiration anormale (gasps)
   → Absence de pouls carotidien (vérifier max 10 secondes)


⚠ ATTENTION aux GASPS : mouvements respiratoires anormaux, lents et inefficaces
Ce ne sont PAS des respirations normales → Considérer comme un AC


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CHAÎNE DE SURVIE

La survie dépend de 4 maillons :

1. ALERTE PRÉCOCE (15, 18, 112)

2. RCP IMMÉDIATE (massage cardiaque)

3. DÉFIBRILLATION PRÉCOCE (DAE)

4. PRISE EN CHARGE MÉDICALISÉE


Chaque minute sans RCP diminue les chances de survie de 10%


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CONDUITE À TENIR


1. VÉRIFIER LA CONSCIENCE

Parler fort : "Monsieur, vous m'entendez ?"
Secouer doucement les épaules
Si pas de réponse → Victime inconsciente


2. ALERTER OU FAIRE ALERTER

Si vous êtes seul :
   → Appeler le 15 ou 18 en haut-parleur
   → Demander un DAE

Si vous êtes à plusieurs :
   → Une personne alerte
   → Une autre va chercher le DAE
   → Vous commencez la RCP


3. VÉRIFIER LA RESPIRATION

Basculer la tête en arrière
Élever le menton
Regarder, écouter, sentir pendant 10 secondes maximum

Si absence de respiration ou gasps → Arrêt cardiaque confirmé


4. DÉBUTER LA RCP IMMÉDIATEMENT

Position du secouriste :
   → À genoux à côté de la victime
   → Épaules à la verticale du sternum

Position des mains :
   → Talon d'une main au centre du thorax
   → Deuxième main par-dessus, doigts entrecroisés
   → Bras tendus

Compressions thoraciques :
   → Fréquence : 100 à 120 compressions par minute
   → Profondeur : 5 à 6 cm chez l'adulte
   → Laisser le thorax reprendre sa position entre chaque compression
   → Minimiser les interruptions


5. INSUFFLATIONS (si formé et capable)

Après 30 compressions : 2 insufflations

Technique :
   → Basculer la tête en arrière, élever le menton
   → Pincer le nez
   → Insuffler pendant 1 seconde (voir le thorax se soulever)
   → Laisser l'air sortir
   → Répéter une 2ème fois

Si vous ne savez pas ou ne pouvez pas : Faire uniquement les compressions


RYTHME : 30 compressions / 2 insufflations


6. UTILISER LE DAE DÈS QU'IL ARRIVE

Allumer le DAE
Suivre les instructions vocales
Dénuder le thorax
Coller les électrodes selon le schéma
Ne toucher personne pendant l'analyse
Si choc conseillé :
   → S'écarter
   → Appuyer sur le bouton de choc
   → Reprendre immédiatement la RCP

Continuer jusqu'à :
   → La victime reprend conscience et respire normalement
   → Les secours médicalisés arrivent et prennent le relais
   → Vous êtes épuisé


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CAS PARTICULIERS


ENFANT (1 à 8 ans)

Compressions : 1 ou 2 mains selon la corpulence
Profondeur : 1/3 de l'épaisseur du thorax (environ 5 cm)
DAE : Électrodes pédiatriques si disponibles


NOURRISSON (< 1 an)

Compressions : 2 doigts au centre du thorax
Profondeur : 4 cm
Insufflations : Bouche à bouche-nez
Rythme : 15 compressions / 2 insufflations (si 2 secouristes)


FEMME ENCEINTE

RCP standard
Surélever la hanche droite (coussin, vêtements) pour déplacer l'utérus


TRAUMATISÉ

RCP standard
Ne pas craindre d'aggraver les lésions : la victime est déjà en arrêt cardiaque


NOYÉ

Commencer par 5 insufflations avant les compressions
Puis RCP standard
"""
            }
        ]
    },
    {
        "id": "pse-ch6",
        "numero": 6,
        "titre": "Malaises et affections spécifiques",
        "description": "Malaise vagal, AVC, infarctus, crise d'asthme, diabète",
        "icon": "Activity",
        "formation_type": "PSE",
        "fiches": [
            {
                "id": "pse-f6-1",
                "titre": "Reconnaître un malaise",
                "contenu": """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                    DÉFINITION DU MALAISE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Un malaise est une sensation pénible traduisant un trouble du fonctionnement de l'organisme, sans pouvoir en identifier immédiatement la cause.


MANIFESTATIONS POSSIBLES

→ Sensation de faiblesse
→ Vertiges, étourdissements
→ Nausées, vomissements
→ Pâleur, sueurs
→ Douleur thoracique
→ Essoufflement
→ Troubles visuels
→ Troubles de la parole
→ Perte de connaissance brève


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CONDUITE À TENIR GÉNÉRALE


1. INSTALLER LA VICTIME

Position adaptée selon les symptômes :

Malaise avec pâleur, sueurs (malaise vagal) :
   → Allonger la victime
   → Surélever les jambes

Gêne respiratoire, douleur thoracique :
   → Position demi-assise

Nausées, vomissements :
   → Position latérale de sécurité si inconsciente
   → Pencher en avant si consciente


2. DESSERRER LES VÊTEMENTS

Col, cravate, ceinture


3. RASSURER LA VICTIME

Parler calmement
Expliquer ce que l'on fait


4. INTERROGER

Méthode SAMPLE :
   → Que ressentez-vous ?
   → Avez-vous des antécédents ?
   → Prenez-vous des médicaments ?
   → Était-ce déjà arrivé ?


5. SURVEILLER

Conscience
Respiration
Pouls
Coloration


6. ALERTER LE 15

Systématiquement si :
   → Malaise prolongé (> 5 minutes)
   → Douleur thoracique
   → Gêne respiratoire
   → Trouble de la parole
   → Faiblesse d'un côté du corps
   → Antécédents cardiaques
   → Personne âgée
   → Diabétique
   → Récidive du malaise


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SIGNES DE GRAVITÉ

⚠ ALERTER IMMÉDIATEMENT LE 15 SI :

→ Douleur thoracique (suspicion infarctus)
→ Trouble de la parole ou paralysie (suspicion AVC)
→ Difficulté respiratoire importante
→ Perte de connaissance même brève
→ Convulsions
→ Sueurs profuses + pâleur extrême
→ Douleur abdominale violente
→ Antécédents cardiaques connus
"""
            },
            {
                "id": "pse-f6-2",
                "titre": "AVC et infarctus",
                "contenu": """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
            ACCIDENT VASCULAIRE CÉRÉBRAL (AVC)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

DÉFINITION

Interruption brutale de la circulation sanguine dans une partie du cerveau.

Deux types :
   → AVC ischémique (80%) : obstruction d'une artère cérébrale
   → AVC hémorragique (20%) : rupture d'une artère cérébrale


RECONNAISSANCE : MÉTHODE FAST


F = FACE (Visage)
   Demander à la personne de sourire
   → Un côté du visage ne suit pas (asymétrie)

A = ARM (Bras)
   Demander de lever les deux bras
   → Un bras ne peut pas se lever ou retombe

S = SPEECH (Parole)
   Demander de répéter une phrase simple
   → Parole incompréhensible ou impossible

T = TIME (Temps)
   Si un seul de ces signes : APPELER LE 15 IMMÉDIATEMENT


AUTRES SIGNES POSSIBLES

→ Perte de vision d'un œil
→ Troubles de l'équilibre
→ Maux de tête intenses et brutaux
→ Troubles de la compréhension


CONDUITE À TENIR

1. Alerter le 15 IMMÉDIATEMENT (urgence absolue)

2. Noter l'heure de début des symptômes (crucial pour le traitement)

3. Installer en position :
   → Demi-assise si conscient
   → PLS si inconscient mais respire

4. Ne rien donner à boire ni à manger

5. Rassurer et surveiller

6. Noter les traitements en cours (anticoagulants +++)


⏱ CHAQUE MINUTE COMPTE
Plus la prise en charge est rapide, moins il y aura de séquelles.


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                    INFARCTUS DU MYOCARDE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

DÉFINITION

Obstruction d'une artère coronaire entraînant une souffrance du muscle cardiaque.


SIGNES TYPIQUES

Douleur thoracique :
   → Intense, en étau, pesanteur
   → Située au centre du thorax
   → Irradiant vers :
      • Mâchoire
      • Épaule et bras gauche
      • Dos (entre les omoplates)
   → Durant plus de 15 minutes
   → Non soulagée par le repos

Signes associés :
   → Angoisse importante (sentiment de mort imminente)
   → Sueurs profuses
   → Pâleur
   → Nausées, vomissements
   → Essoufflement


FORMES ATYPIQUES (surtout chez la femme, diabétique, personne âgée)

→ Douleur abdominale
→ Fatigue intense
→ Essoufflement isolé
→ Malaise


CONDUITE À TENIR

1. Alerter le 15 IMMÉDIATEMENT

2. Mettre au repos absolu :
   → Position demi-assise
   → Desserrer les vêtements
   → Pas d'effort

3. Si traitement par trinitrine prescrit :
   → Aider la victime à le prendre
   → 1 pulvérisation sous la langue
   → Renouveler après 5 minutes si douleur persiste (max 3 fois)

4. Si disponible et victime consciente :
   → Donner 250 mg d'aspirine à croquer (sauf allergie)
   → Demander accord du SAMU

5. Rassurer, parler calmement

6. Surveiller et préparer le DAE (à proximité)

7. Si perte de connaissance :
   → Vérifier respiration
   → RCP si arrêt cardiaque


⚠ NE JAMAIS minimiser les symptômes
⚠ NE PAS laisser la victime conduire
⚠ NE PAS donner à boire ni à manger
"""
            }
        ]
    }
]

print("\n📚 Insertion des chapitres PSE 3-6...")
for ch in pse_chapters_3_6:
    db.chapters.insert_one(ch)
    print(f"  ✅ Ch{ch['numero']}: {ch['titre']}")

print(f"\n🎉 {len(pse_chapters_3_6)} chapitres PSE créés")
print(f"📊 Total dans la base : {db.chapters.count_documents({})} chapitres")

client.close()
