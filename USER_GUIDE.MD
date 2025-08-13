# 📚 Guide Utilisateur de Minou - Animal de Compagnie Virtuel

## 🐾 Table des matières
1. [Présentation de Minou](#-présentation-de-minou)
2. [Installation](#-installation)
3. [Fonctionnalités principales](#-fonctionnalités-principales)
4. [Personnalisation](#-personnalisation)
5. [Dépannage](#-dépannage)
6. [FAQ](#-questions-fréquentes)

## 🌟 Présentation de Minou
Minou est un compagnon virtuel intelligent qui vit sur votre bureau. Il vous aide à rester organisé avec des rappels, des notes et des alertes système, le tout avec une touche ludique.

## 💾 Installation
1. **Prérequis** :
   - Python 3.7+
   - Windows, macOS ou Linux
   - Connexion Internet (pour certaines fonctionnalités)

2. **Installation** :
   ```bash
   # Installer les dépendances
   pip install -r requirements.txt
   
   # Lancer Minou
   python main.py
   ```

## 🎮 Fonctionnalités principales

### Interface utilisateur
- **Fenêtre principale** : Affiche Minou et ses animations
- **Bulle de dialogue** : Messages contextuels
- **Menu système** : Clic droit sur l'icône
- **Chat** : Ouvrir avec un clic sur Minou

### Interactions avec Minou
- **Clic gauche** : Caresser
- **Clic droit** : Menu contextuel
- **Glisser-déposer** : Déplacer Minou
- **Double-clic** : Ouvrir le chat

### Chat intelligent
Communiquez naturellement avec Minou :

#### Commandes de base :
- `Bonjour` / `Salut` - Salutations
- `Comment ça va ?` - État de Minou
- `Tu fais quoi ?` - Activité actuelle
- `Au revoir` - Fermer la session

#### Gestion des notes :
- "Note que j'ai un RDV demain"
- "Retiens le code 1234"
- "Quelles sont mes notes ?"

#### Rappels :
- "Rappelle-moi dans 10 minutes"
- "À 15h, rappelle-moi l'appel"
- "Tous les lundis à 9h, réunion"

### Nettoyage automatique 🧹
Minou gère son espace :
- Les crottes apparaissent aléatoirement
- Cliquez dessus pour les nettoyer
- Nettoyage automatique après un délai
- Récompenses pour un environnement propre

### Surveillance système 💻
- Alerte batterie faible
- Surveillance mémoire/CPU
- Notifications personnalisables

## 🎨 Personnalisation
- Changer le nom de Minou
- Modifier le thème (clair/sombre)
- Ajuster la transparence
- Personnaliser les messages

## 🔧 Dépannage
1. **Minou ne démarre pas**
   - Vérifiez Python 3.7+
   - Installez les dépendances
   - Consultez les logs

2. **Le chat ne répond pas**
   - Vérifiez la connexion Internet
   - Redémarrez Minou
   - Vérifiez les paramètres d'API

## ❓ Questions fréquentes

**Q: Comment désactiver les notifications ?**
R: Via le menu Paramètres > Notifications

**Q: Où sont stockées mes notes ?**
R: Dans le fichier `minou_notes.json`

**Q: Comment mettre à jour Minou ?**
```bash
git pull origin main
pip install -r requirements.txt --upgrade
```

---
*Dernière mise à jour : 13/08/2025*
