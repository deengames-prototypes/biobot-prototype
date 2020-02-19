import tdl
import time

from tdl.event import get


class ExtensibleApp:
    """
    Copypasta from tdl.event.App but without __slots__ defined.
    This hurt to make.
    """
    def __init__(self):
        self._running = False
        self._prev_time = time.clock()

    def ev_QUIT(self, event):
        raise SystemExit()

    def ev_KEYDOWN(self, event):
        pass

    def ev_KEYUP(self, event):
        pass

    def ev_MOUSEDOWN(self, event):
        pass

    def ev_MOUSEUP(self, event):
        pass

    def ev_MOUSEMOTION(self, event):
        pass

    def update(self, delta_time):
        pass

    def suspend(self):
        self._running = False

    def run(self):
        if getattr(self, '_App__running', False):
            raise tdl.TDLError('An App can not be run multiple times simultaneously')
        self._running = True
        while self._running:
            self.run_once()

    def run_once(self):
        for event in get():
            if event.type:  # exclude custom events with a blank type variable
                # call the ev_* methods
                method = 'ev_%s' % event.type  # ev_TYPE
                getattr(self, method)(event)
            if event.type == 'KEYDOWN':
                if event.key == 'CHAR':
                    continue
                # call the key_* methods
                method = 'key_%s' % (event.text if event.key == 'TEXT' else event.keychar)  # key_KEYNAME
                if hasattr(self, method):  # silently exclude undefined methods
                    getattr(self, method)(event)
        new_time = time.clock()
        self.update(new_time - self._prev_time)
        self._prev_time = new_time
