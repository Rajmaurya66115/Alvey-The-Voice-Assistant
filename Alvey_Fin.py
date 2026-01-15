#ALVEY
import pytesseract
from tkinter import simpledialog, messagebox
import pyttsx3
import speech_recognition as sr
from deep_translator import GoogleTranslator
import subprocess
import os
import mediapipe as mp 
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
import cv2
import numpy as np
import customtkinter as ctk
import tkinter as tk
from tkinter import scrolledtext, ttk
from PIL import Image, ImageDraw
import threading
import time
from collections import deque
import math 

#change tesseract path according to your device
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


# ---------------------- VOICE OUTPUT ----------------------

try:
    engine = pyttsx3.init()
except Exception as e:
    engine = None
    print("pyttsx3 init error:", e)


def speak(text):  #This function will turn text into speech using python pyttsx3(Python text to speech Library).
    """Speak text (safe wrapper)."""
    try:
        if engine:
            engine.say(text)
            engine.runAndWait()
    except Exception as e:
        print("TTS Error:", e)


# ---------------------- APP MAPPING ----------------------

#Change the path of each application according to your device, here we are mapping the path of each application to a keyword used to identify them.
app_commands = {
    "notepad": "notepad",
    "calculator": "calc",
    "paint": "mspaint",
    "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "word": r"C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE",
    "excel": r"C:\Program Files\Microsoft Office\root\Office16\EXCEL.EXE",
}


# ---------------------- CORE FUNCTIONS ----------------------

def speech_to_text(): #This will convert speech into text using google speech_recognition 
    try:
        r = sr.Recognizer()
        with sr.Microphone() as source:
            speak("Speak now for speech to text.")
            audio = r.listen(source, timeout=6, phrase_time_limit=8)
        text = r.recognize_google(audio)
        output_label.configure(text=f"Recognized: {text}")
        speak(f"You said: {text}")
    except sr.WaitTimeoutError:
        output_label.configure(text="Listening timed out.")
        speak("Listening timed out.")
    except sr.RequestError as e:
        output_label.configure(text="Speech service error.")
        speak("Speech service error.")
        print("SpeechRecognition RequestError:", e)
    except Exception as e:
        output_label.configure(text="Could not recognize speech.")
        speak("Sorry, I could not understand your speech.")
        print("Speech-to-Text Error:", e)

def send_email(): 
    '''This function is used to send an email, it will first make the user to login into their account
    by entering their email and password, then writing the reciever's address and the message to send.'''
    
    try:
        sender = simpledialog.askstring("Email", "Enter your Gmail (example@gmail.com):")
        if sender is None:
            return
        password = simpledialog.askstring("Password", "Enter App Password:", show="*")
        if password is None:
            return
        receiver = simpledialog.askstring("Email", "Enter Receiver Gmail:")
        if receiver is None:
            return
        content = simpledialog.askstring("Message", "Enter Message:")
        if content is None:
            return
        if not sender or not password or not receiver or not content:
            speak("Missing email information. Cancelled.")
            return

        msg = MIMEText(content)
        msg["Subject"] = "Email from Alvey"
        msg["From"] = sender
        msg["To"] = receiver

        server = smtplib.SMTP("smtp.gmail.com", 587, timeout=15)
        server.starttls()
        server.login(sender, password)
        server.sendmail(sender, receiver, msg.as_string())
        server.quit()
        speak("Email sent successfully!")
        messagebox.showinfo("Success", "Email sent successfully!")
    except smtplib.SMTPAuthenticationError as e:
        speak("Authentication failed. Check email and app password.")
        messagebox.showerror("Authentication Error", "Gmail authentication failed. Use a valid App Password or check account security settings.")
        print("SMTPAuthError:", e)
    except Exception as e:
        speak("Error sending email.")
        messagebox.showerror("Error", f"Failed to send email: {e}")
        print("Send Email Error:", e)

def translate_text(): #This function is used to Translate text using deep-translator.
    try:
        speak("Enter text to translate:")
        text = simpledialog.askstring("Translate", "Enter text to translate:")
        if text is None:
            return
        speak("Enter target language code")
        target = simpledialog.askstring("Translate", "Enter target language code (e.g., en, hi, fr):")
        if not text or not target:
            speak("Translation cancelled.")
            return
        translated = GoogleTranslator(source='auto', target=target).translate(text)
        speak("Here is the translation.")
        speak(translated)
        messagebox.showinfo("Translation Result", translated)
    except Exception as e:
        speak("Error during translation.")
        messagebox.showerror("Error", f"Translation error: {e}")
        print("Translation Error:", e)

