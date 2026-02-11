from database.db_init import db
from datetime import datetime, timedelta

class MFACode(db.Model):

    __tablename__ = "mfa_codes"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    code = db.Column(db.String(10), nullable=False)

    expiration = db.Column(db.DateTime, nullable=False)

    def is_expired(self):
        return datetime.utcnow() > self.expiration
