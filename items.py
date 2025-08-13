"""
Objets interactifs pour Minou - Nourriture et Poop (COMPLET)
"""
import os
import random
from PyQt5.QtWidgets import QLabel, QApplication
from PyQt5.QtGui import QPixmap, QPainter, QColor, QBrush, QPen
from PyQt5.QtCore import Qt, QPoint, pyqtSignal, QTimer, QPropertyAnimation, QEasingCurve, QRectF, QPointF
from config import FOOD_SIZE, POOP_SIZE, DARK_THEME

class FoodItem(QLabel):
    food_removed = pyqtSignal(object)
    
    def __init__(self, image_path="", initial_pos=None):
        super().__init__()
        self.is_valid = False
        self.setup_window()
        self.load_food_sprite(image_path)
        self.position_food(initial_pos)
        
        # Variables pour le drag
        self.dragging = False
        self.offset = QPoint()
        
        # Animation de spawn
        self.spawn_animation = QPropertyAnimation(self, b"windowOpacity")
        self.spawn_animation.setDuration(500)
        self.spawn_animation.setEasingCurve(QEasingCurve.OutBounce)
        
        if self.is_valid:
            self.animate_spawn()
    
    def setup_window(self):
        """Configure la fenêtre de la nourriture"""
        self.setWindowFlags(
            Qt.FramelessWindowHint | 
            Qt.WindowStaysOnTopHint | 
            Qt.BypassWindowManagerHint
        )
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setScaledContents(True)
        self.resize(FOOD_SIZE, FOOD_SIZE)
        self.setToolTip("🍖 Clic et glisse pour déplacer la nourriture !")
    
    def load_food_sprite(self, image_path=""):
        """Charge le sprite de nourriture"""
        if not image_path:
            # Choisir une nourriture aléatoire
            food_dir = os.path.join(os.path.dirname(__file__), 'assets', 'food')
            if os.path.exists(food_dir):
                food_files = [f for f in os.listdir(food_dir) 
                             if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
                if food_files:
                    image_path = os.path.join(food_dir, random.choice(food_files))
        
        if image_path and os.path.exists(image_path):
            original_pixmap = QPixmap(image_path)
            if not original_pixmap.isNull():
                scaled_pixmap = original_pixmap.scaled(
                    FOOD_SIZE, FOOD_SIZE, 
                    Qt.KeepAspectRatio, Qt.SmoothTransformation
                )
                self.setPixmap(scaled_pixmap)
                self.is_valid = True
                return
        
        # Fallback : carré coloré avec effet moderne
        self.create_fallback_food()
        self.is_valid = True
    
    def create_fallback_food(self):
        """Crée une nourriture de fallback avec style moderne"""
        food_emojis = ["🍖", "🍗", "🥩", "🦴", "🐟", "🍤"]
        emoji = random.choice(food_emojis)
        
        self.setText(emoji)
        self.setStyleSheet(f"""
        QLabel {{
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 {DARK_THEME['accent_green']}, 
                stop:1 {DARK_THEME['accent_blue']});
            border-radius: {FOOD_SIZE//2}px;
            border: 3px solid {DARK_THEME['accent_purple']};
            font-size: {FOOD_SIZE//2}px;
            color: white;
            font-weight: bold;
        }}
        QLabel:hover {{
            border: 3px solid {DARK_THEME['accent_blue']};
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 {DARK_THEME['accent_blue']}, 
                stop:1 {DARK_THEME['accent_green']});
        }}
        """)
        self.setAlignment(Qt.AlignCenter)
    
    def position_food(self, initial_pos=None):
        """Positionne la nourriture sur l'écran"""
        if initial_pos:
            self.move(initial_pos)
        else:
            screen_rect = QApplication.desktop().screenGeometry()
            # Éviter les bords pour éviter que la nourriture soit hors écran
            margin = 50
            x = random.randint(margin, screen_rect.width() - FOOD_SIZE - margin)
            y = random.randint(margin, screen_rect.height() - FOOD_SIZE - margin)
            self.move(x, y)
    
    def animate_spawn(self):
        """Animation d'apparition"""
        self.setWindowOpacity(0)
        self.show()
        self.spawn_animation.setStartValue(0)
        self.spawn_animation.setEndValue(1)
        self.spawn_animation.start()
    
    def mousePressEvent(self, event):
        """Début du drag de nourriture"""
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.offset = event.pos()
            self.raise_()  # Mettre au premier plan
            
            # Effet visuel de sélection
            current_style = self.styleSheet()
            self.setStyleSheet(current_style + f"""
            QLabel {{
                border: 4px solid {DARK_THEME['accent_blue']};
                box-shadow: 0px 0px 15px {DARK_THEME['accent_blue']};
                transform: scale(1.1);
            }}
            """)
    
    def mouseMoveEvent(self, event):
        """Déplacement de la nourriture"""
        if self.dragging:
            new_pos = self.mapToGlobal(event.pos() - self.offset)
            screen_rect = QApplication.desktop().screenGeometry()
            
            # Limiter aux bords de l'écran
            x = max(0, min(new_pos.x(), screen_rect.width() - self.width()))
            y = max(0, min(new_pos.y(), screen_rect.height() - self.height()))
            self.move(x, y)
    
    def mouseReleaseEvent(self, event):
        """Fin du drag"""
        if event.button() == Qt.LeftButton:
            self.dragging = False
            
            # Retirer l'effet visuel de sélection
            if hasattr(self, 'original_style'):
                self.setStyleSheet(self.original_style)
            else:
                # Recréer le style de base
                self.load_food_sprite()

class PoopItem(QLabel):
    poop_removed = pyqtSignal(object)
    
    def __init__(self, image_path="", initial_pos=None, near_pet=False, pet_pos=None):
        super().__init__()
        self.is_valid = False
        self.setup_window()
        self.load_poop_sprite(image_path)
        self.position_poop(initial_pos, near_pet, pet_pos)
        
        # Timer pour la décomposition automatique
        self.decay_timer = QTimer()
        self.decay_timer.timeout.connect(self.auto_remove)
        self.decay_timer.start(60000)  # Disparaît après 1 minute si pas nettoyé
        
        # Animation de spawn
        self.spawn_animation = QPropertyAnimation(self, b"windowOpacity")
        self.spawn_animation.setDuration(300)
        self.spawn_animation.setEasingCurve(QEasingCurve.OutCubic)
        
        if self.is_valid:
            self.animate_spawn()
    
    def setup_window(self):
        """Configure la fenêtre du poop"""
        self.setWindowFlags(
            Qt.FramelessWindowHint | 
            Qt.WindowStaysOnTopHint | 
            Qt.BypassWindowManagerHint
        )
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setScaledContents(True)
        self.resize(POOP_SIZE, POOP_SIZE)
        self.setCursor(Qt.PointingHandCursor)  # Curseur de clic
        self.setToolTip("💩 Clic pour nettoyer !")
    
    def load_poop_sprite(self, image_path=""):
        """Charge le sprite de poop"""
        if not image_path:
            # Choisir un poop aléatoire
            poop_dir = os.path.join(os.path.dirname(__file__), 'assets', 'poop')
            if os.path.exists(poop_dir):
                poop_files = [f for f in os.listdir(poop_dir)
                             if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
                if poop_files:
                    image_path = os.path.join(poop_dir, random.choice(poop_files))
        
        if image_path and os.path.exists(image_path):
            original_pixmap = QPixmap(image_path)
            if not original_pixmap.isNull():
                scaled_pixmap = original_pixmap.scaled(
                    POOP_SIZE, POOP_SIZE,
                    Qt.KeepAspectRatio, Qt.SmoothTransformation
                )
                self.setPixmap(scaled_pixmap)
                self.is_valid = True
                return
        
        # Fallback : emoji poop
        self.create_fallback_poop()
        self.is_valid = True
    
    def create_fallback_poop(self):
        """Crée un poop de fallback avec style"""
        poop_emojis = ["💩", "💨", "🟤"]
        emoji = random.choice(poop_emojis)
        
        self.setText(emoji)
        self.setStyleSheet(f"""
        QLabel {{
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 #8B4513, stop:1 #A0522D);
            border-radius: {POOP_SIZE//2}px;
            border: 2px solid #654321;
            font-size: {POOP_SIZE//2}px;
            color: #8B4513;
        }}
        QLabel:hover {{
            border: 2px solid {DARK_THEME['error']};
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 #A0522D, stop:1 #CD853F);
        }}
        """)
        self.setAlignment(Qt.AlignCenter)
    
    def position_poop(self, initial_pos=None, near_pet=False, pet_pos=None):
        """Positionne le poop sur l'écran"""
        if initial_pos:
            self.move(initial_pos)
        elif near_pet and pet_pos:
            # Positionner près de l'animal
            offset_x = random.randint(-30, 30)
            offset_y = random.randint(10, 40)  # Plutôt derrière l'animal
            
            x = pet_pos.x() + offset_x
            y = pet_pos.y() + offset_y
            
            # S'assurer qu'on reste dans l'écran
            screen_rect = QApplication.desktop().screenGeometry()
            x = max(0, min(x, screen_rect.width() - POOP_SIZE))
            y = max(0, min(y, screen_rect.height() - POOP_SIZE))
            
            self.move(x, y)
        else:
            # Position aléatoire
            screen_rect = QApplication.desktop().screenGeometry()
            margin = 30
            x = random.randint(margin, screen_rect.width() - POOP_SIZE - margin)
            y = random.randint(margin, screen_rect.height() - POOP_SIZE - margin)
            self.move(x, y)
    
    def animate_spawn(self):
        """Animation d'apparition du poop"""
        self.setWindowOpacity(0)
        self.show()
        self.spawn_animation.setStartValue(0)
        self.spawn_animation.setEndValue(1)
        self.spawn_animation.start()
    
    def mousePressEvent(self, event):
        """Clic pour nettoyer le poop"""
        if event.button() == Qt.LeftButton:
            self.clean_poop()
    
    def clean_poop(self):
        """Nettoie le poop avec animation"""
        # Animation de disparition
        fade_out = QPropertyAnimation(self, b"windowOpacity")
        fade_out.setDuration(300)
        fade_out.setStartValue(1)
        fade_out.setEndValue(0)
        fade_out.finished.connect(lambda: self.poop_removed.emit(self))
        fade_out.start()
        
        # Arrêter le timer de décomposition
        self.decay_timer.stop()
    
    def auto_remove(self):
        """Suppression automatique après expiration"""
        self.decay_timer.stop()
        self.poop_removed.emit(self)
    
    def enterEvent(self, event):
        """Effet visuel au survol"""
        self.setStyleSheet(self.styleSheet() + f"""
        QLabel {{
            border: 3px solid {DARK_THEME['error']};
            transform: scale(1.1);
        }}
        """)
    
    def leaveEvent(self, event):
        """Retirer l'effet de survol"""
        # Recréer le style de base
        self.create_fallback_poop()

class InteractiveItem(QLabel):
    """Classe de base pour des objets interactifs personnalisés"""
    item_clicked = pyqtSignal(object)
    
    def __init__(self, item_type="generic", size=40):
        super().__init__()
        self.item_type = item_type
        self.item_size = size
        self.setup_base()
    
    def setup_base(self):
        """Configuration de base pour tous les objets interactifs"""
        self.setWindowFlags(
            Qt.FramelessWindowHint | 
            Qt.WindowStaysOnTopHint | 
            Qt.BypassWindowManagerHint
        )
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.resize(self.item_size, self.item_size)
        self.setCursor(Qt.PointingHandCursor)
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.item_clicked.emit(self)
    
    def paintEvent(self, event):
        """Dessine l'objet avec des effets personnalisés"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        try:
            # Dessiner selon le type d'objet
            if self.item_type == "heart":
                self.draw_heart(painter)
            elif self.item_type == "star":
                self.draw_star(painter)
            else:
                self.draw_generic(painter)
        except Exception as e:
            print(f"Erreur dans paintEvent: {e}")
        finally:
            # TRÈS IMPORTANT : Toujours fermer le painter
            painter.end()
    
    def draw_heart(self, painter):
        """Dessine un cœur"""
        painter.setBrush(QBrush(QColor(DARK_THEME['error'])))
        painter.setPen(QPen(QColor(DARK_THEME['text_primary']), 2))
        # Code pour dessiner un cœur...
        painter.drawEllipse(5, 5, self.item_size-10, self.item_size-10)
    
    def draw_star(self, painter):
        """Dessine une étoile"""
        painter.setBrush(QBrush(QColor(DARK_THEME['accent_blue'])))
        painter.setPen(QPen(QColor(DARK_THEME['text_primary']), 2))
        # Code pour dessiner une étoile...
        painter.drawEllipse(5, 5, self.item_size-10, self.item_size-10)
    
    def draw_generic(self, painter):
        """Dessine un objet générique"""
        painter.setBrush(QBrush(QColor(DARK_THEME['accent_green'])))
        painter.setPen(QPen(QColor(DARK_THEME['text_primary']), 2))
        painter.drawRoundedRect(5, 5, self.item_size-10, self.item_size-10, 10, 10)

# Classes utilitaires pour les collections d'objets
class ItemManager:
    """Gestionnaire pour tous les objets interactifs"""
    
    def __init__(self):
        self.food_items = []
        self.poop_items = []
        self.special_items = []
    
    def add_food(self, pos=None):
        """Ajoute un élément de nourriture"""
        food = FoodItem(initial_pos=pos)
        if food.is_valid:
            self.food_items.append(food)
            return food
        return None
    
    def add_poop(self, pos=None, near_pet=False, pet_pos=None):
        """Ajoute un poop"""
        poop = PoopItem(initial_pos=pos, near_pet=near_pet, pet_pos=pet_pos)
        if poop.is_valid:
            self.poop_items.append(poop)
            return poop
        return None
    
    def remove_food(self, food_item):
        """Supprime un élément de nourriture"""
        if food_item in self.food_items:
            food_item.hide()
            food_item.deleteLater()
            self.food_items.remove(food_item)
    
    def remove_poop(self, poop_item):
        """Supprime un poop"""
        if poop_item in self.poop_items:
            poop_item.hide()
            poop_item.deleteLater()
            self.poop_items.remove(poop_item)
    
    def clear_all_food(self):
        """Supprime toute la nourriture"""
        for food in list(self.food_items):
            self.remove_food(food)
    
    def clear_all_poop(self):
        """Supprime tous les poops"""
        for poop in list(self.poop_items):
            self.remove_poop(poop)
    
    def clear_all(self):
        """Supprime tous les objets"""
        self.clear_all_food()
        self.clear_all_poop()
        
        for item in list(self.special_items):
            item.hide()
            item.deleteLater()
        self.special_items.clear()
    
    def get_food_count(self):
        """Retourne le nombre de nourritures actives"""
        return len(self.food_items)
    
    def get_poop_count(self):
        """Retourne le nombre de poops actifs"""
        return len(self.poop_items)
    
    def get_closest_food(self, pos):
        """Trouve la nourriture la plus proche d'une position"""
        if not self.food_items:
            return None
        
        closest_food = None
        min_distance = float('inf')
        
        for food in self.food_items:
            if not food.isHidden():
                food_pos = food.pos()
                distance = ((food_pos.x() - pos.x())**2 + (food_pos.y() - pos.y())**2)**0.5
                if distance < min_distance:
                    min_distance = distance
                    closest_food = food
        
        return closest_food

# Instance globale du gestionnaire d'objets
item_manager = ItemManager()