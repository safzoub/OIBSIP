import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia

engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def get_audio():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
        except sr.WaitTimeoutError:
            print("Listening timed out.")
            return "Timeout"

    try:
        text = recognizer.recognize_google(audio)
        print(f"You said: {text}")
        return text.lower()
    except sr.UnknownValueError:
        return "Sorry, I didn't get that."
    except sr.RequestError as e:
        return f"API unavailable: {e}"
    except Exception as e:
        return f"Error: {e}"

def assistant(text):
    if "hello" in text:
        speak("Hello! How can I help you?")
    elif "time" in text:
        now = datetime.datetime.now()
        speak(f"The time is {now.strftime('%I:%M %p')}")
    elif "date" in text:
        today = datetime.date.today()
        speak(f"Today's date is {today.strftime('%B %d, %Y')}")
    elif "what is" in text:
        topic = text.replace("what is", "").strip()
        try:
            summary = wikipedia.summary(topic, sentences=2)
            speak(summary)
        except Exception:
            speak("Sorry, I couldn't find that information.")
    else:
        speak("Sorry, I don't understand that command yet.")

if __name__ == "__main__":
    speak("Welcome back, A. I am listening.")
    while True:
        user_text = get_audio()
        if user_text == "timeout":
            speak("Timed out waiting for a command.")
        else:
            assistant(user_text)
