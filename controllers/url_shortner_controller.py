from flask_restx import Namespace, Resource, reqparse
from flask import Response

from logging_config import logger

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
        try:
            args = long_url_parser.parse_args()
            long_url =  args.get('long_url')
            if not long_url:
                logger.info('provide a valid url')
                return Response("please provide a valid url", 400)
            logger.info('long-url saved')
            return long_url
        except Exception as e:
            logger.error('error raised', exc_info = True)
            print(e)


    def get(self):
        hash_val = 'ab7D'
        return 'https://shorturl/'+ hash_val