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
backdrop = pygame.image.load("images/maps/donut_plains_1.png").convert_alpha()
backdrop = pygame.transform.scale(backdrop, (decorWidth, backdrop.get_height()/backdrop.get_width()*decorWidth))

def splitTileSet(image, width=32, height=32) -> list:
    return [image.subsurface((x*width, y*height, width, height)) for x in range(image.get_width()//width) for y in range(image.get_height()//height)]

di = 0
def drawMap(dir):
    b = pygame.transform.rotate(backdrop, dir)
    d = 10
    stripHeight = screen.get_height()/40
    y = screen.get_height()-stripHeight
    pos = [0, 0]
    poses = []
    for i in range(40):
        s = pygame.Surface((d, stripHeight))
        s.fill((0, 0, 0))
        s.blit(b, (0, 0), (b.get_width()/2-screen.get_width()/2-d/2+pos[0], b.get_height()/2-screen.get_height()/2+pos[1], d, stripHeight))
        s = pygame.transform.scale(s, (screen.get_width(), stripHeight))
        screen.blit(s, (0, y))
        y -= stripHeight
        d += 2
        pos[0] += math.sin(math.radians(dir))*2
        pos[1] += math.cos(math.radians(dir))*2

while True:
    screen = pygame.surface.Surface(displaySize)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            elif event.key == pygame.K_F11:
                pygame.display.toggle_fullscreen()

    keysPressed = pygame.key.get_pressed()

    if keysPressed[pygame.K_LEFT]:
        di -= 1
    elif keysPressed[pygame.K_RIGHT]:
        di += 1

    drawMap(di)

    ratio = screen.get_width()/screen.get_height()
    scale = min(display.get_width()/screen.get_width(), display.get_height()/screen.get_height())
    newScreen = pygame.transform.scale(screen, (int(screen.get_width()*scale), int(screen.get_height()*scale)))
    difX = display.get_width()/2 - newScreen.get_width()/2
    difY = display.get_height()/2 - newScreen.get_height()/2
    display.blit(newScreen, (difX, difY))

    pygame.display.flip()
    clock.tick(60)
