import pygame, sys, math, random, classes, write2file, read, linkedlist
from pygame.locals import *
from classes import *
from write2file import *
from read import *
from linkedlist.linked_list import *


WINDOWWIDTH = 1200
WINDOWHEIGHT = 800
TEXTCOLOR = (0, 0, 0)
BACKGROUNDCOLOR = (200, 200, 200)
MOUSEUP = 6
MOUSEDOWN = 5
scene = "game"
mousePressed = False
mouseX = 0
mouseY = 0
FPS = 30
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
    global gunOn
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

scene = "game"
maps = [
    [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 0, 0, 1, 3, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 4, 0, 0, 5, 1, 3, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 4, 0, 0, 0, 0, 5, 1, 3, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 4, 0, 0, 0, 0, 0, 0, 5, 1, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 4, 0, 0, 2, 1, 1, 3, 0, 0, 5, 1, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 4, 0, 0, 2, 1, 1, 1, 1, 3, 0, 0, 5, 1, 3, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], [1, 3, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 1, 1, 3, 0, 0, 0, 0, 0, 0, 0, 2, 1, 4, 0, 0, 2, 1, 4, 0, 0, 5, 1, 3, 0, 0, 5, 1, 3, 0, 0, 0, 0, 0, 2, 1, 1, 1, 3, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1], [1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 4, 0, 0, 2, 1, 4, 0, 0, 0, 0, 5, 1, 3, 0, 0, 5, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1], [1, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 1], [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 0, 0, 5, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 4, 0, 0, 0, 0, 5, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 4, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 0, 0, 0, 0, 5, 1, 1, 1, 1, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 1, 1, 1, 4, 0, 0, 0, 0, 1], [1, 0, 0, 0, 0, 0, 0, 0, 0, 5, 1, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 4, 0, 0, 0, 0, 0, 0, 0, 0, 1], [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 1, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 1, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 1, 1, 1, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], [1, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 0, 0, 0, 0, 0, 0, 0, 0, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]],
]
lvl = 0

