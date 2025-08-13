"""
Utilitaires système, rappels et fonctionnalités avancées pour Minou
"""
import json
import os
import random
import datetime
import psutil
from PyQt5.QtCore import QObject, QTimer, pyqtSignal
from PyQt5.QtWidgets import QSystemTrayIcon
from config import config_manager

class ReminderManager(QObject):
    reminder_triggered = pyqtSignal(str)  # Signal émis quand un rappel doit être affiché
    
    def __init__(self):
        super().__init__()
        self.reminders_file = "minou_reminders.json"
        self.reminders = self.load_reminders()
        
        # CORRECTION: Ne pas démarrer le timer dans __init__
        self.check_timer = None
        
    def start_monitoring(self):
        """Démarre la surveillance des rappels - à appeler depuis le thread principal"""
        if self.check_timer is None:
            self.check_timer = QTimer()
            self.check_timer.timeout.connect(self.check_reminders)
            self.check_timer.start(60000)  # 1 minute
        
    def load_reminders(self):
        try:
            if os.path.exists(self.reminders_file):
                with open(self.reminders_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    # Convertir les chaînes de date en objets datetime
                    for reminder in data:
                        reminder['time'] = datetime.datetime.fromisoformat(reminder['time'])
                    return data
        except Exception as e:
            print(f"Erreur lors du chargement des rappels: {e}")
        return []
    
    def save_reminders(self):
        try:
            # Convertir les objets datetime en chaînes pour JSON
            data = []
            for reminder in self.reminders:
                data.append({
                    'time': reminder['time'].isoformat(),
                    'message': reminder['message'],
                    'recurring': reminder.get('recurring', False)
                })
            with open(self.reminders_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Erreur lors de la sauvegarde des rappels: {e}")
    
    def add_reminder(self, time_str, message, recurring=False):
        """Ajoute un rappel. time_str peut être 'dans 5 minutes', '14:30', etc."""
        try:
            reminder_time = self.parse_time(time_str)
            if reminder_time:
                self.reminders.append({
                    'time': reminder_time,
                    'message': message,
                    'recurring': recurring
                })
                self.save_reminders()
                return True
        except Exception as e:
            print(f"Erreur lors de l'ajout du rappel: {e}")
        return False
    
    def parse_time(self, time_str):
        """Parse différents formats de temps"""
        now = datetime.datetime.now()
        time_str = time_str.lower().strip()
        
        # Format "dans X minutes"
        if "dans" in time_str and "minute" in time_str:
            try:
                minutes = int(''.join(filter(str.isdigit, time_str)))
                return now + datetime.timedelta(minutes=minutes)
            except:
                pass
        
        # Format "dans X heures" 
        if "dans" in time_str and "heure" in time_str:
            try:
                hours = int(''.join(filter(str.isdigit, time_str)))
                return now + datetime.timedelta(hours=hours)
            except:
                pass
        
        # Format HH:MM
        if ":" in time_str:
            try:
                time_part = time_str.split()[0] if " " in time_str else time_str
                hour, minute = map(int, time_part.split(":"))
                reminder_time = now.replace(hour=hour, minute=minute, second=0)
                if reminder_time <= now:
                    reminder_time += datetime.timedelta(days=1)
                return reminder_time
            except:
                pass
                
        return None
    
    def check_reminders(self):
        """Vérifie et déclenche les rappels arrivés à échéance"""
        current_time = datetime.datetime.now()
        triggered_reminders = []
        
        for reminder in self.reminders[:]:
            if current_time >= reminder['time']:
                self.reminder_triggered.emit(reminder['message'])
                triggered_reminders.append(reminder)
                
                if not reminder.get('recurring', False):
                    self.reminders.remove(reminder)
        
        if triggered_reminders:
            self.save_reminders()

class SystemMonitor(QObject):
    alert_triggered = pyqtSignal(str, str)  # type, message
    
    def __init__(self):
        super().__init__()
        self.monitor_timer = None
    
    def start_monitoring(self):
        """Démarre la surveillance système - à appeler depuis le thread principal"""
        if config_manager.get("system_monitoring", True) and self.monitor_timer is None:
            self.monitor_timer = QTimer()
            self.monitor_timer.timeout.connect(self.check_system)
            self.monitor_timer.start(30000)  # 30 secondes
        
    def check_system(self):
        if not config_manager.get("system_monitoring", True):
            return
            
        try:
            # Vérification mémoire
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            threshold = config_manager.get("memory_alert_threshold", 90)
            
            if memory_percent > threshold:
                self.alert_triggered.emit(
                    "memory", 
                    f"🔥 Attention ! La mémoire RAM est utilisée à {memory_percent:.1f}%"
                )
            
            # Vérification batterie (si disponible)
            try:
                battery = psutil.sensors_battery()
                if battery:
                    battery_percent = battery.percent
                    battery_threshold = config_manager.get("battery_alert_threshold", 20)
                    
                    if battery_percent < battery_threshold and not battery.power_plugged:
                        self.alert_triggered.emit(
                            "battery",
                            f"🔋 Batterie faible ! Il reste {battery_percent}%"
                        )
            except:
                pass  # Batterie non supportée
                
            # Vérification CPU (si très élevé)
            cpu_percent = psutil.cpu_percent(interval=1)
            if cpu_percent > 95:
                self.alert_triggered.emit(
                    "cpu",
                    f"⚡ Processeur très sollicité : {cpu_percent:.1f}%"
                )
                
        except Exception as e:
            print(f"Erreur monitoring système: {e}")

class MessageGenerator:
    def __init__(self):
        self.love_messages = [
            "Je t'aime beaucoup ! 💕",
            "Tu me manques quand tu n'es pas là... 😢",
            "Tu es la meilleure personne au monde ! ✨",
            "Merci de prendre soin de moi ! 🥰",
            "Tu illumines ma journée ! ☀️",
            "Je suis si heureux de t'avoir ! 😸"
        ]
        
        self.quotes = [
            "\"Le succès, c'est tomber sept fois et se relever huit.\" - Proverbe japonais",
            "\"La seule façon d'atteindre l'impossible est de croire que c'est possible.\" - Alice au Pays des Merveilles",
            "\"Chaque jour est une nouvelle chance de changer votre vie.\"",
            "\"Les rêves ne fonctionnent que si vous travaillez pour eux.\"",
            "\"La motivation vous permet de commencer, l'habitude vous permet de continuer.\"",
            "\"Croyez en vos rêves et ils se réaliseront peut-être. Croyez en vous et ils se réaliseront sûrement.\""
        ]
        
        self.research_suggestions = [
            "Que dirais-tu si on cherchait des recettes faciles et délicieuses ?",
            "J'ai envie d'apprendre quelque chose de nouveau ! On regarde des tutoriels ?",
            "Et si on s'informait sur les dernières actualités technologiques ?",
            "Ça te dit de découvrir de nouveaux endroits à visiter ?",
            "On pourrait chercher des astuces pour améliorer la productivité !",
            "Que penses-tu de regarder des vidéos éducatives intéressantes ?"
        ]
    
    def get_random_love_message(self):
        user_name = config_manager.get("user_name", "mon ami")
        message = random.choice(self.love_messages)
        return f"Hey {user_name} ! {message}"
    
    def get_random_quote(self):
        return random.choice(self.quotes)
    
    def get_random_research_suggestion(self):
        return random.choice(self.research_suggestions)

class NotesManager:
    def __init__(self):
        self.notes_file = "minou_notes.json"
        self.notes = self.load_notes()
        
    def load_notes(self):
        try:
            if os.path.exists(self.notes_file):
                with open(self.notes_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Erreur lors du chargement des notes: {e}")
        return []
    
    def save_notes(self):
        try:
            file_path = os.path.abspath(self.notes_file)
            print(f"🔄 Tentative de sauvegarde des notes dans: {file_path}")
            print(f"Contenu à sauvegarder: {self.notes}")
            
            # Vérifier si le dossier parent existe, sinon le créer
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(self.notes, f, indent=4, ensure_ascii=False)
                
            print("✅ Fichier de notes sauvegardé avec succès")
            
        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            print(f"❌ Erreur lors de la sauvegarde des notes: {e}")
            print(f"Détails de l'erreur: {error_details}")
    
    def add_note(self, content):
        note = {
            'id': len(self.notes) + 1,
            'content': content,
            'timestamp': datetime.datetime.now().isoformat(),
            'tags': self.extract_tags(content)
        }
        self.notes.append(note)
        self.save_notes()
        return note['id']
    
    def extract_tags(self, content):
        """Extrait des tags automatiquement du contenu"""
        words = content.lower().split()
        tags = []
        
        # Tags prédéfinis
        tag_keywords = {
            'travail': ['travail', 'bureau', 'projet', 'réunion', 'deadline'],
            'personnel': ['famille', 'ami', 'personnel', 'maison'],
            'santé': ['médecin', 'santé', 'sport', 'exercice'],
            'shopping': ['acheter', 'shopping', 'magasin', 'commande'],
            'urgent': ['urgent', 'important', 'rapidement', 'vite']
        }
        
        for tag, keywords in tag_keywords.items():
            if any(keyword in words for keyword in keywords):
                tags.append(tag)
                
        return tags
    
    def search_notes(self, query):
        """Recherche dans les notes"""
        query = query.lower()
        results = []
        
        for note in self.notes:
            if (query in note['content'].lower() or 
                any(query in tag for tag in note.get('tags', []))):
                results.append(note)
                
        return results
    
    def get_recent_notes(self, limit=5):
        """Retourne les notes récentes"""
        return sorted(self.notes, key=lambda x: x['timestamp'], reverse=True)[:limit]

def get_system_info():
    """Retourne des informations système formatées"""
    try:
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        
        info = f"💻 Système:\n"
        info += f"• CPU: {cpu_percent:.1f}%\n"
        info += f"• RAM: {memory.percent:.1f}% ({memory.used // (1024**3):.1f}GB/{memory.total // (1024**3):.1f}GB)\n"
        
        try:
            battery = psutil.sensors_battery()
            if battery:
                status = "En charge" if battery.power_plugged else "Sur batterie"
                info += f"• Batterie: {battery.percent}% ({status})\n"
        except:
            pass
            
        return info
    except:
        return "Impossible d'obtenir les informations système"

# Instances globales
reminder_manager = ReminderManager()
system_monitor = SystemMonitor()
message_generator = MessageGenerator()
notes_manager = NotesManager()