from utils.Speech import Speech
from utils.SpeechRecognition import SpeechRecognition


# Serves drink to the customer
class ServeTheDrink(object):
    __running = False
    __speech_recognition = None
    __misspelled = 0
    __answer = None
    __drink = None

    def __init__(self, robot):
        self.robot = robot
        self.__speech = Speech(self.robot)
        self.__waiting = True
        self.__vocab = None

    def run(self, drink):
        self.__running = True
        self.__drink = drink
        self.__speech.say("Hi there, did you order the " + self.__drink + "?")
        self.__vocab = ["Yes", "No", "Maybe", "I don't think so"]
        self.__speech_recognition = SpeechRecognition(self.robot, self.__vocab, self.__situation1_callback)
        self.__speech_recognition.wait_for_answer()

        if self.__answer == "Yes":
            self.__speech.say("great! then I have your drink ready. Here you go.")
            self.__vocab = ["Thank you", "Thanks", "Merci"]
            self.__speech_recognition = SpeechRecognition(self.robot, self.__vocab, self.__situation2_callback)
            self.__speech_recognition.wait_for_answer(10)
        else:
            self.__speech.say("oh, my bad. Enjoy your stay")

        # Close it once you're done!
        self.__speech.close_session()
        self.__running = False

    def __situation1_callback(self, value):
        print("word:\"" + value[0] + "\" recognised with accuracy: " + str(value[1]))
        if value[0] == "Yes":
            if value[1] > 0.35:
                self.__speech_recognition.waiting = False
                self.__answer = value[0]

        elif value[0] in ["No", "I don't think so"]:
            if value[1] > 0.35:
                self.__speech_recognition.waiting = False
                self.__answer = value[0]

        elif value[0] == "Maybe":
            if value[1] > 0.35:
                self.__answer = value[0]
                self.__speech.say("don't play tricks with me! Did you order the " + self.__drink + " or not?")
                while self.__speech.blocked():
                    pass
                self.__speech_recognition.waiting = True  # Stay in the loop

    def __situation2_callback(self, value):
        print("word:\"" + value[0] + "\" recognised with accuracy: " + str(value[1]))
        if value[0] in self.__vocab:
            if value[1] > 0.35:
                self.__speech.say("You're welcome!")
                while self.__speech.blocked():
                    pass
                self.__speech_recognition.waiting = False

    def running(self):
        return self.__running
