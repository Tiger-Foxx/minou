#!/usr/bin/env python3
"""
Minou - Desktop Pet Companion
Application d'animal de compagnie virtuel intelligent avec IA

Auteur: theTigerFox
Version: 2.0
"""

import sys
import os
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QIcon, QFont

# Import des modules de l'application
try:
    from config import config_manager, CAT_WIDTH, CAT_HEIGHT
    from pet import MinouPet
    from utils import reminder_manager, system_monitor, notes_manager
    from ai_manager import gemini_ai
except ImportError as e:
    print(f"❌ Erreur d'import: {e}")
    print("Assurez-vous que tous les fichiers sont dans le même dossier.")
    sys.exit(1)

def check_dependencies():
    """Vérifie les dépendances Python requises"""
    missing_deps = []
    
    try:
        import PyQt5
    except ImportError:
        missing_deps.append("PyQt5")
    
    try:
        import psutil
    except ImportError:
        missing_deps.append("psutil")
    
    # Google Generative AI est optionnel
    try:
        import google.generativeai
        print("✅ Google Generative AI disponible")
    except ImportError:
        print("⚠️ Google Generative AI non installé - Mode hors-ligne seulement")
        print("   Installez avec: pip install google-generativeai")
    
    if missing_deps:
        print(f"❌ Dépendances manquantes: {', '.join(missing_deps)}")
        print("Installez avec:")
        for dep in missing_deps:
            if dep == "PyQt5":
                print("   pip install PyQt5")
            elif dep == "psutil":
                print("   pip install psutil")
        return False
    
    return True

def check_assets():
    """Vérifie que les assets nécessaires sont présents"""
    base_dir = os.path.dirname(__file__)
    
    # Dossiers requis
    required_dirs = [
        os.path.join(base_dir, 'assets', 'cat'),
        os.path.join(base_dir, 'assets', 'dog')
    ]
    
    # Dossiers optionnels mais recommandés
    optional_dirs = [
        os.path.join(base_dir, 'assets', 'food'),
        os.path.join(base_dir, 'assets', 'poop')
    ]
    
    missing_required = []
    missing_optional = []
    
    for dir_path in required_dirs:
        if not os.path.exists(dir_path) or not os.path.isdir(dir_path):
            missing_required.append(dir_path)
    
    for dir_path in optional_dirs:
        if not os.path.exists(dir_path) or not os.path.isdir(dir_path):
            missing_optional.append(dir_path)
    
    if missing_required:
        print("❌ Dossiers d'assets requis manquants:")
        for path in missing_required:
            print(f"   {path}")
        return False
    
    if missing_optional:
        print("⚠️ Dossiers d'assets optionnels manquants:")
        for path in missing_optional:
            print(f"   {path}")
        print("   Certaines fonctionnalités seront limitées.")
    
    print("✅ Assets vérifiés")
    return True

def setup_application():
    """Configure l'application PyQt5"""
    # Attributs haute résolution
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    
    # Création de l'application
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)  # Continuer à tourner en arrière-plan
    
    # Configuration de l'application
    pet_name = config_manager.get("pet_name", "Minou")
    app.setApplicationName(f"{pet_name} Desktop Pet")
    app.setApplicationVersion("2.0")
    app.setOrganizationName("theTigerFox")
    app.setOrganizationDomain("github.com/Tiger-Foxx/minou")
    
    # Icône de l'application (si disponible)
    icon_path = os.path.join(os.path.dirname(__file__), 'assets', 'icon.png')
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))
    
    # Police par défaut
    font = QFont("Segoe UI", 9)
    app.setFont(font)
    
    return app

def show_welcome_message(pet):
    """Affiche un message de bienvenue"""
    pet_name = config_manager.get("pet_name", "Minou")
    user_name = config_manager.get("user_name", "theTigerFox")
    
    # Vérifier si c'est le premier lancement
    first_launch = config_manager.get("first_launch", True)
    
    if first_launch:
        welcome_msg = f"""
🎉 Bienvenue dans {pet_name} v2.0 !

Salut {user_name} ! Je suis {pet_name}, ton nouvel animal de compagnie virtuel intelligent.

✨ Nouveautés de cette version :
• 🤖 Intelligence artificielle avec Gemini
• 💬 Chat interactif (clic droit sur moi)
• ⏰ Système de rappels intelligent
• 📊 Surveillance système
• 🎨 Interface moderne et sombre
• 📝 Prise de notes

🎮 Comment interagir :
• Clic gauche : Me toucher/faire mal
• Clic droit : Menu principal
• Double-clic sur l'icône : Chat rapide
• Glisser : Me déplacer

Configure-moi dans les paramètres ! 
Amuse-toi bien ! 😸
        """
        
        pet.show_bubble(welcome_msg, "info", 10000)
        config_manager.set("first_launch", False)
    else:
        pet.show_bubble(f"Re-coucou {user_name} ! {pet_name} est de retour ! 😸", "love", 4000)

