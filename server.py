from flask import Flask
from flask_restx import Api, Resource
from blueprints import blueprint
from config import config
from core.loggings.logging_config import logger
from core.db_manager.db_manager_core import DatabaseManager
app = Flask(
    __name__
)
#registering the blueprint
app.register_blueprint(blueprint=blueprint)
#using flask-restx for desplaying the swagger page
api = Api(app=app, doc= '/docs')
#start the db-pool
db_config = config.get("db", {})
a = DatabaseManager(
    host= db_config['host'],
    port = db_config['port'],
    username= db_config['username'],
    password= db_config['password']
)
if __name__ == "__main__":
    logger.info("starting the flask server")
    app.run(
        host = '127.0.0.1' ,
        port = 5000,
        debug= True
    )