from flask_restx import Namespace, Resource, reqparse
# from flask import escape
url_shortner_ns = Namespace('url-shortner/')

long_url_parser = reqparse.RequestParser()
long_url_parser.add_argument(
    'long_url',
    type = str,
    help ="pass the long url ",
    location = 'json'
)

@url_shortner_ns.route('')
class UrlShortner(Resource):
    @url_shortner_ns.expect(long_url_parser)
    def post(self):
        args = long_url_parser.parse_args()
        return args.get('long_url')
        #do the stuffs here

    def get(self):
        hash_val = 'ab7D'
        return 'https://shorturl/'+ hash_val