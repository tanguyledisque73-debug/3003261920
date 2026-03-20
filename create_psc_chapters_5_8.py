#!/usr/bin/env python3
"""
Création des chapitres PSC1 5 à 8
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

print("📚 Création des chapitres PSC1 5-8...")

psc_chapters = [
    {
        "id": "psc-ch5",
        "numero": 5,
        "titre": "Arrêt cardiaque et défibrillateur",
        "description": "Reconnaître un arrêt cardiaque, réanimation cardio-pulmonaire, utilisation du DAE",
        "icon": "Heart",
        "formation_type": "PSC",
        "fiches": [
            {
                "id": "psc-f5-1",
                "titre": "Reconnaître l'arrêt cardiaque",
                "contenu": """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                    ARRÊT CARDIAQUE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

DÉFINITION

Le cœur ne fonctionne plus. Il ne pompe plus de sang vers le cerveau et les organes.


URGENCE VITALE ABSOLUE

Chaque minute compte
Sans intervention : MORT en 10 minutes


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

RECONNAÎTRE L'ARRÊT CARDIAQUE


LES 2 SIGNES OBLIGATOIRES

1. La victime est INCONSCIENTE
   → Ne répond pas
   → Ne réagit pas aux stimulations

ET

2. La victime NE RESPIRE PAS ou respiration anormale (gasps)
   → Aucun mouvement thoracique
   → Pas de souffle
   → OU respiration lente, bruyante, inefficace


CES DEUX SIGNES = ARRÊT CARDIAQUE


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CONDUITE À TENIR IMMÉDIATE


1. FAIRE ALERTER LE 15

   Désigner quelqu'un :
   "Vous, en rouge, appelez le 15 et revenez !"


2. FAIRE APPORTER UN DÉFIBRILLATEUR (DAE)

   Désigner une autre personne :
   "Vous, allez chercher un défibrillateur !"


3. DÉBUTER IMMÉDIATEMENT LA RCP

   NE PAS ATTENDRE
   Chaque seconde compte


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

POURQUOI LA RCP EST VITALE ?


SANS RCP

   → Le cerveau meurt en 5 minutes
   → Lésions irréversibles


AVEC RCP IMMÉDIATE

   → Maintient un peu de circulation
   → Oxygène au cerveau
   → Chance de survie multipliée par 3 à 4


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ATTENTION AUX GASPS


DÉFINITION

Mouvements respiratoires anormaux :
   → Lents
   → Irréguliers
   → Bruyants (soupirs)
   → Inefficaces


⚠ LES GASPS NE SONT PAS UNE RESPIRATION NORMALE

➜ Considérer comme un ARRÊT CARDIAQUE
➜ Débuter la RCP
"""
            },
            {
                "id": "psc-f5-2",
                "titre": "Réanimation cardio-pulmonaire (RCP)",
                "contenu": """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        RÉANIMATION CARDIO-PULMONAIRE (RCP)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

OBJECTIF

Remplacer le cœur et les poumons pour maintenir un minimum de circulation sanguine vers le cerveau.


SÉQUENCE

30 COMPRESSIONS THORACIQUES
+
2 INSUFFLATIONS

Répéter sans arrêt jusqu'à :
   → Arrivée du défibrillateur
   → Arrivée des secours
   → La victime reprend une respiration normale


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LES COMPRESSIONS THORACIQUES


POSITION DE LA VICTIME

→ Sur le DOS
→ Sur un SOL DUR
→ Si sur un lit : descendre au sol


POSITION DU SAUVETEUR

→ À GENOUX à côté de la victime
→ Épaules à la verticale du thorax


PLACEMENT DES MAINS

1. Repérer le CENTRE DU THORAX
   → Entre les deux seins
   → Partie inférieure du sternum

2. Placer le TALON d'une main sur le centre du thorax
   → Pas sur les côtes
   → Pas sur le ventre

3. Placer l'AUTRE MAIN par-dessus
   → Doigts ENTRELACÉS ou RELEVÉS
   → Ne pas toucher les côtes

4. Bras TENDUS
   → Coudes bloqués


TECHNIQUE DE COMPRESSION

1. Appuyer VERTICALEMENT
   → Utiliser le poids du corps
   → Pas la force des bras

2. ENFONCER de 5 à 6 cm
   → Adulte : 5-6 cm
   → Enfant : environ 5 cm

