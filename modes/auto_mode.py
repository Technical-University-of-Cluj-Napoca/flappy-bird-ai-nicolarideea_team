import pygame
import config
from game.components import Ground, Pipes
from ai.population import Population
from constants import *


class AutoMode:
    def __init__(self, window):
        self.window = window
        self.population = Population(100)
        self.pipes_spawn_time = PIPE_SPAWN_RATE
        self.font = pygame.font.Font(None, 36)

        config.pipes.clear()

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            return 'menu'
        return None

    def update(self):
        if self.pipes_spawn_time <= 0:
            config.pipes.append(Pipes(WINDOW_WIDTH))
            self.pipes_spawn_time = PIPE_SPAWN_RATE
        self.pipes_spawn_time -= 1

        for p in config.pipes[:]:
            p.update()
            if p.off_screen:
                config.pipes.remove(p)

        if not self.population.extinct():
            self.population.update_live_players()
        else:
            config.pipes.clear()
            self.population.natural_selection()

    def draw(self):
        self.window.fill(BLUE)

        config.ground.draw(self.window)
        for p in config.pipes:
            p.draw(self.window)

        alive = sum(1 for p in self.population.players if p.alive)
        gen_text = self.font.render(f"Generation: {self.population.generation}", True, WHITE)
        alive_text = self.font.render(f"Alive: {alive}/{self.population.size}", True, WHITE)
        species_text = self.font.render(f"Species: {len(self.population.species)}", True, WHITE)

        self.window.blit(gen_text, (10, 10))
        self.window.blit(alive_text, (10, 50))
        self.window.blit(species_text, (10, 90))

        if self.population.players:
            best = max(self.population.players, key=lambda p: p.fitness)
            best_text = self.font.render(f"Best: {best.fitness}", True, (255, 215, 0))
            self.window.blit(best_text, (10, 130))
