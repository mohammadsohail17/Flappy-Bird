import random
import sys
import pygame#set of Python modules designed for developing video games
from pygame.locals import * 

#global variable
FPS=32
SCREENHEIGHT=511
SCREENWIDTH=289
SCREEN=pygame.display.set_mode((SCREENWIDTH,SCREENHEIGHT))#game window
GROUNDY=SCREENHEIGHT*0.8
GAME_SPIRTES={}
GAME_SOUNDS={}
PLAYER='gallery/sprites/bird.png'#LOCATION OF BIRD IMAGE
CHOICE=['gallery/sprites/background.png','gallery/sprites/background1.png']
BACKGROUND=random.choice(CHOICE)#LOCATION OF BACKGROUND IMAGE
PIPE='gallery/sprites/pipe.png'#LOCATION OF PIPE IMAGE

def welcomescreen():
    
    
    playerx=int(SCREENWIDTH/5)
    playery=int((SCREENWIDTH-GAME_SPIRTES['player'].get_height())/2)
    messagex=int((SCREENWIDTH - GAME_SPIRTES['message'].get_width())/2)
    messagey=int(SCREENHEIGHT*0.08)
    basex=0
    
    while True:
        for event in pygame.event.get():
            #if we cross we exit the game 
            if event.type==QUIT or (event.type == KEYDOWN and event.key==K_ESCAPE):
                pygame.quit()#to exit the game
                sys.exit()#to end execution of the code
            #to start the game
            elif event.type==KEYDOWN and (event.key==K_UP or event.key==K_SPACE):
                return
            else:
                 SCREEN.blit(GAME_SPIRTES['background'], (0, 0)) #blit is used to put image on another   
                 SCREEN.blit(GAME_SPIRTES['player'], (playerx, playery))    
                 SCREEN.blit(GAME_SPIRTES['message'], (messagex,messagey ))    
                 SCREEN.blit(GAME_SPIRTES['base'], (basex, GROUNDY))    
                 pygame.display.update()
                 FPSCLOCK.tick(FPS)

def mainGame():
    score=0
    playerx=int(SCREENWIDTH/5)
    playery=int(SCREENWIDTH/2)
    basex=0
    #creating 2 pipes for bliting on the screen
    newPipe1=getRandomPipe()
    newPipe2=getRandomPipe()
    
    upperPipes=[
        {'x': SCREENWIDTH+200, 'y':newPipe1[0]['y']},
        {'x': SCREENWIDTH+200+(SCREENWIDTH/2), 'y':newPipe2[0]['y']},
    ]


    lowerPipes=[
        {'x': SCREENWIDTH+200, 'y':newPipe1[1]['y']},
        {'x': SCREENWIDTH+200+(SCREENWIDTH/2), 'y':newPipe2[1]['y']},
    ]
    pipeVelX = -4#velocity of pipe in x direction

    playerVelY = -9
    playerMaxVelY = 10#maximum velocity
    playerMinVelY = -8#minimum velocity
    playerAccY = 1#velocity when bird is falling

    playerFlapAccv = -8 # velocity while flapping
    playerFlapped = False # It is true only when the bird is flapping

    while True:
        for event in pygame.event.get():
            if event.type==QUIT or (event.type==KEYDOWN and event.key==K_ESCAPE):#to close the game if the player quits
                pygame.QUIT()
                sys.exit()
            if event.type==KEYDOWN and (event.key==K_UP or event.key==K_SPACE):#to start the game when we press space
                if playery>0:
                    playerVelY=playerFlapAccv
                    playerFlapped=True
                    GAME_SOUNDS['wing'].play()#to play the sound when the bird flaps
        crashTest=isCollide(playerx,playery,upperPipes,lowerPipes)#this function returns true if the bird has crashed
        if crashTest:
            return

        playerMidPos= playerx + GAME_SPIRTES['player'].get_width()/2#to know the players mid position
        for pipe in upperPipes:
            pipeMidPos=pipe['x']+GAME_SPIRTES['pipe'][0].get_width()/2#to the know the pipes mid position 
            if pipeMidPos<=playerMidPos<pipeMidPos+4:
                score+=1
                print(f"Your score is {score}")#F-strings provide a way to embed expressions inside string literals, using a minimal syntax
                GAME_SOUNDS['point'].play()#to play the sound when we get a point

        if playerVelY<playerMaxVelY and not playerFlapped:
            playerVelY+=playerAccY#if the player hasn't flapped the bird goes down with an acc of '1'
        if playerFlapped:
            playerFlapped=False
        playerHeight = GAME_SPIRTES['player'].get_height()
        playery = playery + min(playerVelY, GROUNDY - playery - playerHeight)#the bird should go down only till this position
