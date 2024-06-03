import speech_recognition as sr
import pyttsx3
from langdetect import detect
from googletrans import Translator
from gtts import gTTS
from io import BytesIO
import pygame

# Khởi tạo
recognizer = sr.Recognizer()
translator = Translator(service_urls=['translate.google.com'])
tts = pyttsx3.init()
pygame.init()

# Hàm chuyển đổi văn bản thành giọng nói (sử dụng gTTS)
def speak_text(text, language='en'):
    tts = gTTS(text=text, lang=language)
    fp = BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    pygame.mixer.init()
    pygame.mixer.music.load(fp)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

# Hàm nhận dạng giọng nói với xử lý đa ngôn ngữ
def recognize_speech(audio):
    try:
        # Thử nhận dạng bằng tiếng Việt trước
        text = recognizer.recognize_google(audio, language='vi-VN')
    except sr.UnknownValueError:
        try:
            # Nếu không được, thử nhận dạng bằng tiếng Anh
            text = recognizer.recognize_google(audio, language='en-US')
        except sr.UnknownValueError:
            print("Không thể hiểu được âm thanh, vui lòng thử lại.")
            return None  # Trả về None nếu không nhận dạng được
    return text

# Hàm dịch và phát âm
def translate_and_speak(text_to_translate):
    try:
        detected_language = detect(text_to_translate)

        if detected_language == 'vi':
            translation = translator.translate(text_to_translate, dest='en')
            print(f"Dịch sang tiếng Anh: {translation.text}")
            speak_text(translation.text, language='en')

        elif detected_language == 'en':
            translation = translator.translate(text_to_translate, dest='vi')
            print(f"Dịch sang tiếng Việt: {translation.text}")
            speak_text(translation.text, language='vi')

        else:
            print("Ngôn ngữ không được hỗ trợ")

    except sr.RequestError as e:
        print(f"Không thể gửi yêu cầu; {e}")

# Vòng lặp chính
while True:
    try:
        with sr.Microphone() as source:
            print("Hãy nói gì đó...")
            recognizer.adjust_for_ambient_noise(source)
            recognizer.energy_threshold = 1000  # Điều chỉnh độ nhạy microphone
            audio = recognizer.listen(source)

            text = recognize_speech(audio)
            if text:  # Kiểm tra nếu nhận dạng thành công
                print(f"Bạn nói: {text}")
                translate_and_speak(text)

    except KeyboardInterrupt:
        print("Dừng chương trình")
        break
