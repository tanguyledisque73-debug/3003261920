#!/bin/bash

# Script pour corriger le groupe en production
# Remplacez VOTRE_URL par l'URL de votre application déployée
# Remplacez VOTRE_TOKEN par votre token admin

echo "🔧 CORRECTION DU GROUPE EN PRODUCTION"
echo "======================================"
echo ""
echo "ÉTAPE 1: Obtenez votre token admin"
echo "Appelez cette URL depuis votre navigateur ou Postman:"
echo ""
echo "POST https://VOTRE_URL/api/auth/login"
echo '{"email":"ledisque.tanguy73@hotmail.com","password":"NewAdmin123!"}'
echo ""
echo "Copiez le 'token' de la réponse"
echo ""
echo "======================================"
echo "ÉTAPE 2: Corrigez le groupe"
echo "Appelez cette URL:"
echo ""
echo "POST https://VOTRE_URL/api/admin/fix-groupe-formation?token=VOTRE_TOKEN&groupe_code=TEST0000&formation=PSE"
echo ""
echo "======================================"
echo "ÉTAPE 3: Vérifiez"
echo "Reconnectez-vous avec le compte stagiaire et vérifiez les chapitres"
echo ""
