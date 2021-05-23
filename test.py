import sys, pygame
from block import Block
from player import Player
import os
os.environ['SDL_AUDIODRIVER'] = 'dsp'
pygame.init()

size = width, height = 800, 600
speed = [0, 1]
black = 0, 0, 0
RED = (255, 0, 0)

screen = pygame.display.set_mode(size)

#ball = pygame.image.load("intro_ball.gif")
ballrect = pygame.Rect(200, 200, 80, 80) #ball.get_rect()
square = Player(ballrect, speed, RED)

jumped = False
counter = 0
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    #ballrect = ballrect.move(speed)
    #if ballrect.left < 0 or ballrect.right > width:
    #    speed[0] = -speed[0]
    #if ballrect.top < 0 or ballrect.bottom > height:
    #    speed[1] = -speed[1]

    square.update()

    #if square.left() < 0 or square.right() > width:
    #    square.speed[0] = -speed[0]
    if square.top() < 0 or square.bottom() > height:

        square.speed[1] = 0#-square.speed[1]

    if (jumped == False and square.speed[1] == 0):
        counter += 1

    if (jumped == False and counter > 100):
        print("called")
        square.jump()
        jumped = True

    screen.fill(black)
    square.draw(screen)
    #screen.blit(ball, ballrect)
    #pygame.draw.rect(screen, RED, ballrect)
    pygame.display.flip()
