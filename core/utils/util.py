import time
from ..loggings.logging_config import logger
def timeit(func):
    def inner(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        logger.info(f" time taken to execute {time.time() - start_time}s")
        return result
    return inner