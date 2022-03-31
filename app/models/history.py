from datetime import datetime
from app import db
from app.models.utils import ModelMixin


class History(db.Model, ModelMixin):
    id = db.Column(db.Integer, primary_key=True)
    instance = db.Column(db.String(64), nullable=False)
    created_by = db.Column(db.String(64), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    
    def __repr__(self):
        return f"<{self.id}, instance: {self.instance}, created_by: {self.created_by}, created_at: {self.created_at}"
