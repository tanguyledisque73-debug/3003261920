#!/usr/bin/env python3
"""
Ajouter les fiches VRAIMENT manquantes
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

print("📝 Ajout des fiches RÉELLEMENT manquantes...")

# ═══════════════════════════════════════════════════════════
# CHAPITRE 5 : Hémorragies (URGENCE VITALE)
# ═══════════════════════════════════════════════════════════

fiche_hemorragies_ch5 = {
    "id": "pse-f5-4",
    "titre": "Hémorragies externes - Urgence vitale",
    "contenu": """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
            HÉMORRAGIE EXTERNE - URGENCE VITALE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

DÉFINITION

Saignement abondant, visible, qui ne s'arrête pas spontanément.


URGENCE ABSOLUE

Perte de 1 litre de sang → Choc hémorragique
Perte de 2 litres → Risque de décès imminent


RECONNAÎTRE

→ Saignement abondant visible
→ Écoulement continu de sang
→ Flaque de sang qui s'agrandit
→ Vêtements imbibés de sang


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SIGNES DE CHOC HÉMORRAGIQUE

→ Pâleur extrême
→ Sueurs froides
→ Pouls rapide et faible
→ Respiration rapide et superficielle
→ Angoisse intense
→ Soif
→ Confusion, troubles de la conscience
→ Froideur des extrémités


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CONDUITE À TENIR


PRIORITÉ N°1 : ARRÊTER L'HÉMORRAGIE


MÉTHODE 1 : COMPRESSION DIRECTE (à privilégier)

1. METTRE DES GANTS immédiatement

2. COMPRIMER FORTEMENT sur la plaie
   → Avec la paume de la main
   → Utiliser un linge propre, compresse, vêtement
   → Si rien : Main nue (urgence vitale)

3. MAINTENIR LA PRESSION
   → Sans relâcher
   → Pendant toute la durée (15-30 minutes possibles)
   → Jusqu'à l'arrivée des secours

4. ALLONGER la victime

5. ALERTER ou FAIRE ALERTER le 15


Si fatigue musculaire :
   → Demander un relais
   → Transition SANS relâcher la pression


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

MÉTHODE 2 : PANSEMENT COMPRESSIF

Si compression directe efficace mais fatigante :

1. Placer plusieurs compresses épaisses sur la plaie

2. Enrouler fermement avec bande
   → Crêpe ou élastique
   → Serrer fortement

3. Fixer avec sparadrap

4. Vérifier l'efficacité
   → Le saignement doit s'arrêter

⚠ Si le sang traverse :
   → NE PAS retirer le pansement
   → Ajouter des compresses PAR-DESSUS
   → Rebander plus serré


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

MÉTHODE 3 : GARROT (EN DERNIER RECOURS)


UNIQUEMENT SI :

→ Hémorragie d'un membre (bras ou jambe)
→ Compression directe IMPOSSIBLE ou INEFFICACE
→ Amputation traumatique
→ Nombreuses victimes (ne pas rester bloqué sur une seule)
→ Zone de combat, attentat


TECHNIQUE :

1. Placer le garrot ENTRE la plaie et le cœur
   → Quelques centimètres au-dessus de la plaie
   → Sur un membre (jamais sur une articulation)

2. Serrer TRÈS FORT
   → Jusqu'à arrêt COMPLET du saignement
   → Le membre va devenir froid et pâle (normal)

3. Noter l'HEURE de pose
   → Sur le garrot
   → Sur le front de la victime
   → Sur papier

4. Laisser le membre VISIBLE

5. NE JAMAIS desserrer ou retirer
   → Sauf ordre médical du SAMU


MATÉRIEL :

→ Garrot tourniquet (CAT, SOFTT-W) : IDÉAL
→ Ou lien large (> 5 cm) : cravate, écharpe, bande
→ JAMAIS : fil, ficelle, câble électrique


LOCALISATION :

Membre supérieur : Sur le BRAS (jamais avant-bras)
Membre inférieur : Sur la CUISSE (jamais mollet)


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

APRÈS ARRÊT DE L'HÉMORRAGIE


1. ALLONGER la victime
   → Jambes surélevées (si pas de douleur)
   → Favorise le retour veineux


2. COUVRIR
   → Couverture de survie
   → Prévenir l'hypothermie


3. RASSURER
   → Parler calmement
   → "Les secours arrivent"


4. NE PAS DONNER À BOIRE
   → Risque de vomissement
   → Anesthésie possible


5. SURVEILLER
   → Conscience
   → Respiration
   → Réapparition du saignement


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ERREURS À NE PAS COMMETTRE

