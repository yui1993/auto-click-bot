import sys
import time
import pyautogui
from base import Base
pyautogui.PAUSE = 0.1

class Miner(Base):
    def init(self):
        self.db = self.brain.brain
        self._make_db()
        self.setTimeout(1, print, "Press ESC to exit")
    
    def _make_db(self):
        if not self.db.get("Miner", return_false=True): # return False if not found
            self.db.set("Miner", {"clicks": []})
            self.brain.save()
    
    def onPress(self):
        
        def exit():
            print("ESC Key Pressed: exiting..")
            self.loop = False
            sys.exit()

        if len(self.pressed) == 1:
            key = self.pressed[0]
            if "_name_" in key.__dict__:
                if key._name_ == "esc":
                    self.setTimeout(1, exit)
        if len(self.pressed) > 1:
            combo = self.pressed[1].char
            if combo == '\x10': # ctrl + P
                self.speech.talk("Logging clicks")
                self.log_clicks = True
            elif combo == '\x08': # ctrl + H
                self.speech.talk("Stopped logging clicks")
                self.log_clicks = False
            elif combo == '\x16': # ctrl + V
                self.speech.talk("Running clicks")
                self.run_clicks = True
            elif combo == '\x19': # ctrl + Y
                self.speech.talk("Stopped running clicks")
                self.run_clicks = False

    
    def onClick(self, x, y, button, pressed):
        if pressed and self.log_clicks:
            self.db.Miner.clicks.append({
                "x": x,
                "y": y,
                "button": str(button),
                "time": time.time()
            })
            self.brain.save()
    

    def onLoop(self):
        if self.run_clicks:
            clicks = self.db.Miner.clicks
            for index, click in enumerate(clicks):
                secs = click['time']
                if len(clicks)  + 1 > index + 1:
                    index = 0
                secs = int(clicks[index + 1]['time'] - click['time'])
                pyautogui.moveTo(click['x'], click['y'], duration=0.5)
                pyautogui.click(click['x'], click['y'], button=click['button'].split(".")[1])
                if secs > 0:
                    time.sleep(secs)

if __name__=="__main__":
    bot = Miner()
    bot.main()