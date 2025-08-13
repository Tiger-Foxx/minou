"""
Configuration globale pour Minou - Desktop Pet Companion
"""
import json
import os
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QFormLayout, 
                             QLineEdit, QSpinBox, QCheckBox, QPushButton, QLabel,
                             QComboBox, QTextEdit, QTabWidget, QWidget, QSlider)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

# Constantes globales
CAT_WIDTH = 120
CAT_HEIGHT = 120
ANIMATION_FRAME_RATE = 100
MOVEMENT_SPEED = 3
MOVEMENT_CHANGE_DELAY = 3000
RUN_SPEED_MULTIPLIER = 2.5
CLICK_THRESHOLD = 5
JUMP_INITIAL_VELOCITY = 15.0
GRAVITY = 0.8
DEAD_ANIMATION_THRESHOLD = 5
FOOD_SIZE = 40
POOP_SIZE = 25
POOP_SPAWN_INTERVAL = 15000

ANIMATION_FRAMES = {
    "Dead": 10, "Fall": 8, "Hurt": 10, "Idle": 10, 
    "Jump": 8, "Run": 8, "Slide": 10, "Walk": 10
}

# Couleurs du thème sombre high-tech
DARK_THEME = {
    'bg_primary': '#1a1a1a',
    'bg_secondary': '#2d2d2d', 
    'bg_tertiary': '#404040',
    'accent_blue': '#00d4ff',
    'accent_purple': '#8b5cf6',
    'accent_green': '#10b981',
    'text_primary': '#ffffff',
    'text_secondary': '#b3b3b3',
    'border': '#4a4a4a',
    'error': '#ef4444',
    'warning': '#f59e0b',
    # AJOUT des couleurs manquantes :
    'accent_dark_blue': '#0099cc',  # Version plus sombre du bleu
    'accent_orange': '#f97316',  
}

class ConfigManager:
    def __init__(self):
        self.config_file = "minou_config.json"
        self.settings = self.load_settings()
        
    def load_settings(self):
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Erreur lors du chargement de la config: {e}")
        return self.default_settings()
    
    def default_settings(self):
        return {
            # Paramètres de base
            "pet_type": "cat",
            "pet_name": "Minou",
            "user_name": "Mon ami",
            "movement_speed": 3,
            "animation_speed": 100,
            "sound_enabled": True,
            "poop_interval": 15000,
            
            # IA et chat
            "ai_enabled": False,
            "gemini_api_key": "",
            "chat_auto_hide_delay": 5000,
            "personality": "playful",
            
            # Système et rappels
            "system_monitoring": True,
            "memory_alert_threshold": 90,
            "battery_alert_threshold": 20,
            "random_messages_enabled": True,
            "random_message_interval": [300, 900],  # 5-15 minutes
            
            # Notifications
            "love_messages_enabled": True,
            "quotes_enabled": True,
            "research_suggestions_enabled": True,
            
            # Apparence
            "theme": "dark",
            "opacity": 100,
            "bubble_duration": 3000
        }
    
    def save_settings(self):
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Erreur lors de la sauvegarde: {e}")
    
    def get(self, key, default=None):
        return self.settings.get(key, default)
    
    def set(self, key, value):
        self.settings[key] = value
        self.save_settings()

