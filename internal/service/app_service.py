import uuid
from injector import inject
from dataclasses import dataclass
from pkg.sqlalchemy import SQLAlchemy
from internal.model import App

    
@inject
@dataclass
class AppService:
    """AI应用服务类"""
    db: SQLAlchemy

    def create_app(self) -> App:
        with self.db.auto_commit():
            # 1.创建模型的实体类
            app = App(name='测试机器人',account_id=str(uuid.uuid4()),icon='',description='这是一个简单的聊天机器人')
            # 2.将实体类添加到数据库会话中
            self.db.session.add(app)
        return app

    def get_app(self, id: uuid.UUID) -> App:
        return self.db.session.query(App).get(id)  

    def update_app(self, id: uuid.UUID) -> App:
        with self.db.auto_commit():
            app = self.get_app(id)
            app.name = "幕课聊天机器人"
        return app
    
    def delete_app(self, id: uuid.UUID) -> App:
        with self.db.auto_commit():
            app = self.get_app(id)
            self.db.session.delete(app)
        return app