def show_datetime(): #This function will Show current date and time.
    try:
        now = datetime.now()
        dt_string = now.strftime("%Y-%m-%d  |  %H:%M:%S")
        speak(f"The current date and time is {dt_string}")
        messagebox.showinfo("Date & Time", dt_string)
    except Exception as e:
        speak("Error fetching date and time.")
        print("DateTime Error:", e)

def open_app(): #This function will ask the user to type the name of an application to open when he clicks on open application on the main menu, then this will call the open_application_by_name function. 
    apname = simpledialog.askstring("App Launcher", "Enter app name to open")
    if apname:
        output_label.configure(text=f"Opened {apname}")
        open_application_by_name(apname)


def open_application_by_name(app_name): #This function will Open an application by name using mapping.
    try:
        app_name = app_name.strip().lower()
        if app_name in app_commands:
            path = app_commands[app_name]
            if os.path.exists(path):
                subprocess.Popen([path])
            else:
                os.startfile(path)
            speak(f"Opened {app_name}")
            output_label.configure(text=f"Opened {app_name}")
        else:
            speak(f"{app_name} not found in mapping")
            output_label.configure(text=f"{app_name} not in mapping")
    except Exception as e:
        speak(f"Error opening {app_name}")
        print("Open App Error:", e)


# ---------------------- VOICE COMMAND MODE ----------------------

def start_voice_assistant(): #This function will turn ON the voice command mode, which continously listen and takes input from the user and perform the desired functions.
    def _voice_loop():
        r = sr.Recognizer()
        speak("Voice mode activated. Say a command. Say stop to exit.")
        #messagebox.showinfo("Voice Assistant", "Voice Mode Activated!\nSay a command (say 'stop' to exit).")
        while True:
            try:
                with sr.Microphone() as source:
                    audio = r.listen(source, timeout=6, phrase_time_limit=8)
                    output_label.configure(text=f"Listening...")
                    command = r.recognize_google(audio).lower()
            except sr.WaitTimeoutError:
                output_label.configure(text="Listening timed out, say command again.")
                continue
            except Exception as e:
                output_label.configure(text="Could not understand. Speak again.")
                speak("Could not understand. Please say again.")
                print("Voice Recognition Error:", e)
                continue

            output_label.configure(text=f"You said: {command}")
            speak(f"You said: {command}")

            if "stop" in command:
                speak("Voice mode stopped.")
                messagebox.showinfo("Voice Assistant", "Voice mode stopped.")
                break
            elif "email" in command:
                send_email()
            elif "speech to text" in command or "speech-to-text" in command:
                speech_to_text()
            elif "translate" in command:
                translate_text()
            elif "sign language" in command:
                sign_language_mode()
            elif "extract text" in command:
                speak("Performing text extraction, please show the input to the camera to capture")
                Extract_Text_From_Image()
            elif "open" in command:
                app = command.replace("open ", "").strip()
                if app:
                    open_application_by_name(app)
                else:
                    speak("Please say which application to open.")
            elif "date" in command or "time" in command:
                show_datetime()
            else:
                output_label.configure(text="Command not recognized.")
                speak("Command not recognized.")
    threading.Thread(target=_voice_loop, daemon=True).start()


# ---------------------- SIGN LANGUAGE MODE ----------------------


