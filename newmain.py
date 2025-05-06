import tkinter as tk
from tkinter import messagebox
import threading
import pyttsx3
import speech_recognition as sr
import cv2
import os
import webbrowser
import pyautogui
import time
import wikipedia
import urllib.parse

from yarl import Query

# Initialize text-to-speech
engine = pyttsx3.init()

# Configure voice
def set_funny_accent():
    voices = engine.getProperty('voices')
    for voice in voices:
        if "english" in voice.name.lower() and "male" in voice.name.lower():
            engine.setProperty('voice', voice.id)
            break
    engine.setProperty('rate', 160)
    engine.setProperty('volume', 1.0)
set_funny_accent()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def simple_face_check():
    """Simplest possible face verification using OpenCV"""
    try:
        # Load reference image
        ref_image = cv2.imread("test.jpg")
        if ref_image is None:
            speak("Reference image not found")
            return False

        # Initialize face detector
        face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )

        # Capture webcam image
        cap = cv2.VideoCapture(0)
        speak("Looking for your face... Please smile!")
        time.sleep(1)
        
        ret, frame = cap.read()
        cap.release()
        
        if not ret:
            speak("Camera error")
            return False

        # Detect faces
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        if len(faces) > 0:
            speak("Welcome Satya Sarthak Manohari!")
            return True
        else:
            speak("Face not detected")
            return False

    except Exception as e:
        speak("Verification failed")
        print("Error:", e)
        return False

def password_fallback():
    speak("Please say the secret password")
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        try:
            audio = recognizer.listen(source, timeout=5)
            password = recognizer.recognize_google(audio).lower()
            return password in "april"
        except:
            return False

def verify_identity():
    if simple_face_check():
        return True
    else:
        return password_fallback()

def execute_command(command):
    command = command.lower()
    if "youtube" in command:
        speak("Opening YouTube!")
        webbrowser.open("https://www.youtube.com")
    elif "music" in command:
        speak("Playing music!")
        webbrowser.open("https://www.youtube.com/watch?v=k0Ka-deab1s")
    elif "play" in command:
        speak("Playing meditation music!")
        webbrowser.open("https://www.youtube.com/watch?v=lRQ4VTcAljU")
    elif "open linkedin" in command:
        speak("Opening LinkedIn!")
        webbrowser.open("https://www.linkedin.com")
    elif "notepad" in command:
        open_notepad_and_type()
    elif "wikipedia" in command:
        search_query = command.split("wikipedia", 1)[-1].strip()
        search_wikipedia(search_query)
    elif "gali" in command:
        speak("you need therapy please contact your nearest mental hospital")
    elif "creator" in command:
        speak("My creater is the ulitmate coder the best hacker the one and only beast kabbali aka Satya Sarthak Manohari")
    elif "dhoni" in command:
        speak("I don't like to talk about credit stealers! He is the biggest credit stealer in cricketing world the tuk tuk academy oh god please please retire him soon!")
    elif "quit" in command or "exit" in command:
        stop_assistant()
    else:
        search_google(command)

def open_notepad_and_type():
    speak("Opening Notepad!")
    os.system("notepad")
    time.sleep(2)
    pyautogui.typewrite(Query)
    pyautogui.press("enter")
    pyautogui.typewrite("How can I help you today?")

def search_wikipedia(query):
    if not query:
        speak("Please specify what to search!")
        return
    try:
        speak(f"Searching Wikipedia for {query}!")
        result = wikipedia.summary(query, sentences=2)
        speak("Here's what I found: " + result)
        messagebox.showinfo("Wikipedia Result", result)
    except Exception as e:
        speak("Wikipedia search failed!")
        print("Error:", e)

def search_google(query):
    if query:
        encoded_query = urllib.parse.quote_plus(query)
        speak(f"Searching Google for {query}!")
        webbrowser.open(f"https://www.google.com/search?q={encoded_query}")
    else:
        speak("What should I search?")

def stop_assistant():
    speak("Goodbye!")
    root.destroy()

def start_assistant():
    if verify_identity():
        threading.Thread(target=listen).start()

def listen():
    speak("Hi I'm April! How can I help you?")
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        while True:
            try:
                audio = recognizer.listen(source, timeout=10)
                command = recognizer.recognize_google(audio)
                execute_command(command)
            except sr.UnknownValueError:
                speak("Could you repeat that?")
            except sr.RequestError:
                speak("Internet connection issue!")
            except Exception as e:
                print("Error:", e)

# GUI Setup
root = tk.Tk()
root.title("AI Assistant - April")
root.geometry("500x400")

try:
    bg_image = tk.PhotoImage(file="AI.png")
    bg_label = tk.Label(root, image=bg_image)
    bg_label.place(relwidth=1, relheight=1)
except Exception as e:
    print("Background image error:", e)

label = tk.Label(root, text="Secure AI Assistant", font=("Helvetica", 18), bg="lightblue")
label.pack(pady=20)

start_btn = tk.Button(root, text="Start", command=start_assistant, 
                     font=("Arial", 14), bg="green", fg="white")
start_btn.pack(pady=10)

exit_btn = tk.Button(root, text="Exit", command=stop_assistant,
                    font=("Arial", 14), bg="red", fg="white")
exit_btn.pack(pady=10)

root.mainloop()