#to move pipes to the left

        for upperPipe,lowerPipe in zip(upperPipes,lowerPipes):
            upperPipe['x']+=pipeVelX
            lowerPipe['x']+=pipeVelX

        #to add new pipes when the previous one is abt to cross the left most part of the screen
        if 0<upperPipes[0]['x']<5:
            newPipe=getRandomPipe()
            upperPipes.append(newPipe[0])
            lowerPipes.append(newPipe[1])

        #if the pipe is out of the screen it should be removed
        if upperPipes[0]['x']< -GAME_SPIRTES['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)

        #blitting of sprites
        SCREEN.blit(GAME_SPIRTES['background'],(0,0))

        for upperPipe,lowerPipe in zip(upperPipes,lowerPipes):
            SCREEN.blit(GAME_SPIRTES['pipe'][0], (upperPipe['x'], upperPipe['y']))
            SCREEN.blit(GAME_SPIRTES['pipe'][1], (lowerPipe['x'], lowerPipe['y']))
        SCREEN.blit(GAME_SPIRTES['base'],(basex,GROUNDY))
        SCREEN.blit(GAME_SPIRTES['player'],(playerx,playery))
        myDigits = [int(x) for x in list(str(score))]
        width = 0
        for digit in myDigits:
            width += GAME_SPIRTES['numbers'][digit].get_width()
        Xoffset = (SCREENWIDTH - width)/2

        for digit in myDigits:
            SCREEN.blit(GAME_SPIRTES['numbers'][digit], (Xoffset, SCREENHEIGHT*0.12))
            Xoffset += GAME_SPIRTES['numbers'][digit].get_width()
        pygame.display.update()
        FPSCLOCK.tick(FPS)
def isCollide(playerx, playery, upperPipes, lowerPipes):
    if playery> GROUNDY - 25  or playery<0:
        GAME_SOUNDS['hit'].play()
        return True
    
    for pipe in upperPipes:
        pipeHeight = GAME_SPIRTES['pipe'][0].get_height()
        if(playery < pipeHeight + pipe['y'] and abs(playerx - pipe['x']) < GAME_SPIRTES['pipe'][0].get_width()):
            GAME_SOUNDS['hit'].play()
            return True

    for pipe in lowerPipes:
        if (playery + GAME_SPIRTES['player'].get_height() > pipe['y']) and abs(playerx - pipe['x']) < GAME_SPIRTES['pipe'][0].get_width():
            GAME_SOUNDS['hit'].play()
            return True
    return False 
def getRandomPipe():
    #to generate position of random sized pipes we define this function and blit it on the screen 
    pipeHeight = GAME_SPIRTES['pipe'][0].get_height()#to get the height of the pipe
    offset = SCREENHEIGHT/3#minimum height of the pipe
    y2 = offset + random.randrange(0, int(SCREENHEIGHT - GAME_SPIRTES['base'].get_height()  - 1.2 *offset))
    pipeX = SCREENWIDTH + 10
    y1 = pipeHeight - y2 + offset
    pipe = [
        {'x': pipeX, 'y': -y1}, #upper Pipe
        {'x': pipeX, 'y': y2} #lower Pipe
    ]
    return pipe



if __name__=="__main__":
    #game starts from here
    pygame.init()#to initialize all game modules
    FPSCLOCK=pygame.time.Clock()
    pygame.display.set_caption("Flappy Bird")
    GAME_SPIRTES['numbers']=(
        pygame.image.load('gallery/sprites/0.png').convert_alpha(),
        pygame.image.load('gallery/sprites/1.png').convert_alpha(),
        pygame.image.load('gallery/sprites/2.png').convert_alpha(),
        pygame.image.load('gallery/sprites/3.png').convert_alpha(),
        pygame.image.load('gallery/sprites/4.png').convert_alpha(),
        pygame.image.load('gallery/sprites/5.png').convert_alpha(),
        pygame.image.load('gallery/sprites/6.png').convert_alpha(),
        pygame.image.load('gallery/sprites/7.png').convert_alpha(),
        pygame.image.load('gallery/sprites/8.png').convert_alpha(),
        pygame.image.load('gallery/sprites/9.png').convert_alpha(),
    )
    GAME_SPIRTES['message']=pygame.image.load('gallery/sprites/message.png').convert_alpha()
    GAME_SPIRTES['base'] =pygame.image.load('gallery/sprites/base.png').convert_alpha()
    GAME_SPIRTES['pipe']=(pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(),180),
    pygame.image.load(PIPE).convert_alpha())
    # Game sounds
    GAME_SOUNDS['die'] = pygame.mixer.Sound('gallery/audio/die.wav')
    GAME_SOUNDS['hit'] = pygame.mixer.Sound('gallery/audio/hit.wav')
    GAME_SOUNDS['point'] = pygame.mixer.Sound('gallery/audio/point.wav')
    GAME_SOUNDS['swoosh'] = pygame.mixer.Sound('gallery/audio/swoosh.wav')
    GAME_SOUNDS['wing'] = pygame.mixer.Sound('gallery/audio/wing.wav')

    GAME_SPIRTES['background'] = pygame.image.load(BACKGROUND).convert()
    GAME_SPIRTES['player'] = pygame.image.load(PLAYER).convert_alpha()
    while True:
        welcomescreen()#to show welcome screen until we press anything
        mainGame()#main game function