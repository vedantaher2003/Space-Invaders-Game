from turtle import width
import pygame
import random
import math
from pygame import mixer

# Intialization of pygame
pygame.init()

# Creation of screen
screen=pygame.display.set_mode((800,600)) #(width,height)

# Background
background=pygame.image.load("space.jpg")

# Background Sound
'''mixer.music.load("bgmusic.mp3")
mixer.music.play(-1)'''

# Title and Icon
pygame.display.set_caption("Space Inviders")
icon=pygame.image.load("ufo.png")
pygame.display.set_icon(icon)

#Player
playerImg=pygame.image.load("spaceship.png")
playerX=370
playerY=480
playerX_change=0
playerY_change=0

#Enemy
enemyImg=[]
enemyX=[]
enemyY=[]
enemyX_change=[]
enemyY_change=[]
no_of_enemies=5

for i in range(no_of_enemies):
    enemyImg.append(pygame.image.load("enemy.png"))
    enemyX.append(random.randint(0,735))
    enemyY.append(random.randint(0,150))
    enemyX_change.append(0.8)
    enemyY_change.append(0.8)

# Bullet
# Ready : you can't see the bullet on the screen
# Fire : the bullet is currently moving
bulletImg=pygame.image.load("bullet.png")
bulletX=0
bulletY=480
bulletX_change=0
bulletY_change=0.8
bullet_state="ready"

# Score
score_value=0
font = pygame.font.Font("freesansbold.ttf",32)
textX=10
textY=10

def show_score(x,y):
    score=font.render("Score : "+str(score_value),True,(255,255,255))
    screen.blit(score,(x,y))

def player(x,y):
    screen.blit(playerImg,(x,y))

def enemy(x,y,i):
    screen.blit(enemyImg[i],(x,y))

def fire_bullet(x,y):
    global bullet_state
    bullet_state="fire"
    screen.blit(bulletImg,(x+16,y+10))

def isCollision(enemyX,enemyY,bulletX,bulletY):
    distance=math.sqrt((math.pow(enemyX-bulletX,2))+(math.pow(enemyY-bulletY,2)))
    if distance < 27:
        return True
    else:
        return False

# Game loop
running=True

while(running):

    #RGB-Red,Green,Blue
    screen.fill((0,0,0))

    #Background
    screen.blit(background,(0,0))

    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
        
        #keystroke
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_LEFT:
                playerX_change=-0.6
            if event.key==pygame.K_RIGHT:
                playerX_change=0.6
            if event.key==pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_sound=mixer.Sound("gunshot.wav")
                    bullet_sound.play()
                    bulletX=playerX
                    fire_bullet(bulletX,bulletY)
            
        if event.type==pygame.KEYUP:
            if event.key==pygame.K_LEFT or event.key==pygame.K_RIGHT or event.key==pygame.K_UP or event.key==pygame.K_DOWN:
                pass

    # Enemy event
    for i in range(no_of_enemies):
        # Enemy
        enemyX[i]+=enemyX_change[i]
        if enemyX[i]<=0:
            enemyX_change[i]=0.4
            enemyY[i]+=15
        elif enemyX[i]>=768:
            enemyX_change[i]=-0.4
            enemyY[i]+=15

        # Collision
        collision=isCollision(enemyX[i],enemyY[i],bulletX,bulletY)
        if collision:
            explosion_sound=mixer.Sound("explosion.wav")
            explosion_sound.play()
            bulletY=480
            bullet_state="ready"
            score_value+=1 
            print(score_value)
            enemyX[i]=random.randint(0,735)
            enemyY[i]=random.randint(50,150)

        enemy(enemyX[i],enemyY[i],i)

    # Player
    playerX+=playerX_change
    if playerX<=0:
        playerX=0
    elif playerX>=736:
        playerX=736

    playerY+=playerY_change
    if playerY<=0:
        playerY=0
    elif playerY>=536:
        playerY=536

    # Bullet Movement
    if bulletY<=0:
        bulletY=480
        bullet_state="ready"

    if bullet_state is "fire":
        fire_bullet(bulletX,bulletY)
        bulletY-=bulletY_change

    player(playerX,playerY)
    show_score(textX,textY)
    pygame.display.update()