import time


# Helper class for speech recognition
class SpeechRecognition(object):
    waiting = False

    def __init__(self, robot, vocabulary, callback):

        memory = robot.session.service("ALMemory")
        self.__subscriber = memory.subscriber("WordRecognized")
        self.__subscriber.signal.connect(callback)
        self.__speech_recognition = robot.session.service("ALSpeechRecognition")
        self.__speech_recognition.setAudioExpression(False)
        self.__speech_recognition.pause(True)  # Need to pause speech recognition to set parameters
        self.__speech_recognition.removeAllContext()
        self.__speech_recognition.setLanguage("English")
        self.__speech_recognition.setVocabulary(vocabulary, False)
        self.__speech_recognition.pause(False)
        self.__speech_recognition.subscribe("SpeechDetection")
        print('Speech recognition engine started')
        # Switching back and forth from Choreograph and direct programming will
        # lead to a blocked vocabulary / grammar!
        # To handle the error, login to peppers Web-Interface and switch language...

    def wait_for_answer(self, seconds=30):
        self.waiting = True
        print("waiting " + str(seconds) + " Seconds")
        start_time = time.time()
        # Loop in order to quickly kill the subscription once there was an answer
        while time.time() < start_time + seconds and self.waiting:
            pass

        if time.time() > start_time + seconds:
            print("Timed kill of subscription")
        else:
            print("Got an Answer -> waiting set to FALSE")

        self.pause()
        self.unsubscribe()

    def unsubscribe(self):
        self.__speech_recognition.unsubscribe("SpeechDetection")
        print('Speech recognition engine stopped')

    def pause(self):
        self.__speech_recognition.pause(True)
        print('Speech recognition paused')

    def unpause(self):
        self.__speech_recognition.pause(False)
        print('Speech recognition continued')