3. RELÂCHER COMPLÈTEMENT
   → Laisser le thorax reprendre sa position
   → NE PAS décoller les mains

4. RYTHME : 100 à 120 compressions par minute
   → Environ 2 par seconde
   → Rythme de la chanson "Stayin' Alive"


COMPTER À HAUTE VOIX

1, 2, 3, 4, 5... jusqu'à 30


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LES INSUFFLATIONS


APRÈS LES 30 COMPRESSIONS


TECHNIQUE

1. BASCULER LA TÊTE EN ARRIÈRE
   → Main sur le front

2. ÉLEVER LE MENTON
   → 2 doigts sous le menton

3. PINCER LE NEZ
   → Fermer complètement

4. INSUFFLER
   → Bouche grande ouverte
   → Recouvrir la bouche de la victime
   → Souffler progressivement (1 seconde)
   → Regarder le thorax se soulever

5. SE REDRESSER
   → Laisser l'air ressortir
   → Regarder le thorax s'abaisser

6. INSUFFLER UNE 2ᵉ FOIS

7. REPRENDRE IMMÉDIATEMENT 30 compressions


DURÉE D'UNE INSUFFLATION

1 seconde par insufflation
Pas de grandes inspirations


SI LE THORAX NE SE SOULÈVE PAS

   → Vérifier la bascule de la tête
   → Vérifier l'élévation du menton
   → Vérifier que le nez est pincé
   → Souffler un peu plus fort


SI LES INSUFFLATIONS NE FONCTIONNENT PAS

   → Reprendre les compressions
   → Ne pas perdre de temps


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

RYTHME DE LA RCP


CYCLE COMPLET

30 compressions (environ 18 secondes)
+
2 insufflations (environ 5 secondes)

Répéter, répéter, répéter...


NE PAS S'ARRÊTER

Continuer jusqu'à :
   → Arrivée du DAE
   → Arrivée des secours
   → La victime bouge, respire


RELAIS

Si vous êtes fatigué :
   → Demander un relais toutes les 2 minutes
   → Changer RAPIDEMENT (< 5 secondes)


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CAS PARTICULIERS


SI VOUS NE POUVEZ PAS FAIRE D'INSUFFLATIONS

   → Bouche blessée
   → Vomissements
   → Répulsion

   ➜ Faire UNIQUEMENT les compressions thoraciques
   ➜ Sans interruption
   ➜ C'est mieux que rien


NOURRISSON (< 1 an)

   → 2 doigts pour les compressions
   → Enfoncer d'1/3 de l'épaisseur du thorax
   → Insufflations : bouche à bouche-nez


ENFANT (1 à 8 ans)

   → 1 ou 2 mains selon la taille
   → Enfoncer d'environ 5 cm
"""
            },
            {
                "id": "psc-f5-3",
                "titre": "Utilisation du défibrillateur (DAE)",
                "contenu": """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
            DÉFIBRILLATEUR AUTOMATISÉ EXTERNE (DAE)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

DÉFINITION

Appareil qui analyse le rythme cardiaque et délivre un choc électrique si nécessaire pour relancer le cœur.


EFFICACITÉ

Défibrillation dans les 3 premières minutes :
   → 50 à 75 % de survie

Défibrillation après 10 minutes :
   → < 5 % de survie


⏱ CHAQUE MINUTE COMPTE


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

OÙ TROUVER UN DAE ?


LIEUX PUBLICS

→ Gares
→ Aéroports
→ Centres commerciaux
→ Mairies
→ Stades, gymnases
→ Grandes entreprises


SIGNALÉTIQUE

Panneau vert avec un cœur et un éclair


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

UTILISATION DU DAE


PRINCIPE

Le DAE guide vocalement et visuellement
Suivre les instructions de l'appareil


ÉTAPES


1. METTRE EN MARCHE

   → Ouvrir le couvercle
   → OU appuyer sur le bouton vert


2. DÉNUDER LE THORAX

   → Enlever tous les vêtements
   → Si poitrine mouillée : sécher
   → Si poitrine velue : raser si nécessaire (rasoir dans le DAE)


