from RaceCarGame import RaceCarGame
import pygame

# main loop for a player driving the car
if __name__ == '__main__':
    game = RaceCarGame() # instantiates the game

    # loop that runs the game
    while True:

        keys = pygame.key.get_pressed()  # gets the keyboard inputs

        # the game returns the data about the game
        reward, running, score = game.play_step(keys)

        # checks if the game is over
        if running is False:
            break
