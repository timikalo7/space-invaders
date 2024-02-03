import math
import random
import pygame
from pygame import mixer

# Initialize pygame
pygame.init()

# Create the screen
game_screen = pygame.display.set_mode((800, 600))

# Background
background_image = pygame.image.load('background.png')

# Sound
mixer.music.load("background.wav")
mixer.music.play(-1)

# Caption and Icon
pygame.display.set_caption("Galactic Defender")
game_icon = pygame.image.load('ufo.png')
pygame.display.set_icon(game_icon)

# Player
player_image = pygame.image.load('player.png')
player_x = 370
player_y = 480
player_x_change = 0

# Enemy
enemy_images = []
enemy_x = []
enemy_y = []
enemy_x_change = []
enemy_y_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemy_images.append(pygame.image.load('enemy.png'))
    enemy_x.append(random.randint(0, 736))
    enemy_y.append(random.randint(50, 150))
    enemy_x_change.append(4)
    enemy_y_change.append(40)

# Bullet
bullet_image = pygame.image.load('bullet.png')
bullet_x = 0
bullet_y = 480
bullet_x_change = 0
bullet_y_change = 10
bullet_state = "ready"

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

text_x = 10
text_y = 10

# Game Over
game_over_font = pygame.font.Font('freesansbold.ttf', 64)

def display_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    game_screen.blit(score, (x, y))

def display_game_over_text():
    game_over_text = game_over_font.render("GAME OVER", True, (255, 255, 255))
    game_screen.blit(game_over_text, (200, 250))

def display_player(x, y):
    game_screen.blit(player_image, (x, y))

def display_enemy(x, y, i):
    game_screen.blit(enemy_images[i], (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    game_screen.blit(bullet_image, (x + 16, y + 10))

def is_collision(enemy_x, enemy_y, bullet_x, bullet_y):
    distance = math.sqrt(math.pow(enemy_x - bullet_x, 2) + (math.pow(enemy_y - bullet_y, 2)))
    if distance < 27:
        return True
    else:
        return False

# Game Loop
running = True
while running:

    game_screen.fill((0, 0, 0))
    game_screen.blit(background_image, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_x_change = -5
            if event.key == pygame.K_RIGHT:
                player_x_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_sound = mixer.Sound("laser.wav")
                    bullet_sound.play()
                    bullet_x = player_x
                    fire_bullet(bullet_x, bullet_y)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_x_change = 0

    player_x += player_x_change
    if player_x <= 0:
        player_x = 0
    elif player_x >= 736:
        player_x = 736

    for i in range(num_of_enemies):
        if enemy_y[i] > 440:
            for j in range(num_of_enemies):
                enemy_y[j] = 2000
            display_game_over_text()
            break

        enemy_x[i] += enemy_x_change[i]
        if enemy_x[i] <= 0:
            enemy_x_change[i] = 4
            enemy_y[i] += enemy_y_change[i]
        elif enemy_x[i] >= 736:
            enemy_x_change[i] = -4
            enemy_y[i] += enemy_y_change[i]

        collision = is_collision(enemy_x[i], enemy_y[i], bullet_x, bullet_y)
        if collision:
            explosion_sound = mixer.Sound("explosion.wav")
            explosion_sound.play()
            bullet_y = 480
            bullet_state = "ready"
            score_value += 1
            enemy_x[i] = random.randint(0, 736)
            enemy_y[i] = random.randint(50, 150)

        display_enemy(enemy_x[i], enemy_y[i], i)

    if bullet_y <= 0:
        bullet_y = 480
        bullet_state = "ready"

    if bullet_state is "fire":
        fire_bullet(bullet_x, bullet_y)
        bullet_y -= bullet_y_change

    display_player(player_x, player_y)
    display_score(text_x, text_y)
    pygame.display.update()
