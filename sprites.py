import pygame
from colours import Colour
from image_loader import get_image


class Player(pygame.sprite.Sprite):
    velocity = 10
    old_x = 250
    old_y = 250
    facing_right = False
    old_facing_right = False

    def __init__(self):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)

        original_dimensions = (14, 20)
        scale = 5

        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        self.image = get_image('char_standing.png', tuple(i * scale for i in original_dimensions))

        # Fetch the rectangle object that has the dimensions of the image
        # Update the position of this object by setting the values of rect.x and rect.y
        self.rect = self.image.get_rect()
        self.rect.center = (500 / 2, 500 / 2)

    def update(self, *args):
        if self.old_x < self.rect.x:
            # we are moving to the right, so perform a horizontal flip
            self.facing_right = True
        elif self.old_x > self.rect.x:
            self.facing_right = False
        self.old_x = self.rect.x
        self.old_y = self.rect.y
        if self.facing_right is not self.old_facing_right:
            self.image = pygame.transform.flip(self.image, True, False)
            self.old_facing_right = self.facing_right


class Enemy(pygame.sprite.Sprite):

    velocity = 10
    old_x = 400
    old_y = 400
    facing_right = False
    old_facing_right = False

    def __init__(self):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)

        original_dimensions = (17, 11)
        scale = 5

        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        self.image = get_image('spider_standing.png', tuple(i * scale for i in original_dimensions))

        # Fetch the rectangle object that has the dimensions of the image
        # Update the position of this object by setting the values of rect.x and rect.y
        self.rect = self.image.get_rect()
        self.rect.center = (400, 400)

    def update(self, *args):
        # args contains the player sprite, which we can use to check collision

        if self.old_x < self.rect.x:
            # we are moving to the right, so perform a horizontal flip
            self.facing_right = True
        elif self.old_x > self.rect.x:
            self.facing_right = False
        self.old_x = self.rect.x
        self.old_y = self.rect.y
        if self.facing_right is not self.old_facing_right:
            self.image = pygame.transform.flip(self.image, True, False)
            self.old_facing_right = self.facing_right
