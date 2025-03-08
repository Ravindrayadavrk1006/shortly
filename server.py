from flask import Flask
from flask_restx import Api, Resource
from blueprints import blueprint

app = Flask(
    __name__
)
app.register_blueprint(blueprint=blueprint)
#using flask-restx for desplaying the swagger page
api = Api(app=app, doc= '/docs')

#basic flask api
# @app.route('/hello', methods =['GET'])
# def hello_world():
#     return "hello"

#using flask restx
@api.route('/hello')
class HelloWorld(Resource):
    def get(self):
        return 'hello', 200

if __name__ == "__main__":
    app.run(
        host = '127.0.0.1' ,
        port = 5000,
        debug= True
    )