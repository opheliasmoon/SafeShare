import random
from datetime import datetime, timedelta
from models.mfa_model import MFACode
from database.db_init import db
from config import Config

def generate_mfa_code(user_id):

    code = str(random.randint(100000, 999999))

    expiration = datetime.utcnow() + timedelta(seconds=Config.MFA_CODE_EXPIRATION)

    mfa = MFACode(
        user_id=user_id,
        code=code,
        expiration=expiration
    )

    db.session.add(mfa)
    db.session.commit()

    return code