3. COLLER LES ÉLECTRODES

   L'appareil indique où les placer

   ÉLECTRODE 1 : En haut à droite sous la clavicule
   ÉLECTRODE 2 : En bas à gauche sous le sein

   → Bien appuyer pour coller
   → Sur peau NUE
   → Pas sur les seins


4. LAISSER LE DAE ANALYSER

   ⚠ NE PAS TOUCHER LA VICTIME pendant l'analyse

   "Analyse en cours, ne pas toucher la victime"


5. SUIVRE LES INSTRUCTIONS


   SI CHOC CONSEILLÉ

   "Choc conseillé. Écartez-vous."

   → S'ÉCARTER de la victime
   → Vérifier que personne ne la touche
   → Appuyer sur le bouton ORANGE (choc)
   → OU le choc se déclenche automatiquement

   → REPRENDRE IMMÉDIATEMENT la RCP (30:2)


   SI CHOC NON CONSEILLÉ

   "Choc non conseillé. Poursuivre la réanimation."

   → REPRENDRE IMMÉDIATEMENT la RCP


6. CONTINUER

   → Le DAE indique quand s'arrêter pour une nouvelle analyse
   → Suivre les instructions jusqu'à l'arrivée des secours


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

RÈGLES IMPORTANTES


NE JAMAIS ÉTEINDRE LE DAE

   Laisser branché jusqu'à l'arrivée des secours


NE JAMAIS TOUCHER LA VICTIME

   → Pendant l'analyse
   → Pendant le choc


NE PAS DÉCOLLER LES ÉLECTRODES

   Rester en place même si la victime reprend conscience


REPRENDRE LA RCP IMMÉDIATEMENT APRÈS LE CHOC

   Ne pas attendre
   30:2


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CAS PARTICULIERS


VICTIME MOUILLÉE (piscine, pluie)

   → Sécher le thorax avant de coller les électrodes


VICTIME AVEC STIMULATEUR CARDIAQUE (PACEMAKER)

   Bosse sous la peau
   → Coller l'électrode à au moins 8 cm de la bosse


PATCH MÉDICAMENTEUX

   → Enlever le patch
   → Nettoyer la peau


POITRINE VELUE

   → Raser rapidement (rasoir dans le DAE)
   → OU arracher la première paire d'électrodes (les poils partent avec)
   → Coller une deuxième paire


ENFANT (1 à 8 ans)

   → Utiliser les électrodes PÉDIATRIQUES si disponibles
   → OU position antéro-postérieure (1 devant, 1 dans le dos)


NOURRISSON (< 1 an)

   → Utiliser les électrodes pédiatriques
   → Position antéro-postérieure


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SI LA VICTIME REPREND CONNAISSANCE


SIGNES

   → Ouvre les yeux
   → Bouge
   → Respire normalement


CONDUITE À TENIR

1. LAISSER les électrodes en place
2. LAISSER le DAE allumé
3. Mettre en POSITION LATÉRALE DE SÉCURITÉ
4. SURVEILLER la respiration
5. Attendre les secours


SI LA VICTIME ARRÊTE À NOUVEAU DE RESPIRER

   → Remettre sur le dos
   → Reprendre la RCP
   → Le DAE analysera à nouveau
"""
            }
        ]
    },
    {
        "id": "psc-ch6",
        "numero": 6,
        "titre": "Malaises",
        "description": "Reconnaître un malaise, interroger, mettre au repos, surveiller",
        "icon": "Thermometer",
        "formation_type": "PSC",
        "fiches": [
            {
                "id": "psc-f6-1",
                "titre": "Reconnaître un malaise",
                "contenu": """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                        MALAISE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

DÉFINITION

Sensation pénible traduisant un trouble du fonctionnement de l'organisme, sans pouvoir en identifier obligatoirement la cause.


SIGNES VARIÉS

La victime peut présenter :
   → Sensation de faiblesse
   → Vertiges
   → Sueurs
   → Pâleur
   → Nausées
   → Douleurs
   → Malaise général


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

MALAISES GRAVES À RECONNAÎTRE


SIGNES DE GRAVITÉ

→ Douleur dans la poitrine (oppression, serrement)
→ Douleur irradiant dans le bras gauche, la mâchoire
→ Difficulté à respirer
→ Difficulté à parler
→ Paralysie d'un membre, du visage (AVC)
→ Sueurs abondantes
→ Pâleur extrême
→ Angoisse importante


