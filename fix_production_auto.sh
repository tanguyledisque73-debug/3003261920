#!/bin/bash

API_URL="https://code-migrate-3.emergent.host"

echo "🔐 ÉTAPE 1: Connexion admin..."
echo "================================"

# Obtenir le token admin
RESPONSE=$(curl -s -X POST "$API_URL/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email":"ledisque.tanguy73@hotmail.com","password":"NewAdmin123!"}')

echo "Réponse: $RESPONSE"

# Extraire le token
TOKEN=$(echo $RESPONSE | grep -o '"token":"[^"]*' | cut -d'"' -f4)

if [ -z "$TOKEN" ]; then
    echo "❌ Erreur: Impossible d'obtenir le token"
    echo "Réponse complète: $RESPONSE"
    exit 1
fi

echo "✅ Token obtenu: ${TOKEN:0:20}..."
echo ""

echo "🔧 ÉTAPE 2: Correction du groupe..."
echo "================================"

# Corriger le groupe
FIX_RESPONSE=$(curl -s -X POST "$API_URL/api/admin/fix-groupe-formation?token=$TOKEN&groupe_code=TEST0000&formation=PSE")

echo "Réponse: $FIX_RESPONSE"
echo ""

echo "✅ ÉTAPE 3: Vérification..."
echo "================================"

# Vérifier avec le compte stagiaire
STAGIAIRE_RESPONSE=$(curl -s -X POST "$API_URL/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email":"stagiaire.test@secours73.fr","password":"test123"}')

STAGIAIRE_TOKEN=$(echo $STAGIAIRE_RESPONSE | grep -o '"token":"[^"]*' | cut -d'"' -f4)

if [ -z "$STAGIAIRE_TOKEN" ]; then
    echo "❌ Erreur: Impossible de se connecter en stagiaire"
    exit 1
fi

# Récupérer les chapitres
CHAPITRES_RESPONSE=$(curl -s "$API_URL/api/stagiaire/chapitres?token=$STAGIAIRE_TOKEN")

# Compter les chapitres
NB_CHAPITRES=$(echo $CHAPITRES_RESPONSE | grep -o '"numero"' | wc -l)

echo "📚 Nombre de chapitres retournés: $NB_CHAPITRES"
echo ""

if [ "$NB_CHAPITRES" -gt 0 ]; then
    echo "🎉 SUCCÈS ! Les chapitres PSE sont maintenant visibles !"
    echo ""
    echo "Vous pouvez maintenant vous connecter sur:"
    echo "$API_URL"
    echo "avec le compte: stagiaire.test@secours73.fr / test123"
else
    echo "⚠️  Aucun chapitre retourné. Détails de la réponse:"
    echo "$CHAPITRES_RESPONSE"
fi
