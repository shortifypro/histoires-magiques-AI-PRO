from flask import Blueprint, request, jsonify, send_file
from elevenlabs.client import ElevenLabs
from elevenlabs import save
import os
import uuid
from src.models.user import db, User
from src.models.subscription import Story

audio_bp = Blueprint('audio', __name__)

# Configuration ElevenLabs
ELEVENLABS_API_KEY = os.getenv('ELEVENLABS_API_KEY', 'your-elevenlabs-api-key')
client = ElevenLabs(api_key=ELEVENLABS_API_KEY)

# Voix disponibles (à adapter selon votre compte ElevenLabs)
AVAILABLE_VOICES = {
    'female_voice': {
        'name': 'Rachel',
        'voice_id': 'Rachel',  # ID de la voix dans ElevenLabs
        'description': 'Voix féminine douce et chaleureuse, parfaite pour les histoires'
    },
    'male_voice': {
        'name': 'Adam',
        'voice_id': 'Adam',  # ID de la voix dans ElevenLabs
        'description': 'Voix masculine bienveillante, idéale pour les contes'
    }
}

@audio_bp.route('/generate', methods=['POST'])
def generate_audio():
    """Générer l'audio d'une histoire avec ElevenLabs"""
    try:
        data = request.get_json()
        
        story_id = data.get('story_id')
        voice_type = data.get('voice_type', 'female_voice')
        user_email = data.get('user_email')
        
        if not story_id or not user_email:
            return jsonify({'error': 'ID d\'histoire et email utilisateur requis'}), 400
        
        # Vérifier l'utilisateur
        user = User.query.filter_by(email=user_email).first()
        if not user:
            return jsonify({'error': 'Utilisateur non trouvé'}), 404
        
        # Récupérer l'histoire
        story = Story.query.filter_by(id=story_id, user_id=user.id).first()
        if not story:
            return jsonify({'error': 'Histoire non trouvée'}), 404
        
        # Vérifier si l'audio existe déjà
        if story.audio_url:
            return jsonify({
                'success': True,
                'message': 'Audio déjà généré',
                'audio_url': story.audio_url,
                'story': story.to_dict()
            })
        
        # Vérifier la voix sélectionnée
        if voice_type not in AVAILABLE_VOICES:
            voice_type = 'female_voice'
        
        voice_config = AVAILABLE_VOICES[voice_type]
        
        # Préparer le texte pour la narration
        narration_text = prepare_narration_text(story)
        
        # Générer l'audio avec ElevenLabs
        audio_path = generate_story_audio(narration_text, voice_config, story.id)
        
        if not audio_path:
            return jsonify({'error': 'Erreur lors de la génération audio'}), 500
        
        # Mettre à jour l'histoire avec l'URL audio
        story.audio_url = audio_path
        story.voice_type = voice_type
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Audio généré avec succès',
            'audio_url': audio_path,
            'voice_type': voice_type,
            'story': story.to_dict()
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def prepare_narration_text(story):
    """Préparer le texte pour une narration fluide"""
    # Ajouter des pauses et améliorer la fluidité
    text = story.content
    
    # Remplacer les points par des pauses plus longues
    text = text.replace('.', '... ')
    text = text.replace('!', '! ')
    text = text.replace('?', '? ')
    
    # Ajouter une introduction
    intro = f"Voici l'histoire de {story.character_name}. "
    
    # Ajouter une conclusion
    outro = " Et voilà la fin de cette belle histoire. J'espère qu'elle t'a plu !"
    
    return intro + text + outro

def generate_story_audio(text, voice_config, story_id):
    """Générer l'audio avec ElevenLabs"""
    try:
        # Créer le dossier de stockage s'il n'existe pas
        storage_dir = os.path.join(os.path.dirname(__file__), '..', 'static', 'audio')
        os.makedirs(storage_dir, exist_ok=True)
        
        # Nom de fichier unique
        filename = f"story_audio_{story_id}_{uuid.uuid4().hex[:8]}.mp3"
        filepath = os.path.join(storage_dir, filename)
        
        # Générer l'audio avec ElevenLabs
        audio = client.generate(
            text=text,
            voice=voice_config['voice_id'],
            model="eleven_monolingual_v1"  # Modèle optimisé pour une seule langue
        )
        
        # Sauvegarder le fichier audio
        save(audio, filepath)
        
        # Retourner le chemin relatif pour l'URL
        return f"/static/audio/{filename}"
        
    except Exception as e:
        print(f"Erreur génération audio ElevenLabs: {e}")
        # En cas d'erreur, générer un audio de fallback
        return generate_fallback_audio(text, story_id)

