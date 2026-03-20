#!/bin/bash
# Script pour mettre à jour la base de données de production
# À exécuter APRÈS le redéploiement de l'application

PROD_URL="https://code-migrate-3.emergent.host"

echo "🔄 MISE À JOUR DE LA BASE DE DONNÉES DE PRODUCTION"
echo "=================================================="
echo ""
echo "⚠️  ATTENTION: Ce script va réinitialiser TOUTE la base de données"
echo "   et recréer le contenu avec les nouveaux chapitres PSC complets."
echo ""
read -p "Êtes-vous sûr de vouloir continuer? (tapez OUI en majuscules): " confirmation

if [ "$confirmation" != "OUI" ]; then
    echo "❌ Annulé"
    exit 1
fi

echo ""
echo "🔐 ÉTAPE 1: Connexion admin..."
RESPONSE=$(curl -s -X POST "$PROD_URL/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email":"ledisque.tanguy73@hotmail.com","password":"NewAdmin123!"}')

TOKEN=$(echo $RESPONSE | grep -o '"token":"[^"]*' | cut -d'"' -f4)

if [ -z "$TOKEN" ]; then
    echo "❌ Erreur: Impossible d'obtenir le token admin"
    echo "Réponse: $RESPONSE"
    exit 1
fi

echo "✅ Token admin obtenu"
echo ""

echo "🗑️  ÉTAPE 2: Nettoyage de la base (force reseed)..."
RESEED_RESPONSE=$(curl -s -X POST "$PROD_URL/api/admin/force-reseed?token=$TOKEN")
echo "Response: $RESEED_RESPONSE"
echo ""

echo "⏳ Attente de 3 secondes..."
sleep 3

echo "🌱 ÉTAPE 3: Réinitialisation avec nouveau contenu..."
SEED_RESPONSE=$(curl -s -X POST "$PROD_URL/api/seed")
echo "Response: $SEED_RESPONSE"
echo ""

echo "✅ ÉTAPE 4: Vérification..."
# Reconnecter pour avoir un nouveau token
RESPONSE=$(curl -s -X POST "$PROD_URL/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email":"ledisque.tanguy73@hotmail.com","password":"NewAdmin123!"}')

NEW_TOKEN=$(echo $RESPONSE | grep -o '"token":"[^"]*' | cut -d'"' -f4)

if [ ! -z "$NEW_TOKEN" ]; then
    echo "✅ Compte admin recréé avec succès"
    
    # Vérifier les chapitres PSC
    PSC_COUNT=$(curl -s "$PROD_URL/api/psc/chapters" | grep -o '"numero"' | wc -l)
    echo "✅ Chapitres PSC: $PSC_COUNT"
    
    # Vérifier les chapitres PSE
    PSE_RESPONSE=$(curl -s "$PROD_URL/api/chapters?formation_type=PSE")
    PSE_COUNT=$(echo $PSE_RESPONSE | grep -o '"numero"' | wc -l)
    echo "✅ Chapitres PSE: $PSE_COUNT"
else
    echo "⚠️  Vérification manuelle nécessaire"
fi

echo ""
echo "=================================================="
echo "🎉 MISE À JOUR TERMINÉE !"
echo ""
echo "Prochaines étapes:"
echo "1. Connectez-vous sur: $PROD_URL"
echo "2. Email: ledisque.tanguy73@hotmail.com"
echo "3. Mot de passe: NewAdmin123!"
echo "4. Vérifiez que les chapitres PSE et PSC s'affichent correctement"
echo ""
