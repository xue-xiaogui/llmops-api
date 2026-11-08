import dotenv
from injector import Injector
from internal.server.http import Http
from internal.router.router import Router
from config import Config
from pkg.sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .module import ExtensionsModule

# 加载环境变量
dotenv.load_dotenv()
conf = Config()


injector = Injector([ExtensionsModule])

app = Http(__name__, conf=conf, db=injector.get(SQLAlchemy), migrate=injector.get(Migrate), router=injector.get(Router))    

if __name__ == "__main__":
    app.run(debug=True)
   