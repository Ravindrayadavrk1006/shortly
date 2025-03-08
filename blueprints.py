from flask import Blueprint
from flask_restx import Api
from namespaces.url_shortner_namespace import url_shortner_ns


blueprint = Blueprint('api', __name__)
api = Api(blueprint)
api.add_namespace(url_shortner_ns)