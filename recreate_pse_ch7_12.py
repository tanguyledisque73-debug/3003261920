#!/usr/bin/env python3
"""
PSE Chapitres 7 à 12 - Traumatismes, Atteintes circonstancielles, Situations particulières
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

pse_chapters_7_12 = [
    {
        "id": "pse-ch7",
        "numero": 7,
        "titre": "Traumatismes des os et articulations",
        "description": "Fractures, entorses, luxations, traumatismes du rachis, immobilisation",
        "icon": "Bone",
        "formation_type": "PSE",
        "fiches": [
            {
                "id": "pse-f7-1",
                "titre": "Les traumatismes",
                "contenu": """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                    DÉFINITIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

FRACTURE

Rupture de la continuité d'un os.

Types :
   → Fracture fermée : peau intacte
   → Fracture ouverte : os visible, peau lésée


ENTORSE

Lésion des ligaments d'une articulation sans déplacement osseux.

Gravité :
   → Bénigne : élongation
   → Moyenne : déchirure partielle
   → Grave : rupture complète


LUXATION

Déplacement permanent des surfaces articulaires (os sorti de l'articulation).


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SIGNES COMMUNS

→ Douleur importante à la mobilisation
→ Impotence fonctionnelle (impossibilité d'utiliser le membre)
→ Déformation
→ Gonflement (œdème)
→ Ecchymose (hématome)


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CONDUITE À TENIR GÉNÉRALE


1. NE PAS MOBILISER LE MEMBRE

Ne pas essayer de remettre en place
Ne pas retirer les vêtements si douloureux
Laisser dans la position trouvée


2. RECHERCHER UNE COMPLICATION

Hémorragie externe (fracture ouverte)
Absence de pouls en aval
Perte de sensibilité
Plaie associée


3. IMMOBILISER

Dans la position trouvée
Immobiliser l'articulation au-dessus et en dessous de la fracture
Utiliser attelles, écharpes, ou membres sains


4. PROTÉGER UNE FRACTURE OUVERTE

Ne pas toucher l'os
Couvrir avec un pansement stérile
Ne pas nettoyer la plaie


5. APPLICATION DE FROID

Vessie de glace ou poche réfrigérante
Sur un linge (jamais directement sur la peau)
20 minutes maximum
Soulage la douleur et limite le gonflement


6. ALERTER LE 15

Systématiquement pour :
   → Fracture ouverte
   → Déformation importante
   → Traumatisme du rachis
   → Douleur intense
   → Absence de pouls ou sensibilité


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

IMMOBILISATIONS SPÉCIFIQUES


MEMBRE SUPÉRIEUR

Écharpe simple :
   → Triangle de tissu
   → Soutien de l'avant-bras
   → Coude à 90°

Écharpe oblique :
   → Pour immobiliser le bras contre le thorax
   → Triangle passant sous l'aisselle opposée


MEMBRE INFÉRIEUR

Attelle rigide ou à dépression
Immobilisation membre contre membre (jambe saine)


BASSIN

Victime en position jambes fléchies (position antalgique)
Ne jamais mobiliser
Transport médicalisé obligatoire


RACHIS

Maintien tête en position neutre
Collier cervical si disponible
Plan dur pour le transport
Ne jamais mobiliser sauf danger vital
"""
            },
            {
                "id": "pse-f7-2",
                "titre": "Traumatisme du rachis",
                "contenu": """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                TRAUMATISME DU RACHIS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

GRAVITÉ

Le rachis contient la moelle épinière.

Toute lésion de la moelle peut entraîner :
   → Paralysie définitive
   → Tétraplégie (4 membres)
   → Paraplégie (membres inférieurs)
   → Troubles respiratoires
   → Décès


MÉCANISMES À RISQUE

→ Chute de plus de 1 mètre (hauteur)
→ Accident de la route à haute vitesse
→ Choc violent tête, cou ou dos
→ Plongeon en eau peu profonde
→ Défenestration
→ Écrasement
→ Projection violente


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SIGNES DE SUSPICION

INTERROGATOIRE :

→ "Avez-vous mal au cou ou au dos ?"
→ "Avez-vous des fourmillements dans les membres ?"
→ "Pouvez-vous bouger vos doigts ? vos orteils ?"


EXAMEN :

→ Douleur à la palpation du rachis
→ Déformation visible
→ Plaie du dos
→ Perte de sensibilité
→ Impossibilité de bouger un ou plusieurs membres
→ Priapisme (érection réflexe) chez l'homme


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CONDUITE À TENIR


PRINCIPE FONDAMENTAL

NE PAS MOBILISER LA VICTIME sauf danger vital immédiat


SI VICTIME CONSCIENTE :

1. Demander de NE PAS BOUGER

2. Maintien tête :
   → Se placer derrière la victime
   → Mains de chaque côté de la tête
   → Maintenir dans l'axe du corps (position neutre)
   → Ne pas tirer, ne pas tourner

3. Alerter le 15

4. Poser un collier cervical si disponible et formé

5. Maintenir la position jusqu'à l'arrivée des secours


SI VICTIME INCONSCIENTE MAIS RESPIRE :

Dilemme : Libérer les voies aériennes VS Risque rachis

PRIORITÉ = Libérer les voies aériennes

1. Retournement à plusieurs secouristes :
   → Minimum 3 personnes
   → Un maintient la tête dans l'axe
   → Retournement en bloc

2. PLS adaptée avec maintien de l'axe

3. Surveillance continue


SI ARRÊT CARDIAQUE :

LA RCP PRIME SUR TOUT

Retourner la victime sur le dos
Commencer la RCP immédiatement
Le pronostic vital immédiat prime


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

MATÉRIEL SPÉCIALISÉ

Collier cervical (tailles adulte/enfant)
Matelas à dépression
Plan dur
Attelle cervico-thoracique (minerve)

Ce matériel est posé par les secouristes formés ou les équipes SMUR.
"""
            },
            {
                "id": "pse-f7-3",
                "titre": "Traumatisme crânien",
                "contenu": """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                TRAUMATISME CRÂNIEN
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

DÉFINITION

Tout choc reçu sur le crâne.


GRAVITÉ

Le traumatisme crânien peut entraîner :
   → Commotion cérébrale (perte de connaissance brève)
   → Contusion cérébrale
   → Hématome intracrânien (peut se développer plusieurs heures après)
   → Fracture du crâne
   → Lésions mortelles


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SIGNES DE GRAVITÉ

⚠ SIGNES D'ALERTE

→ Perte de connaissance (même brève)
→ Confusion, désorientation
→ Maux de tête intenses
→ Vomissements en jet
→ Troubles visuels
→ Somnolence anormale
→ Convulsions
→ Saignement ou écoulement par le nez ou les oreilles
→ Inégalité pupillaire (anisocorie)
→ Plaie du crâne avec enfoncement
→ Bosse importante (hématome)


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CONDUITE À TENIR


SI VICTIME CONSCIENTE :

1. Installer en position demi-assise (sauf suspicion rachis)

2. Appliquer une compresse sur la plaie si saignement

3. Ne pas appuyer sur un enfoncement

4. Interroger :
   → "Quel est votre nom ?"
   → "Quel jour sommes-nous ?"
   → "Où êtes-vous ?"

5. Alerter le 15 si signe de gravité

6. Surveiller pendant 6 heures minimum


SI VICTIME INCONSCIENTE :

1. Vérifier la respiration

2. Si respire : PLS

3. Si ne respire pas : RCP

4. Alerter le 15 IMMÉDIATEMENT


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SURVEILLANCE POST-TRAUMATIQUE

TOUTE PERSONNE AYANT SUBI UN TRAUMATISME CRÂNIEN DOIT ÊTRE SURVEILLÉE PENDANT 6 À 24 HEURES

Signes à surveiller :
   → État de conscience (réveiller toutes les 2 heures la nuit)
   → Maux de tête croissants
   → Vomissements
   → Comportement anormal
   → Somnolence excessive

Si aggravation : APPELER LE 15 IMMÉDIATEMENT


CONSIGNES À DONNER

Ne pas rester seul pendant 24 heures
Pas de conduite automobile
Pas d'activité physique intense
Éviter l'alcool et les somnifères
Consulter si aggravation
"""
            }
        ]
    },
    {
        "id": "pse-ch8",
        "numero": 8,
        "titre": "Plaies et hémorragies",
        "description": "Plaies simples et graves, hémorragies externes, compression et garrot",
        "icon": "Droplet",
        "formation_type": "PSE",
        "fiches": [
            {
                "id": "pse-f8-1",
                "titre": "Les plaies",
                "contenu": """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                    LES PLAIES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

DÉFINITION

Une plaie est une lésion de la peau avec ou sans atteinte des tissus sous-jacents.


CLASSIFICATION


PLAIE SIMPLE

Petite plaie superficielle, peu saignante, sans corps étranger

Exemples : éraflure, coupure superficielle


PLAIE GRAVE

Plaie avec au moins UN des critères suivants :
   → Saignement abondant (hémorragie)
   → Plaie profonde
   → Corps étranger enfoncé
   → Localisation à risque (thorax, abdomen, cou, œil)
   → Mécanisme violent (arme blanche, balle, explosion)
   → Plaie étendue
   → Morsure (humaine ou animal)
   → Œil atteint
   → Plaie souillée (terre, rouille, excréments)


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CONDUITE À TENIR : PLAIE SIMPLE


1. SE PROTÉGER

Porter des gants à usage unique


2. NETTOYER LA PLAIE

Eau courante + savon
Du centre vers l'extérieur
Sécher par tamponnement


3. DÉSINFECTER

Antiseptique incolore (Bétadine, Chlorhexidine)
Du centre vers l'extérieur


4. PROTÉGER

Pansement adhésif ou compresse + sparadrap


5. CONSEILLER

Surveillance pendant 48 heures
Consulter si signes d'infection :
   → Rougeur, chaleur, gonflement
   → Douleur croissante
   → Écoulement purulent
   → Fièvre

Vérifier la vaccination antitétanique (< 10 ans)


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CONDUITE À TENIR : PLAIE GRAVE


RÈGLES ABSOLUES

✗ NE PAS RETIRER UN CORPS ÉTRANGER ENFONCÉ
✗ NE PAS NETTOYER
✗ NE PAS DÉSINFECTER
✗ NE PAS APPUYER SUR UN ORGANE QUI SORT


1. SE PROTÉGER (gants)

2. ARRÊTER L'HÉMORRAGIE (si présente)
   Voir conduite à tenir hémorragies


3. PROTÉGER LA PLAIE

Pansement stérile
Ne pas toucher la face en contact avec la plaie


4. SI CORPS ÉTRANGER

Ne pas retirer
Stabiliser l'objet (caler avec des compresses)
Protéger autour


5. SI ORGANE SORTI (éviscération)

Ne pas toucher
Recouvrir d'un pansement humide (sérum physiologique)
Victime en position jambes fléchies


6. ALERTER LE 15

Toute plaie grave nécessite un avis médical


7. SURVEILLER

Conscience, respiration, hémorragie
"""
            },
            {
                "id": "pse-f8-2",
                "titre": "Hémorragies externes",
                "contenu": """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                HÉMORRAGIE EXTERNE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

DÉFINITION

Saignement abondant, visible, qui ne s'arrête pas spontanément.


GRAVITÉ

Urgence vitale absolue

Perte de 1 litre de sang = Choc hémorragique
Perte de 2 litres = Risque de décès


SIGNES DE CHOC HÉMORRAGIQUE

→ Pâleur intense
→ Sueurs froides
→ Pouls rapide et faible
→ Respiration rapide
→ Angoisse
→ Soif intense
→ Troubles de la conscience


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CONDUITE À TENIR


PRIORITÉ ABSOLUE : ARRÊTER L'HÉMORRAGIE


1. COMPRESSION DIRECTE (1ère intention)

Technique :
   → Mettre des gants immédiatement
   → Appuyer FORTEMENT sur la plaie avec la main
   → Utiliser un linge propre, compresse, ou à défaut la main nue
   → Maintenir la pression sans relâcher
   → Allonger la victime
   → Alerter ou faire alerter le 15

Durée : Maintenir jusqu'à l'arrivée des secours (peut durer 20-30 minutes)

Si mains fatiguées : Relais par une autre personne SANS relâcher la pression


2. PANSEMENT COMPRESSIF

Si compression directe efficace mais fatiguante :

   → Placer plusieurs compresses sur la plaie
   → Entourer de bandes (crêpe ou élastique)
   → Serrer fortement
   → Fixer avec du sparadrap
   → Vérifier l'efficacité (arrêt du saignement)

⚠ Si le sang traverse : Ajouter des compresses PAR-DESSUS sans retirer les premières


3. GARROT (en dernier recours)

UNIQUEMENT SI :
   → Hémorragie d'un membre
   → Compression directe impossible ou inefficace
   → Nombreuses victimes (ne pas rester bloqué sur une seule)
   → Amputation traumatique


TECHNIQUE DU GARROT :

Matériel :
   → Garrot tourniquet commercial (CAT, SOFTT)
   → Ou lien large (> 5 cm) : cravate, écharpe
   → JAMAIS de fil, ficelle, câble

Pose :
   1. Placer le garrot ENTRE la plaie et le cœur
   2. À quelques centimètres au-dessus de la plaie
   3. Serrer jusqu'à l'arrêt COMPLET du saignement
   4. Noter l'heure de pose (sur le garrot ou le front de la victime)
   5. Laisser le membre visible

⚠ NE JAMAIS desserrer ou retirer un garrot (sauf ordre médical)


LOCALISATIONS :

Membre supérieur : Sur le bras (jamais sur l'avant-bras)
Membre inférieur : Sur la cuisse (jamais sur le mollet)


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

APRÈS L'ARRÊT DE L'HÉMORRAGIE


1. ALLONGER LA VICTIME

Jambes surélevées (sauf douleur)


2. COUVRIR (couverture de survie)

Éviter l'hypothermie


3. RASSURER

Parler calmement
Expliquer que les secours arrivent


4. SURVEILLER

Conscience
Respiration
Réapparition du saignement


5. NE PAS DONNER À BOIRE


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CAS PARTICULIERS


SAIGNEMENT DE NEZ (épistaxis)

Position : Assis, tête penchée EN AVANT
Compression : Pincer les narines 10 minutes
Si échec : Mèche hémostatique
Si récidive ou abondant : Alerter le 15


HÉMORRAGIE BUCCALE

Position : Assis, penché en avant
Faire cracher le sang (ne pas avaler)
Compression si plaie accessible
Alerter le 15


HÉMOPTYSIE (sang venant des poumons)

Sang rouge vif, mousseux, avec toux
Position demi-assise
Alerter le 15 immédiatement


HÉMATÉMÈSE (vomissement de sang)

Sang rouge ou noir (digéré = "marc de café")
Position latérale de sécurité si inconscient
Alerter le 15 immédiatement
"""
            }
        ]
    },
    {
        "id": "pse-ch9",
        "numero": 9,
        "titre": "Brûlures",
        "description": "Brûlures thermiques, chimiques, électriques, évaluation et conduite à tenir",
        "icon": "Flame",
        "formation_type": "PSE",
        "fiches": [
            {
                "id": "pse-f9-1",
                "titre": "Évaluation des brûlures",
                "contenu": """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                ÉVALUATION DES BRÛLURES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

TROIS CRITÈRES DE GRAVITÉ


1. PROFONDEUR

BRÛLURE SUPERFICIELLE (1er degré)
   → Peau rouge
   → Douloureuse
   → Pas de cloque
   → Exemple : coup de soleil

BRÛLURE INTERMÉDIAIRE (2ème degré superficiel)
   → Peau rouge
   → Cloques (phlyctènes)
   → Très douloureuse

BRÛLURE PROFONDE (2ème degré profond et 3ème degré)
   → Peau blanche, brune ou noire
   → Aspect cartonné
   → Peu ou pas douloureuse (nerfs détruits)
   → Peut nécessiter une greffe


2. ÉTENDUE

Règle des 9 de Wallace (adulte) :

   Tête et cou : 9%
   Tronc avant : 18%
   Tronc arrière : 18%
   Chaque bras : 9%
   Chaque jambe : 18%
   Organes génitaux : 1%

Règle de la paume de la main :
   La paume de la main de la victime = 1% de sa surface corporelle


3. LOCALISATION

ZONES À RISQUE (gravité majorée) :

→ Visage (risque d'atteinte respiratoire)
→ Cou
→ Mains (séquelles fonctionnelles)
→ Articulations
→ Organes génitaux
→ Yeux


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

BRÛLURE GRAVE SI :

→ Profondeur : 2ème ou 3ème degré
→ Étendue : > 10% chez l'adulte, > 5% chez l'enfant
→ Localisation à risque
→ Âge extrême (< 5 ans ou > 60 ans)
→ Brûlure chimique ou électrique
→ Brûlure circulaire (tout le tour d'un membre)
→ Inhalation de fumées


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

BRÛLURE SIMPLE

Brûlure du 1er degré ou petit 2ème degré sans critère de gravité
"""
            },
            {
                "id": "pse-f9-2",
                "titre": "Conduite à tenir",
                "contenu": """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        CONDUITE À TENIR : BRÛLURE THERMIQUE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


BRÛLURE SIMPLE


1. REFROIDIR IMMÉDIATEMENT

Eau courante tempérée (15-25°C)
Pendant au moins 5 minutes (idéalement 10-20 min)
À distance de la brûlure (ruissellement)

Effets du refroidissement :
   → Stoppe la progression de la brûlure
   → Soulage la douleur
   → Limite l'œdème

⚠ Ne pas utiliser de glace (risque d'aggravation)


2. RETIRER

Vêtements et bijoux (sauf si collés)
Le plus tôt possible (avant le gonflement)


3. PROTÉGER

Pansement stérile ou linge propre
Ne pas percer les cloques
Ne pas appliquer de corps gras (beurre, huile)
Ne pas appliquer de produit (dentifrice, etc.)


4. SURVEILLER

Signes d'infection dans les jours suivants


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

BRÛLURE GRAVE


1. ÉLOIGNER LA VICTIME DE LA SOURCE

Supprimer la cause si possible et sans danger


2. REFROIDIR (si possible)

Eau courante tempérée 5 minutes minimum
Sauf si brûlure étendue (> 20%) : risque d'hypothermie


3. ALERTER LE 15 IMMÉDIATEMENT


4. NE PAS RETIRER LES VÊTEMENTS COLLÉS

Découper autour si nécessaire


5. PROTÉGER

Champs stériles
Couverture de survie (face dorée contre la peau)


6. ALLONGER LA VICTIME


7. SURVEILLER

Conscience, respiration
Signes de choc


8. NE PAS DONNER À BOIRE


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

BRÛLURE CHIMIQUE


CONDUITE À TENIR :

1. SE PROTÉGER (gants, lunettes)

2. RETIRER les vêtements imbibés

3. RINCER ABONDAMMENT à l'eau courante
   → Pendant 20 minutes minimum
   → De la zone atteinte vers l'extérieur
   → Attention aux projections

4. ALERTER LE 15 ou le 18

5. Identifier le produit (emballage, fiche de sécurité)


PARTICULARITÉS :

Projection oculaire :
   → Rincer œil ouvert pendant 15-20 minutes
   → De l'intérieur vers l'extérieur
   → Alerter immédiatement le 15

Chaux vive :
   → NE PAS rincer immédiatement
   → Épousseter d'abord à sec
   → PUIS rincer abondamment


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

BRÛLURE ÉLECTRIQUE


DANGERS :

→ Brûlures profondes (point d'entrée et sortie)
→ Atteinte cardiaque (troubles du rythme)
→ Lésions musculaires et nerveuses
→ Arrêt cardiaque


CONDUITE À TENIR :

1. COUPER LE COURANT (disjoncteur)

2. Si impossible : éloigner avec objet isolant

3. Vérifier conscience et respiration

4. Si arrêt cardiaque : RCP immédiate

5. ALERTER LE 15 systématiquement

6. Rechercher point d'entrée ET de sortie

7. Position allongée

8. Surveillance cardiaque (monitoring)


⚠ Toute électrisation nécessite un bilan hospitalier
"""
            }
        ]
    },
    {
        "id": "pse-ch10",
        "numero": 10,
        "titre": "Atteintes circonstancielles",
        "description": "Hypothermie, hyperthermie, noyade, intoxications",
        "icon": "Thermometer",
        "formation_type": "PSE",
        "fiches": [
            {
                "id": "pse-f10-1",
                "titre": "Hypothermie et gelures",
                "contenu": """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                    HYPOTHERMIE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

DÉFINITION

Température corporelle centrale inférieure à 35°C.


CLASSIFICATION

HYPOTHERMIE LÉGÈRE : 35°C à 32°C
   → Frissons intenses
   → Pâleur
   → Maladresse des gestes
   → Conscience normale

HYPOTHERMIE MODÉRÉE : 32°C à 28°C
   → Arrêt des frissons
   → Somnolence, confusion
   → Rigidité musculaire
   → Pouls et respiration ralentis

HYPOTHERMIE SÉVÈRE : < 28°C
   → Inconscience
   → Rigidité importante
   → Pouls et respiration très faibles ou absents
   → Aspect de mort apparente


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CONDUITE À TENIR


1. ISOLER DU FROID

Mettre à l'abri (intérieur chauffé si possible)
Retirer les vêtements mouillés
Sécher la victime


2. ENVELOPPER

Couverture de survie (face argentée vers la victime)
Plusieurs couvertures
Couvrir aussi la tête


3. RÉCHAUFFER PROGRESSIVEMENT

⚠ ATTENTION : Réchauffement brutal interdit

Boissons chaudes sucrées SI :
   → Victime consciente
   → Peut avaler
   → Pas d'alcool

Ne pas :
   → Frictionner
   → Donner de l'alcool
   → Mettre source de chaleur directe (radiateur, eau chaude)
   → Faire marcher


4. ALERTER LE 15 si hypothermie modérée ou sévère


5. SURVEILLER

Conscience
Respiration (difficile à voir)
Pouls (peut être très faible)

⚠ Ne pas déclarer un décès : "Personne n'est mort tant qu'elle n'est pas réchauffée"


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

GELURES


DÉFINITION

Lésion locale due au froid intense.

Zones atteintes :
   → Extrémités (doigts, orteils)
   → Nez, oreilles, joues


SIGNES

Stade 1 :
   → Peau blanche, insensible
   → Réversible

Stade 2 :
   → Cloques
   → Peau violacée

Stade 3 :
   → Nécrose (tissus morts)
   → Peau noire


CONDUITE À TENIR

1. Mettre à l'abri du froid

2. NE PAS frictionner

3. NE PAS réchauffer si risque de regel

4. Protéger la zone (pansements secs, stériles)

5. Séparer les doigts (compresses)

6. Alerter le 15 si gelure profonde

7. Pas de marche si pieds gelés
"""
            },
            {
                "id": "pse-f10-2",
                "titre": "Coup de chaleur et déshydratation",
                "contenu": """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                    COUP DE CHALEUR
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

DÉFINITION

Élévation de la température corporelle au-delà de 40°C avec défaillance des mécanismes de régulation.

Urgence vitale (mortalité 20-30%)


FACTEURS DE RISQUE

→ Canicule
→ Effort physique intense
→ Âges extrêmes (enfants, personnes âgées)
→ Maladies chroniques
→ Médicaments (diurétiques, neuroleptiques)
→ Déshydratation


SIGNES

→ Température > 40°C
→ Peau chaude, sèche, rouge
→ ABSENCE de sueur (mécanisme dépassé)
→ Maux de tête violents
→ Nausées, vomissements
→ Confusion, agitation
→ Troubles de la conscience
→ Convulsions possibles


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CONDUITE À TENIR


URGENCE ABSOLUE


1. ALERTER LE 15 IMMÉDIATEMENT


2. REFROIDIR LA VICTIME RAPIDEMENT

Objectif : Faire baisser la température < 39°C en 30 minutes

Méthodes :
   → Déshabiller la victime
   → Placer à l'ombre ou en local frais
   → Asperger d'eau fraîche (pas glacée)
   → Ventiler (éventail, ventilateur)
   → Appliquer linge humide sur le corps
   → Envelopper dans drap humide

⚠ Surveillance : Éviter l'hypothermie (arrêter si frissons)


3. ALLONGER

Jambes surélevées si conscient


4. SI INCONSCIENT

Position latérale de sécurité
Surveiller respiration


5. SURVEILLER

Conscience
Respiration
Température


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

DÉSHYDRATATION


SIGNES

→ Soif intense
→ Fatigue
→ Maux de tête
→ Vertiges
→ Peau sèche, pli cutané
→ Urines foncées, diminuées
→ Confusion (si sévère)


CONDUITE À TENIR

SI VICTIME CONSCIENTE :

1. Mettre à l'ombre, au frais

2. Faire boire :
   → Eau fraîche
   → Par petites quantités répétées
   → Ajouter du sel (pincée) et sucre si effort prolongé

3. Refroidir (ventilation, linge humide)

4. Repos complet

5. Alerter le 15 si :
   → Déshydratation sévère
   → Personne âgée ou enfant
   → Pas d'amélioration


SI VICTIME INCONSCIENTE :

Ne rien donner par la bouche
PLS
Alerter le 15
"""
            }
        ]
    },
    {
        "id": "pse-ch11",
        "numero": 11,
        "titre": "Relevage et brancardage",
        "description": "Techniques de relevage, port du brancard, passages difficiles",
        "icon": "Move",
        "formation_type": "PSE",
        "fiches": [
            {
                "id": "pse-f11-1",
                "titre": "Principes du relevage",
                "contenu": """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                PRINCIPES DU RELEVAGE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

OBJECTIFS

Mobiliser et transporter la victime en toute sécurité :
   → Sans aggraver son état
   → Sans se blesser (secouriste)
   → De manière confortable


NOMBRE DE SECOURISTES

MINIMUM requis :
   → 2 secouristes : Brancardage simple
   → 3 secouristes : Relevage sécurisé
   → 4 secouristes : Relevage d'une victime lourde ou traumatisée


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

RÈGLES DE MANUTENTION


PROTÉGER SON DOS

→ Dos droit
→ Plier les genoux (pas le dos)
→ Se rapprocher de la charge
→ Utiliser la force des jambes


COORDONNER LES MOUVEMENTS

Un chef de manœuvre dirige :
   → Annonce les actions
   → Coordonne les mouvements
   → "Attention pour lever... Levez !"


COMMUNIQUER

Avant chaque mouvement
Pendant le transport
En cas de difficulté


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

TECHNIQUES DE RELEVAGE


PONT SIMPLE (3 secouristes minimum)

Position des secouristes :
   → Secouriste 1 : Tête et thorax
   → Secouriste 2 : Bassin et cuisses
   → Secouriste 3 : Jambes

Technique :
   → S'agenouiller du même côté
   → Passer les bras sous la victime
   → Au signal : soulever ensemble
   → Maintenir à hauteur des genoux
   → Glisser le brancard dessous
   → Déposer doucement

Avantage : Maintien de l'axe corporel


PONT AMÉLIORÉ (4 secouristes)

Comme le pont simple avec un secouriste supplémentaire à la tête pour maintenir l'axe tête-cou-tronc.


PONT NÉERLANDAIS

Permet de retourner une victime sans la mobiliser excessivement.


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

INSTALLATION SUR LE BRANCARD


POSITION DE LA VICTIME

Adapter selon l'état :
   → Allongée sur le dos : Position standard
   → Demi-assise : Gêne respiratoire, douleur thoracique
   → PLS : Inconscient qui respire
   → Jambes fléchies : Traumatisme du bassin


SANGLES DE SÉCURITÉ

Minimum 3 sangles :
   → Thorax (bras le long du corps)
   → Bassin
   → Jambes

Serrer fermement mais sans comprimer
"""
            },
            {
                "id": "pse-f11-2",
                "titre": "Brancardage",
                "contenu": """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                    BRANCARDAGE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

POSITION DES MAINS


PRISE CORRECTE

Paumes vers le bas (pronation)
Pouces vers l'intérieur
Bras tendus
Dos droit


AVANTAGES

Moins de fatigue
Meilleur contrôle du brancard
Répartition du poids


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SENS DE PROGRESSION


PRINCIPE GÉNÉRAL

La victime doit être transportée de manière à pouvoir être surveillée.


EN MARCHE NORMALE

Pieds en avant
Le brancardier arrière peut surveiller la victime


EN MONTÉE D'ESCALIER

Tête en premier (en haut)
Brancard horizontal


EN DESCENTE D'ESCALIER

Tête en premier (en haut)
Brancard horizontal
Descendre marche par marche


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PASSAGES DIFFICILES


FRANCHIR UNE PORTE ÉTROITE

Passage canadien :
   → Basculer le brancard sur la tranche
   → Passer de côté
   → Remettre à l'horizontale


ESCALIERS

→ Un brancardier à la tête (en haut)
→ Un brancardier aux pieds (en bas)
→ Maintenir le brancard HORIZONTAL
→ Descendre/monter marche par marche
→ Synchroniser les mouvements


TERRAIN ACCIDENTÉ

→ Ralentir la progression
→ Annoncer les obstacles
→ Maintenir l'horizontalité
→ Porteurs supplémentaires si besoin


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CONSIGNES DE SÉCURITÉ


POUR LES BRANCARDIERS

→ Vérifier le matériel avant utilisation
→ Respecter les charges maximales
→ Faire des pauses régulières
→ Demander un relais si fatigue
→ Signaler toute difficulté


POUR LA VICTIME

→ Sangler correctement
→ Protéger du froid (couverture)
→ Rassurer pendant le transport
→ Surveiller l'état en permanence
→ Adapter la vitesse à son état
"""
            }
        ]
    },
    {
        "id": "pse-ch12",
        "numero": 12,
        "titre": "Situations particulières",
        "description": "Accouchement inopiné, noyade, plan blanc, situations NRBC",
        "icon": "AlertTriangle",
        "formation_type": "PSE",
        "fiches": [
            {
                "id": "pse-f12-1",
                "titre": "Accouchement inopiné",
                "contenu": """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                ACCOUCHEMENT INOPINÉ
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

RECONNAÎTRE UN ACCOUCHEMENT IMMINENT


SIGNES

→ Contractions rapprochées (< 2 minutes)
→ Envie irrépressible de pousser
→ Tête du bébé visible (couronnement)
→ Poche des eaux rompue


SI L'ACCOUCHEMENT EST IMMINENT

Ne pas tenter de retarder
Ne pas transporter
Préparer l'accouchement sur place
Alerter le 15 (SAMU + pompiers)


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PRÉPARATION


MATÉRIEL NÉCESSAIRE

→ Gants stériles
→ Champs stériles ou draps propres
→ Compresses stériles
→ 2 clamps ou liens propres
→ Ciseaux (désinfectés)
→ Couverture de survie
→ Aspirateur de mucosités si disponible
→ Sac poubelle (pour le placenta)


INSTALLATION DE LA MÈRE

→ Position gynécologique (semi-assise, jambes fléchies écartées)
→ Installer sur un plan propre
→ Champ sous le bassin
→ Préserver l'intimité autant que possible
→ Rassurer, encourager


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

DÉROULEMENT DE L'ACCOUCHEMENT


PHASE D'EXPULSION

→ La mère pousse pendant les contractions
→ Encourager : "Poussez !"
→ Entre les contractions : "Respirez, reposez-vous"

Sortie de la tête :
   → Soutenir délicatement la tête avec les mains
   → NE PAS TIRER
   → Laisser la nature faire


Vérifier le cordon :
   → Si cordon autour du cou : Le faire glisser doucement
   → Si trop serré : Clamper et couper (exceptionnel)


Sortie des épaules :
   → Soutenir la tête et le corps
   → Rotation spontanée de la tête
   → Une épaule puis l'autre


Sortie du corps :
   → Le bébé est glissant : Bien le tenir
   → Sortie rapide du reste du corps


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SOINS AU NOUVEAU-NÉ


IMMÉDIATEMENT APRÈS LA NAISSANCE

1. NOTER L'HEURE DE NAISSANCE

2. SÉCHER ET STIMULER

Essuyer avec linge sec
Stimulation douce (frictionner le dos)


3. ÉVALUER LA RESPIRATION

Le bébé doit crier dans les 30 premières secondes

Si ne respire pas :
   → Libérer les voies aériennes (aspirer bouche et nez)
   → Stimuler (frictionner le dos)
   → Si toujours pas de respiration : ventilation bouche à bouche-nez


4. MAINTIEN AU CHAUD

Essuyer complètement
Envelopper dans linge sec
Bonnet sur la tête
Couverture de survie


5. POSITION

Poser le bébé sur le ventre de la mère (peau à peau)
OU dans les bras de la mère
Tête légèrement plus basse que le corps


6. CORDON OMBILICAL

Attendre l'arrivée des secours si possible

Si nécessaire :
   → 1er clamp à 10 cm du bébé
   → 2ème clamp à 15 cm
   → Couper entre les 2 clamps avec ciseaux désinfectés
   → Surveiller : ne doit pas saigner


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

DÉLIVRANCE (expulsion du placenta)


ATTENDRE

Le placenta sort spontanément 5 à 30 minutes après la naissance


NE PAS TIRER SUR LE CORDON


RÉCUPÉRER LE PLACENTA

→ Dans un sac propre
→ Le conserver (examen médical nécessaire)
→ Vérifier qu'il est complet


SURVEILLER LES SAIGNEMENTS

Saignement normal : modéré
Hémorragie abondante : Alerter, comprimer l'abdomen
"""
            },
            {
                "id": "pse-f12-2",
                "titre": "Noyade",
                "contenu": """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                        NOYADE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

DÉFINITION

Détresse respiratoire causée par l'immersion ou la submersion dans un liquide.


GRAVITÉ

Arrêt respiratoire par spasme laryngé ou inondation pulmonaire
Hypothermie associée
Risque d'arrêt cardiaque


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CONDUITE À TENIR


SORTIE DE L'EAU

→ Sortir la victime de l'eau le plus rapidement possible
→ Maintenir la tête hors de l'eau
→ Appeler à l'aide

⚠ Sécurité du sauveteur : Ne pas se mettre en danger


BILAN IMMÉDIAT

1. Vérifier la conscience

2. Vérifier la respiration


SI VICTIME CONSCIENTE ET RESPIRE :

1. Allonger ou position demi-assise

2. Ôter les vêtements mouillés

3. Sécher et réchauffer (couvertures)

4. Alerter le 15 (systématique)

5. Surveiller :
   → Conscience
   → Respiration
   → Température

⚠ Toute victime de noyade doit être hospitalisée (risque de détresse respiratoire secondaire)


SI VICTIME INCONSCIENTE MAIS RESPIRE :

1. Position latérale de sécurité

2. Retirer vêtements mouillés si possible

3. Couvrir (hypothermie fréquente)

4. Alerter le 15

5. Surveillance continue


SI ARRÊT RESPIRATOIRE OU CARDIAQUE :

1. Alerter ou faire alerter le 15 immédiatement

2. COMMENCER PAR 5 INSUFFLATIONS
   (Les poumons contiennent de l'eau → privilégier les insufflations)

3. Puis RCP standard : 30 compressions / 2 insufflations

4. Poursuivre jusqu'à :
   → Reprise de respiration spontanée
   → Arrivée des secours
   → Épuisement


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PARTICULARITÉS


EAU FROIDE

Hypothermie protectrice possible
Poursuivre la RCP même si prolongée
"Personne n'est morte tant qu'elle n'est pas réchauffée"


VOMISSEMENTS

Fréquents pendant la RCP
Tourner la tête sur le côté
Nettoyer la bouche
Reprendre immédiatement la RCP


NE PAS PERDRE DE TEMPS À :

✗ Vider l'eau des poumons (inefficace)
✗ Compressions abdominales
✗ Retournements multiples
"""
            }
        ]
    }
]

print("\n📚 Insertion des chapitres PSE 7-12...")
for ch in pse_chapters_7_12:
    db.chapters.insert_one(ch)
    print(f"  ✅ Ch{ch['numero']}: {ch['titre']}")

print(f"\n🎉 {len(pse_chapters_7_12)} chapitres PSE créés")
print(f"📊 Total dans la base : {db.chapters.count_documents({})} chapitres")

client.close()
