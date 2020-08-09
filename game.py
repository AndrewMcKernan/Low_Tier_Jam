import pygame
from sprites import *
from colours import Colour
import time


def game_loop():
    # the game loop
    width = 500
    height = 500
    fps = 30

    pygame.init()
    pygame.mixer.init()  # for sound
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Survive")

    enemies = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()

    clock = pygame.time.Clock()

    spider = Enemy()
    enemies.add(spider)
    all_sprites.add(spider)
    player = Player()
    all_sprites.add(player)
    game_running = True
    while game_running:
        start = time.time()
        clock.tick(fps)
        # input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player.rect.x -= player.velocity
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player.rect.x += player.velocity
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            player.rect.y -= player.velocity
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            player.rect.y += player.velocity
        # update stuff
        enemies.update(player)
        player.update()
        # render
        screen.fill(Colour.BLACK)
        all_sprites.draw(screen)

        pygame.display.flip()
        end = time.time()
        print('one loop takes ' + str(end-start))
