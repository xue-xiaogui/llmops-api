"""账户数据模型"""
from internal.extension.database_extension import db


class Account(db.Model):
    """账户模型"""

    __tablename__ = "accounts"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
        }
