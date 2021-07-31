from gtts import gTTS

class TextToSpeech():
    def __init__(self, lang='en', slow=True):
        self.lang = lang
        self.slow = slow
    
    def talk(self, text):
        return gTTS(text=text, lang=self.lang, slow=self.slow)
