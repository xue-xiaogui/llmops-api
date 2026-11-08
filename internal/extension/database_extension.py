"""数据库扩展初始化"""
from pkg.sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# def init_database(app):
#     """初始化数据库扩展"""
#     db.init_app(app)
#     return db 