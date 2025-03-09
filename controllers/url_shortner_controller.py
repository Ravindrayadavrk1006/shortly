from flask_restx import Namespace, Resource, reqparse
from flask import jsonify, make_response
from core.loggings.logging_config import logger
from core.url_shortner_core.url_shortner import UrlShortnerCore
from config import config
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
            logger.info(f"long-url {long_url}")
            if not long_url:
                logger.info('provide a valid url')
                return make_response(jsonify({
                    "error": "Bad Request",
                    "message": "provide valid long-url"
                }),400)
            #main functionality
            redis_config = config.get('redis')
            url_short_obj  = UrlShortnerCore(
                redis_host= redis_config['host'],
                redis_port= redis_config['port'],
                redis_db_number= redis_config['db'],
                redis_username= redis_config['username'],
                redis_password= redis_config["password"],
                shortly_base_url = config.get('application').get('shortly_base_url')
            )
            short_url = url_short_obj.get_shorten_url()
            logger.info(f'generated-short-url {short_url}')
            response = {
                "short_url": short_url,
            }
            return make_response(jsonify(response), 200)
        except Exception as e:
            logger.error('error raised', exc_info = True)
            print(e)


    def get(self):
        hash_val = 'ab7D'
        return 'https://shorturl/'+ hash_val