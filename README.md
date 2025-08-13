# Compapet - Desk Pet Companion (dans sa nouvelle version on va l'appeler 'Minou' ce sera le nouveau nom de projet)

![](https://github.com/user-attachments/assets/b3afd11d-383a-487b-b9a0-385e3ecc2a10)

This is a fun desktop companion application that brings a virtual pet (cat or dog) to your screen. The pet roams around your desktop, performs various animations, and can even chase after food items you place. It also, occasionally, leaves little "surprises" on your screen! You can control the pet's basic movements, toggle audio, and manage food and poop items through a control box or the system tray icon.

## Features

* **Desktop Pet:** A virtual pet that lives on your desktop.
* **Animations:** The pet performs various animations like Idle, Walk, Run, Jump, Slide, Hurt, and even a "Dead" animation if clicked too many times.
* **Random Behavior:** The pet moves randomly around the screen and performs actions autonomously.
* **Manual Control:** A control box allows you to manually move the pet (Up, Down, Left, Right), make it Jump, or Slide.
* **Food Interaction:** You can add food items to the desktop, and your pet will chase and "eat" them. Food items are draggable.
* **Poop Functionality:** Your pet will randomly leave poop items on your desktop. Clicking on a poop item will clear it.
* **System Tray Integration:** Control the pet's visibility, open the control box, toggle audio, add/clear food, add/clear poop, change pet type, and revive the pet from the system tray menu.
* **Pet Type Selection:** Choose between a cat or a dog companion.
* **Audio Feedback:** The pet makes sounds at random intervals (can be disabled).
* **Revive Option:** If the pet "dies" from too many clicks, you can revive it from the system tray.

## Installation

1.  **Prerequisites:**
    * Python 3.x installed on your system.
    * `PyQt5` library. You can install it using pip:
        ```bash
        pip install PyQt5 PyQt5-Qt5 PyQt5-sip
        ```

2.  **Download Assets:**
    Ensure you have the `assets` folder in the same directory as your `main.py` file. The `assets` folder should have the following structure:

    ```
    assets/
    ├── cat/
    │   ├── Dead (1).png
    │   ├── ... (other cat animation frames)
    │   └── audio.wav
    ├── dog/
    │   ├── Dead (1).png
    │   ├── ... (other dog animation frames)
    │   └── audio.wav
    ├── food/
    │   ├── food (1).png
    │   ├── ... (other food frames)
    └── poop/
        ├── poop (1).png
        ├── poop (2).png
        └── ... (other poop frames)
    ```

## How to Run

1.  Navigate to the directory containing `main.py` in your terminal or command prompt.
2.  Run the application using Python:
    ```bash
    python main.py
    ```

The pet companion will appear on your desktop, and a system tray icon will be visible.

## Usage

* **Pet Movement:** The pet will move randomly around your desktop.
* **Dragging the Pet:** Click and drag the pet to move it manually.
* **Interacting with the Pet:** Click the pet multiple times to see different reactions (e.g., "Hurt" animation). If clicked too many times, the pet will play a "Dead" animation and stop moving.
* **System Tray Icon (Right-Click):**
    * **Hide Pet / Show Pet:** Toggles the visibility of the pet on the desktop.
    * **Open Control Box:** Opens a small window with manual movement controls (Up, Down, Left, Right, Jump, Slide).
    * **Disable Audio / Enable Audio:** Toggles the pet's sounds.
    * **Food -> Add Random Food:** Spawns a random food item on your desktop. The pet will automatically try to chase and "eat" it. You can also drag the food items around.
    * **Food -> Clear All Food:** Removes all food items from the desktop.
    * **Poop -> Add Random Poop:** Manually spawns a random poop item near the pet.
    * **Poop -> Clear All Poop:** Removes all poop items from the desktop.
    * **Revive Pet:** If your pet is "dead", this option will become active, allowing you to reset its state and bring it back to life.
    * **Change Pet Type:** Switch between a cat and a dog companion.
    * **Exit:** Quits the application.

* **Control Box (when open):**
    * Use the "Up", "Down", "Left", "Right" buttons to move the pet.
    * Click "Jump" to make the pet jump.
    * Click "Slide" to make the pet slide.
    * Click "Stop" to halt manual movement.
    * You can also use `W`, `A`, `S`, `D` keys for movement, `Space` for jump, and `Shift` for slide when the control box has focus.

* **Cleaning Poop:** Simply click on a poop item on the desktop to make it disappear.

## Troubleshooting

* **"Error: Default 'assets/cat' directory not found..."**: Ensure the `assets/cat` folder and its contents are correctly placed relative to `main.py`.
* **"Warning: 'assets/food' directory not found..."**: Ensure the `assets/food` folder and its contents are correctly placed. Food features will not work without them.
* **"Warning: 'assets/poop' directory not found..."**: Ensure the `assets/poop` folder and its contents are correctly placed. Poop features will not work without them.
* **Pet not moving or animating after dying**: If the pet is dead, it will remain in its final "Dead" frame and stop all movement/animations. Use the "Revive Pet" option in the system tray to bring it back.
* **Food not visible**: Ensure `FOOD_SIZE` in `main.py` matches the actual pixel dimensions of your food sprites (currently set to 40). Also, ensure you are using the "Add Random Food" option from the tray menu.
* **Poop not visible**: Ensure `POOP_SIZE` in `main.py` matches the actual pixel dimensions of your poop sprites (currently set to 25). Also, ensure you are using the "Add Random Poop" option or waiting for automatic spawns.



# Desktop Pet Companion - Documentation Complète (dans sa nouvelle version on va l'appeler 'Minou' ce sera le nouveau nom de projet)

## 📋 Table des matières
1. [Vue d'ensemble](#vue-densemble)
2. [Architecture de l'application](#architecture-de-lapplication)
3. [Fonctionnalités détaillées](#fonctionnalités-détaillées)
4. [Structure du code](#structure-du-code)
5. [Installation et configuration](#installation-et-configuration)
6. [Utilisation](#utilisation)
7. [Améliorations proposées](#améliorations-proposées)

## 🎮 Vue d'ensemble

Desktop Pet Companion est une application PyQt5 qui affiche un animal de compagnie virtuel interactif sur votre bureau. L'animal peut se déplacer librement, réagir aux interactions utilisateur, et effectuer diverses animations. L'application fonctionne comme un widget transparent qui reste toujours au premier plan.

### Caractéristiques principales
- **Animal virtuel animé** (chat ou chien) qui se déplace sur l'écran
- **Système d'animations** complexe avec 8 types différents
- **Interactions physiques** (glisser-déposer, clics, contrôles manuels)
- **Système de nourriture et de besoins** (l'animal peut manger et fait ses besoins)
- **Interface de contrôle** dédiée avec support clavier
- **Icône de barre système** pour un accès rapide aux fonctionnalités
- **Support audio** pour les sons de l'animal

## 🏗️ Architecture de l'application

### Classes principales

#### 1. **CatCompanionApp** (Classe principale)
La classe centrale qui gère l'animal virtuel :
- **Gestion des sprites** : Charge et affiche les animations frame par frame
- **Physique du mouvement** : Calcule position, vélocité, gravité pour les sauts
- **États de l'animal** : Idle, Walk, Run, Jump, Slide, Hurt, Dead, Fall
- **Système de collision** : Détecte les bords de l'écran et rebondit
- **Gestion des interactions** : Répond aux clics, glisser-déposer, contrôles

#### 2. **ControlBox**
Interface de contrôle séparée permettant :
- **Contrôles directionnels** (D-pad virtuel)
- **Actions spéciales** (sauter, glisser)
- **Support clavier** (WASD, flèches, espace, shift)
- **Signaux Qt** pour communication avec l'animal

#### 3. **FoodItem**
Objets de nourriture interactifs :
- **Positionnement aléatoire** ou manuel
- **Draggable** (peut être déplacé)
- **Détection de collision** avec l'animal
- **Système de signaux** pour la consommation

#### 4. **PoopItem**
Déjections de l'animal :
- **Spawn automatique** toutes les 15 secondes
- **Nettoyage au clic**
- **Positionnement** relatif à l'animal

### Système d'animation

L'application utilise un système de sprites frame-by-frame :

```
assets/
├── cat/
│   ├── Idle (1).png ... Idle (10).png
│   ├── Walk (1).png ... Walk (10).png
│   ├── Run (1).png ... Run (8).png
│   ├── Jump (1).png ... Jump (8).png
│   ├── Slide (1).png ... Slide (10).png
│   ├── Hurt (1).png ... Hurt (10).png
│   ├── Dead (1).png ... Dead (10).png
│   ├── Fall (1).png ... Fall (8).png
│   └── audio.wav
├── dog/
│   └── [mêmes fichiers que cat]
├── food/
│   └── [images de nourriture]
└── poop/
    └── [images de déjections]
```

## 🎯 Fonctionnalités détaillées

### Mouvements et comportements

1. **Mouvements aléatoires** (toutes les 3 secondes) :
   - 15% chance : Course vers un bord
   - 15% chance : Glissade
   - 10% chance : Saut
   - 40% chance : Marche aléatoire
   - 20% chance : Repos

2. **Physique réaliste** :
   - Gravité : 0.8 pixels/frame²
   - Vitesse de marche : 3 pixels/frame
   - Vitesse de course : 7.5 pixels/frame
   - Vélocité initiale de saut : 15 pixels/frame

3. **Système de mort** :
   - Après 5 clics consécutifs
   - Animation de mort complète
   - Possibilité de résurrection via menu

### Interactions utilisateur

1. **Glisser-déposer** : Déplace l'animal manuellement
2. **Clics** : Déclenche animation "Hurt", accumulation = mort
3. **Contrôle manuel** : Via ControlBox ou clavier
4. **Menu contextuel** : Via icône système

### Système alimentaire

- **Nourriture** : L'animal court automatiquement vers la nourriture la plus proche
- **Consommation** : Disparition au contact
- **Déjections** : Spawn automatique, nettoyage manuel

## 💻 Structure du code

### Timers et cycles

L'application utilise plusieurs QTimer pour gérer les différents cycles :

1. **animation_timer** (100ms) : Change les frames d'animation
2. **movement_timer** (16ms) : Met à jour la position (~60 FPS)
3. **random_behavior_timer** (3000ms) : Change le comportement
4. **poop_spawn_timer** (15000ms) : Génère les déjections
5. **audio_play_timer** (5-15s aléatoire) : Joue les sons

### Gestion des états

```python
# États principaux
self.is_dead = False
self.is_playing_one_shot_animation = False
self._is_jumping = False
self._is_manual_moving = False
self.is_edge_running = False
self.is_sliding = False
self.dragging = False
```

## 📦 Installation et configuration

### Prérequis

```bash
pip install PyQt5
```

### Structure des fichiers requise

```
project/
├── main.py (le code fourni)
└── assets/
    ├── cat/
    │   ├── [animations].png
    │   └── audio.wav
    ├── dog/
    │   ├── [animations].png
    │   └── audio.wav
    ├── food/
    │   └── [images].png
    └── poop/
        └── [images].png
```

### Lancement

```bash
python main.py
```

## 🎮 Utilisation

### Contrôles clavier
- **WASD / Flèches** : Déplacements
- **Espace** : Saut
- **Shift** : Glissade

### Menu système
- Clic droit sur l'icône → Menu complet
- Clic gauche → Afficher/Masquer

## 🚀 Améliorations proposées

### 1. Restructuration modulaire

**Structure proposée :**

```
desktop_pet/
├── main.py
├── config.py
├── core/
│   ├── __init__.py
│   ├── pet.py          # Classe CatCompanionApp
│   ├── animations.py   # Gestionnaire d'animations
│   └── physics.py      # Moteur physique
├── ui/
│   ├── __init__.py
│   ├── control_box.py  # Interface de contrôle
│   └── tray_menu.py    # Menu système
├── items/
│   ├── __init__.py
│   ├── food.py         # Classe FoodItem
│   └── poop.py         # Classe PoopItem
├── ai/
│   ├── __init__.py
│   ├── gemini_client.py # Client API Gemini
│   └── chat_interface.py # Interface de chat
└── assets/
    └── [fichiers existants]
```

**Exemple de refactoring - physics.py :**

```python
# physics.py
class PhysicsEngine:
    def __init__(self, gravity=0.8, movement_speed=3):
        self.gravity = gravity
        self.movement_speed = movement_speed
        self.run_multiplier = 2.5
        
    def apply_gravity(self, velocity_y, is_jumping):
        if is_jumping:
            return velocity_y + self.gravity
        return velocity_y
    
    def calculate_jump_velocity(self):
        return -15.0
    
    def check_collision(self, x, y, width, height, screen_rect):
        # Logique de collision
        pass
```

### 2. Intégration IA Gemini

**Implementation proposée :**

```python
# ai/gemini_client.py
import google.generativeai as genai
from PyQt5.QtCore import QObject, pyqtSignal

class GeminiAI(QObject):
    response_ready = pyqtSignal(str)
    
    def __init__(self, api_key=None):
        super().__init__()
        self.api_key = api_key
        self.model = None
        self.personality = """Tu es un animal de compagnie virtuel mignon et joueur. 
        Tu réponds de manière amicale et avec des émotions."""
        
    def initialize(self, api_key):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')
        
    def generate_response(self, user_input):
        if not self.model:
            return "Woof! Configure ma clé API d'abord!"
            
        prompt = f"{self.personality}\nUtilisateur: {user_input}\nRéponse:"
        response = self.model.generate_content(prompt)
        return response.text

# ai/chat_interface.py
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QTextEdit, 
                             QLineEdit, QPushButton, QHBoxLayout)

class ChatInterface(QWidget):
    def __init__(self, ai_client):
        super().__init__()
        self.ai_client = ai_client
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Zone d'affichage des messages
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        
        # Zone de saisie
        input_layout = QHBoxLayout()
        self.input_field = QLineEdit()
        self.send_button = QPushButton("Envoyer")
        
        input_layout.addWidget(self.input_field)
        input_layout.addWidget(self.send_button)
        
        layout.addWidget(self.chat_display)
        layout.addLayout(input_layout)
        
        self.setLayout(layout)
        
        # Connexions
        self.send_button.clicked.connect(self.send_message)
        self.input_field.returnPressed.connect(self.send_message)
        
    def send_message(self):
        message = self.input_field.text()
        if message:
            self.chat_display.append(f"Vous: {message}")
            response = self.ai_client.generate_response(message)
            self.chat_display.append(f"Pet: {response}")
            self.input_field.clear()
```

### 3. Système de configuration avancé

**config_manager.py :**

```python
import json
from PyQt5.QtWidgets import QDialog, QFormLayout, QLineEdit, QSpinBox, QCheckBox

class ConfigManager:
    def __init__(self):
        self.config_file = "pet_config.json"
        self.settings = self.load_settings()
    
    def load_settings(self):
        try:
            with open(self.config_file, 'r') as f:
                return json.load(f)
        except:
            return self.default_settings()
    
    def default_settings(self):
        return {
            "api_key": "",
            "pet_type": "cat",
            "movement_speed": 3,
            "animation_speed": 100,
            "sound_enabled": True,
            "poop_interval": 15000,
            "food_attraction_range": 200,
            "personality": "playful",
            "ai_enabled": False
        }
    
    def save_settings(self):
        with open(self.config_file, 'w') as f:
            json.dump(self.settings, f, indent=4)

class SettingsDialog(QDialog):
    def __init__(self, config_manager):
        super().__init__()
        self.config = config_manager
        self.init_ui()
    
    def init_ui(self):
        layout = QFormLayout()
        
        # Clé API
        self.api_key_input = QLineEdit()
        self.api_key_input.setEchoMode(QLineEdit.Password)
        self.api_key_input.setText(self.config.settings.get("api_key", ""))
        layout.addRow("Clé API Gemini:", self.api_key_input)
        
        # Vitesse de mouvement
        self.speed_input = QSpinBox()
        self.speed_input.setRange(1, 10)
        self.speed_input.setValue(self.config.settings.get("movement_speed", 3))
        layout.addRow("Vitesse:", self.speed_input)
        
        # IA activée
        self.ai_checkbox = QCheckBox()
        self.ai_checkbox.setChecked(self.config.settings.get("ai_enabled", False))
        layout.addRow("Activer l'IA:", self.ai_checkbox)
        
        self.setLayout(layout)
```

### 4. Fonctionnalités bureau utiles

**desktop_assistant.py :**

```python
import psutil
import datetime
from PyQt5.QtCore import QTimer

class DesktopAssistant:
    def __init__(self, pet):
        self.pet = pet
        self.init_features()
    
    def init_features(self):
        # Rappels
        self.reminders = []
        self.reminder_timer = QTimer()
        self.reminder_timer.timeout.connect(self.check_reminders)
        self.reminder_timer.start(60000)  # Check chaque minute
    
    def add_reminder(self, time, message):
        self.reminders.append({"time": time, "message": message})
    
    def check_reminders(self):
        current_time = datetime.datetime.now()
        for reminder in self.reminders[:]:
            if current_time >= reminder["time"]:
                self.pet.show_notification(reminder["message"])
                self.reminders.remove(reminder)
    
    def get_system_info(self):
        return {
            "cpu": psutil.cpu_percent(),
            "memory": psutil.virtual_memory().percent,
            "battery": psutil.sensors_battery().percent if psutil.sensors_battery() else None
        }
    
    def monitor_system(self):
        info = self.get_system_info()
        
        # Alertes système
        if info["memory"] > 90:
            self.pet.play_animation("Hurt")
            self.pet.show_bubble("La mémoire est presque pleine!")
        
        if info["battery"] and info["battery"] < 20:
            self.pet.play_animation("Tired")
            self.pet.show_bubble("Batterie faible!")
```

### 5. Système de bulles de dialogue

```python
class SpeechBubble(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.message = ""
        self.fade_timer = QTimer()
        self.fade_timer.timeout.connect(self.fade_out)
        
    def show_message(self, text, duration=3000):
        self.message = text
        self.show()
        self.fade_timer.start(duration)
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Dessiner la bulle
        path = QPainterPath()
        rect = QRectF(10, 10, 200, 50)
        path.addRoundedRect(rect, 10, 10)
        
        # Queue de la bulle
        path.moveTo(30, 60)
        path.lineTo(20, 75)
        path.lineTo(40, 60)
        
        painter.fillPath(path, QColor(255, 255, 255, 230))
        painter.setPen(Qt.black)
        painter.drawText(rect, Qt.AlignCenter, self.message)
```

### 6. Système de personnalisation avancée

```python
class PetCustomizer:
    def __init__(self):
        self.accessories = []
        self.color_filters = {}
        
    def add_accessory(self, accessory_type, image_path):
        """Ajoute des accessoires comme chapeaux, colliers, etc."""
        pass
    
    def apply_color_filter(self, hue_shift, saturation, brightness):
        """Modifie les couleurs du sprite"""
        pass
    
    def create_custom_animation(self, frames):
        """Permet de créer des animations personnalisées"""
        pass
```

### 7. Intégration avec des applications

```python
class AppIntegration:
    def __init__(self, pet):
        self.pet = pet
        
    def pomodoro_timer(self, work_time=25, break_time=5):
        """Timer Pomodoro avec animations"""
        # Pendant le travail : animation "Focus"
        # Pendant la pause : animation "Play"
        pass
    
    def calendar_integration(self):
        """Intégration avec le calendrier système"""
        # Rappels de rendez-vous
        # Anniversaires
        pass
    
    def music_reaction(self):
        """Réagit à la musique jouée"""
        # Danse quand de la musique est détectée
        pass
```

## 📝 Notes de développement

### Points d'amélioration prioritaires

1. **Séparation des responsabilités** : Le fichier unique de 1000+ lignes doit être divisé
2. **Configuration utilisateur** : Interface graphique pour tous les paramètres
3. **Persistance des données** : Sauvegarder l'état, les statistiques, les préférences
4. **Tests unitaires** : Ajouter une suite de tests pour chaque module
5. **Documentation API** : Documenter toutes les classes et méthodes
6. **Optimisation performance** : Réduire l'utilisation CPU avec un sprite caching intelligent

### Bugs connus à corriger

1. Accumulation possible de timers non arrêtés
2. Gestion mémoire des items food/poop (fuite potentielle)
3. Conflits d'états lors d'animations simultanées

Cette documentation fournit une base solide pour comprendre et améliorer l'application Desktop Pet Companion. Les améliorations proposées permettraient de transformer ce projet en une application professionnelle et extensible.


a noter que dans les ameliorations , pourquoi ne pas ajouter des trucs comme des rappels que l'animal peut faire quand on lui donne il stoque dans un fichier a lui qu'il peut checker et rapeller (les rappels on peut les faire via le menu ou si une API de LLM est branchee alors on peut juste lui demander en langue naturelle de faire un rappele et l'API d'IA avec le bon contexte et retournera la bone reponse JSOn que l'on va parser et programmer le rappel).
l'animal eut aussi surveiller la memoire et le CPU par exemple , ou meme d'autres choses (moi je ne m'y connais pas trop mais je suis sure qu'on peut trouver pleins de trucs pratiques).

il peut aussi parler de temps en temps pour nous suggerer de faire des recherches pour nous par exemple.
il peut meme parler de temps e temps pour dire "je t'aime" avec une petite notif. (ou blancer une bonne citation).

il peut aussi servir de pense bete et on lui demande ensuite de restituer les notes prises (bon ca je ne sais pas comment on va s'y prendre)

il connait aussi le nom de l'utilisateur par exemple, et on peut lui donner un nom aussi.
le champ de saisi est tout petit et au dessus de lui et apres un cetain temps il disparait et il faut cliquer sur lui (gauche ou droit on verra ce qui est libre) pour que ce champ apararaisse et on lui parle.

breff on peut lui trouvr pleins d'options simples a faire sur windows mais qui reseront mignonnes et pratiques. c'est vrai que c'est avant tout un divertissement mais il ne faut pas non plus qu'il soit totalement inutile en fait.
(dans sa nouvelle version on va l'appeler 'Minou' ce sera le nouveau nom de projet)

en faisant le plus possible HORS-LIGNE et en prevoyant de bons cas de fallback en cas de non connectivite ou d'absece de cle API


on peut https://pypi.org/project/google-genai/.

https://googleapis.github.io/python-genai/
