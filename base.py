from brain import Brain
from Timer import Time
from text2speech import TextToSpeech
import time
import pynput


class Base():
    def __init__(self, brain_file="brain/brain.json"):
        self.brain = Brain(brain_file)
        self.__timer = Time()
        self.brain.load()
        self.click_listener = pynput.mouse.Listener(on_click=self.onClick)
        self.keyboard_listener = pynput.keyboard.Listener(on_press=self.onKeyPressed, on_release=self.onKeyReleased)
        self.pressed = []
        self.loop = False
        self.click_listener.start()
        self.keyboard_listener.start()
        self.log_clicks = False
        self.run_clicks = False
        self.speech = TextToSpeech()
        self.init()
    
    def onPress(self):
        pass

    def onClick(self, x, y, button, pressed):
        pass

    def init(self):
        pass

    def onLoop(self):
        pass

    def onKeyPressed(self, key):
        if key not in self.pressed:
            self.pressed.append(key)
        try:
            self.onPress()
        except Exception as e:
            print(f"onPress Error: {e}")
    
    def onKeyReleased(self, key):
        if key in self.pressed:
            self.pressed.remove(key)
    
    def setTimeout(self, int, func, *args, **kw):
        t = Time(int, func, *args, **kw)
        t.timeout()
        return t
    
    def setInterval(self, int, func, *args, **kw):
        t = Time(int, func, *args, **kw)
        t.interval()
        return t
    
    def main(self):
        self.loop = True
        while self.loop:
            try:
                self.onLoop()
            except Exception as e:
                print("ERROR:", str(e))
            if not self.run_clicks:
                time.sleep(0.1)
            self.__timer.runall()
