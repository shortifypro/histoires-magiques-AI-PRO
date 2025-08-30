from flask import Blueprint, request, jsonify
import openai
import os
from datetime import datetime
from src.models.user import db, User
from src.models.subscription import Story
from fpdf import FPDF
import uuid

stories_bp = Blueprint('stories', __name__)

# Configuration OpenAI (utilise les variables d'environnement déjà configurées)
openai.api_key = os.getenv('OPENAI_API_KEY')
openai.api_base = os.getenv('OPENAI_API_BASE')

# Templates d'histoires par thème
STORY_THEMES = {
    'aventure': {
        'description': 'Une aventure palpitante pleine de découvertes',
        'keywords': ['exploration', 'courage', 'découverte', 'mystère']
    },
    'amitie': {
        'description': 'Une belle histoire sur l\'importance de l\'amitié',
        'keywords': ['amitié', 'entraide', 'partage', 'loyauté']
    },
    'nature': {
        'description': 'Une histoire qui fait découvrir la beauté de la nature',
        'keywords': ['forêt', 'animaux', 'environnement', 'respect']
    },
    'courage': {
        'description': 'Une histoire qui inspire le courage et la bravoure',
        'keywords': ['bravoure', 'peur', 'dépassement', 'confiance']
    },
    'famille': {
        'description': 'Une histoire chaleureuse sur les liens familiaux',
        'keywords': ['famille', 'amour', 'protection', 'tradition']
    },
    'magie': {
        'description': 'Une histoire fantastique pleine de magie',
        'keywords': ['magie', 'sortilège', 'fée', 'enchantement']
    }
}

CHARACTER_TYPES = {
    'animal': ['renard', 'lapin', 'ours', 'chat', 'chien', 'écureuil', 'hibou'],
    'humain': ['enfant', 'princesse', 'prince', 'aventurier', 'magicien'],
    'fantastique': ['fée', 'dragon', 'licorne', 'elfe', 'gnome']
}