def sign_language_mode():
    def _sign_process():
        mp_hands = mp.solutions.hands
        mp_draw = mp.solutions.drawing_utils
        hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
        
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            speak("Camera Error")
            return

        speak("Sign Mode Started. Hold gesture for action.")
        
        # --- NEW STABILITY VARIABLES ---
        current_gesture = 0
        gesture_start_time = 0
        HOLD_TIME_REQUIRED = 1.5  # Seconds to hold (Adjust this if needed)
        last_action_time = 0
        action_cooldown = 3.0     # Time to wait after an action is done
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret: break
            
            frame = cv2.flip(frame, 1)
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            res = hands.process(rgb)
            
            fingers = 0
            
            # --- MEDIAPIPE LOGIC ---
            if res.multi_hand_landmarks:
                lm = res.multi_hand_landmarks[0].landmark
                # Count Fingers
                if lm[8].y < lm[6].y: fingers += 1 # Index
                if lm[12].y < lm[10].y: fingers += 1 # Middle
                if lm[16].y < lm[14].y: fingers += 1 # Ring
                if lm[20].y < lm[18].y: fingers += 1 # Pinky
                if abs(lm[4].x - lm[0].x) > abs(lm[3].x - lm[0].x): fingers += 1 # Thumb
                
                mp_draw.draw_landmarks(frame, res.multi_hand_landmarks[0], mp_hands.HAND_CONNECTIONS)
            
            # --- TIME LOCK LOGIC ---
            now = time.time()
            
            # Agar ungli change hui, toh timer reset karo
            if fingers != current_gesture:
                current_gesture = fingers
                gesture_start_time = now # Restart timer
            
            # Calculate duration held
            duration_held = now - gesture_start_time
            
            # Determine Status Message & Progress Bar
            status_msg = "Hold Steady..."
            progress = 0
            
            if fingers > 0:
                progress = min(1.0, duration_held / HOLD_TIME_REQUIRED)
                if progress < 1.0:
                    status_msg = f"Holding: {int(progress*100)}%"
                else:
                    status_msg = "Action Triggered!"

            # Check Trigger
            if duration_held > HOLD_TIME_REQUIRED and fingers != 0:
                # Check cooldown (Action turant repeat na ho)
                if (now - last_action_time) > action_cooldown:
                    
                    if fingers == 1:
                        speech_to_text()
                    elif fingers == 2:
                        send_email()
                    elif fingers == 3:
                        translate_text()
                    elif fingers == 4:
                        open_application_by_name("Notepad")
                    elif fingers == 5:
                        show_datetime()
                    
                    # Action lene ke baad timer reset aur cooldown update
                    last_action_time = now
                    gesture_start_time = now # Prevent double trigger
                    status_msg = "Done!"

            # --- UI DRAWING ---
            
            # Top Black Bar
            cv2.rectangle(frame, (0,0), (640, 80), (0,0,0), -1)
            
            # Fingers Text
            cv2.putText(frame, f"Fingers: {fingers}", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
            # Status Text
            cv2.putText(frame, status_msg, (20, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            
            # PROGRESS BAR (Blue Line at bottom of black bar)
            if fingers > 0 and progress < 1.0:
                bar_width = int(640 * progress)
                cv2.rectangle(frame, (0, 75), (bar_width, 80), (255, 200, 0), -1)

            
            cv2.putText(frame, "1.Speech To Text", (250, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
            cv2.putText(frame, "2.Send Mail", (250, 45), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
            cv2.putText(frame, "3.Translate Text", (250, 65), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
            cv2.putText(frame, "4.Open Notepad", (400, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
            cv2.putText(frame, "5.Show Date and Time", (400, 45), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
            
            # Exit Text
            cv2.putText(frame, "Q: Quit", (500, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2) 
            

            cv2.imshow("Alvey - Sign Language Mode", frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        cap.release()
        cv2.destroyAllWindows()
        speak("Sign Language mode Closed")
        
    threading.Thread(target=_sign_process).start()

# ---------------------- ISL TYPING MODE (Indian Sign Language) ----------------------


def get_distance(p1, p2):
    return math.hypot(p1.x - p2.x, p1.y - p2.y)


# Gesture Recognition
def predict_isl_character(landmarks):
    lm = landmarks
    tips = [8, 12, 16, 20]
    dips = [6, 10, 14, 18]

    fingers_open = [lm[tip].y < lm[dip].y for tip, dip in zip(tips, dips)]
    thumb_open = lm[4].x > lm[3].x

    if all(not f for f in fingers_open) and thumb_open:
        return "A"
    if all(fingers_open) and not thumb_open:
        return "B"
    if fingers_open[0] and not any(fingers_open[1:]) and (get_distance(lm[4], lm[12]) < 0.05):
        return "D"
    dist_index_thumb = get_distance(lm[4], lm[8])
    if 0.05 < dist_index_thumb < 0.2 and not fingers_open[1]:
        return "C"
    if all(fingers_open) and thumb_open:
        return "SPACE"
    if not fingers_open[0] and not fingers_open[1] and not fingers_open[2] and fingers_open[3]:
        return "DELETE"
    return ""


def isl_typing_mode():
    def _typing_loop():
        mp_hands = mp.solutions.hands
        mp_draw = mp.solutions.drawing_utils
        hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)

        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("Camera Error")
            return

        speak("ISL Typing Mode Started. Hold gesture to type.")

        typed_text = ""
        last_char = ""
        gesture_start_time = 0
        current_char = ""
        HOLD_TIME_REQUIRED = 2.0  # seconds to hold
        progress = 0

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.resize(frame, (640, 480))
            h, w, c = frame.shape
            frame = cv2.flip(frame, 1)
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            res = hands.process(rgb)

            detected_char = ""

            if res.multi_hand_landmarks:
                for hand_landmarks in res.multi_hand_landmarks:
                    mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                    detected_char = predict_isl_character(hand_landmarks.landmark)

            now = time.time()

            # Reset timer if gesture changes
            if detected_char != current_char:
                current_char = detected_char
                gesture_start_time = now

            duration_held = now - gesture_start_time
            progress = min(1.0, duration_held / HOLD_TIME_REQUIRED)

            status_msg = "Hold Steady..."
            if current_char:
                if progress < 1.0:
                    status_msg = f"Holding {current_char}: {int(progress*100)}%"
                else:
                    status_msg = f"{current_char} Added!"
                    typed_text += " " if current_char == "SPACE" else ("" if current_char == "DELETE" else current_char)
                    if current_char == "DELETE" and typed_text:
                        typed_text = typed_text[:-1]
                    gesture_start_time = now  # reset after action
                    progress = 0

            # --- UI DRAWING ---
            # Top Black Bar
            cv2.rectangle(frame, (0, 0), (w, 100), (0, 0, 0), -1)

            # Typed text (bold white)
            cv2.putText(frame, f"Typed: {typed_text}", (20, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)

            # Status text
            cv2.putText(frame, status_msg, (20, 70),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

            # Menu items (bold white)
            cv2.putText(frame, "A:Fist  B:Palm  C:Curve  D:Index ",
                        (250, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            cv2.putText(frame, "Space:High5  Del:Pinky",
                        (300, 47), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

 # Exit text
            cv2.putText(frame, "Q: Quit", (500, 78),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

            # Progress bar at bottom of header
            bar_top = 95
            bar_bottom = 100
            bar_width = int(w * progress)
            cv2.rectangle(frame, (0, bar_top), (bar_width, bar_bottom), (255, 200, 0), -1)

            cv2.imshow("Alvey - ISL Typing Mode", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()
        speak("ISL Typing Mode Closed.")

    threading.Thread(target=_typing_loop, daemon=True).start()


#-------------------Extract Text From an Image--------------------

def Extract_Text_From_Image(): #This function will extract text from the image and show the bound boxes around each character in the output image, along with showing and speaking out the Extracted Text. 
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        speak("Cannot open webcam.")
        return

    speak("Press 'S' to capture the frame...")

    while True:
        status, frame = cap.read()
        if not status:
            speak("Failed to grab frame.")
            break

        cv2.imshow('Live Feed', frame)

        if cv2.waitKey(1) & 0xFF == ord('s'):
            save_path = r"C:\Temp\Captain.png"
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            cv2.imwrite(save_path, frame)
            print(f"Image saved to {save_path}")
            break

    cap.release()
    cv2.destroyAllWindows()

    img = cv2.imread(save_path)
    if img is None:
        speak("Image not found.")
        return

    mytext = pytesseract.image_to_string(img)
    print("Detected Text:\n", mytext)
    output_label.configure(mytext)
    speak(mytext)
    
    boxes = pytesseract.image_to_boxes(img)
    hIMG, wIMG, _ = img.shape

    for b in boxes.splitlines():
        b = b.split(' ')
        x, y, w, h = int(b[1]), int(b[2]), int(b[3]), int(b[4])
        cv2.rectangle(img, (x, hIMG - y), (w, hIMG - h), (250, 0, 0), 1)
        cv2.putText(img, b[0], (x - 20, hIMG - y - 20), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)

    cv2.imshow("Detected Text", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


# ---------------------- GUI ----------------------

ctk.set_appearance_mode("dark")

root = ctk.CTk()
root.title("ALVEY - Voice Assistant")
root.geometry("600x600")   

#Background_Image
bg_img = Image.open("bgimg.jpg").convert("RGBA")
w, h = bg_img.size

#vignette to add a little bit darkness to the background image to make a good contrast, with the above buttons.
vignette = Image.new("L", (w, h), 0)
draw = ImageDraw.Draw(vignette)
for i in range(int(min(w, h)/2)):
    draw.ellipse((i, i, w-i, h-i), fill=int(255 * (i/(min(w, h)/2))))

overlay = Image.new("RGBA", (w, h), (0, 0, 0, 240))
overlay.putalpha(vignette)

bg_img = Image.alpha_composite(bg_img, overlay)

bg_ctk_image = ctk.CTkImage(light_image=bg_img, dark_image=bg_img, size=(1600,1120))
bg_label = ctk.CTkLabel(root, image=bg_ctk_image, text="")
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

#Main Title Text
main_label = ctk.CTkLabel(root,
                               text="ALVEY",
                               font=ctk.CTkFont(family="Montserrat ExtraBold",size=25, weight="bold"),
                               text_color="#f0fc09",
                               bg_color="black"
                               )
main_label.place(x=250, y=20)

#This is where all the outputs from the programs will be shown, it has a default text as "Welcome to ALVEY!".
output_label = ctk.CTkLabel(root, text="Welcome to ALVEY!",
                            font=ctk.CTkFont(size=12, weight="bold"),
                            text_color="white", bg_color="transparent")
output_label.place(x=230, y=65)

#All the menu buttons that are used are defined here.
btn_font = ctk.CTkFont(family="Roboto", size=12, weight="bold")

ctk.CTkButton(root, text="🎙️Voice Command Mode", command=start_voice_assistant, font=btn_font, hover_color="#2B2B2B", border_color="#FFFFFF", border_width=1, corner_radius=32, width=180, height=40).place(x=65, y=120)
ctk.CTkButton(root, text="✋ Sign Language Mode", command=sign_language_mode, font=btn_font, hover_color="#2b2b2b", border_color="#FFFFFF", border_width=1, corner_radius=32, width=180, height=40).place(x=340, y=120)

ctk.CTkButton(root, text="📧 Send Email", command=send_email, font=btn_font, hover_color="#2b2b2b", border_color="#FFFFFF", border_width=1, corner_radius=32, width=180, height=40).place(x=70, y=215)
ctk.CTkButton(root, text="📝 Open Application", command=open_app, font=btn_font, hover_color="#2b2b2b", border_color="#FFFFFF", border_width=1, corner_radius=32, width=180, height=40).place(x=350, y=215)

ctk.CTkButton(root, text="🌐 Translate Text", command=translate_text, font=btn_font, hover_color="#2b2b2b", border_color="#FFFFFF", border_width=1, corner_radius=32, width=180, height=40).place(x=70, y=310)
ctk.CTkButton(root, text="🗣️Speech-to-Text", command=speech_to_text, font=btn_font, hover_color="#2b2b2b", border_color="#FFFFFF", border_width=1, corner_radius=32, width=180, height=40).place(x=350, y=310)

ctk.CTkButton(root, text="📷 Extract Text From Image", command=Extract_Text_From_Image, font=btn_font, hover_color="#2b2b2b", border_color="#FFFFFF", border_width=1, corner_radius=32, width=380, height=40).place(x=110, y=405)

# ISL TYPING MODE BUTTON (A, B, C, D)
ctk.CTkButton(root, text="🤟 ISL Typing Mode (A-D)", command=isl_typing_mode, font=btn_font, hover_color="#2b2b2b", border_color="#FFFFFF", border_width=1, corner_radius=32, width=380, height=40).place(x=110, y=480)


#This is a tiny Copyright @Alvey text at the bottom. 
copyright_label = ctk.CTkLabel(root,
                               text="© ALVEY 2025",
                               font=ctk.CTkFont(size=8, weight="bold"),
                               text_color="white",
                               fg_color="transparent",
                               bg_color="transparent"
                               )
copyright_label.place(relx=0.5, rely=1.0, anchor="s", y=-5)


speak("Welcome to Alvey")

try:
    root.mainloop()
except KeyboardInterrupt:
    speak("Application closed by user.")
