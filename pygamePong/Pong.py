import pygame, random
from pygame.locals import *

pygame.init()
pygame.display.set_caption('Pong')

icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 155, 0)
blue = (0, 0, 255)

display_width = 850
display_height = 600
FPS = 60
paddle_width = 15
paddle_height = 80
ball_width = 15

clock = pygame.time.Clock()
gameDisplay = pygame.display.set_mode((display_width, display_height))
overlayDisplay = pygame.Surface((display_width, display_height))
alpha = overlayDisplay.set_alpha(105)
overlayDisplay.fill((255, 255, 255))

# INTRO SCREEN
def gameIntro():
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN :
                if event.key == pygame.K_c :
                    intro = False
                elif event.key == pygame.K_q :
                    pygame.quit()
                    quit()
        gameDisplay.fill(black)
        label("Pong" , white , -150 , 'large')
        label("Player 1  -  UP andp DOWN Arrows", white, -40, 'medium')
        label("Player 2  -  W and S Keys", white, 0 , 'medium')
        label("[C] = Play    [P] = Pause    [Q] = Quit", white, 100, 'small')
        label("Made By : Veer Vohra", black, 200, 'small')
        pygame.display.update()
        clock.tick(15)

def draw_dashed_line(surf, color, start_pos, end_pos, width=1, dash_length=10):
    x1, y1 = start_pos
    x2, y2 = end_pos
    dl = dash_length

    if (x1 == x2):
        ycoords = [y for y in range(y1, y2, dl if y1 < y2 else -dl)]
        xcoords = [x1] * len(ycoords)
    elif (y1 == y2):
        xcoords = [x for x in range(x1, x2, dl if x1 < x2 else -dl)]
        ycoords = [y1] * len(xcoords)
    else:
        a = abs(x2 - x1)
        b = abs(y2 - y1)
        c = round(math.sqrt(a**2 + b**2))
        dx = dl * a / c
        dy = dl * b / c

        xcoords = [x for x in numpy.arange(x1, x2, dx if x1 < x2 else -dx)]
        ycoords = [y for y in numpy.arange(y1, y2, dy if y1 < y2 else -dy)]

    next_coords = list(zip(xcoords[1::2], ycoords[1::2]))
    last_coords = list(zip(xcoords[0::2], ycoords[0::2]))
    for (x1, y1), (x2, y2) in zip(next_coords, last_coords):
        start = (round(x1), round(y1))
        end = (round(x2), round(y2))
        pygame.draw.line(surf, color, start, end, width)

# pause
def pause():
    pause = True
    if pause == True:
        gameDisplay.blit(overlayDisplay, (0 , 0))
        label("GAME PAUSED" , black , -100 , 'medium')
        label("Press [C] to continue or [Q] to quit" , black , 25 , 'small')
        label("Press [R] to restart" , black , 55 , 'small')
        pygame.display.update()
        clock.tick(5)
    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    pause = False
                elif event.key == pygame.K_r:
                    gameLoop()
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()

# Font sizes
smallFont = pygame.font.Font("VT323-Regular.ttf", 30)
scoreFont = pygame.font.Font("VT323-Regular.ttf", 40)
medFont = pygame.font.Font("ka1.ttf", 25)
largeFont = pygame.font.Font("ARCADER.TTF", 90)

# Font scheme
def text_object(text , colour , size):
    if size == 'small':
        textSurface = smallFont.render(text, True, colour)
    elif size == 'medium':
        textSurface = medFont.render(text, True, colour)
    if size == 'large':
        textSurface = largeFont.render(text, True, colour)
    return textSurface , textSurface.get_rect()

# Label placement
def label(message, colour, y_displace=0, size='small') :
    textSurf, textRect = text_object(message, colour, size)
    textRect.center = (display_width / 2), ((display_height / 2) + y_displace)
    gameDisplay.blit(textSurf, textRect)


