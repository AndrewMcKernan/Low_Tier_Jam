import pygame
from colours import Colour
from image_loader import get_image


class Player(pygame.sprite.Sprite):
    velocity = 6
    old_x = 250
    old_y = 250
    facing_right = False
    old_facing_right = False
    attack_frame = 0
    attacking = True
    consistent_dimensions = (26, 22)
    scale = 3
    health = 3
    invincibility_frames = 60
    current_invincibility_frame = 0
    is_invincible = False
    attack_cooldown = 15
    time_since_last_attack = 0

    def __init__(self):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)

        original_dimensions = (14, 20)
        # scale = 5
        # consistent_dimensions = (26,22)

        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        self.image = get_image('char_standing_sized.png', tuple(i * self.scale for i in self.consistent_dimensions))

        # Fetch the rectangle object that has the dimensions of the image
        # Update the position of this object by setting the values of rect.x and rect.y
        self.rect = self.image.get_rect()
        self.rect.center = (500 / 2, 500 / 2)

    def begin_attack(self):
        if not self.attacking and self.time_since_last_attack == 0:
            self.attacking = True

    def attack(self):
        if self.attack_frame >= 5:
            self.attack_frame = 0
            self.attacking = False
            return False
        self.attack_frame += 1
        self.time_since_last_attack += 1
        self.image = get_image('attack_' + str(self.attack_frame) + '_sized.png',
                               tuple(i * self.scale for i in self.consistent_dimensions))
        return True

    def update(self, *args):
        if self.is_invincible:
            self.current_invincibility_frame += 1
            if self.current_invincibility_frame > self.invincibility_frames:
                self.is_invincible = False
                self.current_invincibility_frame = 0
        if self.attacking:
            still_attacking = self.attack()
            if self.facing_right and still_attacking:
                # flip horizontally (True) not vertically (False)
                self.image = pygame.transform.flip(self.image, True, False)
        if 0 < self.time_since_last_attack < self.attack_cooldown:
            self.time_since_last_attack += 1
        elif self.time_since_last_attack >= self.attack_cooldown:
            self.time_since_last_attack = 0

        # args contains the list of enemy sprites. If we collide with them, don't allow us to move into them
        enemies_collided = pygame.sprite.spritecollide(self, args[0], False)
        for enemy in enemies_collided:
            if enemy.rect.x > self.rect.x:
                # we collided to the right, don't move right
                if self.rect.x > self.old_x:
                    self.rect.x = self.old_x
            elif enemy.rect.x < self.rect.x:
                # we collided to the left, don't move left
                if self.rect.x < self.old_x:
                    self.rect.x = self.old_x
            if enemy.rect.y > self.rect.y:
                # we collided to the top, don't move down
                if self.rect.y > self.old_y:
                    self.rect.y = self.old_y
            elif enemy.rect.y < self.rect.y:
                # we collided to the bottom, don't move up
                if self.rect.y < self.old_y:
                    self.rect.y = self.old_y
        if self.old_x < self.rect.x:
            # we are moving to the right, so perform a horizontal flip
            self.facing_right = True
        elif self.old_x > self.rect.x:
            self.facing_right = False
        self.old_x = self.rect.x
        self.old_y = self.rect.y
        if self.facing_right is not self.old_facing_right:
            # flip horizontally (True) not vertically (False)
            self.image = pygame.transform.flip(self.image, True, False)
            self.old_facing_right = self.facing_right


class Enemy(pygame.sprite.Sprite):

    velocity = 2
    old_x = 400
    old_y = 400
    facing_right = False
    old_facing_right = False

    def __init__(self):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)

        original_dimensions = (17, 11)
        scale = 3

        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        self.image = get_image('spider_standing.png', tuple(i * scale for i in original_dimensions))

        # Fetch the rectangle object that has the dimensions of the image
        # Update the position of this object by setting the values of rect.x and rect.y
        self.rect = self.image.get_rect()
        self.rect.center = (400, 400)

    def update(self, *args):
        # args[0] contains the player sprite, which allows us to know his position and figure out what to do
        player_sprite = args[0]

        # first, move however we need to move
        # TODO: don't let the velocity allow the x/y coord to exceed the player's current position to prevent jittering
        if player_sprite.rect.x > self.rect.x:
            self.rect.x += self.velocity
        elif player_sprite.rect.x < self.rect.x:
            self.rect.x -= self.velocity
        if player_sprite.rect.y > self.rect.y:
            self.rect.y += self.velocity
        elif player_sprite.rect.y < self.rect.y:
            self.rect.y -= self.velocity
        # then, handle the collision
        collided = pygame.sprite.collide_rect(self, player_sprite)
        if collided:
            if player_sprite.attacking:
                self.kill()
                return
            elif not player_sprite.is_invincible:
                player_sprite.health -= 1
                player_sprite.is_invincible = True
            if player_sprite.rect.x > self.rect.x:
                # we collided to the right, don't move right
                if self.rect.x > self.old_x:
                    self.rect.x = self.old_x
            elif player_sprite.rect.x < self.rect.x:
                # we collided to the left, don't move left
                if self.rect.x < self.old_x:
                    self.rect.x = self.old_x
            if player_sprite.rect.y > self.rect.y:
                # we collided to the top, don't move down
                if self.rect.y > self.old_y:
                    self.rect.y = self.old_y
            elif player_sprite.rect.y < self.rect.y:
                # we collided to the bottom, don't move up
                if self.rect.y < self.old_y:
                    self.rect.y = self.old_y

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


class Life(pygame.sprite.Sprite):

    life_number = None

    def __init__(self, life_number):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
        self.life_number = life_number
        original_dimensions = (26, 22)
        scale = 1

        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        self.image = get_image('life.png', tuple(i * scale for i in original_dimensions))

        # Fetch the rectangle object that has the dimensions of the image
        # Update the position of this object by setting the values of rect.x and rect.y
        self.rect = self.image.get_rect()
        print(original_dimensions[0] * life_number)
        self.rect.x = original_dimensions[0] * life_number * 2
        self.rect.y = 0

    def update(self, *args):
        # args[0] is the health of the player
        if args[0] - 1 < self.life_number:
            self.kill()
