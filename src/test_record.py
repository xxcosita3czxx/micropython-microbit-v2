from microbit import *

mouth_open = Image(
    "09090:"
    "00000:"
    "09990:"
    "90009:"
    "09990"
)
mouth_closed = Image(
    "09090:"
    "00000:"
    "00000:"
    "99999:"
    "00000"
)
play = Image(
    "00000:"
    "04740:"
    "07970:"
    "04740:"
    "00000"
)

my_recording = audio.AudioRecording(duration=5000)

while True:
    if button_a.is_pressed():
        my_track = microphone.record_into(my_recording, wait=False)
        display.show([mouth_open, mouth_closed], loop=True, wait=False, delay=150)
        while button_a.is_pressed() and microphone.is_recording():
            sleep(50)
        microphone.stop_recording()
        display.show(mouth_closed)
        while button_a.is_pressed():
            sleep(50)
        display.clear()
        # amplify volume
        GAIN = 2
        #my_recording *= GAIN
        for i in range(len(my_track)):
            my_track[i] = max(0, min(128 + GAIN * (my_track[i] - 128), 255))
    if button_b.is_pressed():
        audio.play(my_track, wait=False)
        level = 0
        while audio.is_playing():
            l = audio.sound_level()
            if l > level:
                level = l
            else:
                level *= 0.95
            display.show(play * min(1, level / 100))
            x = accelerometer.get_x()
            my_track.set_rate(max(2250, scale(x, (-1000, 1000), (2250, 13374))))
            sleep(5)
        display.clear()
    sleep(100)