CES SIGNES = URGENCE VITALE

Alerter le 15 immédiatement


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

MALAISE CARDIAQUE (INFARCTUS)


SIGNES TYPIQUES

→ Douleur dans la POITRINE
   • Serrement, écrasement
   • Comme un étau
   • Persistante (> 5 minutes)

→ Irradiation de la douleur
   • Bras gauche
   • Mâchoire
   • Dos, épaules

→ Sueurs froides
→ Pâleur
→ Nausées
→ Angoisse


⏱ AGIR VITE SAUVE LE CŒUR

Chaque minute compte pour limiter les dégâts


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ACCIDENT VASCULAIRE CÉRÉBRAL (AVC)


RECONNAÎTRE AVEC LE TEST "VITE"


V - VISAGE paralysé
   → Demander de sourire
   → Bouche déformée d'un côté

I - IMPOSSIBILITÉ de bouger un bras
   → Demander de lever les 2 bras
   → Un bras retombe

T - TROUBLE de la parole
   → Demander de répéter une phrase simple
   → Mots déformés, incompréhensibles

E - EXTRÊME urgence
   → Appeler le 15


AUTRES SIGNES

→ Perte de la vision d'un œil
→ Maux de tête violents et soudains
→ Troubles de l'équilibre


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

AUTRES MALAISES


HYPOGLYCÉMIE (manque de sucre)

Signes :
   → Sueurs
   → Pâleur
   → Tremblements
   → Faim
   → Confusion
   → Faiblesse

Fréquent chez les diabétiques


MALAISE VAGAL (chute de tension)

Signes :
   → Sensation de malaise
   → Vision floue, voile noir
   → Sueurs
   → Nausées
   → Pâleur
   → Peut aller jusqu'à la perte de connaissance brève


CRISE D'ÉPILEPSIE

Signes :
   → Convulsions
   → Raidissement
   → Perte de connaissance
   → Peut mordre la langue, baver
"""
            },
            {
                "id": "psc-f6-2",
                "titre": "Conduite à tenir face à un malaise",
                "contenu": """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
            CONDUITE À TENIR FACE À UN MALAISE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ÉTAPES À SUIVRE


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. METTRE LA PERSONNE AU REPOS


POSITION ADAPTÉE

→ ASSEOIR ou ALLONGER la personne

→ Si malaise général, faiblesse :
   • Allonger sur le dos
   • Surélever les jambes

→ Si douleur thoracique, difficulté à respirer :
   • Position DEMI-ASSISE
   • Tête et dos surélevés

→ Si nausées, vomissements :
   • Position demi-assise
   • Bassin à proximité


DESSERRER LES VÊTEMENTS

   → Cravate
   → Col
   → Ceinture


AÉRER

   → Ouvrir une fenêtre
   → Faire reculer les curieux


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

2. INTERROGER LA PERSONNE


POSER DES QUESTIONS


"Que ressentez-vous ?"
"Où avez-vous mal ?"
"Depuis quand ?"
"Avez-vous déjà eu ce type de malaise ?"
"Prenez-vous des médicaments ?"
"Êtes-vous diabétique ? Cardiaque ?"


RECHERCHER DES INDICES

→ Carte de diabétique
→ Carte de personne cardiaque
→ Médicaments à proximité
→ Bracelet médical


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

3. ALERTER OU NON ?


ALERTER LE 15 SI

→ Premier malaise
→ Malaise qui ne passe pas
→ Signes de gravité :
   • Douleur thoracique
   • Difficulté à respirer
   • Difficulté à parler
   • Paralysie
   • Sueurs abondantes

→ Aggravation de l'état
→ Doute sur la gravité


NE PAS ALERTER SI

→ Malaise habituel connu
→ Amélioration rapide
→ Personne habituée à gérer son malaise (ex: diabétique qui se ressucre)

MAIS rester vigilant et surveiller


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

4. GESTES SPÉCIFIQUES


HYPOGLYCÉMIE (si personne consciente et peut avaler)

RESUCRER :
   → 3 morceaux de sucre
   → OU verre de jus de fruit
   → OU soda sucré
   → PAS de soda light

Amélioration en 5 à 10 minutes

Si pas d'amélioration : Alerter 15


CRISE D'ÉPILEPSIE (convulsions)

