import socket
import speech_recognition as sr


def get_voice_input():
    # Initialize the recognizer
    recognizer = sr.Recognizer()

    # Use the default microphone as the audio source
    with sr.Microphone() as source:
        print("Speak a word...")

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
        return None
    except sr.RequestError as e:
        print(
            "Could not request results from Google Speech Recognition service; {0}".format(
                e
            )
        )
        return None


def main():
    # Set up the server address and port
    server_host = "207.23.187.236"  # Change this to the server's IP address
    server_port = 5555  # Change this to the server's port

    # Connect to the server
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_host, server_port))

    try:
        while True:
            # Get voice input
            voice_input = get_voice_input()
            if voice_input:
                # Send the voice input to the server
                client_socket.sendall(voice_input.encode("utf-8"))

    finally:
        # Close the connection when done
        client_socket.close()


if __name__ == "__main__":
    main()
