from dataclasses import dataclass
from injector import inject
"""应用路由注册"""
from flask import Blueprint, Flask

from internal.handler.app_handler import AppHandler

@inject
@dataclass
class Router:
    app_handler: AppHandler
    def register_routes(self, app: Flask):
        # 创建蓝图
        bp = Blueprint("llmops", __name__, url_prefix="")
        # 将url与对应的控制器方法做绑定
        bp.add_url_rule("/ping", view_func=self.app_handler.ping, methods=["GET"])
        bp.add_url_rule("/apps/<uuid:app_id>/chat", view_func=self.app_handler.debug, methods=["POST"])
        bp.add_url_rule("/app", view_func=self.app_handler.create_app, methods=["POST"])
        bp.add_url_rule("/app/<uuid:id>", view_func=self.app_handler.get_app, methods=["GET"])
        bp.add_url_rule("/app/<uuid:id>", view_func=self.app_handler.update_app, methods=["POST"])
        bp.add_url_rule("/app/<uuid:id>/delete", view_func=self.app_handler.delete_app, methods=["POST"])

        # 注册蓝图
        app.register_blueprint(bp)  
