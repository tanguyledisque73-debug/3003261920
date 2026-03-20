#!/usr/bin/env python3
"""
Compléter les fiches manquantes dans les chapitres PSE
Chaque sujet doit être traité complètement
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

print("📝 Ajout des fiches manquantes...")

# ═══════════════════════════════════════════════════════════
# CHAPITRE 5 : URGENCES VITALES - FICHES MANQUANTES
# ═══════════════════════════════════════════════════════════

nouvelles_fiches_ch5 = [
    {
        "id": "pse-f5-2",
        "titre": "Obstruction des voies aériennes",
        "contenu": """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
            OBSTRUCTION DES VOIES AÉRIENNES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

DÉFINITION

Présence d'un corps étranger dans les voies aériennes empêchant la respiration.


CAUSES

→ Aliment (viande, os, bonbon)
→ Petit objet (jouet chez l'enfant)
→ Vomissures
→ Langue (chez personne inconsciente)


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

OBSTRUCTION PARTIELLE


SIGNES

La victime :
   → Tousse vigoureusement
   → Parle ou émet des sons
   → Respire bruyamment (sifflement)
   → Est consciente et agitée


CONDUITE À TENIR

1. ENCOURAGER À TOUSSER

"Toussez fort !"
Ne rien faire d'autre
La toux est le mécanisme le plus efficace


2. RESTER AVEC LA VICTIME

Surveiller l'évolution


3. SI AGGRAVATION

Passer à la conduite à tenir de l'obstruction totale


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

OBSTRUCTION TOTALE


SIGNES

La victime :
   → Ne peut plus parler ni crier
   → Ne peut plus tousser
   → Fait le signe universel (mains à la gorge)
   → Bouche ouverte, cyanose (devient bleue)
   → Peut perdre connaissance


URGENCE VITALE : Agir immédiatement


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ADULTE ET ENFANT (> 1 an) CONSCIENT


SÉQUENCE D'ACTIONS


1. CLAQUES DANS LE DOS (5 fois)

Position :
   → Se placer sur le côté de la victime
   → Soutenir le thorax d'une main
   → Pencher la victime en avant

Geste :
   → Donner 5 claques vigoureuses entre les omoplates
   → Avec le talon de la main
   → De bas en haut

Vérifier après chaque claque si le corps étranger est expulsé


2. SI ÉCHEC : COMPRESSIONS ABDOMINALES (5 fois)
   Manœuvre de HEIMLICH

Position :
   → Se placer derrière la victime
   → Passer les bras autour de la taille
   → Placer un poing fermé entre le nombril et le sternum
   → Entourer le poing de l'autre main

Geste :
   → Tirer franchement vers soi et vers le haut
   → 5 fois de suite
   → Mouvements secs et rapides


3. ALTERNER

5 claques dans le dos
Puis 5 compressions abdominales
Continuer jusqu'à :
   → Expulsion du corps étranger
   → Victime perd connaissance


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SI LA VICTIME PERD CONNAISSANCE


1. Allonger prudemment au sol

2. Alerter ou faire alerter le 15

3. Débuter immédiatement la RCP
   → 30 compressions thoraciques
   → Vérifier la bouche (retirer corps étranger visible)
   → 2 insufflations
   → Continuer

Les compressions thoraciques peuvent expulser le corps étranger


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

NOURRISSON (< 1 an)


SÉQUENCE ADAPTÉE


1. CLAQUES DANS LE DOS (5 fois)

Position :
   → Asseoir, avant-bras sur la cuisse
   → Nourrisson à plat ventre sur l'avant-bras
   → Tête plus basse que le tronc
   → Soutenir la tête et la mâchoire

Geste :
   → 5 claques entre les omoplates
   → Avec le talon de la main


2. SI ÉCHEC : COMPRESSIONS THORACIQUES (5 fois)

⚠ PAS de compressions abdominales chez le nourrisson

Position :
   → Retourner le nourrisson sur le dos
   → Sur l'autre avant-bras
   → Tête plus basse

Geste :
   → 2 doigts au centre du thorax
   → 5 compressions vers le bas
   → Comme pour un massage cardiaque


3. ALTERNER jusqu'à expulsion ou perte de connaissance


Si perte de connaissance : RCP adaptée au nourrisson


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

FEMME ENCEINTE OU PERSONNE OBÈSE


Remplacer les compressions abdominales par des COMPRESSIONS THORACIQUES

Position du poing : Sur le sternum (partie inférieure)
"""
    },
    {
        "id": "pse-f5-3",
        "titre": "Victime inconsciente qui respire",
        "contenu": """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        VICTIME INCONSCIENTE QUI RESPIRE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

DANGER

Une victime inconsciente allongée sur le dos risque :
   → Chute de la langue en arrière → obstruction
   → Inhalation de vomissures → étouffement
   → Arrêt respiratoire


SOLUTION : POSITION LATÉRALE DE SÉCURITÉ (PLS)


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

TECHNIQUE DE LA PLS (ADULTE)


PRÉPARATION

1. Victime allongée sur le dos

2. Retirer lunettes si présentes

3. S'agenouiller à côté de la victime


ÉTAPES


1. PRÉPARER LE BRAS

Placer le bras du côté du sauveteur à angle droit
Paume de la main vers le haut


2. PLACER LA MAIN OPPOSÉE

Saisir la main opposée de la victime
Placer le dos de cette main contre sa joue (côté sauveteur)
Maintenir la main plaquée contre la joue


3. REPLIER LA JAMBE OPPOSÉE

Attraper la jambe opposée
Plier le genou
Pied au sol


4. FAIRE ROULER

Tirer sur le genou
La victime roule sur le côté
Ajuster la jambe pour stabiliser (genou à 90°)


5. AJUSTEMENTS FINAUX

Ouvrir la bouche (vers le bas)
Vérifier que la respiration est libre
Ajuster la main sous la joue si nécessaire


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

APRÈS LA MISE EN PLS


1. ALERTER LE 15

Si pas déjà fait


2. COUVRIR

Couverture de survie
Éviter l'hypothermie


3. SURVEILLER

Vérifier la respiration toutes les minutes
   → Regarder le ventre/thorax bouger
   → Écouter les bruits respiratoires

Si arrêt respiratoire :
   → Remettre sur le dos
   → Débuter la RCP


4. LIBÉRER LES VOIES AÉRIENNES SI VOMISSEMENTS

Tourner la bouche vers le sol
Nettoyer avec un doigt (gant ou linge)


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CAS PARTICULIERS


FEMME ENCEINTE (> 6 mois)

Préférer le côté gauche (soulage la compression de la veine cave)


TRAUMATISÉ DU RACHIS

PLS uniquement si nécessaire (vomissements, impossibilité de surveiller)
Retournement à plusieurs avec maintien de l'axe


NOURRISSON ET ENFANT

Technique similaire adaptée à la taille
Surveiller encore plus fréquemment
"""
    }
]

# Ajouter les fiches au chapitre 5
db.chapters.update_one(
    {"id": "pse-ch5"},
    {"$push": {"fiches": {"$each": nouvelles_fiches_ch5}}}
)
print("  ✅ Ch5: Ajout de 2 fiches (Obstruction, PLS)")


# ═══════════════════════════════════════════════════════════
# CHAPITRE 6 : MALAISES - FICHES MANQUANTES
# ═══════════════════════════════════════════════════════════

nouvelles_fiches_ch6 = [
    {
        "id": "pse-f6-3",
        "titre": "Crise d'asthme",
        "contenu": """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                    CRISE D'ASTHME
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

DÉFINITION

Rétrécissement brutal des bronches entraînant une gêne respiratoire.


FACTEURS DÉCLENCHANTS

→ Allergènes (pollen, acariens, poils d'animaux)
→ Effort physique
→ Air froid
→ Fumée de cigarette
→ Stress, émotions
→ Infection respiratoire


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SIGNES


CRISE D'ASTHME SIMPLE

→ Gêne respiratoire
→ Sifflements à l'expiration (wheezing)
→ Toux sèche
→ Angoisse
→ Difficulté à parler (phrases courtes)


CRISE GRAVE (URGENCE VITALE)

→ Impossibilité de parler
→ Épuisement
→ Sueurs profuses
→ Cyanose (lèvres bleues)
→ Respiration rapide et superficielle
→ Pouls rapide
→ Somnolence, confusion


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CONDUITE À TENIR


1. INSTALLER

Position demi-assise ou assise
Jamais allongée
Bras en appui (permet de mieux respirer)


2. RASSURER

Parler calmement
Respiration lente et contrôlée


3. AÉRER

Ouvrir les fenêtres
Desserrer les vêtements
Éloigner les personnes


4. AIDER À PRENDRE LE TRAITEMENT

Bronchodilatateur (inhalateur type Ventoline)

Technique d'utilisation :
   → Agiter l'inhalateur
   → Expirer à fond
   → Placer l'embout dans la bouche
   → Déclencher et inspirer profondément en même temps
   → Retenir sa respiration 10 secondes
   → Expirer lentement

Nombre de bouffées : Selon prescription (généralement 2 à 4)
Renouveler après 5-10 minutes si besoin


5. ALERTER LE 15 SI :

→ Première crise d'asthme
→ Pas d'amélioration après traitement
→ Signes de gravité
→ Traitement non disponible
→ Aggravation


6. SURVEILLER

Respiration
Conscience
Coloration
"""
    },
    {
        "id": "pse-f6-4",
        "titre": "Malaise diabétique",
        "contenu": """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                MALAISE DIABÉTIQUE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LE DIABÈTE

Maladie chronique caractérisée par un excès de sucre dans le sang.


DEUX TYPES DE MALAISES


HYPOGLYCÉMIE (manque de sucre)
   Glycémie < 0,60 g/L
   LE PLUS FRÉQUENT ET LE PLUS URGENT


HYPERGLYCÉMIE (excès de sucre)
   Glycémie > 2,50 g/L
   Évolution plus lente


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

HYPOGLYCÉMIE


CAUSES

→ Dose d'insuline trop élevée
→ Repas sauté ou insuffisant
→ Effort physique intense
→ Consommation d'alcool


SIGNES

Début brutal :
   → Sueurs profuses
   → Pâleur
   → Tremblements
   → Sensation de faim
   → Faiblesse
   → Troubles de la concentration
   → Comportement étrange, agressivité
   → Troubles de la conscience
   → Convulsions possibles
   → Coma si non traité


CONDUITE À TENIR


SI VICTIME CONSCIENTE ET PEUT AVALER :

1. DONNER DU SUCRE RAPIDE immédiatement

Sucres rapides :
   → 3 morceaux de sucre
   → 1 verre de jus de fruit
   → 1 canette de soda (non light)
   → 1 cuillère à soupe de miel ou confiture
   → Gel de glucose (tube)


2. INSTALLER confortablement (assis ou allongé)


3. FAIRE SUIVRE de sucres lents (15 min après)

   → Pain, biscuits
   → Éviter une nouvelle hypoglycémie


4. SURVEILLER

Amélioration en 5-10 minutes normalement


5. ALERTER LE 15 SI :

   → Pas d'amélioration
   → Impossibilité d'avaler
   → Perte de connaissance


SI VICTIME INCONSCIENTE :

⚠ NE RIEN DONNER PAR LA BOUCHE

1. Position latérale de sécurité

2. Alerter le 15 immédiatement

3. Surveiller la respiration


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

HYPERGLYCÉMIE


CAUSES

→ Dose d'insuline insuffisante
→ Infection
→ Stress
→ Alimentation trop riche en sucres


SIGNES

Début progressif (heures/jours) :
   → Soif intense
   → Urines abondantes
   → Fatigue importante
   → Nausées, vomissements
   → Douleurs abdominales
   → Respiration rapide et profonde
   → Haleine « fruitée » (acétonique)
   → Troubles de la conscience


CONDUITE À TENIR

1. Alerter le 15

2. Position demi-assise si conscient

3. Ne pas donner de sucre

4. Ne pas donner à boire si vomissements

5. PLS si inconscient

6. Surveiller


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

EN CAS DE DOUTE


Si on ne sait pas si c'est hypo ou hyperglycémie :

DONNER DU SUCRE (si conscient et peut avaler)

Raison : L'hypoglycémie tue en minutes
L'hyperglycémie évolue sur des heures
"""
    },
    {
        "id": "pse-f6-5",
        "titre": "Convulsions",
        "contenu": """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                    CONVULSIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

DÉFINITION

Contractions musculaires involontaires, brutales et incontrôlables.


CAUSES

→ Épilepsie
→ Fièvre élevée (convulsions fébriles chez l'enfant)
→ Hypoglycémie
→ Traumatisme crânien
→ AVC
→ Intoxication
→ Sevrage alcoolique
→ Troubles métaboliques


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SIGNES


CRISE GÉNÉRALISÉE (grand mal)

1. Phase tonique (10-20 secondes)
   → Raideur du corps
   → Perte de connaissance brutale
   → Chute
   → Respiration bloquée

2. Phase clonique (30 secondes à 2 minutes)
   → Secousses musculaires rythmées
   → Morsure de langue possible
   → Perte d'urines
   → Bavage, écume

3. Phase de résolution
   → Relâchement musculaire
   → Respiration bruyante
   → Confusion, somnolence
   → Amnésie de la crise


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CONDUITE À TENIR


PENDANT LA CRISE


1. PROTÉGER LA VICTIME

⚠ NE PAS ESSAYER D'ARRÊTER LES CONVULSIONS

Écarter les objets dangereux
Placer un coussin sous la tête
Desserrer les vêtements (col, cravate)


2. NE PAS :

✗ Mettre quoi que ce soit dans la bouche
✗ Retenir la victime
✗ Donner à boire
✗ Gifler


3. CHRONOMÉTRER

Noter l'heure de début
Durée de la crise


4. OBSERVER

Noter le type de mouvements
Côté des convulsions


APRÈS LA CRISE


1. LIBÉRER LES VOIES AÉRIENNES

Desserrer les vêtements
Ouvrir la bouche si possible


2. POSITION LATÉRALE DE SÉCURITÉ

Dès que les convulsions cessent


3. RASSURER

La personne est confuse
Parler calmement


4. LAISSER RÉCUPÉRER

Ne pas donner à boire immédiatement
Repos dans un endroit calme


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

QUAND ALERTER LE 15 ?


SYSTÉMATIQUEMENT SI :

→ Première crise convulsive
→ Crise durant plus de 5 minutes
→ Crises répétées sans reprise de conscience
→ Traumatisme associé
→ Grossesse
→ Diabète connu
→ Pas de reprise de conscience après 10 minutes
→ Difficulté respiratoire


PAS D'ALERTE NÉCESSAIRE SI :

→ Épileptique connu
→ Crise brève et habituelle
→ Reprise de conscience rapide
→ Entourage peut gérer


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CONVULSIONS FÉBRILES (ENFANT)


Surviennent chez l'enfant de 6 mois à 5 ans lors de fièvre élevée.


CONDUITE À TENIR :

Identique à la crise généralisée

PLUS :
   → Découvrir l'enfant
   → Refroidir (linge humide sur front)
   → Alerter le 15 systématiquement
"""
    }
]

db.chapters.update_one(
    {"id": "pse-ch6"},
    {"$push": {"fiches": {"$each": nouvelles_fiches_ch6}}}
)
print("  ✅ Ch6: Ajout de 3 fiches (Asthme, Diabète, Convulsions)")


# ═══════════════════════════════════════════════════════════
# CHAPITRE 10 : ATTEINTES CIRCONSTANCIELLES - FICHES MANQUANTES
# ═══════════════════════════════════════════════════════════

nouvelles_fiches_ch10 = [
    {
        "id": "pse-f10-3",
        "titre": "Noyade",
        "contenu": """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                    NOYADE - DÉTAILS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

MÉCANISME

Détresse respiratoire par inhalation de liquide (eau douce ou salée).


COMPLICATIONS

→ Arrêt respiratoire (spasme du larynx ou inondation)
→ Hypothermie
→ Arrêt cardiaque
→ Œdème pulmonaire secondaire (plusieurs heures après)


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

EXTRACTION DE L'EAU


SÉCURITÉ DU SAUVETEUR

Ne JAMAIS se mettre en danger
Évaluer ses capacités avant d'entrer dans l'eau


MÉTHODES PAR ORDRE DE PRIORITÉ :

1. TENDRE un objet (perche, corde)

2. LANCER une bouée de sauvetage

3. UTILISER une embarcation

4. NAGER jusqu'à la victime (en dernier recours)


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PRISE EN CHARGE SUR PLACE

Voir conduite à tenir complète dans Ch12 (Situations particulières)


POINTS CLÉS

✓ Sortir de l'eau rapidement
✓ Bilan : conscience + respiration
✓ Si arrêt : Commencer par 5 insufflations puis RCP
✓ Si respire : PLS
✓ Réchauffer
✓ Alerter 15 SYSTÉMATIQUEMENT (même si victime va bien)
✓ Hospitalisation obligatoire (risque d'œdème pulmonaire retardé)
"""
    },
    {
        "id": "pse-f10-4",
        "titre": "Intoxications",
        "contenu": """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                    INTOXICATIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

DÉFINITION

Pénétration dans l'organisme d'une substance toxique.


VOIES D'ENTRÉE

→ INGESTION (bouche) : Médicaments, produits ménagers, champignons, aliments
→ INHALATION (respiration) : CO, gaz, fumées, solvants
→ INJECTION (piqûre) : Drogues, venins
→ CONTACT (peau/yeux) : Produits caustiques, pesticides


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SIGNES GÉNÉRAUX

Variables selon le toxique :
   → Troubles digestifs (nausées, vomissements, diarrhée)
   → Troubles neurologiques (confusion, convulsions, coma)
   → Troubles respiratoires
   → Troubles cardiaques
   → Brûlures (produits caustiques)


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CONDUITE À TENIR GÉNÉRALE


1. SÉCURITÉ

Se protéger (gants, aération si gaz)
Éloigner la victime de la source si nécessaire


2. IDENTIFIER LE TOXIQUE

Emballage, étiquette
Questionner la victime ou l'entourage
Conserver le produit ou l'emballage


3. ALERTER

→ 15 (SAMU)
→ Centre antipoison (numéro local ou 15)

Préciser :
   Produit en cause
   Quantité ingérée/inhalée
   Heure de l'exposition
   Âge et poids de la victime
   Signes présentés


4. SURVEILLER

Conscience
Respiration
Signes d'aggravation


5. GESTES SELON LA VOIE


INGESTION :

✗ NE PAS FAIRE VOMIR (risque d'inhalation, aggravation si caustique)
✗ NE PAS DONNER À BOIRE (sauf avis du 15)
✓ Position demi-assise si conscient
✓ PLS si inconscient
✓ Conserver vomissures spontanées (analyse)


INHALATION :

✓ Aérer, ouvrir portes et fenêtres
✓ Sortir la victime à l'air libre
✓ Desserrer les vêtements
✓ Position demi-assise
✗ Ne pas s'exposer soi-même


CONTACT CUTANÉ :

✓ Retirer vêtements contaminés
✓ Rincer abondamment à l'eau (15-20 min)
✓ Protection des yeux si projection


INJECTION (piqûre, morsure) :

✓ Allonger la victime
✓ Immobiliser le membre
✓ Ne pas inciser, ne pas aspirer
✓ Retirer bague/bracelet (gonflement)


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

INTOXICATION AU MONOXYDE DE CARBONE (CO)


GAZ INVISIBLE, INODORE, MORTEL


SOURCES :

→ Chaudières mal entretenues
→ Chauffages d'appoint
→ Moteurs à combustion (voiture, groupe électrogène)
→ Barbecues, braseros en intérieur


SIGNES :

→ Maux de tête
→ Nausées, vomissements
→ Vertiges
→ Faiblesse
→ Confusion
→ Perte de connaissance
→ Décès

⚠ Souvent plusieurs victimes dans le même lieu


CONDUITE À TENIR :

1. AÉRER immédiatement

2. ÉVACUER la victime à l'air libre
   ⚠ Ne pas s'exposer soi-même

3. Alerter 18 et 15

4. Si inconscient : PLS

5. Si arrêt cardiaque : RCP

6. Oxygène dès que possible

7. Traitement : Oxygénothérapie hyperbare


PRÉVENTION :

→ Entretien annuel des appareils à combustion
→ Ventilation des locaux
→ Détecteurs de CO
→ Ne jamais utiliser chauffage d'appoint ou barbecue en intérieur
"""
    }
]

db.chapters.update_one(
    {"id": "pse-ch10"},
    {"$push": {"fiches": {"$each": nouvelles_fiches_ch10}}}
)
print("  ✅ Ch10: Ajout de 2 fiches (Noyade détails, Intoxications)")

print(f"\n🎉 Fiches manquantes ajoutées avec succès")
print(f"📊 Chapitres complétés : Ch5 (+2), Ch6 (+3), Ch10 (+2)")

client.close()
