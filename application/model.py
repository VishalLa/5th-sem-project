from .database import db, bcrypt
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'admin'
    user_ID = db.Column(db.String(8), primary_key=True, nullable=False)
    user_name = db.Column(db.String(25), nullable=False)
    email = db.Column(db.String(25), nullable=False, unique=True)
    password_hash = db.Column(db.String(240), nullable=False)

    def get_id(self):
        return str(self.user_ID)

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)
    
    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def create_user(cls, user_id, user_name, email, password):
        user = cls(user_ID=user_id, user_name=user_name, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return user
