from flask import Blueprint, request, jsonify
import paypalrestsdk
import os
from src.models.user import db, User
from src.models.subscription import Subscription

paypal_bp = Blueprint('paypal', __name__)

# Configuration PayPal (mode sandbox pour le développement)
paypal_config = {
    "mode": "sandbox",  # "live" pour la production
    "client_id": os.getenv('PAYPAL_CLIENT_ID', 'your-paypal-client-id'),
    "client_secret": os.getenv('PAYPAL_CLIENT_SECRET', 'your-paypal-client-secret')
}

paypalrestsdk.configure(paypal_config)

# Plans d'abonnement PayPal
SUBSCRIPTION_PLANS = {
    'starter': {
        'name': 'Plan Starter',
        'description': 'Histoires illimitées pour une famille',
        'price': '12.00',
        'currency': 'EUR',
        'interval': 'MONTH'
    },
    'family': {
        'name': 'Plan Family',
        'description': 'Plan familial avec fonctionnalités avancées',
        'price': '24.00',
        'currency': 'EUR',
        'interval': 'MONTH'
    }
}

@paypal_bp.route('/create-subscription', methods=['POST'])
def create_subscription():
    """Créer un abonnement PayPal"""
    try:
        data = request.get_json()
        plan_type = data.get('plan_type')
        user_email = data.get('user_email')
        
        if not plan_type or plan_type not in SUBSCRIPTION_PLANS:
            return jsonify({'error': 'Plan d\'abonnement invalide'}), 400
        
        if not user_email:
            return jsonify({'error': 'Email utilisateur requis'}), 400
        
        # Récupérer ou créer l'utilisateur
        user = User.query.filter_by(email=user_email).first()
        if not user:
            user = User(email=user_email, username=user_email.split('@')[0])
            db.session.add(user)
            db.session.commit()
        
        plan_info = SUBSCRIPTION_PLANS[plan_type]
        
        # Créer l'abonnement PayPal
        subscription = paypalrestsdk.Subscription({
            "plan_id": f"P-{plan_type.upper()}-PLAN-ID",  # À remplacer par vos vrais IDs de plan
            "subscriber": {
                "name": {
                    "given_name": user.username or "Utilisateur",
                    "surname": "Histoires Magiques"
                },
                "email_address": user_email
            },
            "application_context": {
                "brand_name": "Histoires Magiques",
                "locale": "fr-FR",
                "shipping_preference": "NO_SHIPPING",
                "user_action": "SUBSCRIBE_NOW",
                "payment_method": {
                    "payer_selected": "PAYPAL",
                    "payee_preferred": "IMMEDIATE_PAYMENT_REQUIRED"
                },
                "return_url": f"{request.host_url}subscription/success",
                "cancel_url": f"{request.host_url}subscription/cancel"
            }
        })
        
        if subscription.create():
            # Sauvegarder l'abonnement en base
            db_subscription = Subscription(
                user_id=user.id,
                paypal_subscription_id=subscription.id,
                plan_type=plan_type,
                status='pending'
            )
            db.session.add(db_subscription)
            db.session.commit()
            
            # Trouver le lien d'approbation
            approval_url = None
            for link in subscription.links:
                if link.rel == "approve":
                    approval_url = link.href
                    break
            
            return jsonify({
                'subscription_id': subscription.id,
                'approval_url': approval_url,
                'status': 'created'
            })
        else:
            return jsonify({'error': 'Erreur lors de la création de l\'abonnement PayPal'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@paypal_bp.route('/execute-subscription', methods=['POST'])
def execute_subscription():
    """Exécuter un abonnement après approbation"""
    try:
        data = request.get_json()
        subscription_id = data.get('subscription_id')
        
        if not subscription_id:
            return jsonify({'error': 'ID d\'abonnement requis'}), 400
        
        # Récupérer l'abonnement PayPal
        subscription = paypalrestsdk.Subscription.find(subscription_id)
        
        if subscription and subscription.status == 'ACTIVE':
            # Mettre à jour l'abonnement en base
            db_subscription = Subscription.query.filter_by(
                paypal_subscription_id=subscription_id
            ).first()
            
            if db_subscription:
                db_subscription.status = 'active'
                
                # Mettre à jour le plan utilisateur
                user = User.query.get(db_subscription.user_id)
                if user:
                    user.subscription_plan = db_subscription.plan_type
                    user.subscription_status = 'active'
                
                db.session.commit()
                
                return jsonify({
                    'status': 'success',
                    'message': 'Abonnement activé avec succès',
                    'subscription': db_subscription.to_dict()
                })
        
        return jsonify({'error': 'Impossible d\'activer l\'abonnement'}), 400
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@paypal_bp.route('/cancel-subscription', methods=['POST'])
def cancel_subscription():
    """Annuler un abonnement"""
    try:
        data = request.get_json()
        user_email = data.get('user_email')
        
        if not user_email:
            return jsonify({'error': 'Email utilisateur requis'}), 400
        
        # Trouver l'utilisateur et son abonnement actif
        user = User.query.filter_by(email=user_email).first()
        if not user:
            return jsonify({'error': 'Utilisateur non trouvé'}), 404
        
        subscription = Subscription.query.filter_by(
            user_id=user.id,
            status='active'
        ).first()
        
        if not subscription:
            return jsonify({'error': 'Aucun abonnement actif trouvé'}), 404
        
        # Annuler l'abonnement PayPal
        paypal_subscription = paypalrestsdk.Subscription.find(subscription.paypal_subscription_id)
        
        cancel_request = {
            "reason": "User requested cancellation"
        }
        
        if paypal_subscription.cancel(cancel_request):
            # Mettre à jour en base
            subscription.status = 'cancelled'
            user.subscription_plan = 'free'
            user.subscription_status = 'cancelled'
            
            db.session.commit()
            
            return jsonify({
                'status': 'success',
                'message': 'Abonnement annulé avec succès'
            })
        else:
            return jsonify({'error': 'Erreur lors de l\'annulation PayPal'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@paypal_bp.route('/subscription-status/<user_email>')
def get_subscription_status(user_email):
    """Récupérer le statut d'abonnement d'un utilisateur"""
    try:
        user = User.query.filter_by(email=user_email).first()
        if not user:
            return jsonify({'error': 'Utilisateur non trouvé'}), 404
        
        subscription = Subscription.query.filter_by(
            user_id=user.id,
            status='active'
        ).first()
        
        return jsonify({
            'user': user.to_dict(),
            'subscription': subscription.to_dict() if subscription else None,
            'can_create_story': user.can_create_story()
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@paypal_bp.route('/webhook', methods=['POST'])
def paypal_webhook():
    """Webhook pour les notifications PayPal"""
    try:
        # Ici vous devriez vérifier la signature du webhook
        # Pour la simplicité, nous traitons directement les données
        
        data = request.get_json()
        event_type = data.get('event_type')
        resource = data.get('resource', {})
        
        if event_type == 'BILLING.SUBSCRIPTION.ACTIVATED':
            subscription_id = resource.get('id')
            
            # Mettre à jour l'abonnement en base
            db_subscription = Subscription.query.filter_by(
                paypal_subscription_id=subscription_id
            ).first()
            
            if db_subscription:
                db_subscription.status = 'active'
                
                user = User.query.get(db_subscription.user_id)
                if user:
                    user.subscription_plan = db_subscription.plan_type
                    user.subscription_status = 'active'
                
                db.session.commit()
        
        elif event_type == 'BILLING.SUBSCRIPTION.CANCELLED':
            subscription_id = resource.get('id')
            
            db_subscription = Subscription.query.filter_by(
                paypal_subscription_id=subscription_id
            ).first()
            
            if db_subscription:
                db_subscription.status = 'cancelled'
                
                user = User.query.get(db_subscription.user_id)
                if user:
                    user.subscription_plan = 'free'
                    user.subscription_status = 'cancelled'
                
                db.session.commit()
        
        return jsonify({'status': 'success'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

