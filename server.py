from flask import Flask
from flask_restx import Api, Resource
from blueprints import blueprint
from core.loggings.logging_config import logger
app = Flask(
    __name__
)
#registering the blueprint
app.register_blueprint(blueprint=blueprint)
#using flask-restx for desplaying the swagger page
api = Api(app=app, doc= '/docs')

if __name__ == "__main__":
    logger.info("starting the flask server")
    app.run(
        host = '127.0.0.1' ,
        port = 5000,
        debug= True
    )