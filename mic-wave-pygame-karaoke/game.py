from pygame import *
import sounddevice as sd
import scipy.io.wavfile as wav

# === Налаштування ===
fs = 44100
recording = None
is_recording = False
voice_file = "voice_record.wav"  # Записаний голос
minus_track = "MinusDuHast.mp3"  # Мінусовка

# Colors
BG_COLOR = 'green'
BTN_COLOR = 'white'
BTN_RECORDING_COLOR = 'yellow'
BTN_TEXT_COLOR = 'black'
BTN_BORDER_COLOR = 'оrange'
BTN_HOVER_COLOR = (200, 200, 200)
BTN_PRESSED_COLOR = (170, 170, 170)

init()
mixer.init()
mixer.music.set_volume(0.5) # гучність мінусовки
window_size = 1200, 600
window = display.set_mode(window_size)
clock = time.Clock()
font.init()
font_big = font.SysFont("Arial", 32)

btn_rect = Rect(425, 250, 350, 80)
rect_color = BTN_COLOR
btn_text = "Запис"


def start_voice_record():
    global recording
    recording = sd.rec(int(fs * 5), samplerate=fs, channels=1, dtype='int16')  # 5 секунд запис мікрофона !!!


def stop_voice_record():
    global recording
    sd.stop()
    if recording is not None:
        wav.write(voice_file, fs, recording)


def play_song_and_voice_together():
    mixer.music.load(minus_track)
    mixer.music.play()
    voice_sound = mixer.Sound(voice_file)
    voice_sound.play()


while True:
    for e in event.get():
        if e.type == QUIT:
            quit()
        if e.type == MOUSEBUTTONDOWN:
            if btn_rect.collidepoint(e.pos):
                if not is_recording:
                    btn_text = "Стоп та прослухати "
                    is_recording = True
                    mixer.music.load(minus_track)
                    mixer.music.play()
                    start_voice_record()
                else:
                    btn_text = "Запис"
                    is_recording = False
                    stop_voice_record()
                    play_song_and_voice_together()

    window.fill(BG_COLOR)
    # Determine button color based on state (recording overrides hover/press)
    mouse_pos = mouse.get_pos()
    mouse_pressed = mouse.get_pressed()[0]

    if is_recording:
        rect_color = BTN_RECORDING_COLOR
    else:
        if btn_rect.collidepoint(mouse_pos):
            if mouse_pressed:
                rect_color = BTN_PRESSED_COLOR
            else:
                rect_color = BTN_HOVER_COLOR
        else:
            rect_color = BTN_COLOR

    # Draw button (fill and border)
    draw.rect(window, rect_color, btn_rect)
    draw.rect(window, BTN_BORDER_COLOR, btn_rect, 3)

    # Center the text on the button
    text_surface = font_big.render(btn_text, True, BTN_TEXT_COLOR)
    text_rect = text_surface.get_rect(center=btn_rect.center)
    window.blit(text_surface, text_rect)

    display.update()
    clock.tick(30)
