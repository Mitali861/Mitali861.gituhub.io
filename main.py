import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
from openai import OpenAI

NEWS_API_KEY = "your_news_api_key_here"
OPENAI_API_KEY = "your_openai_api_key_here"

# Init
recognizer = sr.Recognizer()
engine = pyttsx3.init()

def speak(text: str):
   
    try:
        print(f"🗣️ Meeka: {text}")
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"[ERROR] Speech failed: {e}")

def listen(timeout=3, phrase_time=4) -> str:
    """Listen to microphone input and return recognized text."""
    try:
        with sr.Microphone() as source:
            print("🎤 Listening...")
            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time)
        return recognizer.recognize_google(audio).lower()
    except sr.UnknownValueError:
        return ""
    except Exception as e:
        print(f"[ERROR] Listening failed: {e}")
        return ""

def aiProcess(command: str) -> str:
    """Send user query to OpenAI and return AI response."""
    try:
        client = OpenAI(api_key=OPENAI_API_KEY)
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are Meeka, a smart virtual assistant. Keep responses short."},
                {"role": "user", "content": command}
            ]
        )
        return completion.choices[0].message.content
    except Exception as e:
        print(f"[ERROR] OpenAI request failed: {e}")
        return "Sorry, I couldn’t process that."

def getNews():
   
    try:
        url = f"https://newsapi.org/v2/top-headlines?country=in&apiKey={NEWS_API_KEY}"
        r = requests.get(url)

        if r.status_code != 200:
            speak("Failed to fetch news.")
            return

        articles = r.json().get("articles", [])
        if not articles:
            speak("No news available right now.")
            return

        speak("Here are the top news headlines.")
        for i, article in enumerate(articles[:5], 1):
            speak(f"News {i}: {article['title']}")
    except Exception as e:
        print(f"[ERROR] News fetch failed: {e}")
        speak("Sorry, I cannot fetch news right now.")

def processCommand(c: str):
    print(f"👉 Command received: {c}")

    if "open google" in c:
        webbrowser.open("https://google.com")
        speak("Opening Google.")
    elif "open facebook" in c:
        webbrowser.open("https://facebook.com")
        speak("Opening Facebook.")
    elif "open youtube" in c:
        webbrowser.open("https://youtube.com")
        speak("Opening YouTube.")
    elif "open linkedin" in c:
        webbrowser.open("https://linkedin.com")
        speak("Opening LinkedIn.")
    elif c.startswith("play"):
        song = c.replace("play", "").strip()
        link = musicLibrary.music.get(song)
        if link:
            speak(f"Playing {song}.")
            webbrowser.open(link)
        else:
            speak("Song not found in library.")
    elif "news" in c:
        getNews()
    elif "exit" in c or "quit" in c:
        speak("Goodbye! 👋")
        exit()
    else:
        response = aiProcess(c)
        speak(response)

if __name__ == "__main__":
    speak("✨ Initializing Meeka...")
    while True:
        print("⏳ Waiting for wake word ('meeka')...")
        word = listen(timeout=3, phrase_time=3)

        if word == "meeka":
            speak("Yes, how can I help you?")
            command = listen(timeout=5, phrase_time=7)
            if command:
                processCommand(command)




   




        




  