→ Protéger la tête (coussin, veste)
→ Écarter les objets dangereux
→ NE PAS TENIR la personne
→ NE RIEN METTRE dans la bouche
→ Chronométrer la durée

Après la crise :
   → Mettre en PLS
   → Alerter le 15

Si crise > 5 minutes :
   → Alerter immédiatement


MALAISE VAGAL

→ Allonger
→ Surélever les jambes
→ Desserer vêtements
→ Généralement amélioration rapide


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

5. SURVEILLER


JUSQU'À AMÉLIORATION OU ARRIVÉE DES SECOURS

Vérifier régulièrement :
   → Conscience : parler à la personne
   → Respiration : observer le thorax
   → État général : amélioration ou aggravation ?


RASSURER

   → Parler calmement
   → Expliquer ce qui se passe
   → "Les secours arrivent"


SI PERTE DE CONNAISSANCE

   → Vérifier la respiration
   → Si respire : PLS
   → Si ne respire pas : RCP


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CE QU'IL NE FAUT PAS FAIRE


✗ Donner à boire si inconscience
✗ Donner des médicaments (sauf si médicament habituel de la personne)
✗ Minimiser le malaise
✗ Laisser la personne seule
✗ Laisser fumer
✗ Maintenir de force lors de convulsions
"""
            }
        ]
    },
    {
        "id": "psc-ch7",
        "numero": 7,
        "titre": "Plaies et traumatismes",
        "description": "Plaies simples et graves, traumatismes des os et articulations",
        "icon": "Bandage",
        "formation_type": "PSC",
        "fiches": [
            {
                "id": "psc-f7-1",
                "titre": "Plaies simples et graves",
                "contenu": """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                    PLAIES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

DÉFINITION

Rupture de la barrière cutanée par un agent extérieur.


DEUX TYPES


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PLAIE SIMPLE


CRITÈRES

Une plaie est SIMPLE si :
   ✓ Saignement peu abondant
   ✓ Étendue limitée
   ✓ Superficielle
   ✓ Pas de localisation à risque
   ✓ Pas de corps étranger incrusté


CONDUITE À TENIR


1. SE LAVER LES MAINS

   → Savon
   → Eau


2. NETTOYER LA PLAIE

   → Eau courante propre
   → Du centre vers l'extérieur
   → Savon doux si disponible


3. DÉSINFECTER

   → Antiseptique
   → Compresse stérile
   → Du centre vers l'extérieur


4. PROTÉGER

   → Pansement adhésif
   → OU compresse + sparadrap


5. CONSEILLER

   → Consulter un médecin si :
      • Plaie sale (terre, rouille)
      • Morsure, griffure
      • Vaccination antitétanique non à jour
      • Signes d'infection (rougeur, chaleur, pus)


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PLAIE GRAVE


CRITÈRES

Une plaie est GRAVE si :

   ✗ Saignement abondant (hémorragie)
   ✗ Étendue importante
   ✗ Profonde
   ✗ Localisation à risque :
      • Œil
      • Thorax
      • Abdomen
      • Cou
      • Près d'un orifice naturel
   ✗ Corps étranger incrusté
   ✗ Morsure animale ou humaine
   ✗ Brûlure associée


CONDUITE À TENIR


1. ALERTER LE 15

   Immédiatement


2. NE PAS TOUCHER LA PLAIE

   → Ne pas retirer le corps étranger s'il est incrusté
   → Ne pas mettre d'antiseptique


3. PROTÉGER

   → Recouvrir d'un linge propre
   → Sans appuyer (sauf hémorragie)


4. SI HÉMORRAGIE

   → Compression directe
   → Forte et continue


5. ALLONGER LA VICTIME

   → Position horizontale
   → Surveiller la conscience


6. RASSURER

   → Parler calmement
   → Couvrir si nécessaire


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CAS PARTICULIERS


PLAIE À L'ŒIL

   → NE PAS TOUCHER
   → Protéger avec un gobelet (pas de compression)
   → Alerter 15
   → Allonger tête surélevée


PLAIE AU THORAX

   → Si plaie soufflante (air qui passe)
   → Boucher avec un film plastique
   → Alerter 15
   → Position demi-assise


PLAIE À L'ABDOMEN

   → Ne pas toucher
   → Si intestins sortent : NE PAS LES REMETTRE
   → Protéger avec un linge humide propre
   → Alerter 15
   → Position allongée, jambes fléchies


