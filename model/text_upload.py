# model/text_upload.py
from __init__ import db
from datetime import datetime

class TextUpload(db.Model):
    __tablename__ = 'text_uploads'

    id = db.Column(db.Integer, primary_key=True)
    text_content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    @classmethod
    def create(cls, text_content):
        try:
            text_upload = cls(text_content=text_content)
            db.session.add(text_upload)
            db.session.commit()
            return text_upload
        except Exception as e:
            print(f"Error creating text upload: {e}")
            db.session.rollback()
            return None
