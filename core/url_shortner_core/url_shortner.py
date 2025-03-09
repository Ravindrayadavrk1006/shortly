from ..loggings.logging_config import logger
from ..redis.redis import RedisCore
import string
#below variable consits of a-z,A-Z,0-9 , the order has been randomized for making it less predictable
base62_alphabets = "0ghij4aDEFbc123mSTUlnodefkpqrs569tuvwxyzABVWCGHIJKLOPQR78MNXYZ"
class UrlShortnerCore:
    def __init__(
            self,
            redis_host,
            redis_port,
            redis_db_number = 0,
            redis_username = "",
            redis_password = "",
            shortly_base_url = ""
    ):
        self.redis_host = redis_host
        self.redis_port = redis_port
        self.redis_username = redis_username
        self.redis_password = redis_password
        self.redis_db_number = redis_db_number
        self.encoded_length = 6
        self.shortly_base_url = shortly_base_url

    def get_shorten_url(self):
        try:

            redis_obj = RedisCore(
                host = self.redis_host,
                port = self.redis_port,
                db_number= self.redis_db_number,
                username= self.redis_username,
                password = self.redis_password
            )
            url_counter_uid = redis_obj.fetch_unique_id()
            logger.info(f'unique id from redis {url_counter_uid}')
            hash_val = self._generate_62base_hash(url_counter_uid)

            #form a url and return it 
            if not  self.shortly_base_url[-1] == '/':
                self.shortly_base_url += '/'
            return self.shortly_base_url+hash_val
        except Exception as e:
            raise
    
    def _generate_62base_hash(self, uid):
        base = 62
        encoded = []
        while(uid>0):
            encoded.append(base62_alphabets[uid%base])
            #divide and store the quotient in the uid
            uid //=base
        while len(encoded) < self.encoded_length:
            #add zero at last, we will reverse finally so it's fine
            encoded.append(base62_alphabets[0])
        return ''.join(reversed(encoded))
    
