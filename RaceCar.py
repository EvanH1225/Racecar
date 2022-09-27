import pygame
import numpy as np
from constants import *


def get_max_distance(i):
    if i == 0:
        return 75
    elif i == 1:
        return 100
    elif i == 2:
        return 150
    elif i == 3:
        return 100
    else:
        return 75


class RaceCar(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # position of the race car used to draw it
        # the x and y position is of the center of the car
        self.x = x
        self.y = y

        # width and height of the race car
        self.width = 50
        self.height = self.width / 2.5

        # creating and transforming the car image
        image = pygame.image.load('f1_car.png').convert_alpha()
        self.img = pygame.transform.scale(image, (self.width, self.height))
        self.rect = self.img.get_rect()
        self.rect.centerx, self.rect.centery = self.x, self.y
        self.mask = pygame.mask.from_surface(self.img)

        self.img_copy = self.img.copy()

        # current speed of the race car and the rate at which it accelerates
        self.speed = 0
        self.max_speed = 25
        self.acceleration = 12
        self.slowing_speed = 3

        # the angle depicting how far the car has rotated in radians and the rate of change of that angle
        self.turn_speed = 135
        self.rotation = 90
        self.rotate_image()

        self.distances = [150 for _ in range(7)]
        self.points = [0 for _ in range(7)]

    # unit for acceleration and turn_speed is m/s and rad/s respectively
    # uses fps as a way to use the correct acceleration and turn speed when changing
    def change_speed(self, fps, accelerating=False, braking=False):
        if braking:
            if self.speed - self.acceleration / fps < self.max_speed * -1:
                self.speed = self.max_speed * -1
            else:
                self.speed -= self.acceleration / fps
        elif accelerating:
            if self.speed + self.acceleration / fps > self.max_speed:
                self.speed = self.max_speed
            else:
                self.speed += self.acceleration / fps
        else:
            if self.speed - self.slowing_speed / fps > 0:
                self.speed -= self.slowing_speed / fps
            else:
                self.speed = 0

    # changes the rotation of the car to the left
    def turn_left(self, fps):
        if self.speed != 0:
            self.rotation += self.turn_speed / fps
            self.rotate_image()

    # changes the rotation of the car to the right
    def turn_right(self, fps):
        if self.speed != 0:
            self.rotation -= self.turn_speed / fps
            self.rotate_image()

    # rotates the image based of the rotation
    def rotate_image(self):
        topleft = self.x, self.y
        self.img = pygame.transform.rotate(self.img_copy, self.rotation)
        self.rect = self.img.get_rect(center=self.img.get_rect(topleft=topleft).center)

    # checks if the car mask is overlapping with the track mask
    # returns the area of the space overlapping
    def check_collision(self, track_mask, x=0, y=0):
        car_x, car_y = self.rect.topleft
        offset = (int(car_x - x), int(car_y - y))
        area = track_mask.overlap_area(self.mask, offset)

        return area

    # updates the mask of the car
    def update_mask(self):
        self.mask = pygame.mask.from_surface(self.img)

    # uses the speed of the car to move it to its new position and recalculates the distance vectors
    def update_pos(self, mask):
        vel_x = self.speed * np.cos(np.radians(self.rotation))  # change in the x direction
        vel_y = self.speed * np.sin(
            np.radians(self.rotation)) * -1  # change in the y direction (negative b/c positive and
        # negative is backwards with y
        self.x = self.x + vel_x
        self.y = self.y + vel_y

        self.rect.centerx, self.rect.centery = self.x, self.y

        self.calculate_distances(mask)

    # returns the point that the distance vector reaches
    def get_point(self, angle, index):
        x, y = self.distances[index] * np.cos(np.radians(angle)) + self.x, self.distances[index] * np.sin(
            np.radians(angle)) + self.y
        x = min(max(x, 0), 799)
        y = min(max(y, 0), 799)

        return x, y

    # returns if a point is inside the track mask
    def check_point(self, distance, angle, index, mask):
        point = self.get_point(angle, index)

        return mask.get_at(point) == 0

    # calculates the distances and their points
    def calculate_distances(self, mask):
        for i in range(len(self.distances)):
            start = -90
            step = 180 / (len(self.distances) - 1)
            angle = start + self.rotation * -1 + step * i

            self.distances[i] = 0
            while self.check_point(self.distances[i], angle, i, mask) and self.distances[i] < 200:
                self.distances[i] = self.distances[i] + 1
            self.points[i] = self.get_point(angle, i)

    # draws the lines coming from the car
    def draw_distances(self, win):
        for point in self.points:
            x, y = point
            x = min(max(x, 0), 799)
            y = min(max(y, 0), 799)
            if type(point) is tuple:
                pygame.draw.circle(win, BLUE, (x, y), 4)
                pygame.draw.line(win, BLACK, (x, y), (self.x, self.y))

    # draws the car and its lines
    def draw(self, win):
        self.draw_distances(win)
        win.blit(self.img, self.rect)
