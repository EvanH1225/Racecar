import numpy as np
import pygame
from constants import *


def expand_track(width, height, points):
    tracks = []
    hypo = np.sqrt((width / 2) ** 2 + (height / 2) ** 2)

    for i in range(len(points) - 1):
        x_diff = max(points[i + 1][0] - points[i][0], .00001)
        y_diff = -1 * max(points[i + 1][1] - points[i][1], .00001)

        print(x_diff, y_diff)
        tilt = np.arctan(y_diff/x_diff)

        theta1 = np.pi/2 - np.arctan((width/2) / (height/2))
        theta2 = np.pi - theta1 * 2
        print(theta1, theta2, tilt)

        rect = []
        for n in range(4):
            if n == 0:
                x = points[i][0] - hypo * np.cos(tilt + theta1)
                y = points[i][1] - hypo * np.sin(tilt + theta1)
            elif n == 1:
                x = points[i][0] - hypo * np.cos(tilt + theta1 + theta2)
                y = points[i][1] - hypo * np.sin(tilt + theta1 + theta2)
            elif n == 2:
                x = points[i][0] - hypo * np.cos(tilt + theta1 + np.pi)
                y = points[i][1] - hypo * np.sin(tilt + theta1 + np.pi)
            else:
                x = points[i][0] - hypo * np.cos(tilt + theta1 + theta2 + np.pi)
                y = points[i][1] - hypo * np.sin(tilt + theta1 + theta2 + np.pi)

            rect.append((x, y))

        order = [0, 1, 2, 3]
        rect = [rect[i] for i in order]

        tracks.append(rect)


def draw_line(event, points):
    if pygame.mouse.get_pressed()[0]:
        pos = pygame.mouse.get_pos()
        points.append(pos)
    if event.type == pygame.KEYDOWN:
        expand_track(100, 40, points)

    return points


def update(win, points, tracks):
    win.fill(WHITE)

    if len(points) > 1:
        pygame.draw.aalines(win, BLACK, False, points)

    if len(tracks) > 0:
        for track in tracks:
            pygame.draw.polygon(win, BLACK, track)
