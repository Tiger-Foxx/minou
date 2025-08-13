"""
Composants UI pour Minou - Interface moderne et sombre
"""
import random
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QLabel, QLineEdit, QTextEdit, QApplication, 
                             QGraphicsDropShadowEffect, QFrame)
from PyQt5.QtCore import (Qt, QTimer, QPoint, pyqtSignal, QPropertyAnimation, 
                          QEasingCurve, QRect, QThread, pyqtSlot, QRectF, QPointF)
from PyQt5.QtGui import (QFont, QPainter, QPainterPath, QColor, QBrush, 
                         QPen, QLinearGradient)
from config import DARK_THEME, config_manager
from utils import reminder_manager, notes_manager

class ControlBox(QWidget):
    move_left_signal = pyqtSignal()
    move_right_signal = pyqtSignal()
    move_up_signal = pyqtSignal()
    move_down_signal = pyqtSignal()
    stop_movement_signal = pyqtSignal()
    jump_signal = pyqtSignal()
    slide_signal = pyqtSignal()
    closed_signal = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Contrôle de Minou")
        self.setWindowFlags(Qt.Window | Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedSize(200, 220)
        self._init_ui()
        self.setFocusPolicy(Qt.StrongFocus)
        self._active_movement_keys = set()
        
        # Effet d'ombre
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 212, 255, 100))
        shadow.setOffset(0, 0)
        self.setGraphicsEffect(shadow)

    def _init_ui(self):
        # Widget principal avec fond arrondi
        self.main_widget = QFrame(self)
        self.main_widget.setGeometry(0, 0, 200, 220)
        self.main_widget.setStyleSheet(f"""
        QFrame {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {DARK_THEME['bg_secondary']}, 
                stop:1 {DARK_THEME['bg_primary']});
            border: 2px solid {DARK_THEME['accent_blue']};
            border-radius: 15px;
        }}
        """)
        
        layout = QVBoxLayout(self.main_widget)
        layout.setSpacing(8)
        layout.setContentsMargins(15, 15, 15, 15)
        
        # Titre
        title = QLabel("🎮 CONTRÔLES")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet(f"""
        QLabel {{
            color: {DARK_THEME['text_primary']};
            font-weight: bold;
            font-size: 12px;
            background: none;
            border: none;
        }}
        """)
        layout.addWidget(title)
        
        # D-pad
        d_pad_layout = QVBoxLayout()
        d_pad_layout.setSpacing(5)
        
        # Bouton Up
        top_row = QHBoxLayout()
        self.btn_up = self.create_control_button("▲")
        self.btn_up.pressed.connect(self.move_up_signal)
        self.btn_up.released.connect(self.stop_movement_signal)
        top_row.addStretch()
        top_row.addWidget(self.btn_up)
        top_row.addStretch()
        d_pad_layout.addLayout(top_row)
        
        # Ligne du milieu
        mid_row = QHBoxLayout()
        self.btn_left = self.create_control_button("◄")
        self.btn_left.pressed.connect(self.move_left_signal)
        self.btn_left.released.connect(self.stop_movement_signal)
        
        self.btn_stop = self.create_control_button("■", special=True)
        self.btn_stop.clicked.connect(self.stop_movement_signal)
        
        self.btn_right = self.create_control_button("►")
        self.btn_right.pressed.connect(self.move_right_signal)
        self.btn_right.released.connect(self.stop_movement_signal)
        
        mid_row.addWidget(self.btn_left)
        mid_row.addWidget(self.btn_stop)
        mid_row.addWidget(self.btn_right)
        d_pad_layout.addLayout(mid_row)
        
        # Bouton Down
        bottom_row = QHBoxLayout()
        self.btn_down = self.create_control_button("▼")
        self.btn_down.pressed.connect(self.move_down_signal)
        self.btn_down.released.connect(self.stop_movement_signal)
        bottom_row.addStretch()
        bottom_row.addWidget(self.btn_down)
        bottom_row.addStretch()
        d_pad_layout.addLayout(bottom_row)
        
        layout.addLayout(d_pad_layout)
        
        # Actions
        actions_layout = QHBoxLayout()
        self.btn_jump = self.create_action_button("🦘")
        self.btn_jump.clicked.connect(self.jump_signal)
        self.btn_jump.setToolTip("Saut")
        
        self.btn_slide = self.create_action_button("🛷")
        self.btn_slide.clicked.connect(self.slide_signal)
        self.btn_slide.setToolTip("Glissade")
        
        actions_layout.addWidget(self.btn_jump)
        actions_layout.addWidget(self.btn_slide)
        layout.addLayout(actions_layout)

    def create_control_button(self, text, special=False):
        btn = QPushButton(text)
        color = DARK_THEME['accent_purple'] if special else DARK_THEME['accent_blue']
        btn.setStyleSheet(f"""
        QPushButton {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {color}, stop:1 {DARK_THEME['bg_tertiary']});
            color: white;
            border: 2px solid {color};
            border-radius: 8px;
            font-weight: bold;
            font-size: 16px;
            min-width: 40px;
            min-height: 40px;
        }}
        QPushButton:hover {{
            background: {color};
            box-shadow: 0px 0px 10px {color};
        }}
        QPushButton:pressed {{
            background: {DARK_THEME['bg_tertiary']};
        }}
        """)
        return btn

    def create_action_button(self, text):
        btn = QPushButton(text)
        btn.setStyleSheet(f"""
        QPushButton {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {DARK_THEME['accent_green']}, 
                stop:1 {DARK_THEME['bg_tertiary']});
            color: white;
            border: 2px solid {DARK_THEME['accent_green']};
            border-radius: 8px;
            font-size: 20px;
            font-weight: bold;
            min-width: 50px;
            min-height: 35px;
        }}
        QPushButton:hover {{
            background: {DARK_THEME['accent_green']};
            box-shadow: 0px 0px 15px {DARK_THEME['accent_green']};
        }}
        QPushButton:pressed {{
            background: {DARK_THEME['bg_tertiary']};
        }}
        """)
        return btn

    def keyPressEvent(self, event):
        if event.isAutoRepeat():
            return
            
        key = event.key()
        if key in [Qt.Key_A, Qt.Key_Left]:
            self.move_left_signal.emit()
            self._active_movement_keys.add(key)
        elif key in [Qt.Key_D, Qt.Key_Right]:
            self.move_right_signal.emit()
            self._active_movement_keys.add(key)
        elif key in [Qt.Key_W, Qt.Key_Up]:
            self.move_up_signal.emit()
            self._active_movement_keys.add(key)
        elif key in [Qt.Key_S, Qt.Key_Down]:
            self.move_down_signal.emit()
            self._active_movement_keys.add(key)
        elif key == Qt.Key_Space:
            self.jump_signal.emit()
        elif key == Qt.Key_Shift:
            self.slide_signal.emit()

    def keyReleaseEvent(self, event):
        if event.isAutoRepeat():
            return
            
        key = event.key()
        if key in self._active_movement_keys:
            self._active_movement_keys.remove(key)
            if not self._active_movement_keys:
                self.stop_movement_signal.emit()

    def closeEvent(self, event):
        self.closed_signal.emit()
        super().closeEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_start_position = event.pos()

    def mouseMoveEvent(self, event):
        if hasattr(self, 'drag_start_position'):
            self.move(self.pos() + event.pos() - self.drag_start_position)

