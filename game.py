import pygame
from sprites import *
from colours import Colour
import time
from random import randrange


def game_loop():
    # the game loop
    width = 500
    height = 500
    fps = 30
    max_enemies = 10
    ticks_between_spawns = 15
    ticks_since_last_spawn = 0

    pygame.init()
    pygame.mixer.init()  # for sound
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Survive")

    enemies = pygame.sprite.Group()
    life = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()

    clock = pygame.time.Clock()

    spider = Enemy()
    enemies.add(spider)

    all_sprites.add(spider)
    player = Player()
    all_sprites.add(player)
    for i in range(player.health):
        life_sprite = Life(i)
        all_sprites.add(life_sprite)
        life.add(life_sprite)
    game_running = True
    while game_running:
        # start = time.time()
        clock.tick(fps)
        # input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            player.begin_attack()
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
        player.update(enemies)
        life.update(player.health)
        if len(enemies) < max_enemies and ticks_since_last_spawn > ticks_between_spawns:
            baddie = Enemy()
            # spawn in one of the 4 corners of the map
            x = randrange(2)
            y = randrange(2)
            baddie.rect.x = width * x
            baddie.rect.y = height * y
            enemies.add(baddie)
            all_sprites.add(baddie)
            ticks_since_last_spawn = 0

        if ticks_since_last_spawn <= ticks_between_spawns:
            ticks_since_last_spawn += 1
        # render
        screen.fill(Colour.BLACK)
        all_sprites.draw(screen)

        pygame.display.flip()
        end = time.time()
        # print('one loop takes ' + str(end-start))