class SettingsDialog(QDialog):
    def __init__(self, config_manager, parent=None):
        super().__init__(parent)
        self.config = config_manager
        self.setWindowTitle("Paramètres de Minou")
        self.setFixedSize(500, 600)
        self.setStyleSheet(self.get_dark_style())
        self.init_ui()
        
    def get_dark_style(self):
        return f"""
        QDialog {{
            background-color: {DARK_THEME['bg_primary']};
            color: {DARK_THEME['text_primary']};
            border-radius: 10px;
        }}
        QTabWidget::pane {{
            border: 1px solid {DARK_THEME['border']};
            background-color: {DARK_THEME['bg_secondary']};
            border-radius: 5px;
        }}
        QTabBar::tab {{
            background-color: {DARK_THEME['bg_tertiary']};
            color: {DARK_THEME['text_primary']};
            padding: 8px 16px;
            margin: 2px;
            border-radius: 5px;
        }}
        QTabBar::tab:selected {{
            background-color: {DARK_THEME['accent_blue']};
            color: {DARK_THEME['bg_primary']};
        }}
        QLabel {{
            color: {DARK_THEME['text_primary']};
            font-weight: bold;
        }}
        QLineEdit, QSpinBox, QComboBox {{
            background-color: {DARK_THEME['bg_tertiary']};
            color: {DARK_THEME['text_primary']};
            border: 2px solid {DARK_THEME['border']};
            border-radius: 5px;
            padding: 8px;
            font-size: 12px;
        }}
        QLineEdit:focus, QSpinBox:focus, QComboBox:focus {{
            border-color: {DARK_THEME['accent_blue']};
        }}
        QCheckBox {{
            color: {DARK_THEME['text_primary']};
            spacing: 5px;
        }}
        QCheckBox::indicator {{
            width: 18px;
            height: 18px;
            border-radius: 3px;
            border: 2px solid {DARK_THEME['border']};
            background-color: {DARK_THEME['bg_tertiary']};
        }}
        QCheckBox::indicator:checked {{
            background-color: {DARK_THEME['accent_green']};
            border-color: {DARK_THEME['accent_green']};
        }}
        QPushButton {{
            background-color: {DARK_THEME['accent_blue']};
            color: {DARK_THEME['bg_primary']};
            border: none;
            border-radius: 5px;
            padding: 10px 20px;
            font-weight: bold;
            font-size: 12px;
        }}
        QPushButton:hover {{
            background-color: {DARK_THEME['accent_purple']};
        }}
        QPushButton:pressed {{
            background-color: {DARK_THEME['bg_tertiary']};
        }}
        QTextEdit {{
            background-color: {DARK_THEME['bg_tertiary']};
            color: {DARK_THEME['text_primary']};
            border: 2px solid {DARK_THEME['border']};
            border-radius: 5px;
            padding: 8px;
        }}
        QSlider::groove:horizontal {{
            border: 1px solid {DARK_THEME['border']};
            height: 6px;
            background: {DARK_THEME['bg_tertiary']};
            border-radius: 3px;
        }}
        QSlider::handle:horizontal {{
            background: {DARK_THEME['accent_blue']};
            border: 1px solid {DARK_THEME['accent_blue']};
            width: 18px;
            border-radius: 9px;
        }}
        """
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # Onglets
        tabs = QTabWidget()
        
        # Onglet Général
        general_tab = QWidget()
        general_layout = QFormLayout(general_tab)
        
        self.pet_name_input = QLineEdit()
        self.pet_name_input.setText(self.config.get("pet_name", "Minou"))
        general_layout.addRow("Nom de l'animal:", self.pet_name_input)
        
        self.user_name_input = QLineEdit()
        self.user_name_input.setText(self.config.get("user_name", "Mon ami"))
        general_layout.addRow("Votre nom:", self.user_name_input)
        
        self.pet_type_combo = QComboBox()
        self.pet_type_combo.addItems(["cat", "dog"])
        self.pet_type_combo.setCurrentText(self.config.get("pet_type", "cat"))
        general_layout.addRow("Type d'animal:", self.pet_type_combo)
        
        self.speed_slider = QSlider(Qt.Horizontal)
        self.speed_slider.setRange(1, 10)
        self.speed_slider.setValue(self.config.get("movement_speed", 3))
        general_layout.addRow("Vitesse de mouvement:", self.speed_slider)
        
        self.sound_checkbox = QCheckBox()
        self.sound_checkbox.setChecked(self.config.get("sound_enabled", True))
        general_layout.addRow("Sons activés:", self.sound_checkbox)
        
        tabs.addTab(general_tab, "Général")
        
        # Onglet IA
        ai_tab = QWidget()
        ai_layout = QFormLayout(ai_tab)
        
        self.ai_enabled_checkbox = QCheckBox()
        self.ai_enabled_checkbox.setChecked(self.config.get("ai_enabled", False))
        ai_layout.addRow("Activer l'IA:", self.ai_enabled_checkbox)
        
        self.api_key_input = QLineEdit()
        self.api_key_input.setEchoMode(QLineEdit.Password)
        self.api_key_input.setText(self.config.get("gemini_api_key", ""))
        self.api_key_input.setPlaceholderText("Clé API Gemini (optionnel)")
        ai_layout.addRow("Clé API Gemini:", self.api_key_input)
        
        self.personality_combo = QComboBox()
        self.personality_combo.addItems(["playful", "calm", "energetic", "lazy"])
        self.personality_combo.setCurrentText(self.config.get("personality", "playful"))
        ai_layout.addRow("Personnalité:", self.personality_combo)
        
        tabs.addTab(ai_tab, "Intelligence")
        
        # Onglet Notifications
        notif_tab = QWidget()
        notif_layout = QFormLayout(notif_tab)
        
        self.love_messages_checkbox = QCheckBox()
        self.love_messages_checkbox.setChecked(self.config.get("love_messages_enabled", True))
        notif_layout.addRow("Messages d'affection:", self.love_messages_checkbox)
        
        self.quotes_checkbox = QCheckBox()
        self.quotes_checkbox.setChecked(self.config.get("quotes_enabled", True))
        notif_layout.addRow("Citations motivantes:", self.quotes_checkbox)
        
        self.research_checkbox = QCheckBox()
        self.research_checkbox.setChecked(self.config.get("research_suggestions_enabled", True))
        notif_layout.addRow("Suggestions de recherche:", self.research_checkbox)
        
        self.system_monitoring_checkbox = QCheckBox()
        self.system_monitoring_checkbox.setChecked(self.config.get("system_monitoring", True))
        notif_layout.addRow("Surveillance système:", self.system_monitoring_checkbox)
        
        tabs.addTab(notif_tab, "Notifications")
        
        layout.addWidget(tabs)
        
        # Boutons
        buttons_layout = QHBoxLayout()
        save_btn = QPushButton("Sauvegarder")
        cancel_btn = QPushButton("Annuler")
        
        save_btn.clicked.connect(self.save_settings)
        cancel_btn.clicked.connect(self.reject)
        
        buttons_layout.addWidget(cancel_btn)
        buttons_layout.addWidget(save_btn)
        layout.addLayout(buttons_layout)
        
    def save_settings(self):
        self.config.set("pet_name", self.pet_name_input.text())
        self.config.set("user_name", self.user_name_input.text())
        self.config.set("pet_type", self.pet_type_combo.currentText())
        self.config.set("movement_speed", self.speed_slider.value())
        self.config.set("sound_enabled", self.sound_checkbox.isChecked())
        self.config.set("ai_enabled", self.ai_enabled_checkbox.isChecked())
        self.config.set("gemini_api_key", self.api_key_input.text())
        self.config.set("personality", self.personality_combo.currentText())
        self.config.set("love_messages_enabled", self.love_messages_checkbox.isChecked())
        self.config.set("quotes_enabled", self.quotes_checkbox.isChecked())
        self.config.set("research_suggestions_enabled", self.research_checkbox.isChecked())
        self.config.set("system_monitoring", self.system_monitoring_checkbox.isChecked())
        
        self.accept()

# Instance globale
config_manager = ConfigManager()