✗ Relâcher la pression pour "voir si ça saigne encore"
✗ Nettoyer la plaie (perte de temps)
✗ Retirer les premiers pansements
✗ Desserrer un garrot
✗ Minimiser la gravité
✗ Transporter soi-même à l'hôpital
"""
}

db.chapters.update_one(
    {"id": "pse-ch5"},
    {"$push": {"fiches": fiche_hemorragies_ch5}}
)
print("  ✅ Ch5: Ajout fiche 'Hémorragies externes - Urgence vitale'")


# ═══════════════════════════════════════════════════════════
# CHAPITRE 12 : Plan blanc et NRBC
# ═══════════════════════════════════════════════════════════

nouvelles_fiches_ch12 = [
    {
        "id": "pse-f12-3",
        "titre": "Plan blanc et catastrophes",
        "contenu": """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
            PLAN BLANC ET GESTION DE CRISE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

DÉFINITION DU PLAN BLANC

Dispositif exceptionnel permettant à un établissement de santé de mobiliser immédiatement des moyens supplémentaires pour faire face à une situation de crise.


DÉCLENCHEMENT

Le plan blanc est déclenché en cas de :
   → Afflux massif de victimes
   → Catastrophe naturelle
   → Attentat
   → Accident collectif
   → Épidémie majeure
   → Canicule exceptionnelle


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

OBJECTIFS

→ Augmenter les capacités d'accueil des urgences
→ Mobiliser le personnel (rappel du personnel en repos)
→ Libérer des lits (sortie anticipée de patients stables)
→ Réorganiser les services
→ Annuler les interventions non urgentes


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SITUATION DE CATASTROPHE


DÉFINITION

Événement dépassant les capacités habituelles de secours :
   → Nombre de victimes > moyens disponibles


ORGANISATION DES SECOURS


CHAÎNE DE COMMANDEMENT

Directeur des Opérations de Secours (DOS)
   ↓
Commandant des Opérations de Secours (COS)
   ↓
Secteurs d'intervention


ZONAGE

ZONE D'EXCLUSION (zone rouge)
   → Danger présent
   → Accès interdit sauf équipes spécialisées

ZONE DE SOUTIEN (zone jaune)
   → Poste Médical Avancé (PMA)
   → Triage des victimes
   → Premiers soins

ZONE D'APPUI (zone verte)
   → Poste de Commandement (PC)
   → Noria ambulances
   → Familles, médias


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

TRIAGE DES VICTIMES


Méthode de tri permettant de prioriser les soins en fonction de la gravité et des chances de survie.


CATÉGORIES (Tri START ou similaire)


URGENCE ABSOLUE (UA) - Rouge
   → Détresse vitale immédiate
   → Nécessite soins immédiats
   → Pronostic vital engagé
   → Exemples : Hémorragie, détresse respiratoire

URGENCE RELATIVE (UR) - Jaune
   → Blessures graves mais état stable
   → Peut attendre quelques heures
   → Exemples : Fractures, brûlures moyennes

IMPLIQUÉ (I) - Vert
   → Blessures légères
   → Peut marcher
   → Peut attendre plusieurs heures
   → Exemples : Plaies simples, contusions

DÉCÉDÉ ou DÉPASSÉ (D) - Noir/Blanc
   → Décédé
   → Ou pronostic désespéré avec moyens limités


MATÉRIEL DE TRIAGE

Bracelets ou étiquettes de couleur
Identification par numéro
Traçabilité des victimes


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

RÔLE DU SECOURISTE EN CATASTROPHE


1. Se présenter au Poste de Commandement

2. Recevoir une mission spécifique

3. Travailler en équipe

4. Appliquer les consignes du triage

5. Ne pas se focaliser sur une seule victime

6. Gestes simples et rapides

7. Transmission des informations

8. Gérer ses émotions
"""
    },
    {
        "id": "pse-f12-4",
        "titre": "Risques NRBC",
        "contenu": """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                    RISQUES NRBC
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

DÉFINITION

NRBC : Nucléaire, Radiologique, Biologique, Chimique

Risques liés à des agents dangereux nécessitant une protection et une intervention spécifiques.


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

RISQUE NUCLÉAIRE (N)


SOURCES

→ Centrale nucléaire
→ Explosion nucléaire
→ Bombe sale (explosive + matières radioactives)


DANGERS

