from flask import Blueprint
from flask_restx import Api
from controllers.url_shortner_controller import url_shortner_ns, url_redirect_ns


blueprint = Blueprint('api', __name__)
api = Api(blueprint)
api.add_namespace(url_shortner_ns)
api.add_namespace(url_redirect_ns)