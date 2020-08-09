import pygame
import os
from colours import Colour


def get_image(filename, dimensions=None):
    # set up asset folders
    game_folder = os.path.dirname(__file__)
    img_folder = os.path.join(game_folder, 'sprite_art')
    image = pygame.image.load(os.path.join(img_folder, filename)).convert()
    image.set_colorkey(Colour.BLUE)
    if dimensions is not None:
        image = pygame.transform.scale(image, dimensions)
    return image
