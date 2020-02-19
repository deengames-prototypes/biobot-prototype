import os
from threading import Timer
import time

# Need an object so we get a reference inside our thread when we pass-by-ref
# If this is just a boolean, we pass by value, so updating it does nothing
is_running = {"run": True}


###
# Watch a file. The callback must accept a single argument, which is
# the contents of the file once it's updated. 
###


def watch(filename_to_watch, callback):
    if not os.path.isfile(filename_to_watch):
        raise (Exception("{} doesn't exist in {}".format(filename_to_watch, os.getcwd())))

    w = Watch(filename_to_watch, callback)
    t = Timer(1, w.check_and_notify)  # trigger after 1s
    w.notify(w.get_modified_time())  # trigger immediately
    t.start()


def stop():
    is_running["run"] = False


class Watch:
    def __init__(self, filename, callback):
        self.filename = filename
        self._callback = callback
        self._last_updated = None

    def get_modified_time(self):
        return os.path.getmtime(self.filename)

    def is_updated(self, now):
        return self._last_updated is None or self._last_updated != now

    def notify(self, now):
        self._last_updated = now
        if self._callback is not None:
            with open(self.filename) as f:
                contents = f.read()
            self._callback(contents)
            print("{0} updated".format(self.filename))

    def check_and_notify(self):
        while is_running["run"]:
            now = self.get_modified_time()
            if self.is_updated(now):
                self.notify(now)
            time.sleep(0.5)
