
import math
import pygame
from array import array


class SoundEffects:
    def __init__(self):
        self.enabled = False
        self.sounds = {}

        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init(
                    frequency=22050,
                    size=-16,
                    channels=1
                )

            self.enabled = True

            self.sounds["click"] = self._make_tone(
                [600], 0.05, 0.15
            )
            self.sounds["wrong"] = self._make_tone(
                [240], 0.12, 0.18
            )
            self.sounds["win"] = self._make_tone(
                [523, 659, 784, 1047], 0.12, 0.22
            )
            self.sounds["lose"] = self._make_tone(
                [400, 300, 200], 0.16, 0.20
            )

        except pygame.error as error:
            print(f"Sound effects unavailable: {error}")
            self.enabled = False
            self.sounds = {}

    def _make_tone(self, frequencies, note_duration, volume):
        mixer_info = pygame.mixer.get_init()
        sample_rate = mixer_info[0]
        channels = mixer_info[2]

        samples = array("h")

        for frequency in frequencies:
            count = int(sample_rate * note_duration)

            for i in range(count):
                t = i / sample_rate

                fade_in = min(1.0, i / 300)
                fade_out = min(1.0, (count - i) / 500)
                fade = max(0.0, min(fade_in, fade_out))

                value = (
                    math.sin(2 * math.pi * frequency * t)
                    * volume
                    * fade
                )

                sample = int(value * 32767)

                for _ in range(channels):
                    samples.append(sample)

        return pygame.mixer.Sound(buffer=samples.tobytes())

    def play(self, name):
        if self.enabled and name in self.sounds:
            self.sounds[name].play()

    
    def toggle(self):
        self.enabled = not self.enabled
        return self.enabled



sound_effects = SoundEffects()
