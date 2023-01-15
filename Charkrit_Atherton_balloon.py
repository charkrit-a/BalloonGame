#!.venv\Scripts\python
'''
Charkrit Atherton, 2022

Balloon Game for Junior Engineers Tutor Application

Python 3.11.1
Required modules:
    - pygame-2.1.3.dev8
'''

import os
import pygame #pygame v2.1.3.dev8
import random

def main():
    '''main function'''

    # initialise pygame 
    pygame.init()
    pygame.font.init()

    # Load assets
    balloon = pygame.image.load(os.path.join('Assets', 'Balloon.jpeg'))
    gun = pygame.image.load(os.path.join('Assets', 'Gun.jpg'))
    dart = pygame.image.load(os.path.join('Assets', 'Dart.jpg'))
    font = pygame.font.Font(os.path.join('Assets', 'ComicSansMS3.ttf'), 32)

    # setup display
    pygame.display.set_caption("Charkrit Atherton - Balloon")
    pygame.display.set_icon(balloon)
    
    # create screen
    screen = pygame.display.set_mode((800,500))

    # input and event settings
    pygame.key.set_repeat(200, 10)
    pygame.time.set_timer(pygame.USEREVENT, 10) # setup user event every 10ms

    # variables
    balloonPos = [30,250]
    balloonSpeed = 1
    balloonDir = 1
    balloonDirChange = 0
    gunPos = [670,250]
    bullets = []
    bulletsMissed = 0

    run = True
    state = 0
    while run:
        screen.fill((255, 255, 255)) # fill white

        if state == 0:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: run = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        state = 1

            text = font.render(f'Press Space To Start...', True, (0,0,0))
            screen.blit(text, (250, 220))
        
        elif state == 1:
            # handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT: run = False
                
                # handle inputs
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        if gunPos[1] > 10:
                            gunPos[1] -= 2
                    elif event.key == pygame.K_DOWN:
                        if gunPos[1] < 390:
                            gunPos[1] += 2
                    elif event.key == pygame.K_SPACE:
                        bullets.append([620, gunPos[1]])

                if event.type == pygame.USEREVENT: # every 10ms
                    # do balloon movement
                    balloonSpeed = 1
                    if balloonPos[1] <= 40:
                        balloonDir = 0
                        balloonDirChange = 0
                    elif balloonPos[1] >= 380:
                        balloonDir = 1
                        balloonDirChange = 0
                    elif (balloonDirChange > 100):
                        balloonDir = random.randint(0, 1) # 0 is down, 1 is up
                        balloonDirChange = 0
                    else:
                        balloonDirChange += 1
                    if balloonDir == 1:
                        balloonPos[1] -= balloonSpeed
                    else:
                        balloonPos[1] += balloonSpeed

                    # do bullet movement
                    for idx, b in enumerate(bullets):
                        if b[0] < -80:
                            bullets.pop(idx)
                            bulletsMissed += 1
                        elif (b[0] == 100) and (balloonPos[1]-40 < b[1] < balloonPos[1]+40) and \
                        balloonPos[0] > 0:
                            bullets.pop(idx)
                            balloonPos[0] = -80
                            state = 2
                        b[0] -= 10

            # draw objects on screen
            screen.blit(gun, gunPos)
            screen.blit(balloon, balloonPos)
            for b in bullets:
                screen.blit(dart, b)
            text = font.render(f'Bullets Missed: {bulletsMissed}', True, (0,0,0))
            screen.blit(text, (250, 5))

        elif state == 2:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: run = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        run = False

            text = font.render(f'Game Over', True, (0,0,0))
            screen.blit(text, (250, 180))
            text = font.render(f'Bullets Missed: {bulletsMissed}', True, (0,0,0))
            screen.blit(text, (250, 220))
            text = font.render(f'Press Escape To Quit...', True, (0,0,0))
            screen.blit(text, (250, 260))

        # update frame
        pygame.display.flip()

    pygame.quit()

if __name__ == '__main__':
    main()