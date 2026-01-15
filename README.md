🤖 ALVEY – Multimodal AI Voice & Sign Language Assistant

ALVEY is a Python-based intelligent desktop assistant that combines voice commands, sign language recognition, ISL typing, OCR, translation, and app automation into a single interactive system.
It is designed to enhance accessibility, productivity, and human–computer interaction.

🚀 Features
🎙️ Voice-Based Interaction

Speech-to-text using Google Speech Recognition

Text-to-speech using pyttsx3

Continuous Voice Command Mode

Open applications via voice

Perform actions like:

Send email

Translate text

Extract text from image

Show date & time

✋ Sign Language Control (Gesture-Based Actions)

Using MediaPipe Hands and OpenCV:

1 Finger → Speech to Text

2 Fingers → Send Email

3 Fingers → Translate Text

4 Fingers → Open Notepad

5 Fingers → Show Date & Time

✔️ Stability control with hold-time
✔️ Cooldown to avoid repeated triggers

🤟 ISL Typing Mode (Indian Sign Language)

Real-time gesture-to-text typing

Supports characters:

A, B, C, D

SPACE

DELETE

Progress bar and hold-to-type mechanism

Designed for accessibility & inclusivity

📷 OCR – Extract Text from Image

Live webcam capture

Text extraction using Tesseract OCR

Bounding boxes around detected characters

Reads extracted text aloud

🌐 Language Translation

Uses deep-translator (GoogleTranslator)

Auto-detects source language

Supports multiple target languages

📧 Email Automation

Send emails via Gmail SMTP

Secure login using App Password

GUI-based input for:

Sender

Receiver

Message

🖥️ Application Launcher

Open apps using text, voice, or gesture:

Notepad

Calculator

Paint

Chrome

MS Word

MS Excel

(Custom paths configurable)

🖼️ Modern GUI

Built using CustomTkinter

Dark mode UI

Background image with vignette overlay

Clean & accessible design

🛠️ Technologies Used
Category	Libraries
GUI	customtkinter, tkinter, PIL
Voice	pyttsx3, speech_recognition
Vision	opencv-python, mediapipe, numpy
OCR	pytesseract
Translation	deep-translator
Email	smtplib, email.mime
Utilities	threading, datetime, math, os, subprocess
⚙️ Installation
1️⃣ Clone Repository
git clone https://github.com/your-username/alvey.git
cd alvey

2️⃣ Install Dependencies
pip install opencv-python mediapipe pytesseract pyttsx3 speechrecognition deep-translator customtkinter pillow numpy

3️⃣ Install Tesseract OCR

Download from:
https://github.com/tesseract-ocr/tesseract

Update path in code:

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

▶️ How to Run
python alvey.py


Make sure:

Webcam is connected

Microphone is enabled

Gmail App Password is used for email

🧠 Gesture Reference
Sign Language Mode
Fingers	Action
1	Speech to Text
2	Send Email
3	Translate Text
4	Open Notepad
5	Show Date & Time
ISL Typing Mode
Gesture	Output
Fist	A
Palm	B
Curved Hand	C
Index Finger	D
High Five	SPACE
Pinky	DELETE
🔐 Security Notes

Use Gmail App Password, not your actual Gmail password

Do not hardcode credentials

Internet required for speech recognition & translation

📌 Future Enhancements

Full ISL alphabet support (A–Z)

Offline speech recognition

NLP-based command understanding

Mobile version

Cloud-based model integration

ChatGPT API integration

👨‍💻 Author

Raj Maurya
🎓 Computer Science Engineering
🤖 AI | ML | Computer Vision | Accessibility Tech

📄 License

This project is for educational and research purposes.
You are free to modify and enhance it with attribution.
