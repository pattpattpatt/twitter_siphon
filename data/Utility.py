from threading import Thread, Event

def threaded(fn):
    def wrapper(*args, **kwargs):
        thread = Thread(target=fn, args=args, kwargs=kwargs)
        thread.start()
        return thread
    return wrapper
