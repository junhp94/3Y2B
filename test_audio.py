import speech_recognition as sr


def get_voice_input():
    # Initialize the recognizer
    recognizer = sr.Recognizer()

    # Use the default microphone as the audio source
    with sr.Microphone() as source:
        print("Listening for voice input...")

        # Adjust for ambient noise
        recognizer.adjust_for_ambient_noise(source)

        # Listen for speech
        audio_data = recognizer.listen(source)

        print("Processing voice input...")

    try:
        # Recognize speech using Google Speech Recognition
        text = recognizer.recognize_google(audio_data)
        print("You said:", text)
        return text
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand what you said.")
    except sr.RequestError as e:
        print(
            "Could not request results from Google Speech Recognition service; {0}".format(
                e
            )
        )


if __name__ == "__main__":
    get_voice_input()