→ Irradiation (exposition aux rayonnements)
→ Contamination (particules radioactives sur/dans le corps)
→ Effets immédiats (brûlures, syndrome d'irradiation)
→ Effets à long terme (cancers)


CONDUITE À TENIR

SE METTRE À L'ABRI :
   → Bâtiment en dur
   → Fermer portes et fenêtres
   → Couper ventilation
   → Écouter la radio
   → Suivre les consignes des autorités

NE PAS :
   → S'exposer
   → Aller chercher les enfants à l'école (pris en charge)
   → Téléphoner (saturation des réseaux)


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

RISQUE RADIOLOGIQUE (R)


SOURCES

→ Sources radioactives industrielles ou médicales
→ Accident de transport de matières radioactives


PROTECTION

Distance : S'éloigner de la source
Temps : Limiter le temps d'exposition
Écran : Interposer un obstacle (mur, plomb)


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

RISQUE BIOLOGIQUE (B)


AGENTS

→ Bactéries (anthrax, peste)
→ Virus (variole, fièvres hémorragiques)
→ Toxines (ricine, botulique)


MODES DE TRANSMISSION

→ Aérien (inhalation)
→ Contact (peau, muqueuses)
→ Ingestion (eau, aliments)


SIGNES D'ALERTE

→ Cas groupés de maladies inhabituelles
→ Mortalité animale anormale
→ Syndrome pseudo-grippal massif


PROTECTION

→ EPI adaptés (masque FFP2 minimum, combinaison)
→ Décontamination si nécessaire
→ Isolement des victimes
→ Prophylaxie (antibiotiques préventifs selon agent)


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

RISQUE CHIMIQUE (C)


AGENTS

→ Toxiques industriels (chlore, ammoniac, acide)
→ Gaz de combat (sarin, VX, ypérite)
→ Fumées d'incendie


VOIES DE PÉNÉTRATION

→ Respiratoire (inhalation)
→ Cutanée (contact)
→ Digestive (ingestion)


SIGNES SELON AGENT

Neurotoxiques :
   → Convulsions, myosis, sécrétions
   
Suffocants :
   → Détresse respiratoire, œdème pulmonaire

Vésicants :
   → Brûlures cutanées, cloques


CONDUITE À TENIR

1. FUIR la zone contaminée
   → S'éloigner perpendiculairement au vent
   → Gagner un point haut (gaz lourds au sol)

2. SE CONFINER si impossible de fuir
   → Fermer portes, fenêtres
   → Couper ventilation
   → Colmater les ouvertures (scotch, chiffons humides)

3. SE DÉCONTAMINER
   → Retirer vêtements contaminés (sans les passer par la tête)
   → Douche à l'eau tiède savonneuse (20 min)
   → Du haut vers le bas

4. ALERTER
   → 18 (Pompiers)
   → 15 (SAMU)
   → Préciser suspicion NRBC


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PRINCIPES GÉNÉRAUX NRBC


POUR LE SECOURISTE


⚠ NE PAS INTERVENIR EN ZONE CONTAMINÉE sans :
   → Formation spécifique
   → EPI adaptés (combinaison étanche, ARI)
   → Autorisation et encadrement


RESTER À DISTANCE DE SÉCURITÉ

ALERTER les équipes spécialisées :
   → Pompiers (cellule CMIC)
   → Équipes NRBC militaires si nécessaire


ATTENDRE les consignes


PROTÉGER LES VICTIMES HORS ZONE :
   → Isolement si contamination
   → Décontamination d'urgence (déshabillage + douche)
   → Soins selon symptômes


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

DÉCONTAMINATION D'URGENCE


DÉSHABILLAGE

Retirer TOUS les vêtements et objets
   → 80 à 90% de la décontamination
   → Mettre dans sac étanche
   → Ne pas passer par la tête (couper si nécessaire)


DOUCHE

Eau tiède (pas chaude, ouvre les pores)
Savon doux
Du haut vers le bas
20 minutes minimum
Insister sur cheveux, plis, ongles


HABILLAGE

Vêtements propres ou couverture


⚠ Personnel effectuant la décontamination : EPI obligatoires
"""
    }
]

db.chapters.update_one(
    {"id": "pse-ch12"},
    {"$push": {"fiches": {"$each": nouvelles_fiches_ch12}}}
)
print("  ✅ Ch12: Ajout de 2 fiches (Plan blanc, Risques NRBC)")

print(f"\n🎉 TOUTES les fiches manquantes ont été ajoutées")
print(f"📊 Ch5: 4 fiches | Ch12: 4 fiches")

# Vérification finale
print("\n📊 RÉCAPITULATIF FINAL PSE:")
pse_chapters = db.chapters.find({"formation_type": "PSE"}).sort("numero", 1)
total_fiches = 0
for ch in pse_chapters:
    fiches_count = len(ch['fiches'])
    total_fiches += fiches_count
    print(f"  Ch{ch['numero']}: {ch['titre']} ({fiches_count} fiches)")

print(f"\n✅ TOTAL: 12 chapitres PSE avec {total_fiches} fiches")

client.close()
