import sys, pygame
from block  import Block
from player import Player
from frame  import Frame
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
player = Player(ballrect, speed, RED)

squarerect = pygame.Rect(230, 500, 80, 80)
square = Block(squarerect, [0, 0], (150, 150, 150))
blockmap = [[Block(pygame.Rect(0, 500, 80, 80), [-2, 0], (150, 150, 150))]]
for i in range(1, 12):
    thing = [Block(pygame.Rect(80 * i, 500, 80, 80), [-2, 0], (150, 150, 150))]
    blockmap.append(thing)

for i in range(100):
    thing = [Block(pygame.Rect(880, 500, 80, 80), [-2, 0], (150, 150, 150))]
    blockmap.append(thing)

for i in range(12, 20):
    thing = Block(pygame.Rect(880, 300, 80, 80), [-2, 0], (150, 150, 150))
    blockmap[i].append(thing)

frame = Frame(blockmap, 15)

jumped    = False
speed     = 5 # / max_count
max_count = 5
count     = 0
counter   = 0
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    #ballrect = ballrect.move(speed)
    #if ballrect.left < 0 or ballrect.right > width:
    #    speed[0] = -speed[0]
    #if ballrect.top < 0 or ballrect.bottom > height:
    #    speed[1] = -speed[1]



    count += 1
    if (count <= speed):
        player.update()
        square.update()
        frame.update()
        keys = pygame.key.get_pressed()
        current_blocks = frame.getRelevantBlocks()
        for block in current_blocks:
            if Block.isOnTop(player, block):
                player.speed[1] = 0
                Block.snapOnTop(player, block)
                if keys[pygame.K_UP]:
                    player.jump()
                    #jumped = True
                #square.speed = [-2, 0]
        #if player.top() < 0 or player.bottom() > height:
        #    player.speed[1] = 0#-player.speed[1]

        #if (jumped == False and player.speed[1] == 0):
        #    counter += 1

        #if (jumped == False and counter > 250):
        #    print("called")
        #    player.jump()
        #    jumped = True

    elif (count >= max_count):
        count = 0
    

    #if player.left() < 0 or player.right() > width:
    #    player.speed[0] = -speed[0]
    
    screen.fill(black)
    player.draw(screen)
    square.draw(screen)
    frame.draw(screen)
    #screen.blit(ball, ballrect)
    #pygame.draw.rect(screen, RED, ballrect)
    pygame.display.flip()
