import pygame
from game import components

window_height = 720
window_width = 550
window = pygame.display.set_mode((window_width, window_height))

ground = components.Ground(window_width)
pipes = []
