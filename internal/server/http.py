from flask import Flask
from flask_cors import CORS
from internal.router.router import Router
from config import Config   
from internal.exception import CustomException
from pkg.response import Response, json, HTTPCode
from pkg.sqlalchemy import SQLAlchemy
from flask_migrate import Migrate   
from internal.model import App

class Http(Flask):
    def __init__(self, *args, conf: Config, db: SQLAlchemy, migrate: Migrate, router: Router, **kwargs):    
        # 1。初始化Flask应用
        super().__init__(*args, **kwargs)
        
        # 2.初始化应用配置
        self.config.from_object(conf)

        # 3.注册绑定异常错误处理
        self.register_error_handler(Exception, self._register_errors_handler)

        # 4.注册数据库扩展
        db.init_app(self)
        migrate.init_app(self, db, directory="internal/migration")
 
        CORS(self, resources={r"/*": {
            "origins": "*",
            "supports_credentials": True,
            # "methods": ["GET", "OPTIONS", "POST", "PUT", "DELETE"],
            # "allow_headers": ["Content-Type"]
        }})

        # 5.注册应用路由
        router.register_routes(self)
    
    def _register_errors_handler(self, error: Exception):
        # 1.异常信息是不是我们的自定义异常，如果是可以提取message和code等信息
        if isinstance(error, CustomException):
            return json(Response(message=error.message, code=error.code, data=error.data))
        # 2.如果不是我们的自定义异常，则有可能是程序，数据库抛出的异常，也可以提取信息，设置FAIL状态码
        if self.debug or os.getenv("FLASK_ENV") == "development":
            raise error
        else:
            return json(Response(message=str(error), code=HTTPCode.FAIL, data={}))



