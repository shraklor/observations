import threading


class Event(object):
    def __init__(self):
        self.lock = threading.Lock()
        self.handlers = set()

    def handle(self, handler):
        with self.lock:
            self.handlers.add(handler)
        return self

    def unhandle(self, handler):
        with self.lock:
            try:
                self.handlers.remove(handler)
            except:
                raise ValueError("Handler is not handling this event, so cannot unhandle it.")

        return self

    def fire(self, *args, **kargs):
        with self.lock:
            for handler in self.handlers:
                t = threading.Thread(target=handler, args=args, kwargs=kargs)
                t.daemon = True
                t.start()

    def getHandlerCount(self):
        with self.lock:
            val = len(self.handlers)
        return val

    __iadd__ = handle
    __isub__ = unhandle
    __call__ = fire
    __len__  = getHandlerCount