def generate_fallback_audio(text, story_id):
    """Générer un audio de secours en cas d'erreur avec ElevenLabs"""
    try:
        # Utiliser pyttsx3 comme solution de secours (text-to-speech local)
        import pyttsx3
        
        storage_dir = os.path.join(os.path.dirname(__file__), '..', 'static', 'audio')
        os.makedirs(storage_dir, exist_ok=True)
        
        filename = f"story_audio_fallback_{story_id}_{uuid.uuid4().hex[:8]}.wav"
        filepath = os.path.join(storage_dir, filename)
        
        # Initialiser le moteur TTS
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)  # Vitesse de parole
        engine.setProperty('volume', 0.9)  # Volume
        
        # Sauvegarder l'audio
        engine.save_to_file(text, filepath)
        engine.runAndWait()
        
        return f"/static/audio/{filename}"
        
    except Exception as e:
        print(f"Erreur génération audio fallback: {e}")
        return None

@audio_bp.route('/voices')
def get_available_voices():
    """Récupérer la liste des voix disponibles"""
    try:
        # Essayer de récupérer les voix depuis ElevenLabs
        try:
            elevenlabs_voices = client.voices.get_all()
            voice_list = []
            for voice in elevenlabs_voices.voices:
                voice_list.append({
                    'id': voice.voice_id,
                    'name': voice.name,
                    'category': voice.category if hasattr(voice, 'category') else 'general'
                })
        except:
            # En cas d'erreur, utiliser les voix par défaut
            voice_list = [
                {'id': 'female_voice', 'name': 'Voix féminine', 'category': 'default'},
                {'id': 'male_voice', 'name': 'Voix masculine', 'category': 'default'}
            ]
        
        return jsonify({
            'voices': voice_list,
            'default_voices': AVAILABLE_VOICES
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@audio_bp.route('/story-audio/<int:story_id>')
def get_story_audio(story_id):
    """Récupérer le fichier audio d'une histoire"""
    try:
        story = Story.query.get(story_id)
        if not story or not story.audio_url:
            return jsonify({'error': 'Audio non trouvé'}), 404
        
        # Construire le chemin complet du fichier
        audio_path = os.path.join(
            os.path.dirname(__file__), '..', 'static', 
            story.audio_url.replace('/static/', '')
        )
        
        if not os.path.exists(audio_path):
            return jsonify({'error': 'Fichier audio non trouvé'}), 404
        
        return send_file(audio_path, as_attachment=False)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@audio_bp.route('/regenerate-audio', methods=['POST'])
def regenerate_audio():
    """Régénérer l'audio d'une histoire avec une voix différente"""
    try:
        data = request.get_json()
        
        story_id = data.get('story_id')
        voice_type = data.get('voice_type', 'female_voice')
        user_email = data.get('user_email')
        
        if not story_id or not user_email:
            return jsonify({'error': 'ID d\'histoire et email utilisateur requis'}), 400
        
        # Vérifier l'utilisateur et l'histoire
        user = User.query.filter_by(email=user_email).first()
        if not user:
            return jsonify({'error': 'Utilisateur non trouvé'}), 404
        
        story = Story.query.filter_by(id=story_id, user_id=user.id).first()
        if not story:
            return jsonify({'error': 'Histoire non trouvée'}), 404
        
        # Supprimer l'ancien fichier audio s'il existe
        if story.audio_url:
            old_audio_path = os.path.join(
                os.path.dirname(__file__), '..', 'static',
                story.audio_url.replace('/static/', '')
            )
            if os.path.exists(old_audio_path):
                os.remove(old_audio_path)
        
        # Générer le nouvel audio
        voice_config = AVAILABLE_VOICES.get(voice_type, AVAILABLE_VOICES['female_voice'])
        narration_text = prepare_narration_text(story)
        audio_path = generate_story_audio(narration_text, voice_config, story.id)
        
        if not audio_path:
            return jsonify({'error': 'Erreur lors de la régénération audio'}), 500
        
        # Mettre à jour l'histoire
        story.audio_url = audio_path
        story.voice_type = voice_type
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Audio régénéré avec succès',
            'audio_url': audio_path,
            'voice_type': voice_type,
            'story': story.to_dict()
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