# Actual Game
def gameLoop():
    ball_pos = [400, 300]
    ball_start_speed = random.choice([6, (-6), 5, (-5)])
    ball_velocity = [ball_start_speed, ball_start_speed]
    player_one = [(display_width - 20), (display_height/2)]
    player_two = [5, (display_height/2)]
    one_change = 0
    two_change = 0
    one_score = 0
    two_score = 0
    pygame.display.update()

    gameExit = False
    while not gameExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            # Responding to keyboard events
            if event.type == KEYDOWN :
                if event.key == pygame.K_UP :
                    one_change = -5
                if event.key == pygame.K_DOWN :
                    one_change = 5
                if event.key == pygame.K_w :
                    two_change = -5
                if event.key == pygame.K_s :
                    two_change = 5
                if event.key == pygame.K_p :
                    pause()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    one_change = 0
                if event.key == pygame.K_w or event.key == pygame.K_s:
                    two_change = 0

        gameDisplay.fill(black)

        player_one[1] += one_change
        player_two[1] += two_change

        if player_one[1] + one_change <= 0 or player_one[1] + one_change + paddle_height > display_height:
            one_change = 0
        if player_two[1] + two_change <= 0 or player_two[1] + two_change + paddle_height > display_height:
            two_change = 0

        player_one[1] += one_change
        player_two[1] += two_change

        if ball_pos[1] >= (display_height - 10) or ball_pos[1] < 5:
            ball_velocity[1] = -(ball_velocity[1])

        if (ball_pos[0] + ball_velocity[0]) >= (player_one[0] - 10) and (ball_pos[1] + ball_velocity[1]) >= (player_one[1]) and (ball_pos[1] + ball_velocity[1]) <= (player_one[1] + paddle_height):
            ball_velocity[0] = -(ball_velocity[0])
            ball_velocity[0] *= 1.05
            ball_velocity[1] *= 1.05
        elif (ball_pos[0] + ball_velocity[0]) <= (player_two[0] + 10) and (ball_pos[1] + ball_velocity[1]) >= (player_two[1]) and (ball_pos[1] + ball_velocity[1]) <= (player_two[1] + paddle_height):
            ball_velocity[0] = -(ball_velocity[0])
            ball_velocity[0] *= 1.05
            ball_velocity[1] *= 1.05

        ball_pos[0] += ball_velocity[0]
        ball_pos[1] += ball_velocity[1]

        if ball_pos[0] < (player_two[0]):
            one_score += 1
            ball_pos = [400, 300]
            ball_start_speed = random.choice([6, (-6), 5, (-5)])
            ball_velocity = [ball_start_speed, ball_start_speed]
            player_one = [(display_width - 20), (display_height / 2)]
            player_two = [5, (display_height / 2)]
        elif ball_pos[0] > (player_one[0]):
            two_score += 1
            ball_pos = [400, 300]
            ball_start_speed = random.choice([6, (-6), 5, (-5)])
            ball_velocity = [ball_start_speed, ball_start_speed]
            player_one = [(display_width - 20), (display_height / 2)]
            player_two = [5, (display_height / 2)]

        pygame.draw.rect(gameDisplay, white, [ball_pos[0], ball_pos[1], ball_width, ball_width])

        pygame.draw.rect(gameDisplay, white, [player_one[0], player_one[1], paddle_width, paddle_height])
        pygame.draw.rect(gameDisplay, white, [player_two[0], player_two[1], paddle_width, paddle_height])

        draw_dashed_line(gameDisplay, white, (display_width/2, 5), (display_width/2, display_height), 5, 20)

        one_text = scoreFont.render(str(one_score), True, white)
        two_text = scoreFont.render(str(two_score), True, white)
        gameDisplay.blit(one_text, [(display_width/2 + 35), 10])
        gameDisplay.blit(two_text, [(display_width/2 - 50), 10])

        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()
    quit()

gameIntro()
gameLoop()