CORPS ÉTRANGER INCRUSTÉ

   → NE PAS RETIRER
   → Stabiliser l'objet (caler avec compresses)
   → Alerter 15


AMPUTATION

   → Comprimer le moignon
   → Récupérer le membre sectionné
   → L'envelopper dans un linge propre
   → Le mettre dans un sac plastique
   → Le conserver au frais (pas directement sur glace)
   → L'amener aux secours


MORSURE

   → Nettoyer abondamment à l'eau
   → Alerter 15 ou conseiller consultation
   → Risque de rage (animaux sauvages, chauves-souris)
"""
            },
            {
                "id": "psc-f7-2",
                "titre": "Traumatismes des os et articulations",
                "contenu": """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        TRAUMATISMES DES OS ET ARTICULATIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

TYPES DE TRAUMATISMES

→ FRACTURE : os cassé
→ ENTORSE : lésion d'une articulation
→ LUXATION : os sorti de l'articulation


IMPOSSIBLE DE DISTINGUER À COUP SÛR

Seule une radiographie peut confirmer


PRINCIPE

TOUJOURS considérer comme une fracture


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

RECONNAÎTRE UN TRAUMATISME


SIGNES

→ DOULEUR vive à un membre ou au dos
→ Déformation visible
→ Gonflement
→ Ecchymose (bleu)
→ Impossibilité de bouger
→ Craquement entendu lors du choc


CIRCONSTANCES

→ Chute
→ Choc direct
→ Torsion violente
→ Accident de la route


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CONDUITE À TENIR GÉNÉRALE


PRINCIPE FONDAMENTAL

NE PAS MOBILISER la zone traumatisée


ÉTAPES


1. ÉVITER TOUTE MOBILISATION

   → Ne pas toucher
   → Ne pas déplacer la victime
   → Éviter tout mouvement de la zone touchée


2. ALERTER LE 15

   Si :
   → Traumatisme important
   → Déformation visible
   → Douleur intense
   → Impossibilité de bouger
   → Traumatisme du dos, du cou
   → Victime ne peut pas se déplacer


3. IMMOBILISER

   → Maintenir la zone dans la position trouvée
   → Ne pas chercher à "remettre en place"


4. PROTÉGER

   → Si attente longue : protéger du froid


5. SURVEILLER

   → Conscience
   → Respiration
   → Circulation (doigts/orteils rosés, chauds)


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CAS PARTICULIERS


TRAUMATISME DU DOS OU DU COU


⚠ EXTRÊMEMENT GRAVE
Risque de paralysie


CONDUITE À TENIR

→ NE PAS BOUGER la victime
→ Maintenir la tête dans l'axe du corps
→ Alerter le 15 immédiatement
→ Parler pour maintenir consciente
→ Attendre les secours sans bouger

Exception :
   → Si danger immédiat (incendie, explosion)
   → Dégagement d'urgence


SI LA VICTIME EST DEBOUT

   → Lui demander de ne plus bouger
   → Maintenir la tête à deux mains


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

TRAUMATISME D'UN MEMBRE


MEMBRE SUPÉRIEUR (bras, avant-bras, main)

→ Demander à la victime de maintenir son membre
→ OU maintenir avec une écharpe, un tissu
→ Si douleur tolérable et pas de déformation :
   • Possibilité de se rendre aux urgences par ses propres moyens


MEMBRE INFÉRIEUR (jambe, pied)

→ NE PAS faire lever la victime
→ Alerter le 15
→ Attendre les secours
→ Allonger la victime


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

FRACTURE OUVERTE


DÉFINITION

Os cassé avec plaie en regard


CONDUITE À TENIR

1. ALERTER le 15 immédiatement

2. Ne PAS toucher
   → Ne pas remettre l'os en place

3. PROTÉGER la plaie
   → Linge propre sans appuyer

4. SI HÉMORRAGIE
   → Compression de chaque côté de la plaie
   → PAS sur l'os

5. Surveiller


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ENTORSE BÉNIGNE


SI

→ Douleur modérée
→ Gonflement léger
→ Peut encore bouger l'articulation


CONDUITE À TENIR

