from datetime import datetime
from traceback import format_exc
from decorator import decorator


@decorator
def exception_handler(func, *args, **kwargs):
    try:
        result = func(*args, **kwargs)
        return result
    except Exception as error:
        f = open("{}_{}_error.log".format(func.__name__, datetime.now().strftime('%m_%d_%Y')), "a")
        f.write(format_exc())
        f.close()