@stories_bp.route('/generate', methods=['POST'])
def generate_story():
    """Générer une nouvelle histoire personnalisée"""
    try:
        data = request.get_json()
        
        # Paramètres requis
        user_email = data.get('user_email')
        character_name = data.get('character_name', 'Héros')
        character_type = data.get('character_type', 'enfant')
        theme = data.get('theme', 'aventure')
        moral = data.get('moral', 'Il faut toujours croire en soi')
        age_range = data.get('age_range', '4-8')
        
        if not user_email:
            return jsonify({'error': 'Email utilisateur requis'}), 400
        
        # Vérifier l'utilisateur et ses crédits
        user = User.query.filter_by(email=user_email).first()
        if not user:
            # Créer un nouvel utilisateur
            user = User(email=user_email, username=user_email.split('@')[0])
            db.session.add(user)
            db.session.commit()
        
        # Vérifier si l'utilisateur peut créer une histoire
        if not user.can_create_story():
            return jsonify({
                'error': 'Plus de crédits disponibles',
                'credits_remaining': 0,
                'subscription_required': True
            }), 403
        
        # Générer l'histoire avec OpenAI
        story_content = generate_story_content(
            character_name, character_type, theme, moral, age_range
        )
        
        if not story_content:
            return jsonify({'error': 'Erreur lors de la génération de l\'histoire'}), 500
        
        # Créer le titre automatiquement
        title = f"Les aventures de {character_name}"
        if theme in STORY_THEMES:
            title = f"{character_name} et {STORY_THEMES[theme]['description'].lower()}"
        
        # Sauvegarder l'histoire en base
        story = Story(
            user_id=user.id,
            title=title,
            content=story_content,
            character_name=character_name,
            character_type=character_type,
            theme=theme,
            moral=moral
        )
        db.session.add(story)
        
        # Utiliser un crédit gratuit si nécessaire
        if user.subscription_plan == 'free':
            user.use_free_credit()
        
        db.session.commit()
        
        # Générer le PDF
        pdf_path = generate_pdf_booklet(story)
        if pdf_path:
            story.pdf_url = pdf_path
            db.session.commit()
        
        # Générer automatiquement l'audio avec la voix par défaut
        audio_path = None
        try:
            from src.routes.audio import generate_story_audio, prepare_narration_text, AVAILABLE_VOICES
            
            voice_config = AVAILABLE_VOICES['female_voice']  # Voix par défaut
            narration_text = prepare_narration_text(story)
            audio_path = generate_story_audio(narration_text, voice_config, story.id)
            
            if audio_path:
                story.audio_url = audio_path
                story.voice_type = 'female_voice'
                db.session.commit()
        except Exception as e:
            print(f"Erreur génération audio automatique: {e}")
            # Continue sans audio si erreur
        
        return jsonify({
            'success': True,
            'story': story.to_dict(),
            'credits_remaining': max(0, user.free_credits_total - user.free_credits_used) if user.subscription_plan == 'free' else 'unlimited',
            'pdf_ready': bool(pdf_path),
            'audio_ready': bool(audio_path)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def generate_story_content(character_name, character_type, theme, moral, age_range):
    """Générer le contenu de l'histoire avec OpenAI"""
    try:
        # Construire le prompt personnalisé
        theme_info = STORY_THEMES.get(theme, STORY_THEMES['aventure'])
        
        prompt = f"""
Écris une belle histoire pour enfants de {age_range} ans avec les éléments suivants :

PERSONNAGE PRINCIPAL :
- Nom : {character_name}
- Type : {character_type}

THÈME : {theme_info['description']}
MORALE : {moral}

CONSIGNES :
- Histoire de 300-500 mots, adaptée aux enfants de {age_range} ans
- Langage simple et imagé
- Début captivant, développement avec un petit défi, fin heureuse
- Intégrer naturellement la morale : "{moral}"
- Ton chaleureux et bienveillant
- Descriptions visuelles pour stimuler l'imagination

L'histoire doit être complète, avec un début, un milieu et une fin satisfaisante.
"""

        # Appel à l'API OpenAI
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Tu es un conteur expert spécialisé dans les histoires pour enfants. Tu écris des histoires captivantes, éducatives et adaptées à l'âge des enfants."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=800,
            temperature=0.8
        )
        
        story_content = response.choices[0].message.content.strip()
        return story_content
        
    except Exception as e:
        print(f"Erreur génération OpenAI: {e}")
        # Histoire de fallback en cas d'erreur
        return generate_fallback_story(character_name, character_type, theme, moral)

def generate_fallback_story(character_name, character_type, theme, moral):
    """Histoire de secours en cas d'erreur avec l'API"""
    return f"""
Il était une fois {character_name}, un petit {character_type} très curieux qui vivait dans un joli village.

Un matin, {character_name} décida de partir à l'aventure pour découvrir le monde qui l'entourait. En chemin, il rencontra de nombreux défis, mais grâce à sa détermination et à l'aide de ses nouveaux amis, il réussit à les surmonter.

À la fin de son voyage, {character_name} comprit une chose importante : {moral}.

Depuis ce jour, {character_name} partage cette précieuse leçon avec tous ceux qu'il rencontre, rendant le monde un peu plus beau chaque jour.

Et ils vécurent tous heureux pour toujours !
"""

def generate_pdf_booklet(story):
    """Générer un livret PDF de l'histoire"""
    try:
        # Créer le dossier de stockage s'il n'existe pas
        storage_dir = os.path.join(os.path.dirname(__file__), '..', 'static', 'stories')
        os.makedirs(storage_dir, exist_ok=True)
        
        # Nom de fichier unique
        filename = f"story_{story.id}_{uuid.uuid4().hex[:8]}.pdf"
        filepath = os.path.join(storage_dir, filename)
        
        # Créer le PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font('Arial', 'B', 16)
        
        # Titre
        pdf.cell(0, 10, story.title.encode('latin-1', 'replace').decode('latin-1'), 0, 1, 'C')
        pdf.ln(10)
        
        # Informations sur l'histoire
        pdf.set_font('Arial', 'I', 10)
        pdf.cell(0, 5, f"Personnage: {story.character_name}", 0, 1)
        pdf.cell(0, 5, f"Theme: {story.theme}", 0, 1)
        pdf.ln(5)
        
        # Contenu de l'histoire
        pdf.set_font('Arial', '', 12)
        
        # Diviser le texte en lignes pour le PDF
        lines = story.content.split('\n')
        for line in lines:
            if line.strip():
                # Encoder en latin-1 pour éviter les erreurs d'encodage
                encoded_line = line.encode('latin-1', 'replace').decode('latin-1')
                pdf.multi_cell(0, 6, encoded_line)
                pdf.ln(2)
        
        # Sauvegarder le PDF
        pdf.output(filepath)
        
        # Retourner le chemin relatif pour l'URL
        return f"/static/stories/{filename}"
        
    except Exception as e:
        print(f"Erreur génération PDF: {e}")
        return None

@stories_bp.route('/user-stories/<user_email>')
def get_user_stories(user_email):
    """Récupérer toutes les histoires d'un utilisateur"""
    try:
        user = User.query.filter_by(email=user_email).first()
        if not user:
            return jsonify({'error': 'Utilisateur non trouvé'}), 404
        
        stories = Story.query.filter_by(user_id=user.id).order_by(Story.created_at.desc()).all()
        
        return jsonify({
            'user': user.to_dict(),
            'stories': [story.to_dict() for story in stories],
            'total_stories': len(stories)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@stories_bp.route('/story/<int:story_id>')
def get_story(story_id):
    """Récupérer une histoire spécifique"""
    try:
        story = Story.query.get(story_id)
        if not story:
            return jsonify({'error': 'Histoire non trouvée'}), 404
        
        return jsonify({
            'story': story.to_dict()
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@stories_bp.route('/themes')
def get_themes():
    """Récupérer la liste des thèmes disponibles"""
    return jsonify({
        'themes': STORY_THEMES,
        'character_types': CHARACTER_TYPES
    })

@stories_bp.route('/user-credits/<user_email>')
def get_user_credits(user_email):
    """Récupérer les crédits restants d'un utilisateur"""
    try:
        user = User.query.filter_by(email=user_email).first()
        if not user:
            return jsonify({'error': 'Utilisateur non trouvé'}), 404
        
        return jsonify({
            'user': user.to_dict(),
            'can_create_story': user.can_create_story(),
            'credits_remaining': max(0, user.free_credits_total - user.free_credits_used) if user.subscription_plan == 'free' else 'unlimited'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