→ Application de glace (dans un linge, 15-20 min)
→ Repos
→ Surélévation du membre
→ Consultation médicale dans les 24-48h
→ Bandage élastique si disponible


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CE QU'IL NE FAUT PAS FAIRE


✗ Manipuler, mobiliser la zone traumatisée
✗ Essayer de "remettre en place"
✗ Faire marcher une personne avec traumatisme à la jambe
✗ Redresser un membre déformé
✗ Enlever une chaussure si cheville traumatisée (sauf si nécessaire)
"""
            }
        ]
    },
    {
        "id": "psc-ch8",
        "numero": 8,
        "titre": "Brûlures",
        "description": "Évaluer la gravité, refroidir, protéger",
        "icon": "Flame",
        "formation_type": "PSC",
        "fiches": [
            {
                "id": "psc-f8-1",
                "titre": "Types et gravité des brûlures",
                "contenu": """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                        BRÛLURES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

DÉFINITION

Destruction de la peau et des tissus par :
   → Chaleur (flammes, liquide chaud, objet chaud)
   → Produit chimique
   → Électricité
   → Soleil (coup de soleil grave)
   → Froid (gelures)


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ÉVALUER LA GRAVITÉ


TROIS CRITÈRES


1. PROFONDEUR


BRÛLURE DU 1er DEGRÉ

→ Rougeur
→ Douleur
→ Pas de cloque
→ Comme un coup de soleil

Exemple : coup de soleil léger


BRÛLURE DU 2ᵉ DEGRÉ

→ Rougeur
→ CLOQUES (phlyctènes)
→ Douleur INTENSE
→ Peau humide

Exemple : eau bouillante


BRÛLURE DU 3ᵉ DEGRÉ

→ Peau blanche, brune ou noire
→ Peau cartonnée, sèche
→ ABSENCE de douleur (nerfs détruits)
→ Très grave

Exemple : flammes, électricité


2. ÉTENDUE


RÈGLE DE LA PAUME DE LA MAIN

La paume de la main de la victime = 1 % de sa surface corporelle


BRÛLURE ÉTENDUE

Si > 10 % du corps (taille adulte)
Si > 5 % chez l'enfant


3. LOCALISATION


LOCALISATIONS GRAVES

→ VISAGE (yeux, nez, bouche)
→ COU
→ MAINS
→ ARTICULATIONS
→ ORGANES GÉNITAUX
→ PRÈS D'UN ORIFICE NATUREL


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

BRÛLURE SIMPLE


CRITÈRES

Brûlure SIMPLE si :
   ✓ 1er degré (rougeur)
   ✓ 2ᵉ degré peu étendue (< taille de la moitié de la paume)
   ✓ Pas de localisation grave


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

BRÛLURE GRAVE


CRITÈRES

