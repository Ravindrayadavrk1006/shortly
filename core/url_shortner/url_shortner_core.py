from ..loggings.logging_config import logger
from ..redis.redis import RedisCore
from ..db_manager.db_manager_core import DatabaseManager
import string
#below variable consits of a-z,A-Z,0-9 , the order has been randomized for making it less predictable
base62_alphabets = "0ghij4aDEFbc123mSTUlnodefkpqrs569tuvwxyzABVWCGHIJKLOPQR78MNXYZ"
class UrlShortnerCore:
    def __init__(
            self,
            db_host,
            db_port,
            db_password,
            db_username,
            redis_host,
            redis_port,
            redis_db_number = 0,
            redis_username = "",
            redis_password = "",
            shortly_base_url = "",
    ):
        self.db_host = db_host
        self.db_port = db_port
        self.db_password = db_password
        self.db_username = db_username

        self.redis_host = redis_host
        self.redis_port = redis_port
        self.redis_username = redis_username
        self.redis_password = redis_password
        self.redis_db_number = redis_db_number
        self.encoded_length = 6
        self.shortly_base_url = shortly_base_url
    
    def initialize(self):
        self.redis_obj  = RedisCore(
                host = self.redis_host,
                port = self.redis_port,
                db_number= self.redis_db_number,
                username= self.redis_username,
                password = self.redis_password
            )
        self.db_manager = DatabaseManager(
                host= self.db_host,
                port = self.db_port,
                username= self.db_username,
                password= self.db_password
            )
    def get_shorten_url(self, long_url):
        try:
            #initialize the objects 
            self.initialize()

            url_counter_uid = self.redis_obj.fetch_unique_id()
            logger.info(f'unique id from redis {url_counter_uid}')
            hash_val = self._generate_62base_hash(url_counter_uid)
            
            all_stored_data = self.get_all_shortened_url()
            logger.info(all_stored_data)

            #insert the value in the table
            self.db_manager.insert_into_table(
                short_hash= hash_val,
                long_url= long_url,
                url_counter= url_counter_uid
            )
            #form a url and return it 
            if not  self.shortly_base_url[-1] == '/':
                self.shortly_base_url += '/'
            return self.shortly_base_url+hash_val
        
        except Exception as e:
            logger.error(f"{e}")
            raise
    
    def get_all_shortened_url(self):
        rows = self.db_manager.get_all_rows()
        return rows
    
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
    

    def get_long_url(self, short_url):
        try:
            self.initialize()
            if(short_url[-1] == '/'):
                short_url = short_url[:-1]
            hash_val = short_url.split('/')[-1]
            if(not isinstance(hash_val, str)):
                raise Exception('hash should be of type string')
            entire_row = self.db_manager.get_long_url(short_hash= hash_val)
            return entire_row[2]
        except Exception as e:
            raise