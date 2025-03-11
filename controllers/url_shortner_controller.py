from flask_restx import Namespace, Resource, reqparse
from flask import jsonify, make_response, redirect
from core.loggings.logging_config import logger
from core.url_shortner.url_shortner_core import UrlShortnerCore
from config import config
url_shortner_ns = Namespace('url-shortner/')

long_url_parser = reqparse.RequestParser()
long_url_parser.add_argument(
    'long_url',
    type = str,
    help ="pass the long url ",
    location = 'json'
)
short_url_parser = reqparse.RequestParser()
short_url_parser.add_argument(
    'short_url',
    type = str,
    help ="pass the short url",
    location = "args",
    required = True
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

            db_config = config.get('db')

            url_short_obj  = UrlShortnerCore(
                db_host= db_config['host'],
                db_port= db_config['port'],
                db_username= db_config['username'],
                db_password= db_config['password'],
                redis_host= redis_config['host'],
                redis_port= redis_config['port'],
                redis_db_number= redis_config['db'],
                redis_username= redis_config['username'],
                redis_password= redis_config["password"],
                shortly_base_url = config.get('application').get('shortly_base_url')
            )
            short_url = url_short_obj.get_shorten_url(long_url= long_url)
            logger.info(f'generated-short-url {short_url}')
            response = {
                "short_url": short_url,
            }
            return make_response(jsonify(response), 200)
        except Exception as e:
            logger.error('error raised', exc_info = True)
            print(e)



url_redirect_ns = Namespace('')


@url_redirect_ns.route('/<string:hash_value>')
class UrlRedirect(Resource):
    def get(self, hash_value):
        try:
            if not hash_value:
                return make_response(jsonify({"message": "provide the short-url"}), 400)
            
            redis_config = config.get('redis')
            db_config = config.get('db')
            url_short_obj  = UrlShortnerCore(
                    db_host= db_config['host'],
                    db_port= db_config['port'],
                    db_username= db_config['username'],
                    db_password= db_config['password'],
                    redis_host= redis_config['host'],
                    redis_port= redis_config['port'],
                    redis_db_number= redis_config['db'],
                    redis_username= redis_config['username'],
                    redis_password= redis_config["password"],
                    shortly_base_url = config.get('application').get('shortly_base_url')
                )
            long_url = url_short_obj.get_long_url(short_url=hash_value)
            if not long_url:
                return make_response(jsonify({"error": "short url not found"}, 404))
            return redirect(long_url, code = 302)
        except Exception as e:
            return make_response(jsonify({"error": e.message}),500)