def setup_error_handlers():
    """Configure la gestion d'erreur globale"""
    def handle_exception(exc_type, exc_value, exc_traceback):
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return
        
        error_msg = f"Erreur inattendue: {exc_value}"
        print(f"❌ {error_msg}")
        
        # Essayer d'afficher une boîte de dialogue d'erreur
        try:
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Critical)
            msg_box.setWindowTitle("Erreur - Minou")
            msg_box.setText("Une erreur inattendue s'est produite.")
            msg_box.setDetailedText(str(exc_value))
            msg_box.setStandardButtons(QMessageBox.Ok)
            msg_box.exec_()
        except:
            pass  # Si même la boîte de dialogue échoue
    
    sys.excepthook = handle_exception

def create_startup_timer(pet):
    """Crée des tâches de démarrage différées"""
    def delayed_startup():
        # Messages de statut différés
        QTimer.singleShot(2000, lambda: show_welcome_message(pet))
        
        # Vérification de l'IA après 5 secondes
        QTimer.singleShot(5000, lambda: check_ai_status(pet))
        
        # Premier message de système après 10 secondes si activé
        if config_manager.get("system_monitoring", True):
            QTimer.singleShot(10000, lambda: show_system_status(pet))
    
    QTimer.singleShot(1000, delayed_startup)

def check_ai_status(pet):
    """Vérifie le statut de l'IA et informe l'utilisateur"""
    if config_manager.get("ai_enabled", False):
        api_key = config_manager.get("gemini_api_key", "")
        if api_key:
            if gemini_ai.api_available:
                pet.show_bubble("🤖 IA Gemini connectée ! Tu peux me parler ! 💭", "info", 3000)
            else:
                pet.show_bubble("⚠️ Problème avec l'IA - Mode hors-ligne activé", "alert", 4000)
        else:
            pet.show_bubble("💡 Configure une clé API Gemini dans les paramètres pour l'IA !", "info", 4000)

def show_system_status(pet):
    """Affiche le statut système initial"""
    from utils import get_system_info
    try:
        info = get_system_info()
        pet.show_bubble(f"📊 Système OK !\n{info}", "info", 4000)
    except:
        pass  # Erreur silencieuse pour le statut système

def main():
    """Fonction principale"""
    print("🐾 Démarrage de Minou Desktop Pet v2.0...")
    print(f"👤 Utilisateur: {config_manager.get('user_name', 'theTigerFox')}")
    print(f"🐱 Animal: {config_manager.get('pet_name', 'Minou')}")
    
    # Vérifications préliminaires
    if not check_dependencies():
        print("❌ Dépendances manquantes. Installation requise.")
        return 1
    
    if not check_assets():
        print("❌ Assets manquants. Vérifiez le dossier assets/.")
        return 1
    
    # Configuration de l'application
    app = setup_application()
    setup_error_handlers()
    
    try:
        # Création de l'animal de compagnie
        print("🎮 Création de l'animal virtuel...")
        pet = MinouPet()
        
        # Tâches de démarrage
        create_startup_timer(pet)
        
        # Message de démarrage dans la barre système
        pet_name = config_manager.get("pet_name", "Minou")
        if pet.tray_icon.supportsMessages():
            pet.tray_icon.showMessage(
                f"{pet_name} est prêt !",
                f"Ton animal de compagnie virtuel intelligent est maintenant actif. "
                f"Clic droit pour accéder au menu principal.",
                pet.tray_icon.Information,
                4000
            )
        
        print(f"✅ {pet_name} est maintenant actif !")
        print("💡 Clic droit sur l'animal ou l'icône système pour accéder aux options")
        print("💬 Double-clic sur l'icône système pour ouvrir le chat")
        print("⚙️ Utilisez le menu système pour configurer l'IA et les paramètres")
        
        # Lancement de la boucle principale
        return app.exec_()
        
    except KeyboardInterrupt:
        print("\n👋 Arrêt demandé par l'utilisateur")
        return 0
    except Exception as e:
        print(f"❌ Erreur fatale: {e}")
        return 1
    finally:
        # Nettoyage
        try:
            config_manager.save_settings()
            print("💾 Configuration sauvegardée")
        except:
            pass

if __name__ == "__main__":
    sys.exit(main())