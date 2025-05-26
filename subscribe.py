import os
try:
    import pygame
except ImportError:
    os.system("pip install pygame")
    import pygame
#os.system("pip install pygame")
import sys, math

pygame.init()
displaySize = (320, 240)
display = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
pygame.display.set_caption("Coinx Kart")

clock = pygame.time.Clock()

decorWidth = 320*2
backdrop = pygame.image.load("images/backdrop.png").convert_alpha()
backdrop = pygame.transform.scale(backdrop, (decorWidth, backdrop.get_height()/backdrop.get_width()*decorWidth))

player = {"x":0 , "y":0 , "z":0, "dir":0}
cJumpSprite = pygame.image.load("images/player/chargedjump.png").convert_alpha()
cJumping = False
cJumpingTimer = 0
playerSprites = {"front":[pygame.image.load("images/player/forward.png").convert_alpha()],"left":[pygame.image.load("images/player/left.png").convert_alpha()],"right":[pygame.image.load("images/player/right.png").convert_alpha()],"charged":[cJumpSprite.subsurface(0,0,32,32),cJumpSprite.subsurface(32,0,32,32)], "driftingLeft":[pygame.image.load("images/player/left2.png").convert_alpha()], "driftingRight":[pygame.image.load("images/player/right2.png").convert_alpha()]}
keysPressed = {}
spd = 0.6
timer = 0
animSpeed = 10
drift = 0
drifting = False
driftingLeft = False

def updatePlayer():
    global cJumping, cJumpingTimer, drift, driftingLeft, drifting
    if not keysPressed[pygame.K_SPACE]:
        drifting = False
    if not cJumping and (not drifting or (driftingLeft and keysPressed[pygame.K_SPACE])) and (keysPressed[pygame.K_LEFT] or (driftingLeft and drifting)):
        player["dir"] += spd
        if pygame.K_SPACE in newKeys:
            drift = 0
            drifting = True
            driftingLeft = True
        elif keysPressed[pygame.K_SPACE] and drifting:
            drift += 1
            player["dir"] += spd/2
    elif not cJumping and (not drifting or (not driftingLeft and keysPressed[pygame.K_SPACE])) and (keysPressed[pygame.K_RIGHT] or (not driftingLeft and drifting)):
        player["dir"] -= spd
        if pygame.K_SPACE in newKeys:
            drift = 0
            drifting = True
            driftingLeft = False
        elif keysPressed[pygame.K_SPACE] and drifting:
            drift += 1
            player["dir"] -= spd/2
    else:
        if pygame.K_SPACE in newKeys:
            if not cJumping:
                cJumping = True
                cJumpingTimer = 0
        elif not keysPressed[pygame.K_SPACE]:
            if cJumpingTimer > 60 and cJumping:
                print('yoo')
            cJumping = False
        elif keysPressed[pygame.K_SPACE]:
            cJumpingTimer += 1

def drawPlayer():
    playerSprite = "front"
    if cJumping:
        playerSprite = "charged"
    elif drifting:
        if not driftingLeft:
            playerSprite = "driftingLeft"
        else:
            playerSprite = "driftingRight"
    elif keysPressed[pygame.K_LEFT]:
        playerSprite = "left"
    elif keysPressed[pygame.K_RIGHT]:
        playerSprite = "right"
    sprite = playerSprites[playerSprite][math.floor(timer/animSpeed)%len(playerSprites[playerSprite])]
    screen.blit(sprite, (screen.get_width()/2-sprite.get_width()/2, screen.get_height()/2-sprite.get_height()/2))

while True:
    screen = pygame.surface.Surface(displaySize)
    newKeys = []
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            newKeys.append(event.key)

    keysPressed = pygame.key.get_pressed()
    timer += 1

    updatePlayer()

    screen.fill((0, 0, 0))
    display.fill((0, 0, 0))
    vdx = player['dir']
    if vdx < 0:
        vdx *= -1
        vdx = vdx%decorWidth
        vdx *= -1
    else:
        vdx = vdx%decorWidth
    screen.blit(backdrop, (vdx-decorWidth, 0))
    screen.blit(backdrop, (vdx, 0))
    screen.blit(backdrop, (vdx+decorWidth, 0))
    drawPlayer()

    ratio = screen.get_width()/screen.get_height()
    scale = min(display.get_width()/screen.get_width(), display.get_height()/screen.get_height())
    newScreen = pygame.transform.scale(screen, (int(screen.get_width()*scale), int(screen.get_height()*scale)))
    difX = display.get_width()/2 - newScreen.get_width()/2
    difY = display.get_height()/2 - newScreen.get_height()/2
    display.blit(newScreen, (difX, difY))

    pygame.display.flip()
    clock.tick(60)