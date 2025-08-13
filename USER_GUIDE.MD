# 📚 Guide Utilisateur Complet - Minou Desktop Pet

## 🐾 Qu'est-ce que Minou ?
Minou est bien plus qu'un simple animal de compagnie virtuel ! C'est votre compagnon intelligent qui vit sur votre bureau et vous assiste dans votre quotidien. Il peut répondre à vos questions, prendre des notes, programmer des rappels, surveiller votre système, et tout ça avec une personnalité attachante et pleine d'humour !

---

## 🚀 Installation Rapide

### Prérequis
- **Python 3.7+** installé sur votre système
- **Système d'exploitation** : Windows, macOS ou Linux
- **Connexion Internet** (optionnelle, pour l'IA avancée)

### Installation
```bash
# 1. Téléchargez le projet
git clone https://github.com/votre-repo/minou-desktop-pet
cd minou-desktop-pet

# 2. Installez les dépendances
pip install -r requirements.txt

# 3. Lancez Minou
python main.py
```

### Premier lancement
Au premier démarrage, Minou vous accueillera et vous proposera de configurer vos préférences de base (nom, type d'animal, etc.).

---

## 🎮 Interactions avec Minou

### Contrôles de base
| Action | Résultat |
|--------|----------|
| **Clic gauche** | Caresser Minou (attention à ne pas trop cliquer !) |
| **Clic maintenu + glisser** | Déplacer Minou sur l'écran |
| **Clic droit sur Minou** | Menu contextuel rapide |
| **Double-clic sur Minou** | Ouvrir l'interface de chat |
| **Clic sur l'icône système** | Afficher/Masquer Minou |
| **Clic droit sur l'icône système** | Menu complet |
| **Double-clic sur l'icône système** | Ouvrir directement le chat |

### Animations et comportements
- **Idle** : Minou se repose tranquillement
- **Walk** : Se promène sur votre écran
- **Run** : Court vers les bords de l'écran
- **Jump** : Fait des bonds joyeux
- **Slide** : Glisse avec style
- **Hurt** : Réaction quand vous cliquez trop
- **Dead** : Animation dramatique si vous êtes trop brutal !

---

## 💬 Système de Chat Intelligent

### Comment ouvrir le chat
1. **Double-clic** sur Minou
2. **Double-clic** sur l'icône système
3. **Menu contextuel** → "💬 Parler à Minou"

### Interface de chat
- **Champ de saisie** : Tapez votre message naturellement
- **Bouton 💬** : Envoyer le message
- **Bouton ✕** : Fermer le chat
- **Auto-fermeture** : Se ferme automatiquement après 30 secondes d'inactivité
- **Pendant la frappe** : L'auto-fermeture est suspendue

### Types de réponses selon votre configuration

#### Mode Hors-ligne (sans API IA)
Minou répondra avec des réponses pré-programmées basiques :
- Salutations simples
- Réactions émotionnelles
- Commandes de base (notes, rappels)
- **Limitation** : Ne peut pas répondre à des questions complexes comme "Quelle est la capitale de la Chine ?"

#### Mode IA Avancée (avec API Gemini)
Avec une clé API configurée, Minou devient un vrai assistant intelligent :
- **Questions générales** : "Quelle est la capitale de la Chine ?" → Réponse précise
- **Calculs** : "Combien font 15 × 23 ?" → Calcul automatique
- **Conseils** : "Comment organiser mon temps ?" → Suggestions personnalisées
- **Conversations** : Discussions naturelles et contextuelles
- **Aide technique** : Questions sur programmation, dépannage, etc.

---

## 📝 Gestion des Notes

### Créer des notes
```
Exemples de commandes :
- "Note que j'ai RDV chez le dentiste jeudi"
- "Retiens le code wifi : ABC123"
- "Noter : acheter du lait et des œufs"
- "Souviens-toi que Marie préfère le thé au café"
```

### Consulter vos notes
- **Menu système** → "📝 Mes notes"
- Dans le chat : "Quelles sont mes notes ?"
- Affichage des 3 dernières notes par défaut

---

## ⏰ Système de Rappels

### Programmer des rappels
```
Formats supportés :
- "Rappelle-moi dans 10 minutes de prendre mes médicaments"
- "Dans 2 heures, rappel réunion équipe"
- "À 15h30, appeler le client"
```

### Types de rappels
- **Ponctuels** : Une seule fois
- **Notifications** : Bulle + son + notification système
- **Persistance** : Les rappels survivent au redémarrage

---

## 🍖 Système d'Alimentation

### Nourrir Minou
- **Menu système** → "🍖 Nourriture" → "Ajouter nourriture"
- La nourriture apparaît aléatoirement sur l'écran
- **Minou court automatiquement** vers la nourriture la plus proche
- **Déplaçable** : Vous pouvez faire glisser la nourriture
- **Réaction** : Minou montre sa satisfaction en mangeant

### Nettoyage
- **Menu** → "Nettoyer nourriture" pour tout supprimer d'un coup

---

## 💩 Système de Besoins Naturels (Oui, c'est drôle !)

### Comment ça marche
- **Spawn automatique** : Minou fait ses besoins toutes les 1-2 minutes
- **Spawn manuel** : Menu → "💩 Propreté" → "Faire ses besoins"
- **Nettoyage** : Cliquez sur une crotte pour la nettoyer
- **Auto-nettoyage** : Les crottes disparaissent automatiquement après un moment
- **Réaction de Minou** : "Oops... désolé ! 💩"

### Gestion de la propreté
- **Nettoyage global** : Menu → "Nettoyer" pour tout nettoyer d'un coup
- **Récompenses** : Un environnement propre rend Minou plus heureux !

---

## 🎵 Système Audio

### Contrôle du son
- **Menu système** → "🔊 Désactiver son" / "🔇 Activer son"
- **Sons aléatoires** : Minou fait des bruits toutes les 1-5 minutes
- **Sons contextuels** : Réactions aux interactions

### Types de sons
- **Sons d'animal** : Miaulements (chat) ou aboiements (chien)
- **Fréquence** : Réglable dans les paramètres
- **Volume système** : Respecte les paramètres audio de votre OS

---

## 🎮 Télécommande de Minou

### Ouvrir la télécommande
- **Menu système** → "🎮 Télécommande"
- **Interface moderne** avec D-pad et boutons d'action

### Contrôles disponibles
- **Flèches directionnelles** : Déplacer Minou manuellement
- **W, A, S, D** : Déplacement alternatif au clavier
- **Bouton Stop** : Arrêter le mouvement
- **🦘 Saut** : Faire sauter Minou (Barre d'espace)
- **🛷 Glissade** : Animation de glissade (Shift)

### Mode de contrôle
- **Activation automatique** : Ouvrir la télécommande désactive les mouvements aléatoires
- **Fermeture** : Minou reprend ses activités normales après 15 secondes

---

## 😴 Mode Tranquille

### Activer le mode tranquille
- **Menu système** → "🐾 Animal" → "😴 Rester tranquille"
- **Effet immédiat** : Minou arrête tous ses mouvements et sons

### Qu'est-ce qui s'arrête ?
- ❌ Mouvements aléatoires
- ❌ Sons automatiques
- ❌ Messages spontanés
- ❌ Spawn de crottes
- ✅ Chat et interactions manuelles restent disponibles

### Sortie du mode tranquille
- **Manuelle** : Menu → "😸 Reprendre activité"
- **Automatique** : Minou peut reprendre activité après 30-60 secondes aléatoirement

---

## 🐱 Types d'Animaux

### Changer de type
- **Menu système** → "🐾 Animal" → "Changer type"
- **Chat 🐱** : Miaulements, comportement félin
- **Chien 🐶** : Aboiements, comportement canin

### Différences
- **Sprites différents** : Animations et apparence uniques
- **Sons spécifiques** : Miaulements vs aboiements
- **Comportements** : Légères variations dans les réactions

---

## ⚙️ Paramètres et Personnalisation

### Accéder aux paramètres
- **Menu système** → "⚙️ Paramètres"

### Options disponibles

#### Identité
- **Nom de Minou** : Personnalisez le nom de votre compagnon
- **Votre nom** : Comment Minou vous appelle
- **Type d'animal** : Chat ou Chien

#### Comportement
- **Vitesse de mouvement** : De très lent à très rapide
- **Fréquence des mouvements** : Intervalles entre les actions
- **Messages aléatoires** : Activer/désactiver les messages spontanés
- **Personnalité** : Joueur, Calme, Énergique, Paresseux

#### IA et Communication
- **Clé API Gemini** : Pour l'intelligence artificielle avancée
- **Mode IA** : Activé/Désactivé
- **Langue de réponse** : Français par défaut

#### Audio
- **Sons activés** : Oui/Non
- **Volume** : Contrôlé par le système
- **Fréquence des sons** : De rare à fréquent

#### Interface
- **Thème** : Sombre (par défaut) / Clair
- **Transparence** : Niveau d'opacité
- **Position de démarrage** : Aléatoire ou fixe

---

## 🔧 Intelligence Artificielle Avancée

### Configuration de l'API Gemini

#### Obtenir une clé API
1. Allez sur [Google AI Studio](https://aistudio.google.com/)
2. Créez un compte Google si nécessaire
3. Générez une clé API gratuite
4. Copiez la clé

#### Configuration dans Minou
1. **Menu** → "⚙️ Paramètres"
2. **Section IA** → Coller votre clé API
3. **Activer l'IA** → Cocher la case
4. **Sauvegarder** → Redémarrer Minou

### Différence avec et sans IA

#### Sans IA (Mode hors-ligne)
```
Vous : "Quelle est la capitale de la Chine ?"
Minou : "Miaou ! Je ne comprends pas tout mais j'aime qu'on me parle ! 😺"
```

#### Avec IA (Mode intelligent)
```
Vous : "Quelle est la capitale de la Chine ?"
Minou : "La capitale de la Chine est Pékin (Beijing) ! 🏮 C'est une ville fascinante avec une histoire millénaire !"
```

### Capacités de l'IA
- **Questions générales** : Géographie, histoire, sciences, etc.
- **Calculs complexes** : Mathématiques, conversions, statistiques
- **Conseils personnalisés** : Productivité, santé, loisirs
- **Aide technique** : Programmation, dépannage informatique
- **Conversations naturelles** : Discussions fluides et contextuelles
- **Traductions** : Langues multiples
- **Créativité** : Histoires, poèmes, idées

---

## 📊 Surveillance Système

### Informations surveillées
- **CPU** : Pourcentage d'utilisation
- **Mémoire RAM** : Utilisation et disponibilité
- **Batterie** : Niveau et état (sur portables)
- **Stockage** : Espace disque disponible

### Alertes automatiques
- **Mémoire critique** : > 90% → Minou joue l'animation "Hurt"
- **Batterie faible** : < 20% → "Batterie faible !"
- **CPU surchargé** : > 95% → Alerte de performance

### Consulter les infos
- **Menu système** → "📊 Info système"
- **Affichage dans une bulle** avec détails complets

---

## 💌 Messages et Citations

### Messages d'amour spontanés
Minou vous envoie parfois des messages affectueux :
- "Je t'aime ! 💖"
- "Tu me manques quand tu n'es pas là ! 🥺"
- "Tu es le meilleur humain du monde ! 😻"

### Citations inspirantes
Messages motivants aléatoirement :
- "💎 Le succès n'est pas final, l'échec n'est pas fatal : c'est le courage de continuer qui compte."
- "💎 La seule façon de faire du bon travail est d'aimer ce que vous faites."

### Suggestions de recherche
Minou peut vous suggérer des sujets intéressants :
- "💡 Pourquoi ne pas rechercher des recettes de cuisine japonaise ?"
- "💡 Ça te dirait d'apprendre quelque chose sur l'astronomie ?"

### Configuration
- **Menu Paramètres** → Activer/désactiver chaque type de message
- **Fréquence** : De 10 minutes à 60 minutes d'intervalle

---

## 🎭 Réactions et Animations

### Interactions avec Minou

#### Caresses (Clic simple)
- **1er clic** : "Miaou ! 😸" + animation normale
- **2e clic** : "Aïe ! 😿" + animation "Hurt"  
- **3e clic** : "Arrête ! 😾" + animation "Hurt"
- **4e clic** : "Tu me fais mal ! 😭" + animation "Hurt"
- **5e clic** : "💀 Animation de mort dramatique"

#### Résurrection
- Après la "mort", **menu système** → "💖 Ressusciter"
- Minou revient à la vie avec un message joyeux

### Comportements aléatoires
- **Longues pauses** : 30 secondes à 10 minutes sans bouger
- **Exploration** : Course vers les bords de l'écran
- **Acrobaties** : Sauts et glissades spontanées
- **Repos** : Periods d'inactivité pour ne pas déranger

---

## 🏠 Gestion de l'Environnement

### Positionnement
- **Démarrage aléatoire** : Minou apparaît à un endroit différent à chaque lancement
- **Déplacement libre** : Reste dans les limites de l'écran
- **Rebonds** : Rebondit sur les bords de manière réaliste

### Collision et physique
- **Gravité** : Les sauts suivent une physique réaliste
- **Momentum** : Les mouvements ont de l'inertie
- **Détection des bords** : Minou ne peut pas sortir de l'écran

---

## 🔄 Mises à Jour et Maintenance

### Vérifier les mises à jour
```bash
# Dans le dossier de Minou
git pull origin main
pip install -r requirements.txt --upgrade
```

### Sauvegarde des données
Vos données personnelles sont stockées dans :
- **Notes** : `data/notes.json`
- **Configuration** : `data/config.json`
- **Rappels** : `data/reminders.json`

### Réinitialisation
Pour remettre Minou à zéro :
1. Fermer complètement Minou
2. Supprimer le dossier `data/`
3. Relancer → Configuration initiale

---

## 🆘 Dépannage

### Problèmes courants

#### Minou ne démarre pas
```bash
# Vérifier Python
python --version  # Doit être 3.7+

# Réinstaller les dépendances
pip install -r requirements.txt --force-reinstall

# Vérifier les logs
python main.py --debug
```

#### Le chat ne répond pas
1. **Vérifiez la connexion Internet** (pour l'IA)
2. **Vérifiez la clé API** dans les paramètres
3. **Redémarrez Minou**

#### Minou est trop actif/inactif
- **Paramètres** → Ajuster la "Fréquence des mouvements"
- **Mode tranquille** pour le calmer temporairement

#### Sons ne marchent pas
1. Vérifier le **volume système**
2. **Menu** → Vérifier que les sons sont activés
3. Vérifier les fichiers dans `assets/cat/audio.wav` et `assets/dog/audio.wav`

#### Interface graphique corrompue
```bash
# Réinitialiser l'interface
python main.py --reset-ui
```

### Logs et Debug
- **Fichier de log** : `minou.log`
- **Mode verbose** : `python main.py --verbose`
- **Debug IA** : Activable dans les paramètres

---

## 📱 Intégration Système

### Barre des tâches
- **Icône animée** : Reflète l'état de Minou
- **Notifications système** : Pour les rappels et alertes
- **Démarrage automatique** : Optionnel au boot du système

### Raccourcis clavier globaux (Futurs)
- `Ctrl + Alt + M` : Afficher/Masquer Minou
- `Ctrl + Alt + C` : Ouvrir le chat rapidement

### Compatibilité
- **Windows** : 7, 8, 10, 11
- **macOS** : 10.14+
- **Linux** : Ubuntu 18+, Fedora 30+, Arch Linux

---

## 🎯 Conseils d'Utilisation

### Optimiser l'expérience
1. **Configurez l'IA** pour des réponses intelligentes
2. **Personnalisez le nom** pour une relation plus proche
3. **Ajustez la fréquence** selon votre tolérance aux interruptions
4. **Utilisez les notes** pour vos tâches importantes
5. **Mode tranquille** pendant le travail concentré

### Bonnes pratiques
- **Ne cliquez pas trop** sur Minou (il n'aime pas ça !)
- **Nettoyez régulièrement** les crottes pour maintenir un environnement propre
- **Interagissez** régulièrement pour maintenir l'engagement
- **Sauvegardez** votre configuration avant les mises à jour

### Utilisation professionnelle
- **Rappels de réunions** via le chat
- **Notes rapides** pendant les appels
- **Surveillance système** pour les développeurs
- **Assistant IA** pour les recherches rapides

---

## 🌟 Fonctionnalités Avancées

### Commandes cachées
Dans le chat, essayez :
- `"debug"` : Informations techniques
- `"stats"` : Statistiques d'utilisation
- `"easter egg"` : Surprise ! 🎉

### API et extensibilité
Minou est conçu pour être extensible :
- **Plugins** : Architecture modulaire
- **Thèmes personnalisés** : CSS-like styling
- **Intégrations** : APIs tierces possibles

---

## 📞 Support et Communauté

### Signaler un bug
1. **Issue GitHub** avec logs
2. **Description détaillée** du problème
3. **Étapes de reproduction**
4. **Configuration système**

### Demandes de fonctionnalités
- **Discussions GitHub** pour les idées
- **Votes communautaires** pour les priorités

### Contribuer
- **Code** : Pull requests bienvenues
- **Traductions** : Aide pour d'autres langues
- **Documentation** : Améliorations du guide

---

## 🏆 Remerciements

Minou est développé avec ❤️ par la communauté. Merci à tous les contributeurs qui rendent ce projet possible !

**Technologies utilisées :**
- **Python** + **PyQt5** pour l'interface
- **Google Gemini AI** pour l'intelligence artificielle
- **Sprites animés** pour les visuels
- **Architecture modulaire** pour l'extensibilité

---

## 📄 Licence et Légal

Ce projet est distribué sous licence MIT. Consultez le fichier `LICENSE` pour plus de détails.

**Note importante :** L'utilisation de l'API Gemini est soumise aux conditions de Google. Minou ne stocke aucune donnée personnelle sur des serveurs externes.

---

*Dernière mise à jour : 13 août 2025*
*Version du guide : 2.0*

**🎉 Amusez-vous bien avec Minou ! 🐾**