Brûlure GRAVE si :

   ✗ 2ᵉ degré étendue
   ✗ 3ᵉ degré
   ✗ Localisation grave (visage, mains, cou, articulations)
   ✗ Origine électrique
   ✗ Origine chimique
   ✗ Victime : nourrisson, personne âgée
   ✗ Brûlure circulaire (tour d'un membre)
   ✗ Inhalation de fumées


⚠ TOUTE BRÛLURE GRAVE = URGENCE VITALE


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CAS PARTICULIERS


BRÛLURE ÉLECTRIQUE

Toujours GRAVE
   → Lésions internes possibles
   → Risque cardiaque
   → Alerter 15


BRÛLURE CHIMIQUE

Toujours GRAVE
   → Lésions progressives
   → Pénétration en profondeur
   → Rinçage prolongé obligatoire


INHALATION DE FUMÉES

Signes :
   → Toux
   → Difficulté à respirer
   → Suie dans le nez, la bouche
   → Voix enrouée

➜ Toujours GRAVE
➜ Alerter 15
"""
            },
            {
                "id": "psc-f8-2",
                "titre": "Conduite à tenir face aux brûlures",
                "contenu": """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        CONDUITE À TENIR FACE AUX BRÛLURES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PRINCIPE GÉNÉRAL


1ʳᵉ ACTION IMMÉDIATE

ARROSER IMMÉDIATEMENT À L'EAU


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

BRÛLURE SIMPLE


CONDUITE À TENIR


1. REFROIDIR IMMÉDIATEMENT

   → EAU FRAÎCHE (15-25°C)
   → EAU COURANTE
   → Pendant 5 MINUTES minimum

   Effets :
      • Stoppe la progression de la brûlure
      • Diminue la douleur
      • Limite l'étendue


2. RETIRER

   → Vêtements NON COLLÉS
   → Bijoux, montre (avant le gonflement)

   ⚠ Ne PAS retirer les vêtements collés à la peau


3. PROTÉGER

   → Pansement propre non adhésif
   → OU linge propre


4. CONSEILLER

   Consulter un médecin si :
      → Doute sur la gravité
      → Cloques étendues
      → Douleur importante


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

BRÛLURE GRAVE


CONDUITE À TENIR


1. SUPPRIMER LA CAUSE SI POSSIBLE

   → Éloigner de la source de chaleur
   → Éteindre les flammes (rouler au sol, couverture)
   → ATTENTION : se protéger


2. ALERTER LE 15

   Immédiatement


3. REFROIDIR

   → EAU FRAÎCHE (15-25°C) sur la zone brûlée
   → Pendant 5 MINUTES minimum
   → Jusqu'à diminution de la douleur

   ⚠ Sauf si :
      • Brûlure étendue (> 10 % adulte, > 5 % enfant)
        → Risque d'hypothermie
      • Brûlure électrique
      • Si la victime tremble, a froid


4. RETIRER

   → Vêtements NON COLLÉS
   → Bijoux, montre

   ⚠ NE PAS retirer :
      • Vêtements collés
      • Tout ce qui adhère à la peau


5. PROTÉGER

   → Recouvrir d'un drap propre
   → OU champs stérile si disponible


6. ALLONGER

   → Position horizontale
   → Sauf difficulté respiratoire : demi-assis


7. COUVRIR

   → Couverture
   → Éviter l'hypothermie


8. SURVEILLER

   → Conscience
   → Respiration


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CAS PARTICULIERS


BRÛLURE CHIMIQUE


CONDUITE À TENIR

1. SE PROTÉGER
   → Gants
   → Éviter tout contact avec le produit

2. ARROSER ABONDAMMENT À L'EAU
   → Immédiatement
   → Eau courante
   → Pendant 20 MINUTES minimum
   → Retirer les vêtements contaminés EN ARROSANT

3. ALERTER LE 15
   → Préciser le produit en cause

4. Continuer d'arroser jusqu'à l'arrivée des secours


⚠ Exception : certains produits (chaux vive, sodium)
   → Brosser à sec AVANT d'arroser


BRÛLURE PAR ÉLECTRICITÉ


CONDUITE À TENIR

1. COUPER LE COURANT
   → Disjoncteur

2. NE PAS REFROIDIR
   → Sauf avis du 15

3. ALERTER LE 15
   → Brûlure électrique toujours grave

4. Surveiller
   → Risque d'arrêt cardiaque


BRÛLURE INTERNE (inhalation de fumées)


SIGNES

→ Suie autour du nez, de la bouche
→ Toux
→ Difficultés respiratoires
→ Voix rauque


CONDUITE À TENIR

1. ALERTER LE 15
   → Urgence vitale

2. Mettre la victime DEMI-ASSISE

3. Desserrer les vêtements

4. Surveiller la respiration


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CE QU'IL NE FAUT PAS FAIRE


✗ Percer les cloques
✗ Mettre de la glace directement
✗ Mettre du beurre, huile, dentifrice, etc.
✗ Arracher les vêtements collés
✗ Toucher la brûlure avec les doigts
✗ Mettre du coton (fibres collent)
✗ Donner à boire si brûlure étendue


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

APRÈS LES SOINS


SURVEILLANCE

→ Signes d'infection (rougeur, chaleur, pus)
→ Fièvre
→ Douleur qui augmente

➜ Consultation médicale


PRÉVENTION DU TÉTANOS

Vérifier la vaccination antitétanique
"""
            }
        ]
    }
]

# Insertion des chapitres PSC 5-8
for ch in psc_chapters:
    db.chapters.insert_one(ch)
    print(f"  ✅ Ch{ch['numero']}: {ch['titre']}")

print(f"\n🎉 Chapitres PSC 5-8 créés")
print(f"📊 Total chapitres: PSE={db.chapters.count_documents({'formation_type': 'PSE'})} | PSC={db.chapters.count_documents({'formation_type': 'PSC'})}")

client.close()
