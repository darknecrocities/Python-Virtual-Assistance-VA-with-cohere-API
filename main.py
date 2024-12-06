import cohere
import pyttsx3
import speech_recognition as sr  
import datetime
import os
import webbrowser
import sounddevice as sd 
import numpy as np
import pywhatkit as kit  
import time


COHERE_API_KEY = 'OADTtY6Pxh04GXBTiTg4WbqN2UzxFdot8KEYwAMR'
co = cohere.Client(COHERE_API_KEY)


engine = pyttsx3.init()

def speak(audio):

    engine.say(audio)
    engine.runAndWait()

def greet_user():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speak("Good Morning!")
    elif 12 <= hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("Boot sequence complete. Jarvis is at your service.")
    speak("Is there anything i can assist you Sir?")

def take_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening... Please speak.")
        recognizer.adjust_for_ambient_noise(source)  # Adjust for background noise
        try:
            # Listen with a timeout to give the user enough time to finish their speech
            audio_data = recognizer.listen(source, timeout=5, phrase_time_limit=10)  # 5 seconds timeout, 10 seconds max speech duration
            print("Recognizing...")
            query = recognizer.recognize_google(audio_data, language='en-in')
            print(f"User said: {query}")
        except sr.WaitTimeoutError:
            print("Listening timeout. Please try again.")
            return None
        except sr.UnknownValueError:
            print("Sorry, I couldn't understand. Could you please repeat?")
            return None
        except sr.RequestError as e:
            print(f"Error with the speech service; {e}")
            return None
    return query.lower()

def perform_task(query):
    """Perform tasks based on user query."""
    if 'hello jarvis' in query:
        speak("Hello, how can I assist you today?")
    
    elif 'thank you jarvis' in query:
        speak("You're welcome sir!")
    
    elif 'open facebook' in query:
        speak("Opening Facebook")
        webbrowser.open("https://www.facebook.com")
    
    elif 'open youtube' in query:
        speak("Opening YouTube")
        webbrowser.open("https://www.youtube.com")
        
    elif 'open canvas' in query:
        speak("Opening canvas")
        webbrowser.open("https://hau.instructure.com")
    
    elif 'open github' in query:
        speak("Opening github")
        webbrowser.open("https://github.com")
        
    elif 'open cisco' in query or 'open net acad' in query:
        speak("Opening Cisco NetAcad")
        webbrowser.open("https://www.netacad.com")
        
    elif 'open gmail' in query or 'check gmail' in query:
        speak("Opening gmail")
        webbrowser.open("https://mail.google.com/mail/u/0/#inbox")
        
    elif 'open messenger' in query:
        speak("Opening Messenger")
        webbrowser.open("https://www.messenger.com/e2ee/t/27837038135895225") 
    
    elif 'play music on youtube' in query:
        speak("What song would you like to play?")
        song = take_command()
        if song:
            speak(f"Playing {song} on YouTube")
            kit.playonyt(song)
    
    elif 'play music' in query:
        speak("Playing music")
        music_dir = "C:\\Users\\YourUsername\\Music"  
        songs = os.listdir(music_dir)
        os.startfile(os.path.join(music_dir, songs[0]))
        
    elif 'open discord' in query:
        speak("Opening Discord")
        discord_shortcut = r"C:\Users\Arron\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Discord Inc\Discord.lnk" 
        os.startfile(discord_shortcut)

    
    elif 'open messenger' in query:
        speak("Opening Discord")
        discord_shortcut = r"C:\Users\Arron\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Discord Inc\Discord.lnk"  
        os.startfile(discord_shortcut)

    
    elif 'open vscode' in query or 'open visual studio' in query or 'jarvis time to work' in query:
        speak("Opening Visual Studio Code")
        os.system('code')  

    elif 'jarvis war mode' in query or 'jarvis war' in query or 'war mode' in query:
        speak("War Mode: Activated. Weapons online. Let's take this to the next level.")
        os.system("code")  
    
    elif 'the time' in query:
        str_time = datetime.datetime.now().strftime("%H:%M:%S")
        speak(f"The time is {str_time}")

    elif 'open google' in query:
        speak("Opening Google")
        webbrowser.open("https://www.google.com")
    
    elif 'write a summary' in query:
        speak("Please tell me what you want to summarize.")
        content = take_command()
        if content:
            result = process_with_cohere(f"Summarize the following: {content}")
            speak(f"Here's the summary: {result}")
        
    elif 'Shutdown jarvis' in query or 'quit' in query or 'exit' in query or 'shutdown' in query:
        speak("Shutdown Complete! Have a great day sir!")
        exit()
    
    else:
        speak("Let me scan your request.")
        result = process_with_cohere(f"Respond to the following request: {query}")
        speak(result)


def process_with_cohere(prompt):
    response = co.generate(
        model='command-xlarge-nightly',
        prompt=prompt,
        max_tokens=50,
        temperature=0.7,
    )
    return response.generations[0].text.strip()

def main():
    greet_user()
    while True:
        query = take_command()
        if query:
            perform_task(query)

if __name__ == "__main__":
    main()
