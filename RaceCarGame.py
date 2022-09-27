import pygame
import numpy as np
from constants import *
from RaceCar import RaceCar
import copy

pygame.init()


class RaceCarGame:

    def __init__(self):
        # pygame window and clock
        self.win = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()

        # loading in the image of the track
        track_img = pygame.image.load('race_track.png')
        self.track = pygame.transform.scale(track_img, (WIDTH, HEIGHT))

        # loading in the track mask (where the car can and can't drive)
        track_outline_img = pygame.image.load('race_track_outline.png').convert_alpha() # the actual image
        self.track_outline = pygame.transform.scale(track_outline_img, (WIDTH, HEIGHT))
        self.track_mask = pygame.mask.from_surface(self.track_outline)  # the pygame.mask

        # creates the car
        self.car = RaceCar(75, 450)

        # the game outputs
        self.running = True
        self.reward = 0  # for Q_Learning
        self.score = 0  # how far the car has driven

    # resets the game state back to the starting position
    def reset(self):
        self.car = RaceCar(75, 450)

        self.running = True
        self.reward = 0
        self.score = 0

    # updates the window - does this every frame
    def update(self):
        self.win.fill(BLACK)
        self.win.blit(self.track, (0, 0))
        # self.win.blit(self.track_outline, (0, 0))

        self.car.draw(self.win)

        pygame.display.flip()

    # runs the game: checking for inputs and updating each frame then pasting it to the screen
    def play_step(self, keys):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

        # tells the car how to move based on key inputs
        if keys[pygame.K_UP]:
            self.car.change_speed(FPS, accelerating=True)
        elif keys[pygame.K_DOWN]:
            self.car.change_speed(FPS, braking=True)
        else:
            self.car.change_speed(FPS)
        if keys[pygame.K_RIGHT]:
            self.car.turn_right(FPS)
        if keys[pygame.K_LEFT]:
            self.car.turn_left(FPS)

        self.car.update_pos(self.track_mask)  # updates the position of the car based off speed
        self.car.update_mask()  # updates the mask of the car to have accurate collisions

        # checks if the car has collised with the track and ends the game if it has
        area = self.car.check_collision(self.track_mask)  # returns how many pixels of the car are overlapping the track
        if area > 200:
            self.running = False

        # updates screen and controls frames per second
        self.update()
        self.clock.tick(FPS)

        # returns the current state of the game
        return self.reward, self.running, self.score


