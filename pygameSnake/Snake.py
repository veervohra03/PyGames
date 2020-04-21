import pygame , time , random
from pygame.locals import *

pygame.init()
pygame.display.set_caption('Snake')

icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)

snake_head_img = pygame.image.load('snek_Head.png')
apple_img = pygame.image.load('apple.png')

black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
green = (0,155,0)
blue = (0,0,255)

display_width = 800
display_height = 600
FPS = 30
block_size = 21
AppleThickness = 32
direction = "right"

clock = pygame.time.Clock()
gameDisplay = pygame.display.set_mode((display_width, display_height))
overlayDisplay = pygame.Surface((800,600))
overlayDisplay.set_alpha(105)
overlayDisplay.fill((255 , 255 , 255))

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
        gameDisplay.fill(white)
        label("SNAKE" , green , -200 , 'large')
        label("Eat the apples to grow" , red , -60 , 'medium')
        label("Navigate with your arrow keys" , red , -20 , 'small')
        label("Don't eat your self" , black , 10 , 'small')
        label("Don't run into the edges" , black , 30 , 'small')
        label("Don't stop moving" , black , 50 , 'small')
        label("[C] = Play    [P] = Pause    [Q] = Quit" , black , 100 , 'small')
        label("Made By : Veer Vohra", black, 200, 'small')
        pygame.display.update()
        clock.tick(15)

# Choosing the random coordiantes of the apple
def randAppleGen():
    randApple_x = round(random.randrange(0 , display_width - AppleThickness))
    randApple_y = round(random.randrange(0 , display_height - AppleThickness))
    return randApple_x , randApple_y

# drawing the snake
def snake(block_size , snake_list):
    if direction == "right" :
        head = pygame.transform.rotate(snake_head_img , 270)
    if direction == "left" :
        head = pygame.transform.rotate(snake_head_img , 90)
    if direction == "up" :
        head = snake_head_img
    if direction == "down" :
        head = pygame.transform.rotate(snake_head_img , 180)
    gameDisplay.blit(head , (snake_list[-1][0] ,  snake_list[-1][1]) )
    for XnY in snake_list[:-1]:
        pygame.draw.rect(gameDisplay , green , [XnY[0] , XnY[1] , block_size , block_size])

# pause
def pause():
    pause = True
    if pause == True:
        gameDisplay.blit(overlayDisplay, (0 , 0))
        label("GAME PAUSED" , black , -100 , 'large')
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

# Score
def score(score):
    text = smallFont.render("Score : " + str(score) , True , black)
    gameDisplay.blit(text , [0,0])

# Font sizes
smallFont = pygame.font.Font("VT323-Regular.ttf", 25)
medFont = pygame.font.Font("ARCADER.TTF", 20)
largeFont = pygame.font.Font("ka1.ttf", 80)

# Font scheme
def text_object(text , colour , size):
    if size == 'small':
        textSurface = smallFont.render(text , True , colour)
    elif size == 'medium':
        textSurface = medFont.render(text , True , colour)
    if size == 'large':
        textSurface = largeFont.render(text , True , colour)
    return textSurface , textSurface.get_rect()

# Label placement
def label(message , colour, y_displace=0 , size = 'small') :
    textSurf , textRect = text_object(message , colour , size)
    textRect.center = (display_width / 2) , ((display_height / 2) + y_displace)
    gameDisplay.blit(textSurf , textRect)

# Actual Game
def gameLoop():
    global direction
    lead_x = display_width / 2
    lead_y = display_height / 2
    lead_x_change = 10
    lead_y_change = 0
    gameExit = False
    gameOver = False
    randApple_x , randApple_y = randAppleGen()
    snake_list = []
    snake_length = 1
    direction = 'right'

    while not gameExit:
        # GAME OVER
        if gameOver == True:
            gameDisplay.blit(overlayDisplay, (0 , 0))
            label("GAME OVER" , red , -40 , "large")
            label("Press [C] to PLAY AGAIN OR press [Q] to QUIT" , black , 30 , "small")
            label("Score : " + str(snake_length - 1) , black , 70 , "medium")
            pygame.display.update()

        while gameOver == True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    gameOver == False
                    gameExit = True
                if event.type == pygame.KEYDOWN :
                    if event.key == pygame.K_q :
                        gameExit = True
                        gameOver = False
                    elif event.key == pygame.K_c :
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            # Responding to keyboard events
            if event.type == KEYDOWN :
                if event.key == pygame.K_LEFT :
                    if direction != 'left':
                        lead_x_change -= block_size / 2
                        lead_y_change = 0
                        direction = 'left'
                elif event.key == pygame.K_RIGHT :
                    if direction != 'right':
                        lead_x_change += block_size / 2
                        lead_y_change = 0
                        direction = 'right'
                elif event.key == pygame.K_UP :
                    if direction != 'up':
                        lead_y_change -= block_size / 2
                        lead_x_change = 0
                        direction = 'up'
                elif event.key == pygame.K_DOWN :
                    if direction != 'down':
                        lead_y_change += block_size / 2
                        lead_x_change = 0
                        direction = 'down'
                elif event.key == pygame.K_p :
                    pause()
                    counter = 3
                    while counter > 0 :
                        gameDisplay.fill(white)
                        pygame.display.flip()
                        label(str(counter) , black , 0 , 'large')
                        pygame.display.flip()
                        time.sleep(1)
                        counter -= 1

        # Checking if the user is ded
        if lead_x >= display_width or lead_x < 0 or lead_y >= display_height or lead_y < 0:
            gameOver = True
        if lead_x_change == 0 and lead_y_change == 0:
            gameOver = True

        lead_x += lead_x_change
        lead_y += lead_y_change

        gameDisplay.fill(white) # fills the screen with the colour white

        # Drawing the apple
        #pygame.draw.rect(gameDisplay , red , [randApple_x , randApple_y , AppleThickness , AppleThickness])
        gameDisplay.blit(apple_img , (randApple_x , randApple_y))

        # Lenghthening the snek
        snakeHead = []
        snakeHead.append(lead_x)
        snakeHead.append(lead_y)
        snake_list.append(snakeHead)

        if len(snake_list) > snake_length:
            del snake_list[0]

        for each_segment in snake_list[:-1] :
            if each_segment == snakeHead:
                gameOver = True

        snake(block_size , snake_list)

        score(snake_length - 1)

        pygame.display.update()

        # Checking for Snek-Apple collision
        if lead_x > randApple_x and lead_x < (randApple_x + AppleThickness) or (lead_x + block_size) > randApple_x and (lead_x + block_size) < (randApple_x + AppleThickness):
            if lead_y > randApple_y and lead_y < (randApple_y + AppleThickness):
                randApple_x , randApple_y = randAppleGen()
                snake_length += 1
            elif (lead_y + block_size) > randApple_y and (lead_y + block_size) < (randApple_y + AppleThickness):
                randApple_x , randApple_y = randAppleGen()
                snake_length += 1

        clock.tick(FPS)

    pygame.quit()
    quit()

gameIntro()
gameLoop()