class SpeechBubble(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.message = ""
        self.bubble_type = "normal"  # normal, love, alert, info
        
        # Timer pour l'auto-disparition
        self.fade_timer = QTimer()
        self.fade_timer.timeout.connect(self.fade_out)
        
        # Animation d'apparition
        self.appear_animation = QPropertyAnimation(self, b"windowOpacity")
        self.appear_animation.setDuration(300)
        self.appear_animation.setEasingCurve(QEasingCurve.OutCubic)
        
    def show_message(self, text, msg_type="normal", duration=3000):
        self.message = text
        self.bubble_type = msg_type
        
        # Calculer la taille nécessaire
        font = QFont("Arial", 11, QFont.Bold)
        metrics = self.fontMetrics()
        text_rect = metrics.boundingRect(0, 0, 300, 100, Qt.TextWordWrap, text)
        
        bubble_width = max(200, text_rect.width() + 40)
        bubble_height = max(60, text_rect.height() + 30)
        self.resize(bubble_width, bubble_height + 20)  # +20 pour la queue
        
        # Animation d'apparition
        self.setWindowOpacity(0)
        self.show()
        self.appear_animation.setStartValue(0)
        self.appear_animation.setEndValue(1)
        self.appear_animation.start()
        
        if duration > 0:
            self.fade_timer.start(duration)
    
    def fade_out(self):
        self.fade_timer.stop()
        self.hide()
    
    def paintEvent(self, event):
        """Dessine la bulle de dialogue"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        try:
            # Couleurs selon le type
            colors = {
                "normal": (DARK_THEME['bg_secondary'], DARK_THEME['text_primary']),
                "love": (DARK_THEME['accent_purple'], "white"),
                "alert": (DARK_THEME['error'], "white"), 
                "info": (DARK_THEME['accent_blue'], "white")
            }
            
            bg_color, text_color = colors.get(self.bubble_type, colors["normal"])
            
            # CORRECTION : Utiliser QRectF au lieu de QRect
            rect = QRectF(10.0, 10.0, float(self.width() - 20), float(self.height() - 30))
            
            # Fond avec gradient
            gradient = QLinearGradient(rect.topLeft(), rect.bottomLeft())
            gradient.setColorAt(0, QColor(bg_color))
            gradient.setColorAt(1, QColor(bg_color).darker(120))
            
            path = QPainterPath()
            path.addRoundedRect(rect, 15.0, 15.0)  # CORRECTION : utiliser des float
            
            # Queue de la bulle (correction des types aussi)
            queue_start = QPointF(rect.center().x() - 15.0, rect.bottom())
            queue_tip = QPointF(rect.center().x(), float(self.height() - 5))
            queue_end = QPointF(rect.center().x() + 15.0, rect.bottom())
            
            path.moveTo(queue_start)
            path.lineTo(queue_tip)
            path.lineTo(queue_end)
            path.closeSubpath()
            
            # Ombre portée
            shadow_path = QPainterPath(path)
            shadow_path.translate(2, 2)
            painter.fillPath(shadow_path, QColor(0, 0, 0, 100))
            
            # Bulle principale
            painter.fillPath(path, QBrush(gradient))
            painter.setPen(QPen(QColor(bg_color).lighter(150), 2))
            painter.drawPath(path)
            
            # Texte
            painter.setPen(QColor(text_color))
            font = QFont("Arial", 11, QFont.Bold)
            painter.setFont(font)
            
            # CORRECTION : Convertir QRectF en QRect pour drawText
            text_rect = rect.toRect().adjusted(10, 10, -10, -10)
            painter.drawText(text_rect, Qt.AlignCenter | Qt.TextWordWrap, self.message)
            
        except Exception as e:
            print(f"Erreur dans paintEvent: {e}")
        finally:
            # TRÈS IMPORTANT : Toujours fermer le painter
            painter.end()

class MinimalChatInterface(QWidget):
    chat_message_sent = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedSize(300, 40)
        
        self.is_expanded = False
        self.auto_hide_timer = QTimer()
        self.auto_hide_timer.timeout.connect(self.collapse)
        self.auto_hide_timer.setSingleShot(True)
        
        self._init_ui()
        self.hide()  # Caché par défaut
        
    def _init_ui(self):
        # Container principal
        self.container = QFrame(self)
        self.container.setGeometry(0, 0, 300, 40)
        
        # Layout principal
        layout = QHBoxLayout(self.container)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)
        
        # Champ de saisie (initialement petit)
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Parle à Minou...")
        self.input_field.setStyleSheet(f"""
        QLineEdit {{
            background-color: {DARK_THEME['bg_secondary']};
            color: {DARK_THEME['text_primary']};
            border: 2px solid {DARK_THEME['accent_blue']};
            border-radius: 18px;
            padding: 8px 15px;
            font-size: 12px;
        }}
        QLineEdit:focus {{
            border-color: {DARK_THEME['accent_purple']};
            background-color: {DARK_THEME['bg_primary']};
        }}
        """)
        
        # Bouton d'envoi
        self.send_btn = QPushButton("💬")
        self.send_btn.setFixedSize(30, 30)
        self.send_btn.setStyleSheet(f"""
        QPushButton {{
            background-color: {DARK_THEME['accent_blue']};
            color: white;
            border: none;
            border-radius: 15px;
            font-size: 14px;
        }}
        QPushButton:hover {{
            background-color: {DARK_THEME['accent_purple']};
        }}
        """)
        
        layout.addWidget(self.input_field)
        layout.addWidget(self.send_btn)
        
        # Connexions
        self.input_field.returnPressed.connect(self.send_message)
        self.send_btn.clicked.connect(self.send_message)
        self.input_field.textChanged.connect(self.on_text_changed)
        
        # Style du container
        self.update_style()
    
    def update_style(self):
        self.container.setStyleSheet(f"""
        QFrame {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {DARK_THEME['bg_secondary']}, 
                stop:1 {DARK_THEME['bg_primary']});
            border: 2px solid {DARK_THEME['accent_blue']};
            border-radius: 20px;
        }}
        """)
        
        # Effet d'ombre
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(0, 212, 255, 80))
        shadow.setOffset(0, 2)
        self.container.setGraphicsEffect(shadow)
    
    def show_chat(self):
        """Affiche l'interface de chat"""
        self.show()
        self.input_field.setFocus()
        
        # Auto-hide après un certain temps si pas d'activité
        delay = config_manager.get("chat_auto_hide_delay", 5000)
        self.auto_hide_timer.start(delay)
    
    def collapse(self):
        """Cache l'interface de chat"""
        if not self.input_field.hasFocus():
            self.hide()
    
    def on_text_changed(self):
        """Appelé quand l'utilisateur tape"""
        self.auto_hide_timer.stop()  # Arrête l'auto-hide pendant la frappe
        
        if self.input_field.text():
            # Redémarrer l'auto-hide
            delay = config_manager.get("chat_auto_hide_delay", 5000)
            self.auto_hide_timer.start(delay)
    
    def send_message(self):
        """Envoie le message"""
        text = self.input_field.text().strip()
        if text:
            self.chat_message_sent.emit(text)
            self.input_field.clear()
            
            # Cache l'interface après envoi
            QTimer.singleShot(500, self.collapse)
    
    def mousePressEvent(self, event):
        """Permet de déplacer la fenêtre"""
        if event.button() == Qt.LeftButton:
            self.drag_start_position = event.pos()
    
    def mouseMoveEvent(self, event):
        if hasattr(self, 'drag_start_position'):
            self.move(self.pos() + event.pos() - self.drag_start_position)

