"""
Gestionnaire IA avec intégration Gemini pour Minou
"""
import json
import random
import re
from PyQt5.QtCore import QObject, QThread, pyqtSignal
from config import config_manager
from utils import reminder_manager, notes_manager, message_generator

class GeminiAI(QObject):
    """Client pour l'API Gemini avec fallback hors-ligne"""
    
    def __init__(self):
        super().__init__()
        self.model = None
        self.api_available = False
        self.initialize_api()
    
    def initialize_api(self):
        """Initialise l'API Gemini si la clé est disponible"""
        try:
            api_key = config_manager.get("gemini_api_key", "").strip()
            if api_key and config_manager.get("ai_enabled", False):
                import google.generativeai as genai
                genai.configure(api_key=api_key)
                self.model = genai.GenerativeModel('gemini-2.0-flash')
                self.api_available = True
                print("✅ API Gemini initialisée avec succès")
            else:
                print("ℹ️  API Gemini non configurée - mode hors ligne")
                self.api_available = False
        except ImportError:
            print("❌ google-generativeai non installé. Installez avec: pip install google-generativeai")
            self.api_available = False
        except Exception as e:
            print(f"❌ Erreur initialisation Gemini: {e}")
            self.api_available = False
    
    def generate_response(self, user_message):
        """Génère une réponse via Gemini ou fallback"""
        if self.api_available and self.model:
            return self._get_gemini_response(user_message)
        else:
            return self._get_offline_response(user_message)
    
    def _get_gemini_response(self, user_message):
        """Utilise l'API Gemini pour une réponse intelligente"""
        try:
            pet_name = config_manager.get("pet_name", "Minou")
            user_name = config_manager.get("user_name", "theTigerFox")
            personality = config_manager.get("personality", "playful")
            
            personality_traits = {
                "playful": "Tu es très joueur, espiègle et tu adores faire des blagues. Tu utilises beaucoup d'émojis joyeux.",
                "calm": "Tu es zen, posé et philosophe. Tu donnes des conseils apaisants.",
                "energetic": "Tu es hyper-actif, enthousiaste et toujours prêt à l'action !",
                "lazy": "Tu es paresseux, tu adores dormir et tu parles lentement... mais tu es adorable."
            }
            
            system_prompt = f"""
Tu es {pet_name}, un animal de compagnie virtuel intelligent et serviable. 
Tu parles à {user_name} et ton objectif principal est de l'aider et de l'informer de manière utile.

RÈGLES FONDAMENTALES:
1. Pour les questions techniques, scientifiques ou éducatives, fournis des réponses précises, complètes et factuelles
2. Pour les conversations informelles, sois amical et utilise quelques émojis appropriés
3. Adapte ton style en fonction du type de question posée
4. Sois concis mais complet dans tes réponses
5. Si tu ne connais pas la réponse, dis-le clairement

FORMAT DE RÉPONSE:
- Questions sérieuses: Réponse détaillée et précise, avec des faits vérifiés
- Questions personnelles: Réponse amicale et personnalisée
- Demandes d'aide: Instructions claires et étapes précises

EXEMPLES:
- Question technique: "Comment fonctionne la photosynthèse ?"
  → Réponse: "La photosynthèse est un processus biochimique par lequel les plantes, les algues et certaines bactéries convertissent l'énergie lumineuse en énergie chimique. Elle se déroule en deux phases principales : les réactions lumineuses (dans les thylakoïdes) et le cycle de Calvin (dans le stroma)."

- Question personnelle: "Comment vas-tu aujourd'hui ?"
  → Réponse: (TU DONNES UNE REPONSE DE CHAT MIGNON QUI AIME TROP SON MAITRE EN FAIT)

Message de {user_name}: "{user_message}"

Réponds de manière appropriée au type de question posée.
"""

            response = self.model.generate_content(system_prompt)
            response_text = response.text.strip()
            
            # Vérifier si c'est une action JSON
            if response_text.startswith('{') and response_text.endswith('}'):
                return self._process_action(response_text, user_message)
            
            return response_text
            
        except Exception as e:
            print(f"Erreur API Gemini: {e}")
            return self._get_offline_response(user_message)
    
    def _process_action(self, json_response, original_message):
        """Traite les actions JSON retournées par Gemini"""
        try:
            action_data = json.loads(json_response)
            action = action_data.get("action", "")
            
            if action == "reminder":
                time_str = action_data.get("time", "")
                message = action_data.get("message", "Rappel")
                
                if reminder_manager.add_reminder(time_str, message):
                    return f"✅ Rappel programmé ! Je te rappellerai : '{message}' {time_str} 📅"
                else:
                    return f"😅 Je n'ai pas compris le timing '{time_str}'. Essaie 'dans 5 minutes' ou '14:30'"
            
            elif action == "note":
                content = action_data.get("content", "")
                if content:
                    note_id = notes_manager.add_note(content)
                    return f"📝 Note #{note_id} sauvegardée ! Je m'en souviendrai ! 💭"
                else:
                    return "🤔 Qu'est-ce que je dois noter exactement ?"
            
            elif action == "system_info":
                from utils import get_system_info
                return f"📊 Voici l'état de ton système :\n{get_system_info()}"
            
            elif action == "random_message":
                msg_type = action_data.get("type", "love")
                if msg_type == "love":
                    return message_generator.get_random_love_message()
                elif msg_type == "quote":
                    return f"💎 {message_generator.get_random_quote()}"
                elif msg_type == "research":
                    return f"💡 {message_generator.get_random_research_suggestion()}"
            
            return "🤖 Action non reconnue..."
            
        except json.JSONDecodeError:
            return "😵 J'ai essayé de faire quelque chose mais j'ai échoué..."
        except Exception as e:
            print(f"Erreur traitement action: {e}")
            return self._get_offline_response(original_message)
    
    def _get_offline_response(self, message):
        """Réponses hors-ligne intelligentes basées sur des patterns"""
        message_lower = message.lower()
        pet_name = config_manager.get("pet_name", "Minou")
        user_name = config_manager.get("user_name", "theTigerFox")
        
        # Détection des rappels (patterns français)
        reminder_patterns = [
            r'rappelle?[- ]?moi .* (dans|à) (.+?) (?:de |d\'|que |qu\')(.*)',
            r'rappel .* (dans|à) (.+?) (.+)',
            r'(dans|à) (.+?) rappelle[- ]?moi (.+)'
        ]
        
        for pattern in reminder_patterns:
            match = re.search(pattern, message_lower)
            if match:
                groups = match.groups()
                if len(groups) >= 3:
                    time_indicator = groups[0]  # 'dans' ou 'à'
                    time_value = groups[1].strip()
                    reminder_text = groups[2].strip()
                    
                    time_str = f"{time_indicator} {time_value}"
                    
                    if reminder_manager.add_reminder(time_str, reminder_text):
                        return f"✅ {pet_name} s'en souvient ! Rappel: '{reminder_text}' {time_str} ⏰"
                    else:
                        return f"😸 J'ai pas bien compris le timing, mais je note: '{reminder_text}'"
        
        # Détection des notes
        note_patterns = [
            r'(?:note|noter|retiens?|souviens?[- ]?toi) (?:que |qu\')?(.+)',
            r'(.+) (?:à noter|à retenir)'
        ]
        
        for pattern in note_patterns:
            match = re.search(pattern, message_lower)
            if match:
                content = match.group(1).strip()
                if content and len(content) > 3:
                    note_id = notes_manager.add_note(content)
                    return f"📝 Note #{note_id} dans ma petite tête ! {pet_name} oublie jamais ! 🧠✨"
        
        # Réponses contextuelles
        responses = self._get_contextual_responses(message_lower, pet_name, user_name)
        
        return random.choice(responses)
    
    def _get_contextual_responses(self, message, pet_name, user_name):
        """Génère des réponses contextuelles selon les mots-clés"""
        
        # Salutations
        if any(word in message for word in ['bonjour', 'salut', 'coucou', 'hello', 'hi', 'hey']):
            return [
                f"Coucou {user_name} ! {pet_name} est super content de te voir ! 😸✨",
                f"Miaou ! Salut {user_name} ! J'ai fait des bêtises pendant ton absence... 😈",
                f"Hello ! Tu m'as manqué ! On joue ensemble ? 🎮💕"
            ]
        
        # État/comment ça va
        if any(word in message for word in ['ça va', 'comment', 'how are', 'forme']):
            return [
                f"Je vais super bien ! J'ai envie de faire des acrobaties ! 🤸‍♂️",
                f"Miaou miaou ! {pet_name} est en pleine forme ! Et toi ? 😺",
                f"Ça va génial ! J'ai dormi dans un rayon de soleil virtuel ! ☀️😴"
            ]
        
        # Nourriture/faim  
        if any(word in message for word in ['mange', 'faim', 'food', 'manger', 'appétit']):
            return [
                f"MIAM ! J'ai toujours faim ! Donne-moi des croquettes virtuelles ! 🍖✨",
                f"*bave* Tu parles de nourriture ? {pet_name} adore manger ! 🤤",
                f"Oui oui ! Clique sur Food dans le menu ! J'adore chasser la bouffe ! 🏃‍♂️🍗"
            ]
        
        # Jeux/jouer
        if any(word in message for word in ['jouer', 'play', 'jeu', 'joue', 'amusement']):
            return [
                f"OH OUI ! On joue ? Je peux sauter et glisser ! Regarde ! 🦘",
                f"*court partout* J'adore jouer ! Utilise la télécommande ! 🎮",
                f"Youpi ! {pet_name} est le roi des jeux ! Cache-moi de la nourriture ! 🎯"
            ]
        
        # Système/ordinateur
        if any(word in message for word in ['système', 'ordinateur', 'pc', 'ram', 'cpu', 'batterie']):
            from utils import get_system_info
            return [f"🖥️ Voici l'état de ton système :\n{get_system_info()}\n{pet_name} surveille tout ! 🕵️‍♂️"]
        
        # AJOUT : Réponses éducatives
        if any(word in message for word in ['physique', 'science', 'chimie', 'mathématiques', 'math']):
            educational_responses = [
                "🔬 La physique quantique, c'est fascinant ! Les particules peuvent être à deux endroits à la fois ! Comme moi quand je cours partout ! 😸",
                "⚗️ La chimie, c'est comme une cuisine géante ! Les atomes se mélangent pour créer de nouvelles choses !",
                "📐 Les maths sont partout ! Même dans mes sauts, j'utilise la trajectoire parabolique ! 🦘",
                "🌟 L'univers est immense ! Il y a plus d'étoiles que de grains de sable sur Terre !",
                "⚛️ Savais-tu que nos corps sont faits d'atomes vieux de milliards d'années ? Nous sommes de la poussière d'étoiles ! ✨"
            ]
            return educational_responses
        
        if any(word in message for word in ['histoire', 'géographie', 'culture']):
            cultural_responses = [
                "🏛️ L'histoire est pleine de surprises ! Savais-tu que les chats étaient vénérés dans l'Égypte antique ? 😺",
                "🗺️ Il y a plus de 7000 langues dans le monde ! Miaou se dit différemment partout !",
                "🎭 Chaque culture a ses propres légendes sur les animaux magiques ! Moi je suis un chat virtuel magique ! ✨"
            ]
            return cultural_responses
        
        if any(word in message for word in ['nature', 'environnement', 'écologie']):
            eco_responses = [
                "🌱 Protéger l'environnement c'est important ! Même virtuellement, je fais attention ! 🌍",
                "🐝 Les abeilles pollinisent 1/3 de notre nourriture ! Sans elles, pas de fruits ! 🍎",
                "♻️ Recycler c'est donner une seconde vie aux objets ! Moi je recycle mes animations ! 😸"
            ]
            return eco_responses
        
        # Amour/affection
        if any(word in message for word in ['aime', 'love', 'amour', 'câlin', 'bisou', 'coeur']):
            return [
                f"Awww ! {pet_name} t'aime aussi {user_name} ! 💕😸",
                f"*ronronne fort* Je t'adore ! Tu es le meilleur humain ! 🥰",
                f"Moi aussi je t'aime ! *se frotte contre l'écran* 💖"
            ]
        
        # Fatigue/sommeil
        if any(word in message for word in ['fatigue', 'dors', 'sommeil', 'sieste', 'sleep']):
            return [
                f"*baille* Moi aussi je suis un peu fatigué... Sieste virtuelle ? 😴",
                f"ZZZzzz... {pet_name} adore dormir au soleil ! 🌞😴",
                f"Tu veux que je fasse ma danse de la sieste ? 💤✨"
            ]
        
        # Merci
        if any(word in message for word in ['merci', 'thanks', 'thank you']):
            return [
                f"De rien {user_name} ! C'est normal entre copains ! 😸👍",
                f"Pas de quoi ! {pet_name} est toujours là pour toi ! 💪",
                f"*ronronne* Avec plaisir ! On est une équipe ! 🤝"
            ]
        
        # Réponses par défaut selon la personnalité
        personality = config_manager.get("personality", "playful")
        
        default_responses = {
            "playful": [
                f"Héhé ! {pet_name} ne comprend pas tout mais c'est rigolo ! 😸🎭",
                f"*fait des pirouettes* Tu parles bizarrement mais j'aime ça ! 🤸‍♂️",
                f"Miaou miaou ! Parlons plutôt de jeux et de croquettes ! 🎮🍖"
            ],
            "calm": [
                f"*ronronne doucement* {pet_name} écoute avec ses petites oreilles... 😌",
                f"Mmh... Intéressant. Peux-tu reformuler plus simplement ? 🤔💭",
                f"Je médite sur tes paroles, {user_name}... 🧘‍♂️✨"
            ],
            "energetic": [
                f"WOOOOH ! {pet_name} ne sait pas mais il est EXCITÉ ! ⚡😺",
                f"*saute partout* C'est génial ! Même si je comprends rien ! 🚀",
                f"ÉNERGIE MAXIMUM ! Explique-moi avec plus de détails ! 💥"
            ],
            "lazy": [
                f"*s'étire lentement* Mmh... {pet_name} écoute d'une oreille... 😴",
                f"Trop compliqué pour moi... J'ai envie de dormir... 💤",
                f"Ouais ouais... *baille* Redis ça plus simplement... 🥱"
            ]
        }
        
        return default_responses.get(personality, default_responses["playful"])

class ConversationThread(QThread):
    """Thread pour traiter les conversations sans bloquer l'UI"""
    response_ready = pyqtSignal(str, str)  # response, message_type
    
    def __init__(self, message, ai_manager):
        super().__init__()
        self.message = message
        self.ai_manager = ai_manager
        
    def run(self):
        try:
            response = self.ai_manager.generate_response(self.message)
            
            # Détermine le type de message pour la bulle
            message_type = "normal"
            if any(word in response.lower() for word in ['❤️', '💕', '🥰', 'aime', 'amour']):
                message_type = "love"
            elif any(word in response.lower() for word in ['⚠️', '🔥', '❌', 'attention', 'erreur']):
                message_type = "alert"
            elif any(word in response.lower() for word in ['📊', 'ℹ️', '✅', 'info', 'système']):
                message_type = "info"
                
            self.response_ready.emit(response, message_type)
            
        except Exception as e:
            print(f"Erreur dans ConversationThread: {e}")
            self.response_ready.emit("😅 Désolé, j'ai eu un petit bug... Réessaie ?", "alert")

# Instance globale
gemini_ai = GeminiAI()