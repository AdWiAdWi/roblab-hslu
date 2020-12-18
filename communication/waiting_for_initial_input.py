from utils.Speech import Speech
from utils.SpeechRecognition import SpeechRecognition


# Waiting for initial input of barkeeper at the start
class WaitingForInput(object):
    __running = False
    __speech_recognition = None
    __misspelled = 0

    def __init__(self, robot):
        self.robot = robot
        self.__speech = Speech(self.robot)
        self.__waiting = True
        self.__vocab = None

    def run(self):
        self.__running = True
        print("Initial waiting Situation - Pepper is dreaming....")
        self.__vocab = ["Pepper", "Hey"]
        self.__speech_recognition = SpeechRecognition(self.robot, self.__vocab, self.__situation1_callback)
        self.__speech_recognition.wait_for_answer()
        self.__speech.say("Yes?")

        # Pepper shall do some work!
        self.__vocab = ["Serve", "Customer", "serve customer"]
        self.__speech_recognition = SpeechRecognition(self.robot, self.__vocab, self.__situation2_callback)
        self.__speech_recognition.wait_for_answer()
        self.__speech.say("Ok, I'm on my way")

        # Close it once you're done!
        self.__speech.close_session()
        self.__running = False

    def __situation1_callback(self, value):
        print("word:\"" + value[0] + "\" recognised with accuracy: " + str(value[1]))
        if value[0] in self.__vocab:
            if value[1] > 0.35:
                self.__speech_recognition.waiting = False

    def __situation2_callback(self, value):
        print("word:\"" + value[0] + "\" recognised with accuracy: " + str(value[1]))
        if value[0] in self.__vocab:
            if value[1] > 0.35:
                self.__speech_recognition.waiting = False

            else:
                self.__speech_recognition.pause()
                self.__speech.not_understood(self.__misspelled)
                self.__speech_recognition.unpause()
                self.__misspelled += 1

    def running(self):
        return self.__running
