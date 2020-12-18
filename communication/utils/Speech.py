import time


# Helper class for speaking
class Speech:
    is_blocked = False

    def __init__(self, robot):
        self.__al_dialog = robot.session.service("ALDialog")
        self.__al_tts = robot.session.service("ALAnimatedSpeech")
        self.__al_dialog.setLanguage("English")
        self.__speech_recognition = robot.session.service("ALSpeechRecognition")

    def say(self, text_to_say):
        self.is_blocked = True
        # Pepper should not listen to himself
        self.__speech_recognition.pause(True)
        self.__al_tts.say(text_to_say)
        self.__speech_recognition.pause(False)
        time.sleep(0.5)
        self.is_blocked = False

    def say_slowly(self, text_to_say):
        original_speed = self.__al_tts.getParameter("speed")
        self.__al_tts.setParameter("speed", 60)
        self.say(text_to_say)
        self.__al_tts.setParameter("speed", original_speed)

    def say_terminator(self, text_to_say):
        original_pitch = self.__al_tts.getParameter("pitchShift")
        self.__al_tts.setParameter("pitchShift", 0.5)
        self.say_slowly(text_to_say)
        self.__al_tts.setParameter("pitchShift", original_pitch)

    def not_understood(self, count):
        if count == 0:
            self.say("Sorry, I was not able to understand you.")
            time.sleep(0.5)
            self.say("Can you please repeat?")
        else:
            self.say("I still did not get it...")
            time.sleep(0.5)
            self.say("Please give it another Try")
            self.say_slowly("and speak slowly...")

    def close_session(self):
        self.__al_dialog.closeSession()

    def blocked(self):
        return self.is_blocked
