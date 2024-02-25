import time
from io import BytesIO
from gtts import gTTS
from pygame import mixer
from pydub import AudioSegment

def tts_play(text):
    tts = gTTS(text)
    audio_bytes_io = BytesIO()
    tts.write_to_fp(audio_bytes_io)
    audio_bytes_io.seek(0)
    audio = AudioSegment.from_file(audio_bytes_io, format="mp3")
    audio_duration = len(audio) / 1000.0
    audio_bytes_io.seek(0)
    mixer.music.load(audio_bytes_io, "mp3")
    mixer.music.play()
    time.sleep(audio_duration)
