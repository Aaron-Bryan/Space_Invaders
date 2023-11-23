import math
import random

import pygame
from pygame import mixer


# Intialize the pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('background.jpg')

#Background Audio
#mixer.music.load("background.wav")
#mixer.music.play(-1)

# Caption and Icon
pygame.display.set_caption("Bootleg Galaga")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# Player
player_model = pygame.image.load('spaceship.png')
player_x = 370
player_y = 480
player_movement_x = 0
player_movement_y = 0


# Enemy
enemy_model = []
enemy_x = []
enemy_y = []
enemy_movement_x = []
enemy_movement_y = []
max_enemies = 6

for i in range(max_enemies):
    enemy_model.append(pygame.image.load("alien.png"))
    enemy_x.append(random.randint(0, 725))
    enemy_y.append(random.randint(50, 100))
    enemy_movement_x.append(0.3)
    enemy_movement_y.append(40)

# Projectile
projectile_model = pygame.image.load("bullet.png")
# Starting coordinates
projectile_x = player_x
projectile_y = player_y
projectile_movement_x = 0
projectile_movement_y = 2
projectile_state = "ready"

score_value = 0
font = pygame.font.Font("freesansbold.ttf", 32)

score_x = 350
score_y = 10

game_over_x = 200
game_over_y = 250

game_over_font = pygame.font.Font("freesansbold.ttf", 64)

def show_score(position_x, position_y):
    score = font.render("Score :" + str(score_value), True, (255, 255, 255))
    screen.blit(score, (position_x, position_y))

def game_over(position_x, position_y):
    game_over_text = game_over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(game_over_text, (position_x, position_y))

def player(position_x, position_y):
    screen.blit(player_model, (position_x, position_y))


def enemy(position_x, position_y, i):
    screen.blit(enemy_model[i], (position_x, position_y))


def projectile_release(position_x, position_y):
    global projectile_state
    projectile_state = "fire"
    screen.blit(projectile_model, (position_x + 15, position_y + 15))


def collision(enemy_x, enemy_y, variable_x, variable_y):
    distance = math.sqrt(math.pow(enemy_x - variable_x, 2) + (math.pow(enemy_y - variable_y, 2)))
    if distance < 30:
        return True
    else:
        return False


# Game Loop
running = True
while running:

    # Reminder: Screen first before any of the elements, it'll overlap the elements if you added it after anything else
    # RGB = Red, Green, Blue
    screen.fill((0, 0, 0))
    # Background
    screen.blit(background, (0, 0))

    # Quit Function
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Check if a button is pressed on the keyboard
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_movement_x = -0.5
            if event.key == pygame.K_RIGHT:
                player_movement_x = 0.5
            if event.key == pygame.K_UP:
                player_movement_y = -0.5
                #print("Up button works")
            if event.key == pygame.K_DOWN:
                player_movement_y = 0.5
                #print("Down button works")
            if event.key == pygame.K_SPACE:
                if projectile_state is "ready":
                    #projectile_audio = mixer.Sound("projectile_audio.wav")
                    #projectile_audio.play()

                    projectile_x = player_x
                    projectile_y = player_y
                    projectile_release(projectile_x, projectile_y)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                player_movement_x = 0
                player_movement_y = 0

    # Player Movement
    player_x = player_x + player_movement_x
    player_y = player_y + player_movement_y
    if player_x <= 0:
        player_x = 0
    elif player_x >= 725:
        player_x = 725
    elif player_y <= 10:
        player_y = 10
    elif player_y >= 525:
        player_y = 525

    # Enemy Movement
    for i in range(max_enemies):

        """
        #Game Over
        if enemy_y[i] > 200:
            for j in range(max_enemies):
                enemy_y[j] = 2000
            game_over(game_over_x, game_over_y)
            break
        """


        player_col = collision(enemy_x[i], enemy_y[i], player_x, player_y)
        if player_col:

            for j in range(max_enemies):
                enemy_y[j] = 2000
            print("You lost Dipshit")

            game_over(game_over_x, game_over_y)
            running = False


        enemy_x[i] = enemy_x[i] + enemy_movement_x[i]
        if enemy_x[i] <= 0:
            enemy_movement_x[i] = 0.3
            enemy_y[i] = enemy_y[i] + enemy_movement_y[i]
        elif enemy_x[i] >= 725:
            enemy_movement_x[i] = -0.3
            enemy_y[i] = enemy_y[i] + enemy_movement_y[i]

        # Collision
        col = collision(enemy_x[i], enemy_y[i], projectile_x, projectile_y)
        if col:
            #collision_audio = mixer.Sound("collision_audio.wav")
            #collision_audio.play()

            projectile_y = player_y
            projectile_state = "ready"
            score_value = score_value + 1
            print(score_value)

            enemy_x[i] = random.randint(0, 725)
            enemy_y[i] = random.randint(50, 150)

        enemy(enemy_x[i], enemy_y[i], i)

    # Bullet Movement
    if projectile_y <= 0:
        projectile_y = player_y
        projectile_state = "ready"

    if projectile_state is "fire":
        projectile_release(projectile_x, projectile_y)
        projectile_y = projectile_y - projectile_movement_y

    player(player_x, player_y)
    show_score(score_x, score_y)
    pygame.display.update()

    #Is this good enough
