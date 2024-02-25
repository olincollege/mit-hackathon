import speech_recognition as sr

# Initialize the recognizer
r = sr.Recognizer()

# Loop infinitely for user to
# speak
def voice_command():
    while 1:

        # Exception handling to handle
        # exceptions at the runtime
        try:

            # use the microphone as source for input.
            # with sr.Microphone() as source2:

            #     # wait for a second to let the recognizer
            #     # adjust the energy threshold based on
            #     # the surrounding noise level
            #     print("enter while")
            #     r.adjust_for_ambient_noise(source2, duration=1)
            #     print("after adjustment")
            #     # listens for the user's input
            #     audio2 = r.listen(source2, timeout=2)
            #     print("middle")
            #     # Using google to recognize audio
            #     MyText = r.recognize_google(audio2)
            #     MyText = MyText.lower()
                
            #     print("Did you say ", MyText)
                MyText = "What a"
                return MyText
                # SpeakText(MyText)

        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))

        except sr.UnknownValueError:
            print("unknown error occurred")
