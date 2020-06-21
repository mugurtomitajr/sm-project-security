from gpiozero.tones import Tone
from gpiozero import TonalBuzzer
#while True:
    #tone = Tone(frequency=1440.0)
    #TonalBuzzer(14)


import simpleaudio as sa

filename = '../resources/song.wav'
wave_obj = sa.WaveObject.from_wave_file(filename)
play_obj = wave_obj.play()
play_obj.wait_done()
