from  redis import Redis
from core.CustomExceptions.custom_exceptions import RedisException
from core.loggings.logging_config import logger


class RedisCore:
    def __init__(self, host, port, username = "", password = "" ):
        self.redis_host = host
        self.redis_port = port
        self.redis_username = username
        self.redis_password = password

    def create_client(self):
        try:
            if(self.redis_username and self.redis_password):
                return Redis(
                    host= self.redis_host,
                    port = self.redis_port,
                    username= self.redis_username,
                    password= self.redis_password,
                    decode_responses= True
                )
            else:
                return Redis(
                    host =self.redis_host,
                    port= self.redis_port,
                    decode_responses= True
                )
        except Exception:
            logger.exception('Redis client creation error', exc_info= True)
            raise RedisException('Exceptions raised in creating redis client')
        
    def fetch_unique_id(self):
        logger.info('Creating redis client')
        redis_client = self.create_client()
        redis_url_uid = redis_client.incr('url_counter')
        logger.info(f'Redis unique id {redis_url_uid}')
        return redis_url_uid