# Classes pour gérer l'IA et les réponses automatiques
class AIResponseThread(QThread):
    response_ready = pyqtSignal(str)
    
    def __init__(self, message, parent=None):
        super().__init__(parent)
        self.message = message
        
    def run(self):
        try:
            # Tentative avec l'API Gemini si configurée
            api_key = config_manager.get("gemini_api_key", "")
            if api_key and config_manager.get("ai_enabled", False):
                response = self.get_ai_response(self.message, api_key)
            else:
                response = self.get_fallback_response(self.message)
                
            self.response_ready.emit(response)
        except Exception as e:
            print(f"Erreur IA: {e}")
            self.response_ready.emit(self.get_fallback_response(self.message))
    
    def get_ai_response(self, message, api_key):
        """Utilise l'API Gemini pour générer une réponse"""
        try:
            import google.generativeai as genai
            
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-2.0-flash')
            
            pet_name = config_manager.get("pet_name", "Minou")
            user_name = config_manager.get("user_name", "mon ami")
            personality = config_manager.get("personality", "playful")
            
            personality_prompts = {
                "playful": "Tu es un animal de compagnie virtuel très joueur et espiègle",
                "calm": "Tu es un animal de compagnie virtuel calme et sage",
                "energetic": "Tu es un animal de compagnie virtuel plein d'énergie et enthousiaste",
                "lazy": "Tu es un animal de compagnie virtuel paresseux mais adorable"
            }
            
            prompt = f"""
            Tu es {pet_name}, {personality_prompts.get(personality, personality_prompts['playful'])}.
            Tu parles à {user_name}. 
            
            Règles importantes:
            - Réponds de façon courte et mignonne (max 2 phrases)
            - Utilise des émojis appropriés
            - Si on te demande un rappel, réponds au format JSON: {{"action": "reminder", "time": "temps", "message": "message"}}
            - Si on te demande de prendre une note, réponds au format JSON: {{"action": "note", "content": "contenu"}}
            - Sinon, réponds normalement en tant qu'animal mignon
            
            Message de {user_name}: {message}
            
            Ta réponse:
            """
            
            response = model.generate_content(prompt)
            return response.text.strip()
            
        except ImportError:
            print("google-generativeai non installé")
            return self.get_fallback_response(message)
        except Exception as e:
            print(f"Erreur API Gemini: {e}")
            return self.get_fallback_response(message)
    
    def get_fallback_response(self, message):
        """Réponses hors-ligne basées sur des mots-clés"""
        message = message.lower()
        pet_name = config_manager.get("pet_name", "Minou")
        
        # Détection de rappels
        if any(word in message for word in ['rappel', 'rappelle', 'reminder', 'dans', 'à']):
            return self.parse_reminder_request(message)
        
        # Détection de notes
        if any(word in message for word in ['note', 'noter', 'retiens', 'souviens']):
            return self.parse_note_request(message)
        
        # Réponses émotionnelles
        if any(word in message for word in ['bonjour', 'salut', 'hello', 'hi']):
            return f"Salut ! Je suis {pet_name} et je suis ravi de te voir ! 😸"
        
        if any(word in message for word in ['ça va', 'comment', 'how are you']):
            return "Je vais super bien ! J'ai envie de jouer ! 🎾"
        
        if any(word in message for word in ['merci', 'thanks']):
            return "De rien ! C'est normal entre amis ! 💕"
        
        if any(word in message for word in ['mange', 'faim', 'food']):
            return "Miam miam ! J'adore manger ! Donne-moi de la nourriture ! 🍖"
        
        if any(word in message for word in ['jouer', 'play', 'jeu']):
            return "Oh oui ! Jouons ensemble ! Je peux sauter et glisser ! 🎮"
        
        # Réponse par défaut
        responses = [
            f"Miaou ! Je ne comprends pas tout mais j'aime qu'on me parle ! 😺",
            f"*ronronne* C'est gentil de discuter avec {pet_name} ! 💭",
            f"Je suis juste un petit animal virtuel, mais j'essaie de comprendre ! 🤔",
            f"*remue la queue* Tu peux me donner à manger ou jouer avec moi ! 🐾"
        ]
        
        return random.choice(responses)
    
    def parse_reminder_request(self, message):
        """Parse une demande de rappel et retourne du JSON"""
        # Exemples: "rappelle moi dans 5 minutes de boire", "rappel à 14:30 réunion"
        
        # Extraction basique du temps et du message
        time_part = ""
        reminder_message = message
        
        if "dans" in message:
            parts = message.split("dans", 1)
            if len(parts) > 1:
                time_info = parts[1].split("de", 1)
                if len(time_info) > 1:
                    time_part = f"dans {time_info[0].strip()}"
                    reminder_message = time_info[1].strip()
        
        elif "à" in message:
            parts = message.split("à", 1)
            if len(parts) > 1:
                time_info = parts[1].split(" ", 1)
                if len(time_info) > 1:
                    time_part = time_info[0].strip()
                    reminder_message = time_info[1].strip()
        
        if not time_part:
            time_part = "dans 10 minutes"
        
        if not reminder_message or reminder_message == message:
            reminder_message = "Rappel programmé"
            
        return f'{{"action": "reminder", "time": "{time_part}", "message": "{reminder_message}"}}'
    
    def parse_note_request(self, message):
        """Parse une demande de note et retourne du JSON"""
        # Retire les mots de commande pour extraire le contenu
        for word in ['note', 'noter', 'retiens', 'souviens']:
            message = message.replace(word, '', 1).strip()
        
        if message:
            return f'{{"action": "note", "content": "{message}"}}'
        
        return "Je n'ai pas compris quoi noter... 🤔"