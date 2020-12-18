from utils.Speech import Speech
from utils.SpeechRecognition import SpeechRecognition


# Asks customer what drink he wants
class AskCustomerForDrink(object):
    __running = False
    __ordered_drink = None
    __misspelled = 0
    __answer = None
    __drink = None
    __in_loop = False

    def __init__(self, robot):
        self.robot = robot
        self.__speech = Speech(self.robot)
        self.__waiting = True
        self.__vocab = None

    def run(self):
        self.__running = True
        self.__speech.say("Hi, I'm Pepper. Would you like to drink something?")
        print("Hi, I'm Pepper. Would you like to drink something?")
        self.__vocab = ["Yes", "No", "Later", "Maybe later"]
        self.__speech_recognition = SpeechRecognition(self.robot, self.__vocab, self.__situation1_callback)
        self.__speech_recognition.wait_for_answer()

        # Customer wants to order something
        if self.__answer == "Yes":

            self.__in_loop = True
            self.__ordered_drink = True
            # Loop until decision
            loops = 1
            while self.__in_loop:
                print("----------We are in loop number " + str(loops) + "    Flag:in_loop = " + str(self.__in_loop))
                loops += 1

                if self.__in_loop:  # Doublecheck
                    self.__vocab = ["What", "What do you have", "Recommend", "Recommendation", "Beer", "Whisky",
                                    "Negroni"]
                    self.__speech_recognition = SpeechRecognition(self.robot, self.__vocab, self.__situation2_callback)
                    self.__speech_recognition.wait_for_answer()

                    if self.__answer == "Recommend":
                        self.__answer = None
                        self.__vocab = ["Yes", "No"]
                        self.__speech_recognition = SpeechRecognition(self.robot, self.__vocab,
                                                                      self.__situation_beer_yes_no_callback)
                        self.__speech_recognition.wait_for_answer()
            else:
                self.__ordered_drink = False

        # Close it once you're done!
        self.__speech.close_session()
        self.__running = False
        return self.__drink, self.__ordered_drink

    # SR Callback functions
    def __situation1_callback(self, value):
        print("word:\"" + value[0] + "\" recognised with accuracy: " + str(value[1]))
        if "Yes" in value[0]:
            if value[1] > 0.35:
                self.__answer = value[0]
                self.__speech.say("Great! What can I bring you?")
                while self.__speech.blocked():
                    pass
                self.__speech_recognition.waiting = False

        elif "No" in value[0]:
            if value[1] > 0.35:
                self.__answer = value[0]
                self.__speech.say("Oh, Ok. See you around then")
                while self.__speech.blocked():
                    pass
                self.__speech_recognition.waiting = False

        elif value[0] in ["Later", "Maybe later"]:
            if value[1] > 0.35:
                self.__answer = value[0]
                self.__speech.say_terminator("Alright. I'll be back")
                while self.__speech.blocked():
                    pass
                self.__speech_recognition.waiting = False

    def __situation2_callback(self, value):
        print("word:\"" + value[0] + "\" recognised with accuracy: " + str(value[1]))
        if value[0] in ["What", "What do you have"]:
            if value[1] > 0.35:
                self.__answer = value[0]
                self.__speech.say("Right now, we are a bit short in Stock. \
                But I can offer you either a Beer, a Whisky or a Negroni. - what can I bring you?")
                while self.__speech.blocked():
                    pass
                self.__speech_recognition.waiting = False

        elif value[0] in ["Recommend", "Recommendation"]:
            if value[1] > 0.35:
                self.__answer = "Recommend"
                self.__speech.say("Sure! We are famous for the  A I Beer. Should I bring you one of these?")
                while self.__speech.blocked():
                    pass
                self.__speech_recognition.waiting = False


        elif value[0] in ["Beer", "Whisky", "Negroni"]:
            if value[1] > 0.35:
                self.__in_loop = False  # Jump out of the loop
                self.__drink = value[0]
                self.__speech.say("Perfect! Stay put. I'll bring you a " + value[0] + " a.s.a.p")
                while self.__speech.blocked():
                    pass
                self.__speech_recognition.waiting = False

    def __situation_beer_yes_no_callback(self, value):
        print("word:\"" + value[0] + "\" recognised with accuracy: " + str(value[1]))
        if value[0] == "Yes":
            if value[1] > 0.35:
                self.__in_loop = False  # Jump out of the loop
                self.__drink = "Beer"
                self.__speech.say("Wise choice! You won't regret it")
                while self.__speech.blocked():
                    pass
                self.__speech_recognition.waiting = False

        elif value[0] == "No":
            if value[1] > 0.35:
                self.__speech.say("Ok, what can I bring you instead?")
                while self.__speech.blocked():
                    pass
                self.__speech_recognition.waiting = False

    def running(self):
        return self.__running

    def getdrink(self):
        return self.__drink
