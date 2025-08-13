"""
Classe principale Minou - Animal de compagnie virtuel intelligent
"""
import sys
import os
import random
import math
from PyQt5.QtWidgets import (QWidget, QLabel, QApplication, QSystemTrayIcon, 
                             QMenu, QAction, QStyle)
from PyQt5.QtGui import QPixmap, QTransform, QIcon
from PyQt5.QtCore import Qt, QTimer, QPoint
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl


from config import (CAT_WIDTH, CAT_HEIGHT, ANIMATION_FRAME_RATE, MOVEMENT_SPEED,
                    MOVEMENT_CHANGE_DELAY, RUN_SPEED_MULTIPLIER, CLICK_THRESHOLD,
                    JUMP_INITIAL_VELOCITY, GRAVITY, DEAD_ANIMATION_THRESHOLD,
                    ANIMATION_FRAMES, config_manager, SettingsDialog)

from ui_components import ControlBox, SpeechBubble, MinimalChatInterface
from ai_manager import ConversationThread, gemini_ai
from items import FoodItem, PoopItem
from utils import (reminder_manager, system_monitor, message_generator, 
                   notes_manager, get_system_info)

class MinouPet(QWidget):
    def __init__(self):
        super().__init__()
        self.init_window()
        self.init_variables()
        self.init_ui_components()
        self.init_timers()
        self.init_audio()
        self.init_tray_menu()
        self.load_assets()
        self.setup_connections()
        self.start_pet()

    def init_window(self):
        """Initialise la fenêtre principale"""
        pet_name = config_manager.get("pet_name", "Minou")
        self.setWindowTitle(f"{pet_name} - Desktop Pet")
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.resize(CAT_WIDTH, CAT_HEIGHT)

    def init_variables(self):
        """Initialise toutes les variables d'état"""
        # Animation et sprites
        self.current_asset_type = config_manager.get("pet_type", "cat")
        self.sprites = {}
        self.current_animation = 'Idle'
        self.current_frame_index = 0
        
        # Position et mouvement
        self._current_x = 0.0
        self._current_y = 0.0
        self.cat_velocity_x = 0.0
        self.cat_velocity_y = 0.0
        self.moving_right = True
        
        # États
        self.is_dead = False
        self.is_playing_one_shot_animation = False
        self._is_jumping = False
        self._is_manual_moving = False
        self.is_edge_running = False
        self.is_sliding = False
        self.dragging = False
        self.quiet_mode = False  # AJOUT : Mode tranquille
        
        # Interactions
        self._click_count = 0
        self.offset = QPoint()
        self.mouse_press_pos = QPoint()
        
        # Objets et cibles
        self.active_food_items = []
        self.active_poop_items = []
        self.target_food_item = None
        
        # Cibles pour mouvements spéciaux
        self.target_x = 0
        self.target_y = 0
        self.slide_target_pos = QPoint()
        
        # Composants UI
        self.control_box = None
        self.speech_bubble = None
        self.chat_interface = None
        
        # Thread pour l'IA
        self.conversation_thread = None

    def init_ui_components(self):
        """Initialise les composants d'interface"""
        # Label principal pour l'animal
        self.pet_label = QLabel(self)
        self.pet_label.setGeometry(0, 0, CAT_WIDTH, CAT_HEIGHT)
        self.pet_label.setAlignment(Qt.AlignCenter)
        
        # Bulle de dialogue
        self.speech_bubble = SpeechBubble()
        
        # Interface de chat minimaliste
        self.chat_interface = MinimalChatInterface()
        self.chat_interface.chat_message_sent.connect(self.handle_user_message)

    def init_timers(self):
        """Initialise tous les timers"""
        # Timer d'animation (change les frames)
        self.animation_timer = QTimer(self)
        self.animation_timer.timeout.connect(self._next_frame)
        
        # Timer de mouvement (met à jour la position)
        self.movement_timer = QTimer(self)
        self.movement_timer.timeout.connect(self._update_position)
        
        # Timer de comportement aléatoire
        self.random_behavior_timer = QTimer(self)
        self.random_behavior_timer.timeout.connect(self._random_movement)
        
        # Timer pour les messages aléatoires
        self.random_message_timer = QTimer(self)
        self.random_message_timer.timeout.connect(self._show_random_message)
        
        # Timer pour spawn automatique de poop
        self.poop_spawn_timer = QTimer(self)
        self.poop_spawn_timer.timeout.connect(self._spawn_random_poop)
        
        # Timer cooldown après mort
        self._dead_animation_cooldown_timer = QTimer(self)
        self._dead_animation_cooldown_timer.setSingleShot(True)
        self._dead_animation_cooldown_timer.timeout.connect(self._dead_animation_cooldown_finished)

    def init_audio(self):
        """Initialise le système audio"""
        self.media_player = QMediaPlayer(self)
        self.audio_files = {}
        self.audio_play_timer = QTimer(self)
        self.audio_play_timer.timeout.connect(self._play_random_audio)
        self.media_player.stateChanged.connect(self._audio_state_changed)

    def init_tray_menu(self):
        """Initialise l'icône et le menu de la barre système"""
        self.tray_icon = QSystemTrayIcon(self)
        pet_name = config_manager.get("pet_name", "Minou")
        self.tray_icon.setToolTip(f"{pet_name} - Desktop Pet")
        
        # Menu contextuel
        tray_menu = QMenu()
        
        # Actions principales
        self.toggle_visibility_action = QAction("Masquer", self)
        self.toggle_visibility_action.triggered.connect(self.toggle_visibility)
        tray_menu.addAction(self.toggle_visibility_action)
        
        self.open_control_box_action = QAction("🎮 Télécommande", self)
        self.open_control_box_action.triggered.connect(self._open_control_box)
        tray_menu.addAction(self.open_control_box_action)
        
        self.chat_action = QAction("💬 Parler à Minou", self)
        self.chat_action.triggered.connect(self._show_chat)
        tray_menu.addAction(self.chat_action)
        
        tray_menu.addSeparator()
        
        # Sous-menu Nourriture
        food_menu = QMenu("🍖 Nourriture", self)
        
        add_food_action = QAction("Ajouter nourriture", self)
        add_food_action.triggered.connect(self.add_random_food)
        food_menu.addAction(add_food_action)
        
        clear_food_action = QAction("Nettoyer nourriture", self)
        clear_food_action.triggered.connect(self.clear_all_food)
        food_menu.addAction(clear_food_action)
        
        tray_menu.addMenu(food_menu)
        
        # Sous-menu Propreté
        poop_menu = QMenu("💩 Propreté", self)
        
        add_poop_action = QAction("Faire ses besoins", self)
        add_poop_action.triggered.connect(self.add_random_poop)
        poop_menu.addAction(add_poop_action)
        
        clean_poop_action = QAction("Nettoyer", self)
        clean_poop_action.triggered.connect(self.clear_all_poop)
        poop_menu.addAction(clean_poop_action)
        
        tray_menu.addMenu(poop_menu)
        
        tray_menu.addSeparator()
        
        # Actions système
        self.toggle_audio_action = QAction("🔊 Désactiver son", self)
        self.toggle_audio_action.triggered.connect(self._toggle_audio)
        tray_menu.addAction(self.toggle_audio_action)
        
        # Sous-menu Animal
        pet_menu = QMenu("🐾 Animal", self)
        
        self.revive_pet_action = QAction("💖 Ressusciter", self)
        self.revive_pet_action.triggered.connect(self._reset_pet)
        self.revive_pet_action.setEnabled(False)
        pet_menu.addAction(self.revive_pet_action)
        
        # Changement de type
        pet_type_menu = QMenu("Changer type", self)
        self.cat_action = QAction("🐱 Chat", self, checkable=True)
        self.dog_action = QAction("🐶 Chien", self, checkable=True)
        self.cat_action.triggered.connect(lambda: self.change_pet_type('cat'))
        self.dog_action.triggered.connect(lambda: self.change_pet_type('dog'))
        pet_type_menu.addAction(self.cat_action)
        pet_type_menu.addAction(self.dog_action)
        pet_menu.addMenu(pet_type_menu)
        
        # AJOUT : Option Rester tranquille
        self.stay_quiet_action = QAction("😴 Rester tranquille", self)
        self.stay_quiet_action.triggered.connect(self._toggle_quiet_mode)
        pet_menu.addAction(self.stay_quiet_action)
        
        tray_menu.addMenu(pet_menu)
        
        # Paramètres et informations
        settings_action = QAction("⚙️ Paramètres", self)
        settings_action.triggered.connect(self._open_settings)
        tray_menu.addAction(settings_action)
        
        info_action = QAction("📊 Info système", self)
        info_action.triggered.connect(self._show_system_info)
        tray_menu.addAction(info_action)
        
        notes_action = QAction("📝 Mes notes", self)
        notes_action.triggered.connect(self._show_notes)
        tray_menu.addAction(notes_action)
        
        tray_menu.addSeparator()
        
        # Quitter
        exit_action = QAction("❌ Quitter", self)
        exit_action.triggered.connect(QApplication.instance().quit)
        tray_menu.addAction(exit_action)
        
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.activated.connect(self.on_tray_icon_activated)
        
        # Animation de l'icône tray
        self.tray_icon_current_frame_index = 0
        self.tray_animation_timer = QTimer(self)
        self.tray_animation_timer.timeout.connect(self._update_tray_icon_animation)

    def setup_connections(self):
        """Configure toutes les connexions de signaux"""
        # Connexions des utilitaires
        reminder_manager.reminder_triggered.connect(self._show_reminder)
        system_monitor.alert_triggered.connect(self._show_system_alert)
        
        # AJOUT: Démarrer la surveillance depuis le thread principal
        reminder_manager.start_monitoring()
        system_monitor.start_monitoring()

    def load_assets(self):
        """Charge tous les assets (sprites, audio, etc.)"""
        self.change_pet_type(self.current_asset_type)
        self._set_initial_position()

    def start_pet(self):
        """Démarre tous les timers et affiche l'animal"""
        # Démarrage des timers principaux
        self.animation_timer.start(config_manager.get("animation_speed", ANIMATION_FRAME_RATE))
        self.movement_timer.start(16)  # ~60 FPS
        
        # CORRECTION : Premier intervalle aléatoire plus long
        initial_behavior_delay = random.randint(15000, 45000)  # 15-45 secondes
        self.random_behavior_timer.start(initial_behavior_delay)
        
        # Poop encore moins fréquent
        self.poop_spawn_timer.start(random.randint(60000, 120000))  # 1-2 minutes
        
        # Messages aléatoires beaucoup moins fréquents
        if config_manager.get("random_messages_enabled", True):
            interval_range = config_manager.get("random_message_interval", [1200, 3600])  # 20-60 min
            interval = random.randint(interval_range[0], interval_range[1]) * 1000
            self.random_message_timer.start(interval)
        
        # Audio moins fréquent
        if config_manager.get("sound_enabled", True):
            self.audio_play_timer.start(random.randint(90000, 180000))  # 1.5-3 minutes
        
        # Animation du tray
        self.tray_animation_timer.start(ANIMATION_FRAME_RATE * 2)
        
        # Affichage
        self.show()
        self.tray_icon.show()
        
        # Message de bienvenue
        user_name = config_manager.get("user_name", "theTigerFox")
        pet_name = config_manager.get("pet_name", "Minou")
        welcome_msg = f"Coucou {user_name} ! {pet_name} est là ! 😸✨"
        self.show_bubble(welcome_msg, "love", 4000)
        
    def _load_sprites(self):
        """Charge tous les sprites pour le type d'animal actuel"""
        all_sprites = {}
        asset_dir = os.path.join(os.path.dirname(__file__), 'assets', self.current_asset_type)
        
        if not os.path.exists(asset_dir):
            print(f"❌ Dossier assets manquant: {asset_dir}")
            return {}
        
        for anim_name, num_frames in ANIMATION_FRAMES.items():
            all_sprites[anim_name] = []
            for i in range(1, num_frames + 1):
                sprite_path = os.path.join(asset_dir, f'{anim_name} ({i}).png')
                try:
                    pixmap = QPixmap(sprite_path)
                    if not pixmap.isNull():
                        scaled_pixmap = pixmap.scaled(
                            CAT_WIDTH, CAT_HEIGHT, 
                            Qt.KeepAspectRatio, Qt.SmoothTransformation
                        )
                        all_sprites[anim_name].append(scaled_pixmap)
                    else:
                        print(f"⚠️ Sprite manquant: {sprite_path}")
                except Exception as e:
                    print(f"❌ Erreur chargement sprite {sprite_path}: {e}")
        
        return all_sprites
    
    def _load_audio_file(self, pet_type):
        """Charge le fichier audio pour le type d'animal"""
        audio_path = os.path.join(os.path.dirname(__file__), 'assets', pet_type, 'audio.wav')
        if os.path.exists(audio_path):
            return QUrl.fromLocalFile(audio_path)
        else:
            print(f"⚠️ Audio manquant: {audio_path}")
            return None
    
    def change_pet_type(self, pet_type):
        """Change le type d'animal (chat/chien)"""
        self.current_asset_type = pet_type
        config_manager.set("pet_type", pet_type)
        
        # Décocher l'ancien type
        self.cat_action.setChecked(pet_type == 'cat')
        self.dog_action.setChecked(pet_type == 'dog')
        
        # Charger les nouveaux sprites
        self.sprites = self._load_sprites()
        self.audio_files[self.current_asset_type] = self._load_audio_file(self.current_asset_type)
        
        if self.sprites:
            self._set_animation('Idle')
            self._update_tray_icon_animation()
            print(f"✅ Changement vers {pet_type} réussi")
        else:
            print(f"❌ Échec du changement vers {pet_type}")
            # Retour au chat par défaut
            self.current_asset_type = 'cat'
            self.sprites = self._load_sprites()
    
    def _set_initial_position(self):
        """Place l'animal à une position aléatoire sur l'écran"""
        screen_rect = QApplication.desktop().screenGeometry()
        max_x = screen_rect.width() - self.width()
        max_y = screen_rect.height() - self.height()
        
        self._current_x = float(random.randint(100, max(200, max_x - 100)))
        self._current_y = float(random.randint(100, max(200, max_y - 100)))
        self.move(int(self._current_x), int(self._current_y))
    
    def _set_animation(self, animation_name):
        """Change l'animation actuelle"""
        if (self.is_playing_one_shot_animation and 
            animation_name != self.current_animation and 
            animation_name != 'Dead'):
            return
        
        if (animation_name not in self.sprites or 
            not self.sprites[animation_name]):
            animation_name = 'Idle'
        
        if self.current_animation != animation_name:
            self.current_animation = animation_name
            self.current_frame_index = 0
            self._update_sprite_display()
    
    def _next_frame(self):
        """Passe à la frame suivante de l'animation"""
        sprites = self.sprites.get(self.current_animation)
        if not sprites:
            return
        
        # Animation de mort : arrêter à la dernière frame
        if (self.current_animation == 'Dead' and 
            self.current_frame_index == len(sprites) - 1):
            self._update_sprite_display()
            return
        
        self.current_frame_index = (self.current_frame_index + 1) % len(sprites)
        self._update_sprite_display()
    
    def _update_sprite_display(self):
        """Met à jour l'affichage du sprite"""
        sprites = self.sprites.get(self.current_animation)
        if sprites and self.current_frame_index < len(sprites):
            pixmap = sprites[self.current_frame_index]
            
            # Retourner le sprite si l'animal va vers la gauche
            if not self.moving_right:
                pixmap = pixmap.transformed(QTransform().scale(-1, 1))
            
            self.pet_label.setPixmap(pixmap)
        else:
            self.pet_label.clear()
    
    def _update_position(self):
        """Met à jour la position de l'animal (appelé 60 fois par seconde)"""
        if self.is_dead or self.dragging:
            return
        
        screen_rect = QApplication.desktop().screenGeometry()
        max_x = screen_rect.width() - self.width()
        ground_y = float(screen_rect.height() - self.height())
        
        # Gestion des sauts avec gravité
        if self._is_jumping:
            self._handle_jumping(ground_y, max_x)
            return
        
        # Ne pas bouger pendant certaines animations
        if (self.is_playing_one_shot_animation and not self._is_jumping) or \
           self._dead_animation_cooldown_timer.isActive():
            return
        
        # Gestion de la poursuite de nourriture
        self._handle_food_chasing()
        
        # Mise à jour de la position
        self._current_x += self.cat_velocity_x
        self._current_y += self.cat_velocity_y
        
        # Gestion des différents types de mouvements
        if self.is_sliding:
            self._handle_sliding(max_x, ground_y)
        elif self.is_edge_running:
            self._handle_edge_running(max_x, ground_y)
        else:
            self._handle_normal_movement(max_x, ground_y)
    
    def _handle_jumping(self, ground_y, max_x):
        """Gère la physique des sauts"""
        self.cat_velocity_y += GRAVITY
        self._current_y += self.cat_velocity_y
        
        # Atterrissage
        if self._current_y >= ground_y:
            self._current_y = ground_y
            self.cat_velocity_y = 0.0
            self._is_jumping = False
            self.is_playing_one_shot_animation = False
            self._set_animation('Idle')
            
            if not self._is_manual_moving:
                self.random_behavior_timer.start(MOVEMENT_CHANGE_DELAY)
        
        # Mouvement horizontal pendant le saut
        self._current_x += self.cat_velocity_x
        self._current_x = max(0.0, min(self._current_x, float(max_x)))
        self.move(int(self._current_x), int(self._current_y))
    
    def _handle_food_chasing(self):
        """Gère la logique de poursuite de nourriture"""
        if (self._is_manual_moving or self.is_sliding or 
            self._is_jumping or self.is_playing_one_shot_animation):
            return
        
        # Chercher la nourriture la plus proche
        if not self.target_food_item or self.target_food_item.isHidden():
            closest_food = None
            min_distance = float('inf')
            
            for food in self.active_food_items:
                if not food.isHidden():
                    food_pos = food.pos()
                    pet_pos = QPoint(int(self._current_x), int(self._current_y))
                    distance = math.sqrt(
                        (food_pos.x() - pet_pos.x())**2 + 
                        (food_pos.y() - pet_pos.y())**2
                    )
                    if distance < min_distance:
                        min_distance = distance
                        closest_food = food
            
            self.target_food_item = closest_food
        
        # Poursuivre la nourriture ciblée
        if self.target_food_item and not self.target_food_item.isHidden():
            target_pos = self.target_food_item.pos()
            target_x = target_pos.x() + self.target_food_item.width() // 2
            target_y = target_pos.y() + self.target_food_item.height() // 2
            
            pet_center_x = self._current_x + CAT_WIDTH // 2
            pet_center_y = self._current_y + CAT_HEIGHT // 2
            
            dx = target_x - pet_center_x
            dy = target_y - pet_center_y
            distance = math.sqrt(dx*dx + dy*dy)
            
            # Manger la nourriture si assez proche
            if distance < 30:
                self.target_food_item.food_removed.emit(self.target_food_item)
                self.target_food_item = None
                self.cat_velocity_x = 0.0
                self.cat_velocity_y = 0.0
                self._set_animation('Idle')
                
                # Montrer satisfaction
                self.show_bubble("Miam miam ! Délicieux ! 😋", "love", 2000)
                
                if not self._is_manual_moving and not self.active_food_items:
                    self.random_behavior_timer.start(MOVEMENT_CHANGE_DELAY)
            else:
                # Courir vers la nourriture
                self.random_behavior_timer.stop()
                speed = config_manager.get("movement_speed", MOVEMENT_SPEED)
                self.cat_velocity_x = (dx / distance) * speed * RUN_SPEED_MULTIPLIER
                self.cat_velocity_y = (dy / distance) * speed * RUN_SPEED_MULTIPLIER
                self._set_animation('Run')
    
    def _handle_sliding(self, max_x, ground_y):
        """Gère le mouvement de glissade"""
        # Vérifier si on a atteint la cible
        target_reached_x = (
            (self.cat_velocity_x > 0 and self._current_x >= self.slide_target_pos.x()) or
            (self.cat_velocity_x < 0 and self._current_x <= self.slide_target_pos.x()) or
            abs(self.cat_velocity_x) < 0.1
        )
        
        target_reached_y = (
            (self.cat_velocity_y > 0 and self._current_y >= self.slide_target_pos.y()) or
            (self.cat_velocity_y < 0 and self._current_y <= self.slide_target_pos.y()) or
            abs(self.cat_velocity_y) < 0.1
        )
        
        if target_reached_x and (self.cat_velocity_y == 0 or target_reached_y):
            # Fin de la glissade
            self._current_x = float(self.slide_target_pos.x())
            if self.cat_velocity_y != 0:
                self._current_y = float(self.slide_target_pos.y())
            
            self.is_sliding = False
            self.cat_velocity_x = 0.0
            self.cat_velocity_y = 0.0
            self._set_animation('Idle')
            
            if not self._is_manual_moving and not self.target_food_item:
                self.random_behavior_timer.start(MOVEMENT_CHANGE_DELAY)
        else:
            # Continuer la glissade
            self._current_x = max(0.0, min(self._current_x, float(max_x)))
            self._current_y = max(0.0, min(self._current_y, ground_y))
            self.move(int(self._current_x), int(self._current_y))
            
            # Mettre à jour la direction
            if self.cat_velocity_x > 0:
                self.moving_right = True
            elif self.cat_velocity_x < 0:
                self.moving_right = False
            
            self._set_animation('Slide')
    
    def _handle_edge_running(self, max_x, ground_y):
        """Gère la course vers les bords"""
        self._current_x = max(0.0, min(self._current_x, float(max_x)))
        self._current_y = max(0.0, min(self._current_y, ground_y))
        self.move(int(self._current_x), int(self._current_y))
        
        # Vérifier si on a atteint la cible ou un bord
        target_reached = (
            abs(self._current_x - self.target_x) < 10 and
            abs(self._current_y - self.target_y) < 10
        )
        
        hit_boundary = (
            self._current_x <= 0 or self._current_x >= max_x or
            self._current_y <= 0 or self._current_y >= ground_y
        )
        
        if target_reached or hit_boundary:
            self.is_edge_running = False
            self.cat_velocity_x = 0.0
            self.cat_velocity_y = 0.0
            self._set_animation('Idle')
            
            if (not self._is_manual_moving and not self.target_food_item and 
                not self._dead_animation_cooldown_timer.isActive()):
                self.random_behavior_timer.start(MOVEMENT_CHANGE_DELAY)
        else:
            # Continuer la course
            if self.cat_velocity_x > 0:
                self.moving_right = True
            elif self.cat_velocity_x < 0:
                self.moving_right = False
            self._set_animation('Run')
    
    def _handle_normal_movement(self, max_x, ground_y):
        """Gère les mouvements normaux avec rebonds"""
        bounced = False
        
        # Rebonds sur les bords
        if self._current_x < 0:
            self._current_x = 0.0
            if not self._is_manual_moving and not self.target_food_item:
                self.cat_velocity_x *= -1
            bounced = True
        elif self._current_x > max_x:
            self._current_x = float(max_x)
            if not self._is_manual_moving and not self.target_food_item:
                self.cat_velocity_x *= -1
            bounced = True
        
        if self._current_y < 0:
            self._current_y = 0.0
            if not self._is_manual_moving and not self.target_food_item:
                self.cat_velocity_y *= -1
            bounced = True
        elif self._current_y > ground_y:
            self._current_y = ground_y
            if not self._is_manual_moving and not self.target_food_item:
                self.cat_velocity_y *= -1
            bounced = True
        
        self.move(int(self._current_x), int(self._current_y))
        
        # Mettre à jour la direction
        if self.cat_velocity_x > 0:
            self.moving_right = True
        elif self.cat_velocity_x < 0:
            self.moving_right = False
        
        # Choisir l'animation appropriée
        if not self.is_playing_one_shot_animation:
            has_velocity = abs(self.cat_velocity_x) > 0.1 or abs(self.cat_velocity_y) > 0.1
            
            if not self._is_manual_moving and not self.target_food_item:
                if has_velocity and self.current_animation != 'Walk':
                    self._set_animation('Walk')
                elif not has_velocity and self.current_animation != 'Idle':
                    self._set_animation('Idle')
            elif self._is_manual_moving:
                if has_velocity:
                    self._set_animation('Walk')
                else:
                    self._set_animation('Idle')
    
    def _random_movement(self):
        """Génère un mouvement aléatoire avec de longues pauses"""
        if (self.is_playing_one_shot_animation or self.is_sliding or 
            self._is_manual_moving or self.is_dead or self.target_food_item or
            self.quiet_mode):
            return
        
        choice = random.random()
        speed = config_manager.get("movement_speed", MOVEMENT_SPEED)
        
        # NOUVELLES PROBABILITÉS : Beaucoup plus de pauses !
        if choice < 0.60:  # 60% de chance de ne rien faire (LONG IDLE)
            self.cat_velocity_x = 0.0
            self.cat_velocity_y = 0.0
            self._set_animation('Idle')
            
            # Programmer le prochain mouvement dans LONGTEMPS
            next_delay = random.choice([
                random.randint(30000, 60000),    # 30s-1min (40% de chance)
                random.randint(60000, 120000),   # 1-2min (30% de chance)  
                random.randint(120000, 300000),  # 2-5min (20% de chance)
            ])
            
            print(f"😴 Minou se repose pendant {next_delay//1000} secondes")
            self.random_behavior_timer.start(next_delay)
            
        elif choice < 0.75:  # 15% de chance de marcher un peu
            angle = random.uniform(0, 2 * math.pi)
            vx = speed * random.uniform(0.5, 1.0) * math.cos(angle)
            vy = speed * random.uniform(0.5, 1.0) * math.sin(angle)
            
            self.cat_velocity_x = vx
            self.cat_velocity_y = vy
            self._set_animation('Walk')
            
            # Marcher pendant peu de temps seulement
            walk_duration = random.randint(3000, 8000)  # 3-8 secondes
            QTimer.singleShot(walk_duration, self._stop_walking)
            
            # Prochain comportement dans un délai moyen
            next_delay = random.randint(20000, 90000)  # 20s-1.5min
            self.random_behavior_timer.start(next_delay)
            
        elif choice < 0.85:  # 10% de chance de courir vers un bord
            self._start_edge_run()
            # Edge run programme son propre prochain délai
            next_delay = random.randint(45000, 180000)  # 45s-3min après la course
            QTimer.singleShot(10000, lambda: self.random_behavior_timer.start(next_delay))
            
        elif choice < 0.92:  # 7% de chance de glisser
            self._start_slide_behavior()
            # Même logique que pour la course
            next_delay = random.randint(30000, 120000)  # 30s-2min après glissade
            QTimer.singleShot(8000, lambda: self.random_behavior_timer.start(next_delay))
            
        else:  # 8% de chance de sauter
            self._play_one_shot_animation('Jump')
            # Délai après le saut
            next_delay = random.randint(25000, 90000)  # 25s-1.5min
            QTimer.singleShot(5000, lambda: self.random_behavior_timer.start(next_delay))

    def _stop_walking(self):
        """Arrête la marche et met en idle"""
        if not self.is_playing_one_shot_animation and not self._is_manual_moving:
            self.cat_velocity_x = 0.0
            self.cat_velocity_y = 0.0
            self._set_animation('Idle')

    def _check_activity(self):
        """Vérifie s'il faut reprendre l'activité après le mode tranquille"""
        if self.quiet_mode:
            # Chance de reprendre l'activité automatiquement
            if random.random() < 0.3:  # 30% de chance de reprendre
                self._resume_activity()
            else:
                # Rester tranquille encore un peu
                QTimer.singleShot(random.randint(60000, 180000), self._check_activity)

    def _resume_activity(self):
        """Reprend l'activité normale"""
        self.quiet_mode = False
        
        if not self.is_dead:
            # Reprendre avec un délai initial plus long
            initial_delay = random.randint(30000, 120000)  # 30s-2min
            self.random_behavior_timer.start(initial_delay)
            
            if config_manager.get("sound_enabled", True):
                self.audio_play_timer.start(random.randint(60000, 180000))
            
            # Messages et poop avec délais longs
            if config_manager.get("random_messages_enabled", True):
                self.random_message_timer.start(random.randint(300000, 1800000))  # 5-30min
            
            self.poop_spawn_timer.start(random.randint(120000, 300000))  # 2-5min
        
        self.stay_quiet_action.setText("😴 Rester tranquille")
    
    def _start_edge_run(self):
        """Démarre une course vers un bord aléatoire"""
        screen_rect = QApplication.desktop().screenGeometry()
        edges = ['top', 'bottom', 'left', 'right']
        edge = random.choice(edges)
        
        if edge == 'top':
            self.target_x = random.randint(0, screen_rect.width() - CAT_WIDTH)
            self.target_y = 0
        elif edge == 'bottom':
            self.target_x = random.randint(0, screen_rect.width() - CAT_WIDTH)
            self.target_y = screen_rect.height() - CAT_HEIGHT
        elif edge == 'left':
            self.target_x = 0
            self.target_y = random.randint(0, screen_rect.height() - CAT_HEIGHT)
        else:  # right
            self.target_x = screen_rect.width() - CAT_WIDTH
            self.target_y = random.randint(0, screen_rect.height() - CAT_HEIGHT)
        
        dx = float(self.target_x) - self._current_x
        dy = float(self.target_y) - self._current_y
        distance = math.sqrt(dx*dx + dy*dy)
        
        if distance < 1.0:
            return
        
        speed = config_manager.get("movement_speed", MOVEMENT_SPEED)
        self.cat_velocity_x = (dx / distance) * speed * RUN_SPEED_MULTIPLIER
        self.cat_velocity_y = (dy / distance) * speed * RUN_SPEED_MULTIPLIER
        self.is_edge_running = True
        self._set_animation('Run')
    
    def _start_slide_behavior(self):
        """Démarre une glissade"""
        screen_rect = QApplication.desktop().screenGeometry()
        slide_types = ['horizontal', 'diagonal_down']
        slide_type = random.choice(slide_types)
        
        if slide_type == 'horizontal':
            # Glissade horizontale
            self.target_y = int(self._current_y)
            
            # Choisir une direction avec assez d'espace
            min_distance = 100
            possible_targets = []
            
            if self._current_x + min_distance < screen_rect.width() - CAT_WIDTH:
                possible_targets.extend(range(
                    int(self._current_x + min_distance), 
                    screen_rect.width() - CAT_WIDTH
                ))
            
            if self._current_x - min_distance > 0:
                possible_targets.extend(range(0, int(self._current_x - min_distance)))
            
            self.target_x = random.choice(possible_targets) if possible_targets else int(self._current_x)
            
        else:  # diagonal_down
            # Glissade diagonale vers le bas
            min_y = int(self._current_y + 50)
            self.target_y = random.randint(
                min_y, 
                screen_rect.height() - CAT_HEIGHT
            ) if min_y < screen_rect.height() - CAT_HEIGHT else int(self._current_y)
            
            # Position X légèrement décalée
            offset = random.randint(-100, 100)
            self.target_x = max(0, min(
                int(self._current_x + offset), 
                screen_rect.width() - CAT_WIDTH
            ))
        
        # Calculer la vélocité
        dx = float(self.target_x) - self._current_x
        dy = float(self.target_y) - self._current_y
        distance = math.sqrt(dx*dx + dy*dy)
        
        if distance < 1.0:
            return
        
        speed = config_manager.get("movement_speed", MOVEMENT_SPEED) * 1.5
        self.cat_velocity_x = (dx / distance) * speed
        self.cat_velocity_y = (dy / distance) * speed
        
        self.is_sliding = True
        self.slide_target_pos = QPoint(self.target_x, self.target_y)
        self._set_animation('Slide')
    
    def _play_one_shot_animation(self, animation_name):
        """Joue une animation unique (non-looping)"""
        if self.is_dead or animation_name not in self.sprites:
            return
        
        self.is_playing_one_shot_animation = True
        self.random_behavior_timer.stop()
        self._is_manual_moving = False
        self.cat_velocity_x = 0.0
        self.media_player.stop()
        
        if animation_name == 'Jump':
            self.cat_velocity_y = -JUMP_INITIAL_VELOCITY
            self._is_jumping = True
        else:
            self.cat_velocity_y = 0.0
            duration_ms = len(self.sprites[animation_name]) * ANIMATION_FRAME_RATE
            QTimer.singleShot(duration_ms, self._one_shot_animation_finished)
        
        self.current_animation = animation_name
        self.current_frame_index = 0
        self._update_sprite_display()
    
    def _one_shot_animation_finished(self):
        """Appelé quand une animation unique se termine"""
        if self.current_animation == 'Dead':
            self.is_playing_one_shot_animation = False
            self.is_dead = True
            self.revive_pet_action.setEnabled(True)
            return
        
        self.is_playing_one_shot_animation = False
        self._set_animation('Idle')
        
        # CORRECTION : Ne pas redémarrer immédiatement, laisser du temps
        if (not self._is_manual_moving and not self.is_dead and 
            not self.target_food_item):
            # Délai aléatoire long avant le prochain mouvement
            delay = random.randint(20000, 120000)  # 20s-2min
            self.random_behavior_timer.start(delay)
        
        if (config_manager.get("sound_enabled", True) and 
            self.media_player.state() == QMediaPlayer.StoppedState and 
            not self.is_dead):
            self.audio_play_timer.start(random.randint(60000, 300000))  # 1-5min

    def _on_control_box_closed(self):
        """Appelé quand la boîte de contrôle est fermée"""
        self.control_box = None
        self._is_manual_moving = False
        
        # CORRECTION : Laisser un délai après fermeture des contrôles
        if not self.is_playing_one_shot_animation and not self.is_dead and not self.active_food_items:
            delay = random.randint(15000, 60000)  # 15s-1min de pause
            self.random_behavior_timer.start(delay)
        
        self.cat_velocity_x = 0.0
        self.cat_velocity_y = 0.0
        self._set_animation('Idle')
        
        if config_manager.get("sound_enabled", True) and not self.is_dead:
            self.audio_play_timer.start(random.randint(30000, 120000))  # 30s-2min
        
    def _play_dead_animation(self):
        """Joue l'animation de mort"""
        if 'Dead' not in self.sprites:
            self._play_one_shot_animation('Hurt')
            return
        
        self.is_playing_one_shot_animation = True
        self.random_behavior_timer.stop()
        self.movement_timer.stop()
        self.audio_play_timer.stop()
        self.media_player.stop()
        self.target_food_item = None
        self.is_dead = True
        
        # Arrêter tous les mouvements
        self._is_manual_moving = False
        self.is_edge_running = False
        self.is_sliding = False
        self._is_jumping = False
        self.cat_velocity_x = 0.0
        self.cat_velocity_y = 0.0
        
        self.current_animation = 'Dead'
        self.current_frame_index = 0
        self._update_sprite_display()
        
        # Aller à la dernière frame et s'arrêter
        duration = (len(self.sprites['Dead']) - 1) * ANIMATION_FRAME_RATE
        QTimer.singleShot(duration, self._reached_last_dead_frame)
        
        # Message dramatique
        pet_name = config_manager.get("pet_name", "Minou")
        self.show_bubble(f"{pet_name} est K.O. ! 💀", "alert", 5000)
    
    def _reached_last_dead_frame(self):
        """Atteint la dernière frame de l'animation de mort"""
        if 'Dead' in self.sprites:
            self.current_frame_index = len(self.sprites['Dead']) - 1
            self._update_sprite_display()
        
        self.animation_timer.stop()
        self.movement_timer.stop()
        self.revive_pet_action.setEnabled(True)
    
    def _dead_animation_cooldown_finished(self):
        """Appelé quand le cooldown après mort se termine"""
        self.is_playing_one_shot_animation = False
        self.animation_timer.start(config_manager.get("animation_speed", ANIMATION_FRAME_RATE))
        self.movement_timer.start(16)
        
        self._set_animation('Idle')
        if not self._is_manual_moving and not self.target_food_item:
            self.random_behavior_timer.start(MOVEMENT_CHANGE_DELAY)
        
        if config_manager.get("sound_enabled", True):
            self.audio_play_timer.start(random.randint(1000, 5000))
    
    def _reset_pet(self):
        """Ressuscite l'animal"""
        pet_name = config_manager.get("pet_name", "Minou")
        
        # Remettre tous les états à zéro
        self.is_dead = False
        self.is_playing_one_shot_animation = False
        self._is_manual_moving = False
        self.is_edge_running = False
        self.is_sliding = False
        self._is_jumping = False
        self.cat_velocity_x = 0.0
        self.cat_velocity_y = 0.0
        self._click_count = 0
        self.target_food_item = None
        self.revive_pet_action.setEnabled(False)
        
        # Redémarrer les timers
        self.animation_timer.start(config_manager.get("animation_speed", ANIMATION_FRAME_RATE))
        self.movement_timer.start(16)
        self.random_behavior_timer.start(MOVEMENT_CHANGE_DELAY)
        
        if config_manager.get("sound_enabled", True):
            self.audio_play_timer.start(random.randint(1000, 5000))
        
        self._set_animation('Idle')
        
        # Message de résurrection
        self.show_bubble(f"{pet_name} est de retour ! 💖", "love", 3000)
    
    # Méthodes de gestion de la nourriture et objets
    def add_random_food(self):
        """Ajoute un élément de nourriture aléatoire"""
        food_item = FoodItem()
        if food_item.is_valid:
            food_item.food_removed.connect(self._on_food_removed)
            self.active_food_items.append(food_item)
            food_item.show()
            self.raise_()
            
            # Message encourageant
            self.show_bubble("Miam ! De la nourriture ! 🍖", "love", 2000)
        else:
            print("⚠️ Impossible de créer la nourriture - assets manquants")
    
    def _on_food_removed(self, food_item):
        """Appelé quand une nourriture est supprimée/mangée"""
        if food_item in self.active_food_items:
            food_item.hide()
            food_item.deleteLater()
            self.active_food_items.remove(food_item)
            
            if self.target_food_item == food_item:
                self.target_food_item = None
    
    def clear_all_food(self):
        """Supprime toute la nourriture"""
        for food_item in list(self.active_food_items):
            food_item.hide()
            food_item.deleteLater()
        
        self.active_food_items.clear()
        self.target_food_item = None
        print("🧹 Toute la nourriture a été nettoyée")
    
    def add_random_poop(self):
        """Ajoute un élément poop près de l'animal"""
        poop_item = PoopItem(near_pet=True, pet_pos=QPoint(int(self._current_x), int(self._current_y)))
        if poop_item.is_valid:
            poop_item.poop_removed.connect(self._on_poop_removed)
            self.active_poop_items.append(poop_item)
            poop_item.show()
            
            # Message gêné
            self.show_bubble("Oops... désolé ! 💩", "normal", 2000)
        else:
            print("⚠️ Impossible de créer le poop - assets manquants")
    
    def _spawn_random_poop(self):
        """Spawn automatique de poop (appelé par timer)"""
        if not self.is_dead and random.random() < 0.3:  # 30% de chance
            self.add_random_poop()
    
    def _on_poop_removed(self, poop_item):
        """Appelé quand un poop est nettoyé"""
        print(f"🧹 [MinouPet] _on_poop_removed() appelé pour {poop_item}")
        if poop_item in self.active_poop_items:
            print(f"   🔍 PoopItem trouvé dans active_poop_items (count: {len(self.active_poop_items)})")
            poop_item.hide()
            print("   👻 PoopItem masqué")
            poop_item.deleteLater()
            print("   🗑️  PoopItem marqué pour suppression")
            self.active_poop_items.remove(poop_item)
            print(f"   ✅ PoopItem retiré de active_poop_items (nouveau count: {len(self.active_poop_items)})")
        else:
            print("   ❌ PoopItem non trouvé dans active_poop_items")
    
    def clear_all_poop(self):
        """Nettoie tous les poops"""
        for poop_item in list(self.active_poop_items):
            poop_item.hide()
            poop_item.deleteLater()
        
        self.active_poop_items.clear()
        print("🧹 Tout le poop a été nettoyé")
    
    # Méthodes audio
    def _play_random_audio(self):
        """Joue un son aléatoire"""
        if not config_manager.get("sound_enabled", True) or self.is_dead:
            return
        
        audio_url = self.audio_files.get(self.current_asset_type)
        if audio_url and not audio_url.isEmpty():
            self.media_player.setMedia(QMediaContent(audio_url))
            self.media_player.play()
        
        # CORRECTION : Sons TRÈS espacés (2-10 minutes)
        next_audio_delay = random.choice([
            random.randint(120000, 300000),   # 2-5min (50% de chance)
            random.randint(300000, 600000),   # 5-10min (30% de chance)  
            random.randint(600000, 1200000)   # 10-20min (20% de chance)
        ])
        
        print(f"🔊 Prochain son dans {next_audio_delay//60000} minutes")
        self.audio_play_timer.start(next_audio_delay)
    
    def _audio_state_changed(self, state):
        """Appelé quand l'état audio change"""
        if (state == QMediaPlayer.StoppedState and 
            config_manager.get("sound_enabled", True) and 
            not self._is_manual_moving and 
            not self.is_playing_one_shot_animation and 
            not self.is_dead):
            self.audio_play_timer.start(random.randint(5000, 15000))
    
    def _toggle_audio(self):
        """Active/désactive l'audio"""
        current = config_manager.get("sound_enabled", True)
        config_manager.set("sound_enabled", not current)
        
        if config_manager.get("sound_enabled", True):
            self.toggle_audio_action.setText("🔊 Désactiver son")
            if not self.is_dead:
                self.audio_play_timer.start(random.randint(1000, 5000))
        else:
            self.toggle_audio_action.setText("🔇 Activer son")
            self.media_player.stop()
            self.audio_play_timer.stop()
    
    # Méthodes de contrôle manuel
    def _open_control_box(self):
        """Ouvre la boîte de contrôle"""
        if self.control_box is None:
            self.control_box = ControlBox(self)
            
            # Connexions des signaux
            self.control_box.move_left_signal.connect(self.start_manual_move_left)
            self.control_box.move_right_signal.connect(self.start_manual_move_right)
            self.control_box.move_up_signal.connect(self.start_manual_move_up)
            self.control_box.move_down_signal.connect(self.start_manual_move_down)
            self.control_box.stop_movement_signal.connect(self.stop_manual_movement)
            self.control_box.jump_signal.connect(self._manual_jump)
            self.control_box.slide_signal.connect(self._manual_slide)
            self.control_box.closed_signal.connect(self._on_control_box_closed)
            
            # Position de la boîte près de l'animal
            pet_pos = self.pos()
            self.control_box.move(pet_pos.x() + CAT_WIDTH + 20, pet_pos.y())
        
        self.control_box.show()
        self.control_box.activateWindow()
        self.control_box.raise_()
        
        # Arrêter les mouvements automatiques
        if not self.is_dead:
            self.random_behavior_timer.stop()
        
        self.is_edge_running = False
        self.is_sliding = False
        self._is_jumping = False
        self._is_manual_moving = True
        self.cat_velocity_x = 0.0
        self.cat_velocity_y = 0.0
        self._set_animation('Idle')
        self.media_player.stop()
        self.audio_play_timer.stop()
        self.target_food_item = None
    
    def _on_control_box_closed(self):
        """Appelé quand la boîte de contrôle est fermée"""
        self.control_box = None
        self._is_manual_moving = False
        
        if not self.is_playing_one_shot_animation and not self.is_dead and not self.active_food_items:
            self.random_behavior_timer.start(MOVEMENT_CHANGE_DELAY)
        
        self.cat_velocity_x = 0.0
        self.cat_velocity_y = 0.0
        self._set_animation('Idle')
        
        if config_manager.get("sound_enabled", True) and not self.is_dead:
            self.audio_play_timer.start(random.randint(1000, 5000))
    
    def _start_manual_movement(self, vx, vy):
        """Démarre un mouvement manuel"""
        if self._is_jumping or self.is_sliding or self.is_dead:
            return
        
        self._is_manual_moving = True
        self.random_behavior_timer.stop()
        self.is_edge_running = False
        
        speed = config_manager.get("movement_speed", MOVEMENT_SPEED)
        self.cat_velocity_x = vx * speed
        self.cat_velocity_y = vy * speed
        
        if abs(vx) > 0.1 or abs(vy) > 0.1:
            self._set_animation('Walk')
        else:
            self._set_animation('Idle')
        
        self.media_player.stop()
        self.audio_play_timer.stop()
        self.target_food_item = None
    
    def start_manual_move_left(self):
        self.moving_right = False
        self._start_manual_movement(-1.0, 0.0)
    
    def start_manual_move_right(self):
        self.moving_right = True
        self._start_manual_movement(1.0, 0.0)
    
    def start_manual_move_up(self):
        self._start_manual_movement(0.0, -1.0)
    
    def start_manual_move_down(self):
        self._start_manual_movement(0.0, 1.0)
    
    def stop_manual_movement(self):
        """Arrête le mouvement manuel"""
        if not self._is_jumping and not self.is_sliding and not self.is_dead:
            self.cat_velocity_x = 0.0
            self.cat_velocity_y = 0.0
            self._set_animation('Idle')
        
        if (config_manager.get("sound_enabled", True) and 
            self.media_player.state() == QMediaPlayer.StoppedState and 
            not self.is_dead):
            self.audio_play_timer.start(random.randint(1000, 5000))
    
    def _manual_jump(self):
        """Saut manuel"""
        if not self._is_jumping and not self.is_playing_one_shot_animation and not self.is_dead:
            self.stop_manual_movement()
            self._play_one_shot_animation('Jump')
    
    def _manual_slide(self):
        """Glissade manuelle"""
        if not self.is_sliding and not self.is_playing_one_shot_animation and not self.is_dead:
            self.stop_manual_movement()
            self._start_slide_behavior()
    
    # Méthodes d'interface utilisateur
    def show_bubble(self, message, bubble_type="normal", duration=3000):
        """Affiche une bulle de dialogue au-dessus de l'animal avec durée adaptative"""
        if not self.speech_bubble:
            return
        
        # Calculer la durée en fonction de la longueur du message
        if duration == 3000 or duration == 5000:  # Si c'est la durée par défaut
            # Calcul intelligent : ~200ms par mot + temps de base
            word_count = len(message.split())
            char_count = len(message)
            
            # Temps de base + temps de lecture
            base_time = 2000  # 2 secondes de base
            reading_time = max(
                word_count * 400,    # 400ms par mot (lecture normale)
                char_count * 50      # 50ms par caractère (sécurité)
            )
            
            # Durée totale avec limites
            calculated_duration = base_time + reading_time
            duration = max(4000, min(calculated_duration, 20000))  # Entre 4s et 20s
            
            print(f"💬 Bulle: {word_count} mots, {char_count} chars -> {duration//1000}s")
        
        # Position de la bulle au-dessus de l'animal
        pet_pos = self.pos()
        bubble_x = pet_pos.x() + CAT_WIDTH // 2 - 100  # Centrer approximativement
        bubble_y = pet_pos.y() - 80  # Au-dessus de l'animal
        
        # S'assurer que la bulle reste à l'écran
        screen_rect = QApplication.desktop().screenGeometry()
        bubble_x = max(10, min(bubble_x, screen_rect.width() - 220))
        bubble_y = max(10, bubble_y)
        
        self.speech_bubble.move(bubble_x, bubble_y)
        self.speech_bubble.show_message(message, bubble_type, duration)
    
    def _show_chat(self):
        """Affiche l'interface de chat"""
        if not self.chat_interface:
            return
        
        # Position du chat près de l'animal
        pet_pos = self.pos()
        chat_x = pet_pos.x() + CAT_WIDTH // 2 - 150
        chat_y = pet_pos.y() - 50
        
        # S'assurer que le chat reste à l'écran
        screen_rect = QApplication.desktop().screenGeometry()
        chat_x = max(10, min(chat_x, screen_rect.width() - 310))
        chat_y = max(10, chat_y)
        
        self.chat_interface.move(chat_x, chat_y)
        self.chat_interface.show_chat()
    
    def handle_user_message(self, message):
        """Traite un message de l'utilisateur"""
        print(f"👤 {config_manager.get('user_name', 'theTigerFox')}: {message}")
        
        # Démarrer le thread de conversation
        if self.conversation_thread and self.conversation_thread.isRunning():
            self.conversation_thread.terminate()
        
        self.conversation_thread = ConversationThread(message, gemini_ai)
        self.conversation_thread.response_ready.connect(self._handle_ai_response)
        self.conversation_thread.start()
        
        # Montrer que Minou "réfléchit"
        self.show_bubble("🤔 Hmm...", "info", 1000)
    
    def _handle_ai_response(self, response, message_type):
        """Traite la réponse de l'IA"""
        pet_name = config_manager.get("pet_name", "Minou")
        print(f"🤖 {pet_name}: {response}")
        
        # AJOUT : Parser les commandes JSON
        try:
            import json
            import re
            
            # Chercher du JSON dans la réponse
            json_pattern = r'\{"action":\s*"[^"]+",.*?\}'
            json_matches = re.findall(json_pattern, response, re.DOTALL)
            
            if json_matches:
                for json_str in json_matches:
                    try:
                        command = json.loads(json_str)
                        action = command.get("action", "")
                        
                        if action == "note":
                            content = command.get("content", "")
                            if content:
                                # Sauvegarder la note
                                notes_manager.add_note(content)
                                print(f"📝 Note sauvegardée: {content}")
                                
                                # Confirmation à l'utilisateur
                                self.show_bubble(f"📝 Note sauvegardée: {content[:40]}...", "info", 4000)
                                
                                # Ne pas afficher le JSON dans la bulle
                                clean_response = response.replace(json_str, "").strip()
                                if clean_response:
                                    self.show_bubble(clean_response, message_type, 5000)
                                return
                        
                        elif action == "reminder":
                            time_str = command.get("time", "")
                            message = command.get("message", "")
                            if time_str and message:
                                # TODO: Implémenter les rappels avec reminder_manager
                                print(f"⏰ Rappel programmé: {time_str} - {message}")
                                self.show_bubble(f"⏰ Rappel programmé: {message}", "info", 4000)
                                
                                # Ne pas afficher le JSON dans la bulle
                                clean_response = response.replace(json_str, "").strip()
                                if clean_response:
                                    self.show_bubble(clean_response, message_type, 5000)
                                return
                                
                    except json.JSONDecodeError:
                        print(f"❌ Erreur parsing JSON: {json_str}")
                        continue
        
        except Exception as e:
            print(f"❌ Erreur lors du traitement de la réponse IA: {e}")
        
        # Afficher la réponse normale dans une bulle (sans JSON)
        self.show_bubble(response, message_type, 5000)
        
    # Méthodes de messages et notifications
    def _show_random_message(self):
        """Affiche un message aléatoire"""
        if self.is_dead:
            return
        
        message_types = []
        
        if config_manager.get("love_messages_enabled", True):
            message_types.append("love")
        
        if config_manager.get("quotes_enabled", True):
            message_types.append("quote")
        
        if config_manager.get("research_suggestions_enabled", True):
            message_types.append("research")
        
        if not message_types:
            return
        
        message_type = random.choice(message_types)
        
        if message_type == "love":
            message = message_generator.get_random_love_message()
            bubble_type = "love"
        elif message_type == "quote":
            message = f"💎 {message_generator.get_random_quote()}"
            bubble_type = "info"
        else:  # research
            message = f"💡 {message_generator.get_random_research_suggestion()}"
            bubble_type = "normal"
        
        self.show_bubble(message, bubble_type, 4000)
        
        # Programmer le prochain message
        if config_manager.get("random_messages_enabled", True):
            interval_range = config_manager.get("random_message_interval", [300, 900])
            interval = random.randint(interval_range[0], interval_range[1]) * 1000
            self.random_message_timer.start(interval)
    
    def _show_reminder(self, reminder_message):
        """Affiche un rappel"""
        self.show_bubble(f"⏰ Rappel: {reminder_message}", "alert", 6000)
        
        # Notification système si disponible
        pet_name = config_manager.get("pet_name", "Minou")
        if self.tray_icon.supportsMessages():
            self.tray_icon.showMessage(
                f"Rappel de {pet_name}",
                reminder_message,
                QSystemTrayIcon.Information,
                5000
            )
    
    def _show_system_alert(self, alert_type, message):
        """Affiche une alerte système"""
        self.show_bubble(message, "alert", 5000)
        
        # Jouer une animation selon le type
        if alert_type == "memory" and not self.is_dead:
            self._play_one_shot_animation('Hurt')
        elif alert_type == "battery" and not self.is_dead:
            self._set_animation('Idle')  # Animation calme pour économiser
    
    # Méthodes de menu et paramètres
    def _open_settings(self):
        """Ouvre la fenêtre de paramètres"""
        settings_dialog = SettingsDialog(config_manager, self)
        if settings_dialog.exec_() == settings_dialog.Accepted:
            self._apply_new_settings()
    
    def _apply_new_settings(self):
        """Applique les nouveaux paramètres"""
        # Mettre à jour la vitesse de mouvement
        # (sera appliqué automatiquement via config_manager)
        
        # Mettre à jour le type d'animal si nécessaire
        new_pet_type = config_manager.get("pet_type", "cat")
        if new_pet_type != self.current_asset_type:
            self.change_pet_type(new_pet_type)
        
        # Mettre à jour l'audio
        if config_manager.get("sound_enabled", True):
            if not self.audio_play_timer.isActive() and not self.is_dead:
                self.audio_play_timer.start(random.randint(1000, 5000))
        else:
            self.media_player.stop()
            self.audio_play_timer.stop()
        
        # Mettre à jour les messages aléatoires
        if config_manager.get("random_messages_enabled", True):
            if not self.random_message_timer.isActive():
                interval_range = config_manager.get("random_message_interval", [300, 900])
                interval = random.randint(interval_range[0], interval_range[1]) * 1000
                self.random_message_timer.start(interval)
        else:
            self.random_message_timer.stop()
        
        # Réinitialiser l'IA
        gemini_ai.initialize_api()
        
        print("✅ Paramètres appliqués")
    
    def _show_system_info(self):
        """Affiche les informations système"""
        info = get_system_info()
        self.show_bubble(info, "info", 8000)
    
    def _show_notes(self):
        """Affiche les notes récentes"""
        recent_notes = notes_manager.get_recent_notes(3)
        
        if not recent_notes:
            message = "📝 Aucune note sauvegardée"
        else:
            message = "📝 Mes dernières notes:\n"
            for i, note in enumerate(recent_notes, 1):
                content = note['content'][:30] + "..." if len(note['content']) > 30 else note['content']
                message += f"{i}. {content}\n"
        
        self.show_bubble(message, "info", 6000)
    
    # Méthodes de tray icon
    def _update_tray_icon_animation(self):
        """Met à jour l'animation de l'icône tray"""
        idle_sprites = self.sprites.get('Idle')
        if idle_sprites:
            self.tray_icon_current_frame_index = (self.tray_icon_current_frame_index + 1) % len(idle_sprites)
            pixmap = idle_sprites[self.tray_icon_current_frame_index]
            self.tray_icon.setIcon(QIcon(pixmap))
        else:
            self.tray_icon.setIcon(self.style().standardIcon(QStyle.SP_ComputerIcon))
    
    def toggle_visibility(self):
        """Bascule la visibilité de l'animal"""
        if self.isVisible():
            self.hide()
            self.toggle_visibility_action.setText("Afficher")
        else:
            self.show()
            self.toggle_visibility_action.setText("Masquer")
            
            if not self._is_manual_moving and not self.is_dead:
                self.random_behavior_timer.start(MOVEMENT_CHANGE_DELAY)
    
    def on_tray_icon_activated(self, reason):
        """Appelé quand l'icône tray est activée"""
        if reason == QSystemTrayIcon.Trigger:
            self.toggle_visibility()
        elif reason == QSystemTrayIcon.DoubleClick:
            self._show_chat()
    
    # Méthodes d'événements de souris
    def mousePressEvent(self, event):
        """Gestion du clic de souris"""
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.mouse_press_pos = event.globalPos()
            self.offset = event.pos()
            
            # Arrêter les mouvements automatiques
            self.random_behavior_timer.stop()
            self._dead_animation_cooldown_timer.stop()
            self._is_manual_moving = False
            self.cat_velocity_x = 0.0
            self.cat_velocity_y = 0.0
            self._set_animation('Idle')
            self.is_edge_running = False
            self.is_sliding = False
            self._is_jumping = False
            self.media_player.stop()
            self.target_food_item = None
            
            if self.is_dead:
                self.is_dead = False  # Permettre de bouger même mort
    
    def mouseMoveEvent(self, event):
        """Gestion du déplacement de souris (drag)"""
        if self.dragging:
            new_pos = self.mapToGlobal(event.pos() - self.offset)
            self.move(new_pos)
            self._current_x = float(new_pos.x())
            self._current_y = float(new_pos.y())
    
    def mouseReleaseEvent(self, event):
        """Gestion du relâchement de souris"""
        if event.button() == Qt.LeftButton:
            self.dragging = False
            mouse_release_pos = event.globalPos()
            distance_moved = (mouse_release_pos - self.mouse_press_pos).manhattanLength()
            
            # Si c'est un clic (pas un drag)
            if distance_moved < CLICK_THRESHOLD and not self.is_dead:
                self._click_count += 1
                
                if self._click_count >= DEAD_ANIMATION_THRESHOLD:
                    self._play_dead_animation()
                    self._click_count = 0
                else:
                    self._play_one_shot_animation('Hurt')
                    
                    # Messages selon le nombre de clics
                    if self._click_count == 1:
                        self.show_bubble("Aïe ! 😿", "normal", 2000)
                    elif self._click_count == 2:
                        self.show_bubble("Arrête ! 😾", "alert", 2000)
                    elif self._click_count >= 3:
                        self.show_bubble("Tu me fais mal ! 😭", "alert", 2000)
            
            elif self.is_dead:
                self._click_count = 0
            
            # Reprendre les activités normales si pas mort
            if not self.is_dead:
                if not self._is_manual_moving and not self.active_food_items:
                    self.random_behavior_timer.start(MOVEMENT_CHANGE_DELAY)
                
                if (config_manager.get("sound_enabled", True) and 
                    self.media_player.state() == QMediaPlayer.StoppedState):
                    self.audio_play_timer.start(random.randint(1000, 5000))
        
        # Vérifier si on doit chasser de la nourriture
        if (not self.dragging and not self.target_food_item and 
            self.active_food_items and not self.is_dead):
            self.target_food_item = self.active_food_items[0]
            if self.target_food_item:
                pass
    
    def _toggle_quiet_mode(self):
        """Active/désactive le mode tranquille"""
        self.quiet_mode = not self.quiet_mode
        
        if self.quiet_mode:
            # Arrêter tous les mouvements et sons
            self.random_behavior_timer.stop()
            self.audio_play_timer.stop()
            self.random_message_timer.stop()
            self.poop_spawn_timer.stop()
            self.media_player.stop()
            
            # Arrêter les mouvements en cours
            self.cat_velocity_x = 0.0
            self.cat_velocity_y = 0.0
            self.is_edge_running = False
            self.is_sliding = False
            self._set_animation('Idle')
            
            # Mettre à jour l'interface
            self.stay_quiet_action.setText("😸 Reprendre activité")
            self.show_bubble("😴 Mode tranquille activé - Je vais me reposer un peu...", "info", 4000)
            
            # Planifier un retour à l'activité plus tard (30-60 secondes)
            QTimer.singleShot(random.randint(30000, 60000), self._check_activity)
        else:
            # Reprendre l'activité immédiatement
            self._resume_activity()
            
            self.stay_quiet_action.setText("😴 Rester tranquille")
            self.show_bubble("😸 Je reprends mes activités !", "love", 2000)

# ... (code inchangé)
        """Gestion de la fermeture de l'application"""
        if self.control_box:
            self.control_box.close()
        
        if self.speech_bubble:
            self.speech_bubble.close()
        
        if self.chat_interface:
            self.chat_interface.close()
        
        # Arrêter tous les timers
        self.media_player.stop()
        self.audio_play_timer.stop()
        self._dead_animation_cooldown_timer.stop()
        self.random_message_timer.stop()
        
        # Nettoyer les objets
        self.clear_all_food()
        self.clear_all_poop()
        
        # Arrêter les threads
        if self.conversation_thread and self.conversation_thread.isRunning():
            self.conversation_thread.terminate()
            self.conversation_thread.wait(1000)
        
        if QApplication.quitOnLastWindowClosed():
            self.tray_icon.hide()
            event.accept()
        else:
            event.ignore()
            self.hide()
            
            pet_name = config_manager.get("pet_name", "Minou")
            self.tray_icon.showMessage(
                pet_name,
                f"{pet_name} continue de vivre dans la barre système ! Clique pour le faire revenir.",
                QSystemTrayIcon.Information,
                3000
            )