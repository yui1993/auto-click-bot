import time
import uuid

class Time:
    _timers = {"cancel": []}
    def __init__(self, int=None, func=None, *args, **kw):
        self.int = int
        self.func = func
        self.args = args
        self.kwargs = kw
        self.id = uuid.uuid4().hex
        self.mode = None
        self.time = time.time()
    
    def interval(self):
        self.mode = "interval"
        self._add()
    
    def timeout(self):
        self.mode = "timeout"
        self._add()
    
    def cancel(self):
        do = True
        for timer in self._timers['cancel']:
            if timer.id == self.id:
                do = False
        if do:
            self._timers['cancel'].append(self)
    
    def _add(self):
        self._timers[self.id] = self
    
    def _cancel(self, id=None):
        if id in self._timers:
            del self._timers[id]
        else:
            if self.id in self._timers:
                del self._timers[self.id]
    
    def runall(self):
        for id, timer_object in iter(self._timers.items()):
            if id != "cancel":
                now = int((time.time() - timer_object.time))
                if now == timer_object.int:
                    timer_object.func(*timer_object.args, **timer_object.kwargs)
                    if timer_object.mode == "interval":
                        timer_object.time = time.time_ns()
                    else:
                        timer_object.cancel()
                
        for timer in self._timers['cancel']:
            timer._cancel()
        self._timers['cancel'] = []