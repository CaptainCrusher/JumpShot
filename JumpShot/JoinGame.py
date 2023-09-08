import pygame, sys, math, random, classes, write2file, read
from pygame.locals import *
from classes import *
from write2file import *
from read import *

WINDOWWIDTH = 1200
WINDOWHEIGHT = 800
TEXTCOLOR = (0, 0, 0)
BACKGROUNDCOLOR = (230, 230, 230)
MOUSEUP = 6
MOUSEDOWN = 5
scene = "game"
mousePressed = False
mouseX = 0
mouseY = 0
FPS = 60
pygame.init()
mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('Jump Shot Remastered')

keys = []
for i in range(100000):
 keys.append(False)

SPACE = 32
BACKSPACE = 8
ENTER = 13
PERIOD = 46
COMMA = 44
QUESTION = 47
EXCLAMATION = 49
LSHIFT = 304
RSHIFT = 303
QUOTE = 39
NUMPAD_LEFT = 260
NUMPAD_RIGHT = 262
NUMPAD_UP = 264
frameCount = 0


def drawText(text, font, col, surface, x, y, **kwargs):
    angle = kwargs.get("angle", 0)
    textobj = pygame.transform.rotate(font.render(text, 1, col), angle)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)
def drawTextCorner(text, font, col, surface, x, y, **kwargs):
    angle = kwargs.get("angle", 0)
    textobj = pygame.transform.rotate(font.render(text, 1, col), angle)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)
def fontSize(size):
    return pygame.font.SysFont(None, size)

def keyListener():
    global mouseX
    global mouseY
    global keys
    global mousePressed
    event = pygame.event.get()
    if len(event) > 0:
        for i in range(len(event)):
            if event[i].type == KEYDOWN:
                #print(event[i].key)
                keys[event[i].key] = True
            elif event[i].type == KEYUP:
                keys[event[i].key] = False
            elif event[i].type == MOUSEDOWN:
                mousePressed = True
            elif event[i].type == MOUSEUP:
                mousePressed = False
            elif event[i].type == MOUSEMOTION:
                mouseX = event[i].pos[0]
                mouseY = event[i].pos[1]
            elif event[i].type == QUIT:
                pygame.quit()
                sys.exit()

while True:
    frameCount += 1;
    keyListener()
    windowSurface.fill(BACKGROUNDCOLOR)
    mainClock.tick(FPS)
    pygame.display.update()
