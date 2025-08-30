from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from src.models.user import db

class Subscription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    paypal_subscription_id = db.Column(db.String(255), unique=True, nullable=True)
    plan_type = db.Column(db.String(50), nullable=False)  # 'starter', 'family'
    status = db.Column(db.String(50), nullable=False, default='active')  # 'active', 'cancelled', 'expired'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime, nullable=True)
    
    # Relation avec User
    user = db.relationship('User', backref=db.backref('subscriptions', lazy=True))

    def __repr__(self):
        return f'<Subscription {self.id} - {self.plan_type}>'

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'paypal_subscription_id': self.paypal_subscription_id,
            'plan_type': self.plan_type,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'expires_at': self.expires_at.isoformat() if self.expires_at else None
        }

class Story(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    audio_url = db.Column(db.String(500), nullable=True)
    pdf_url = db.Column(db.String(500), nullable=True)
    character_name = db.Column(db.String(100), nullable=True)
    character_type = db.Column(db.String(100), nullable=True)
    theme = db.Column(db.String(100), nullable=True)
    moral = db.Column(db.String(255), nullable=True)
    voice_type = db.Column(db.String(50), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relation avec User
    user = db.relationship('User', backref=db.backref('stories', lazy=True))

    def __repr__(self):
        return f'<Story {self.id} - {self.title}>'

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'title': self.title,
            'content': self.content,
            'audio_url': self.audio_url,
            'pdf_url': self.pdf_url,
            'character_name': self.character_name,
            'character_type': self.character_type,
            'theme': self.theme,
            'moral': self.moral,
            'voice_type': self.voice_type,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

