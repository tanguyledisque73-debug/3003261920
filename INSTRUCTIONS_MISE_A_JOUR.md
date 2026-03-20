# 🚀 Instructions pour Mettre à Jour la Production

## Problème Actuel
Le compte stagiaire test n'a plus de chapitres PSE en production parce que la base de données doit être réinitialisée avec le nouveau contenu (chapitres PSC complets).

## ✅ Solution en 2 Étapes

### ÉTAPE 1: Redéployer l'Application

1. Dans votre interface Emergent, cliquez sur **"Deploy"** ou **"Redeploy"**
2. Attendez que le déploiement soit terminé (quelques minutes)
3. Vérifiez que l'application est accessible sur : https://code-migrate-3.emergent.host

### ÉTAPE 2: Réinitialiser la Base de Données

**Option A - Via Script (Plus simple)**

```bash
bash /app/update_production.sh
```

Le script va :
- Se connecter avec votre compte admin
- Nettoyer la base de données
- Réinitialiser avec tout le nouveau contenu (PSE + PSC complets)

**Option B - Manuellement (Si le script ne fonctionne pas)**

1. **Obtenir votre token admin:**
```bash
curl -X POST "https://code-migrate-3.emergent.host/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email":"ledisque.tanguy73@hotmail.com","password":"NewAdmin123!"}'
```
Copiez le `token` de la réponse.

2. **Forcer le reseed (remplacez VOTRE_TOKEN):**
```bash
curl -X POST "https://code-migrate-3.emergent.host/api/admin/force-reseed?token=VOTRE_TOKEN"
```

3. **Réinitialiser la base:**
```bash
curl -X POST "https://code-migrate-3.emergent.host/api/seed"
```

## ✅ Vérification

Après la réinitialisation :

1. Allez sur https://code-migrate-3.emergent.host
2. Connectez-vous avec le compte stagiaire test :
   - Email: `stagiaire.test@secours73.fr`
   - Mot de passe: `test123`
3. Cliquez sur "Chapitres"
4. **Vous devriez voir les 12 chapitres PSE !**

## 📊 Contenu Complet Après Mise à Jour

- ✅ 12 chapitres PSE (37 fiches)
- ✅ 8 chapitres PSC (19 fiches) avec contenu professionnel complet
- ✅ 20 quiz (96 questions)
- ✅ Formatage professionnel SANS markdown

## ⚠️ Important

Cette opération va **réinitialiser toute la base de données**, y compris les comptes utilisateurs. Après la réinitialisation :

- Le compte admin sera recréé : `ledisque.tanguy73@hotmail.com` / `NewAdmin123!`
- Le compte formateur test : `test@secours73.fr` / `test123`
- Le compte stagiaire test : `stagiaire.test@secours73.fr` / `test123`

Si vous aviez d'autres utilisateurs créés, ils seront supprimés.

## 🆘 Besoin d'Aide ?

Si vous rencontrez un problème, partagez-moi :
1. L'URL de votre application
2. Le message d'erreur exact (capture d'écran)
3. Les logs si possibles
