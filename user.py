from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Système de crédits gratuits
    free_credits_used = db.Column(db.Integer, default=0)
    free_credits_total = db.Column(db.Integer, default=3)
    
    # Informations d'abonnement
    subscription_plan = db.Column(db.String(50), default='free')  # 'free', 'starter', 'family'
    subscription_status = db.Column(db.String(50), default='active')  # 'active', 'cancelled', 'expired'

    def __repr__(self):
        return f'<User {self.email}>'

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'free_credits_used': self.free_credits_used,
            'free_credits_total': self.free_credits_total,
            'free_credits_remaining': max(0, self.free_credits_total - self.free_credits_used),
            'subscription_plan': self.subscription_plan,
            'subscription_status': self.subscription_status
        }
    
    def has_free_credits(self):
        """Vérifie si l'utilisateur a encore des crédits gratuits"""
        return self.free_credits_used < self.free_credits_total
    
    def use_free_credit(self):
        """Utilise un crédit gratuit"""
        if self.has_free_credits():
            self.free_credits_used += 1
            return True
        return False
    
    def can_create_story(self):
        """Vérifie si l'utilisateur peut créer une histoire"""
        if self.subscription_plan in ['starter', 'family']:
            return True
        return self.has_free_credits()
