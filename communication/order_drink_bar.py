from utils.Speech import Speech
from utils.SpeechRecognition import SpeechRecognition


# Orders desired drink at the bar
class OrderDrinkBar(object):
    __running = False
    __speech_recognition = None
    __misspelled = 0
    __drink = None

    def __init__(self, robot):
        self.robot = robot
        self.__speech = Speech(self.robot)
        self.__waiting = True
        self.__vocab = None

    def run(self, drink):
        self.__running = True
        self.__drink = drink
        self.__speech.say("Hey Barkeeper!")
        self.__speech.say("A customer ordered a drink.")
        self.__vocab = ["what does he want", "what drink", "what"]
        self.__speech_recognition = SpeechRecognition(self.robot, self.__vocab, self.__situation1_callback)
        self.__speech_recognition.wait_for_answer()
        self.__speech.say("He asked for a" + self.__drink)

        self.__vocab = ["here", "here you go", "there you go"]
        self.__speech_recognition = SpeechRecognition(self.robot, self.__vocab, self.__situation2_callback)
        self.__speech_recognition.wait_for_answer()
        self.__speech.say("Perfect! I'm sure He'll love it!")

        # Close it once you're done!
        self.__speech.close_session()
        self.__running = False

    def __situation1_callback(self, value):
        print("word:\"" + value[0] + "\" recognised with accuracy: " + str(value[1]))
        if value[0] in self.__vocab:
            if value[1] > 0.35:
                self.__speech_recognition.waiting = False
            else:
                self.__speech.not_understood(self.__misspelled)
                self.__misspelled += 1

    def __situation2_callback(self, value):
        print("word:\"" + value[0] + "\" recognised with accuracy: " + str(value[1]))
        if value[0] in self.__vocab:
            if value[1] > 0.35:
                self.__speech_recognition.waiting = False
            else:
                self.__speech.not_understood(self.__misspelled)
                self.__misspelled += 1

    def running(self):
        return self.__running
