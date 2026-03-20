#!/usr/bin/env python3
"""
Script pour corriger le groupe de test en production
À exécuter pour mettre à jour la base de production Atlas
"""
import os
import sys

# Demander confirmation
print("⚠️  CE SCRIPT VA METTRE À JOUR LA BASE DE PRODUCTION")
print("=" * 60)
print("\nQue va faire ce script :")
print("1. Se connecter à la base de production (Atlas)")
print("2. Mettre à jour le 'Groupe Test' avec formation = 'PSE'")
print("\nCela permettra aux stagiaires de voir les chapitres PSE.")
print("=" * 60)

# Pour l'instant, afficher juste les instructions
print("\n📋 INSTRUCTIONS POUR CORRIGER EN PRODUCTION:\n")
print("Option 1: Via l'interface admin de MongoDB Atlas")
print("   1. Connectez-vous à MongoDB Atlas")
print("   2. Allez dans votre cluster")
print("   3. Cliquez sur 'Browse Collections'")
print("   4. Trouvez la collection 'groupes'")
print("   5. Trouvez le document avec code 'TEST0000'")
print("   6. Modifiez le champ 'formation' de 'N/A' à 'PSE'")
print("   7. Sauvegardez")
print()
print("Option 2: Via l'API admin (RECOMMANDÉ)")
print("   Je vais créer un endpoint API pour vous permettre de corriger cela")
print()
print("Option 3: Redéploiement complet")
print("   Redéployez l'application avec toutes les nouvelles données")
