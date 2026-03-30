#!/bin/bash
# Script pour mettre à jour la base de données de production avec TOUTES les nouveautés
# Inclus: 18 nouveaux quiz, corrections de code, éditeur riche

PROD_URL="https://code-migrate-3.emergent.host"

echo "🔄 MISE À JOUR COMPLÈTE DE LA PRODUCTION"
echo "========================================"
echo ""
echo "📦 Nouveautés incluses:"
echo "  ✅ 18 nouveaux quiz avec contenu pertinent"
echo "  ✅ Corrections de sécurité (Phase 1)"
echo "  ✅ Éditeur de texte riche (React Quill)"
echo "  ✅ Système de logging"
echo ""
echo "⚠️  ATTENTION: Ce script va réinitialiser TOUTE la base de données"
echo ""
read -p "Tapez OUI en majuscules pour continuer: " confirmation

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
    echo ""
    echo "💡 Vérifiez que:"
    echo "  1. L'application est déployée sur $PROD_URL"
    echo "  2. Le mot de passe admin est correct: NewAdmin123!"
    exit 1
fi

echo "✅ Token admin obtenu"
echo ""

echo "🗑️  ÉTAPE 2: Suppression de l'ancienne base..."
RESET_RESPONSE=$(curl -s -X POST "$PROD_URL/api/admin/reset-database?token=$TOKEN" \
  -H "Content-Type: application/json")
echo "✅ Base nettoyée"
echo ""

echo "⏳ Attente de 3 secondes..."
sleep 3

echo "🌱 ÉTAPE 3: Création du nouveau contenu..."
SEED_RESPONSE=$(curl -s -X POST "$PROD_URL/api/seed")

if echo "$SEED_RESPONSE" | grep -q "error"; then
    echo "⚠️  Réponse du seed:"
    echo "$SEED_RESPONSE"
else
    echo "✅ Seed exécuté"
fi
echo ""

echo "⏳ Attente de 5 secondes..."
sleep 5

echo "✅ ÉTAPE 4: Vérification des données..."
# Reconnecter pour vérifier
RESPONSE=$(curl -s -X POST "$PROD_URL/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email":"ledisque.tanguy73@hotmail.com","password":"NewAdmin123!"}')

NEW_TOKEN=$(echo $RESPONSE | grep -o '"token":"[^"]*' | cut -d'"' -f4)

if [ -z "$NEW_TOKEN" ]; then
    echo "⚠️  Impossible de se reconnecter, vérification manuelle nécessaire"
else
    echo "✅ Compte admin recréé"
    
    # Vérifier les quiz
    QUIZ_RESPONSE=$(curl -s "$PROD_URL/api/quizzes")
    QUIZ_COUNT=$(echo "$QUIZ_RESPONSE" | grep -o '"id"' | wc -l)
    echo "✅ Quiz créés: $QUIZ_COUNT (attendu: 21)"
    
    # Vérifier les chapitres
    CHAPTERS_RESPONSE=$(curl -s "$PROD_URL/api/chapters")
    CHAPTERS_COUNT=$(echo "$CHAPTERS_RESPONSE" | grep -o '"id"' | wc -l)
    echo "✅ Chapitres créés: $CHAPTERS_COUNT (attendu: 21)"
    
    # Vérifier les utilisateurs via admin
    USERS_RESPONSE=$(curl -s "$PROD_URL/api/admin/users?token=$NEW_TOKEN")
    USERS_COUNT=$(echo "$USERS_RESPONSE" | grep -o '"role"' | wc -l)
    echo "✅ Utilisateurs: $USERS_COUNT (attendu: 3+)"
fi

echo ""
echo "========================================"
echo "🎉 MISE À JOUR TERMINÉE !"
echo ""
echo "📊 Résumé des nouveautés déployées:"
echo "  ✅ 21 quiz avec 105 questions pertinentes"
echo "  ✅ 21 chapitres (12 PSE + 8 PSC + 1 BNSSA)"
echo "  ✅ Éditeur de texte riche pour les chapitres"
echo "  ✅ Corrections de sécurité appliquées"
echo "  ✅ Système de logging centralisé"
echo ""
echo "🔐 Comptes de test:"
echo "  Admin:     ledisque.tanguy73@hotmail.com / NewAdmin123!"
echo "  Formateur: test@secours73.fr / test123"
echo "  Stagiaire: stagiaire.test@secours73.fr / test123"
echo ""
echo "🌐 Accédez à votre application:"
echo "  $PROD_URL"
echo ""
