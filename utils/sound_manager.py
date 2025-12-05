import pygame


class SoundManager:
    _loaded = False

    @staticmethod
    def load():
        if SoundManager._loaded:
            return

        pygame.mixer.init()

        SoundManager.flap = pygame.mixer.Sound("assets/sounds/flap.wav")
        SoundManager.score = pygame.mixer.Sound("assets/sounds/score.wav")
        SoundManager.death = pygame.mixer.Sound("assets/sounds/death.wav")

        SoundManager._loaded = True

    @staticmethod
    def play_flap():
        SoundManager.load()
        SoundManager.flap.play(maxtime=120)

    @staticmethod
    def play_score():
        SoundManager.load()
        SoundManager.score.play(maxtime=150)

    @staticmethod
    def play_death():
        SoundManager.load()
        SoundManager.death.play(maxtime=250)