aiMaps = [
    [[[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []], [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []], [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []], [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []], [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []], [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []], [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []], [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []], [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []], [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [3, 3, 3, 3, 3, 3, 3], [], [], [], [], [], [], [], [], [], [], [], [2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3], [2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3], [], [], [], [], [], [], [], [], [], [2, 2, 2, 2, 2, 2], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []], [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [3, 3, 3, 3, 3, 3], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [2, 2, 2, 2, 2, 2, 2], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []], [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [3, 3, 3, 3, 3, 3, 3, 3], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [2, 2, 2, 2, 2, 2], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []], [[], [], [], [], [], [], [], [], [], [3, 3, 3, 3, 3, 3], [], [], [], [], [2, 2, 2, 2, 2, 2, 2, 2], [], [2, 2, 2, 2, 2, 2], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [3, 3, 3, 3, 3, 3, 3], [], [3, 3, 3, 3, 3, 3, 3, 3, 3, 3], [], [], [], [], [2, 2, 2, 2, 2, 2], [], [], [], [], [], [], [], [], []], [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []], [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [3, 3, 3, 3, 3, 3, 3, 2, 2, 2, 2], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [3, 3, 3, 3, 3, 3, 2, 2, 2, 2, 2], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []], [[], [3, 3, 3, 3, 3, 3, 3], [], [], [], [], [], [], [], [], [], [], [], [], [3, 3, 3, 3, 3, 3, 3, 1, 1, 1, 1, 1, 1, 1], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1], [], [], [], [], [], [], [], [], [], [], [], [], [2, 2, 2, 2, 2, 2, 2, 2, 2], []], [[], [3, 3, 3, 3, 3, 3, 3, 3, 3], [], [], [], [], [], [], [], [2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [1, 1, 1, 1, 3, 3, 3, 3], [], [], [], [], [], [], [], [2, 2, 2, 2, 2, 2, 2, 2], []], [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []], [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [2, 2, 2, 2, 2, 2, 2], [], [], [], [], [], [], [], [], [], [], [], [2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3], [], [], [], [], [], [], [], [], [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 2, 2, 2, 2], [], [], [], [], [], [], [], [], [], [3, 3, 3, 3, 3, 3, 3, 3], [], [], [], [], [], [], [], [], [], [], [], [], [], []], [[], [], [], [], [], [2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [2, 2, 2, 2, 2, 3, 3, 3, 3], [], [], [], [], []], [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [3, 3, 3, 3, 3, 3], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [2, 2, 2, 2, 2, 2, 2, 2, 2], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []], [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []], [[], [3, 3, 3, 3, 3, 3, 3], [], [], [], [3, 3, 3, 3, 3, 3, 1, 1, 1, 1, 1], [], [], [], [2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3], [], [], [], [], [1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 3, 3, 3], [], [], [], [], [], [], [], [], [], [], [], [1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2], [], [], [], [3, 3, 3, 3, 3, 3, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1], [3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1], [], [], [], [], [], [], [], [], [], [], [], [], [], [1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2], [], [], [], [], [3, 3, 3, 3, 3, 3, 3, 2, 2, 2, 2, 2, 2], [], [], [], [2, 2, 2, 2, 2, 2, 1, 1, 1, 1], [], [], [], [2, 2, 2, 2, 2, 2, 2, 2], []], [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []], [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []], [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []], [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [2, 2, 2, 2, 2, 3, 3, 3, 3], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2], [1, 1, 1, 1, 1, 3, 3, 3, 3], [], [], [], [], [], [], [], [], [], [], [], [], [], [2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3], [], [], [], [], [], [], [], [], [], [], [], [], [], []], [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []], [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []], [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [3, 3, 3, 3, 3, 3, 3, 2, 2, 2, 2, 2, 2], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []], [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [1, 1, 1, 1, 1], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [1, 1, 1, 1, 1, 1, 1], [], [], [], [], [], [], [], [], [], [], [], [], [], []], [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []], [[], [], [], [], [], [], [], [], [], [], [2, 2, 2, 2, 2, 2, 3, 3, 3, 3], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [3, 3, 3, 3, 2, 2, 2, 2, 2], [], [], [], [], [], [], [], [], [], []], [[], [3, 3, 3, 3, 3, 3, 3], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [2, 2, 2, 2, 2, 2, 2], []], [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []]],
]

blocks = LinkedList()
aiStuff = LinkedList()
for col in range(len(maps[lvl])):
    for row in range(len(maps[lvl][col])):
        if maps[lvl][col][row] != 0:
            blocks.add_to_back([maps[lvl][col][row], row, col])
        if len(aiMaps[lvl][col][row]) > 0:
            aiStuff.add_to_back([[], row, col])
            for i in range(len(aiMaps[lvl][col][row])):
                a = aiMaps[lvl][col][row]
                if i == 0:
                    aiStuff.back.key[0].append(a[i])
                else:
                    if a[i] != a[i-1]:
                        aiStuff.back.key[0].append(a[i])
                    





players = LinkedList()
players.add_to_back(Player(100, 100, (0, 200, 230), 0, gun=0))
players.back.key.you = True
for i in range(9):
    print(i+1)
    players.add_to_back(Player(random.randint(50, WINDOWWIDTH-70), random.randint(50, WINDOWHEIGHT-170), (0, 200, 50), i+1, gun=0))
    nextId = i+2

bullets = LinkedList()

def friendly(col):
    if col == (0,200,230) or col == (0,0,255):
        return col == (0,200,230) or col == (0,0,255)
    elif col == (255,0,0) or col == (200,0,0):
        return col == (255,0,0) or col == (200,0,0)

def realPlayer(col):
    return col == (0,200,230) or col == (255,0,0)


def drawBullets(key, value):
    newKey = key
    pygame.draw.line(windowSurface, (0,0,0), (key[0], key[1]), (key[0]-(key[2]*min(math.sqrt(key[4]), 4)), key[1]-(key[3]*min(math.sqrt(key[4]), 4))), min(round(math.sqrt(key[4])), 5))
    newKey[0] += newKey[2]
    newKey[1] += newKey[3]
    return (newKey, value)

blockCol = []

def collideBullets(key, value):
    x = key[0]
    y = key[1]
    row = blockCol[1]
    col = blockCol[2]
    if blockCol[0] == 1:
        if x > row*blockSize and x < row*blockSize+blockSize and y > col*blockSize and y < col*blockSize+blockSize:
            return False
    elif blockCol[0] != 0:
        if pointInWedge(blockCol[0], row*blockSize, col*blockSize, x, y):
            return False
    return True



def printBullets(key, value):
    print(key)

def drawBlocks(key, value):
    global blockCol
    global bullets
    blockCol = key
    bullets.in_filter(collideBullets)
    row = key[1]
    col = key[2]
    if key[0] == 1:
        pygame.draw.rect(windowSurface, (100,100,100), (row*blockSize, col*blockSize, blockSize, blockSize))
    elif key[0] == 2:
        pygame.draw.polygon(windowSurface, (100,100,100), ((row*blockSize+blockSize, col*blockSize), (row*blockSize+blockSize, col*blockSize+blockSize), (row*blockSize,col*blockSize+blockSize)))
    elif key[0] == 3:
        pygame.draw.polygon(windowSurface, (100,100,100), ((row*blockSize, col*blockSize), (row*blockSize+blockSize, col*blockSize+blockSize), (row*blockSize,col*blockSize+blockSize)))
    elif key[0] == 4:
        pygame.draw.polygon(windowSurface, (100,100,100), ((row*blockSize, col*blockSize), (row*blockSize+blockSize, col*blockSize), (row*blockSize,col*blockSize+blockSize)))
    elif key[0] == 5:
        pygame.draw.polygon(windowSurface, (100,100,100), ((row*blockSize+blockSize, col*blockSize), (row*blockSize+blockSize, col*blockSize+blockSize), (row*blockSize,col*blockSize)))

playerInfo = LinkedList()
playerCol = 0
deadAI = LinkedList()
def collideWithPlayer(key, value):
    global playerInfo
    global deadAI
    if key[0] > playerCol.x and key[0] < playerCol.x+playerCol.w and key[1] > playerCol.y and key[1] < playerCol.y+playerCol.h:
        playerInfo.add_to_back([playerCol.id, "damage", key[4], key[5]])
        return False
    return True

def runDeadPlayers(key, value):
    return (key-1, value)

def spawn(key, value):
    if key <= 0:
        global nextId
        global players
        players.add_to_back(Player(random.randint(50, WINDOWWIDTH-70), random.randint(50, WINDOWHEIGHT-170), (0, 200, 50), nextId, gun=0))
        nextId += 1
        return False
    else:
        return True

def runPlayers(key, value):
    global bullets
    global playerCol
    global playerInfo
    global you
    playerInfo = key.draw(windowSurface, playerInfo)
    newKey = key
    newBullets = []
    if realPlayer(key.teamColor):
        newBullets = newKey.playPlayer(mousePressed, mouseX, mouseY, keys, blocks)
    else:
        newBullets = newKey.playAI(blocks, aiStuff, players)
    for bullet in newBullets:
        bullets.add_to_back(bullet)
    if key.you:
        you = key
    playerCol = key
    bullets.in_filter(collideWithPlayer)
    return (newKey, value)

def outOfHealth(key, value):
    if key.health < 0:
        global playerInfo
        playerInfo.add_to_back([key.lastShot, "kill", 0])
        if not key.you:
            deadAI.add_to_back(5*FPS)
        return False
    return True

blockSize = 20
you = players.back.key
while True:
    frameCount += 1;
    keyListener()
    windowSurface.fill(BACKGROUNDCOLOR)
    if scene == "game" or scene == "respawn":
        you = "dead"

        blocks.loop(drawBlocks)
        players.in_map(runPlayers)        
        bullets.in_map(drawBullets)
        players.in_filter(outOfHealth)
        deadAI.in_map(runDeadPlayers)
        deadAI.in_filter(spawn)

        if you == "dead":
            if scene == "game":
                scene = "respawn"
                respawnTimer = 5*FPS
        else:
            you.gun.draw(windowSurface, 0.1, [70, WINDOWHEIGHT-60], 0)
            drawTextCorner(you.gun.name, fontSize(20), (0,0,0), windowSurface, 130, WINDOWHEIGHT-55)
            pygame.draw.rect(windowSurface, (200,0,0), (10, WINDOWHEIGHT-15, you.health*3, 10))
            if you.delay < 0:
                pygame.draw.rect(windowSurface, (0,150,0), (10, WINDOWHEIGHT-30, 300-((max(you.delay, 0)/you.gun.firerate)*300), 10))
            else:
                pygame.draw.rect(windowSurface, (100,100,0), (10, WINDOWHEIGHT-30, 300-((max(you.delay, 0)/you.gun.firerate)*300), 10))
    if scene == "respawn":
        windowSurface.fill(BACKGROUNDCOLOR)
        respawnTimer -= 1
        if respawnTimer > 0:
            drawText("RESPAWN IN: " + str(math.ceil(respawnTimer/FPS)), fontSize(100), (0,0,0), windowSurface, WINDOWWIDTH/2, WINDOWHEIGHT/4)
        else:
            drawText("PRESS SPACE TO RESPAWN", fontSize(100), (0,0,0), windowSurface, WINDOWWIDTH/2, WINDOWHEIGHT/4)
            if keys[SPACE] or keys[ENTER] or keys[K_w]:
                players.add_to_back(Player(100, 100, (0, 200, 230), nextId, gun=0))
                players.back.key.you = True
                nextId += 1
                scene = "game"
                
    mainClock.tick(FPS)
    pygame.display.update()
