import pygame, math, sys, random
from pygame.locals import *



def pointInWedge(wedge, wedgeX, wedgeY, pointX, pointY):
    blockSize = 20
    if pointX >= wedgeX and pointX <= wedgeX+blockSize and pointY >= wedgeY and pointY <= wedgeY+blockSize:
        if wedge == 2:
            return pointX+pointY > wedgeX+wedgeY+blockSize
        elif wedge == 3:
            return pointX-wedgeX < pointY-wedgeY
        elif wedge == 4:
            return pointX+pointY < wedgeX+wedgeY+blockSize
        elif wedge == 5:
            return pointX-wedgeX > pointY-wedgeY
        else:
            return True
    else:
        return False

class Player:

    def __init__(this, x, y, teamColor, player, **kwargs):
        this.x = x
        this.y = y
        this.w = kwargs.get("width", 20)
        this.h = kwargs.get("height", 20)
        this.hat = kwargs.get("hat", 0)
        this.gunOn = kwargs.get("gun", 0)
        this.gun = guns[this.gunOn]
        this.speed = kwargs.get("speed", 2.5)
        this.gravity = kwargs.get("gravity", 0.1)
        this.jumpHeight = kwargs.get("jumpHeight", 5)
        this.maxSpeed = kwargs.get("maxSpeed", 4)
        this.teamColor = teamColor
        this.cursor = [0,0]
        this.yVel = 0
        this.theKey = 0
        this.delay = random.randint(0, this.gun.firerate)
        this.dir = random.randint(0,4)
        if this.dir == 2:
            this.dir = 0
        this.id = player
        this.health = 100
        this.inBlock = False
        this.outOfBlock = True
        this.lastShot = player
        this.you = False
        this.kills = 0
        
    def loopInfo(this, key, value):
        if key[0] == this.id:
            if key[1] == "damage":
                this.health -= key[2]
                this.lastShot = key[3]
            elif key[1] == "kill":
                this.gunOn += 1
                if this.gunOn > len(guns)-1:
                    this.gunOn = len(guns)-1
                this.gun = guns[this.gunOn]
                this.health += 20
                this.kills += 1
            return False
        return True
        
    def draw(this, surface, playerInfo):
        pygame.draw.rect(surface, this.teamColor, (this.x,this.y,this.w,this.h))
        this.gun.draw(surface, 0.03, [this.x+this.w/2,this.y+this.h/2], math.atan2(this.cursor[1]-this.y, this.cursor[0]-this.x))
        return playerInfo.filter(this.loopInfo)
        
    def playPlayer(this, mouseState, mouseX, mouseY, keys, blocks):
        this.cursor = [mouseX, mouseY]
        if keys[K_a] or keys[K_LEFT]:
            this.x -= this.speed
            this.theKey = K_LEFT
        if keys[K_d] or keys[K_RIGHT]:
            this.x += this.speed
            this.theKey = K_RIGHT
        blocks.loop(this.Xcol)
        if (keys[K_w] or keys[K_UP]) and this.yVel == 0:
            this.yVel = -this.jumpHeight-0.001
        this.yVel += this.gravity
        if this.yVel > this.maxSpeed:
            this.yVel = this.maxSpeed
        this.y += this.yVel
        blocks.loop(this.Ycol)
        this.delay -= 1
        if mouseState and this.delay < 0:
            this.delay = this.gun.firerate
            returnArray = []
            for i in range(this.gun.shots):
                angle = math.atan2(this.cursor[1]-this.y-this.h/2, this.cursor[0]-this.x-this.w/2)
                spread = random.randrange(-this.gun.spread, this.gun.spread)*math.pi/180
                velX = math.cos(angle + spread)
                velY = math.sin(angle + spread)
                offsetX = math.cos(angle)
                offsetY = math.sin(angle)
                returnArray.append([this.x+offsetX*30+this.w/2, this.y+offsetY*30+this.h/2, velX*this.gun.bulletspeed, velY*this.gun.bulletspeed, this.gun.damage*100, this.id])
            return returnArray
        else:
            return []
            
    def playAI(this, blocks, aiTrigger, players):
        this.outOfBlock = True
        aiTrigger.loop(this.changeDir)
        this.inBlock = not this.outOfBlock
        this.closestPlayer = 1000000
        players.loop(this.shootClosestPlayer)
        if this.dir == 0 or this.dir == 1:
            this.x -= this.speed
            this.theKey = K_LEFT
        elif this.dir == 3 or this.dir == 4:
            this.x += this.speed
            this.theKey = K_RIGHT
        blocks.loop(this.Xcol)
        if (this.dir == 1 or this.dir == 2 or this.dir == 3) and this.yVel == 0:
            this.yVel = -this.jumpHeight-0.001
        this.yVel += this.gravity
        if this.yVel > this.maxSpeed:
            this.yVel = this.maxSpeed
        this.y += this.yVel
        blocks.loop(this.Ycol)
        this.delay -= 1
        if this.delay < 0:
            this.delay = this.gun.firerate
            returnArray = []
            for i in range(this.gun.shots):
                angle = math.atan2(this.cursor[1]-this.y-this.h/2, this.cursor[0]-this.x-this.w/2)
                spread = random.randrange(-this.gun.spread, this.gun.spread)*math.pi/180
                velX = math.cos(angle + spread)
                velY = math.sin(angle + spread)
                offsetX = math.cos(angle)
                offsetY = math.sin(angle)
                returnArray.append([this.x+offsetX*30+this.w/2, this.y+offsetY*30+this.h/2, velX*this.gun.bulletspeed, velY*this.gun.bulletspeed, this.gun.damage, this.id])
            return returnArray
        else:
            return []
            
    def shootClosestPlayer(this, key, value):
        if key.id != this.id:
            d = math.dist((this.x, this.y), (key.x, key.y))
            if d < this.closestPlayer:
                this.closestPlayer = d
                this.cursor[0] = key.x+key.w/2
                this.cursor[1] = key.y+key.h/2
                
            
    def changeDir(this, key, value):
        blockSize = 20
        row = key[1]
        col = key[2]
        if this.x+this.w > row*blockSize and this.x < row*blockSize+blockSize and this.y+this.h > col*blockSize and this.y < col*blockSize+blockSize:
            this.outOfBlock = False
            if not this.inBlock:
                options = key[0]
                dirOptions = []
                for option in options:
                    if option == 1:
                        dirOptions.append(2)
                    elif option == 2:
                        dirOptions.append(0)
                        dirOptions.append(1)
                    elif option == 3:
                        dirOptions.append(3)
                        dirOptions.append(4)
                this.dir = dirOptions[random.randint(0, len(dirOptions)-1)]
                this.inBlock = True
            
            
    def pointInBlock(this, blockX, blockY, pointX, pointY):
        blockSize = 20
        return pointX > blockX and pointX < blockX+blockSize and pointY > blockY and pointY < blockY+blockSize
    
    def Xcol(this, key, value):
        blockSize = 20
        row = key[1]
        col = key[2]
        if key[0] == 1:
            if this.x+this.w > row*blockSize and this.x < row*blockSize+blockSize and this.y+this.h > col*blockSize and this.y < col*blockSize+blockSize:
                if this.theKey == K_RIGHT:
                    this.x = row*blockSize-this.w
                elif this.theKey == K_LEFT:
                    this.x = row*blockSize+blockSize
        elif key[0] == 2:
            if pointInWedge(2, row*blockSize, col*blockSize, this.x, this.y) or pointInWedge(2, row*blockSize, col*blockSize, this.x+this.w, this.y) or pointInWedge(2, row*blockSize, col*blockSize, this.x, this.y+this.h):
                if this.theKey == K_LEFT:
                    this.x += this.speed
                elif this.theKey == K_RIGHT:
                    this.x -= this.speed
            elif pointInWedge(2, row*blockSize, col*blockSize, this.x+this.w, this.y+this.h):
                this.y -= this.speed
                this.yVel = 0
            elif this.pointInBlock(row*blockSize, col*blockSize, this.x+this.w, this.y):
                if this.theKey == K_LEFT:
                    this.x += this.speed
                elif this.theKey == K_RIGHT:
                    this.x -= this.speed
        elif key[0] == 3:
            if pointInWedge(3, row*blockSize, col*blockSize, this.x, this.y) or pointInWedge(3, row*blockSize, col*blockSize, this.x+this.w, this.y) or pointInWedge(3, row*blockSize, col*blockSize, this.x+this.w, this.y+this.h):
                if this.theKey == K_LEFT:
                    this.x += this.speed
                elif this.theKey == K_RIGHT:
                    this.x -= this.speed
            elif pointInWedge(3, row*blockSize, col*blockSize, this.x, this.y+this.h):
                this.y -= this.speed
                this.yVel = 0
            elif this.pointInBlock(row*blockSize, col*blockSize, this.x, this.y):
                if this.theKey == K_LEFT:
                    this.x += this.speed
                elif this.theKey == K_RIGHT:
                    this.x -= this.speed
        elif key[0] == 4:
            if pointInWedge(4, row*blockSize, col*blockSize, this.x, this.y+this.h) or pointInWedge(4, row*blockSize, col*blockSize, this.x+this.w, this.y) or pointInWedge(4, row*blockSize, col*blockSize, this.x+this.w, this.y+this.h):
                if this.theKey == K_LEFT:
                    this.x += this.speed
                elif this.theKey == K_RIGHT:
                    this.x -= this.speed
            elif pointInWedge(4, row*blockSize, col*blockSize, this.x, this.y):
                this.y += this.speed
            elif this.pointInBlock(row*blockSize, col*blockSize, this.x, this.y+this.h):
                if this.theKey == K_LEFT:
                    this.x += this.speed
                elif this.theKey == K_RIGHT:
                    this.x -= this.speed
        elif key[0] == 5:
            if pointInWedge(5, row*blockSize, col*blockSize, this.x, this.y) or pointInWedge(5, row*blockSize, col*blockSize, this.x, this.y+this.h) or pointInWedge(5, row*blockSize, col*blockSize, this.x+this.w, this.y+this.h):
                if this.theKey == K_LEFT:
                    this.x += this.speed
                elif this.theKey == K_RIGHT:
                    this.x -= this.speed
            elif pointInWedge(5, row*blockSize, col*blockSize, this.x+this.w, this.y):
                this.y += this.speed
            elif this.pointInBlock(row*blockSize, col*blockSize, this.x+this.w, this.y+this.h):
                if this.theKey == K_LEFT:
                    this.x += this.speed
                elif this.theKey == K_RIGHT:
                    this.x -= this.speed
    def Ycol(this, key, value):
        blockSize = 20
        row = key[1]
        col = key[2]
        if key[0] == 1:
            if this.x+this.w > row*blockSize and this.x < row*blockSize+blockSize and this.y+this.h > col*blockSize and this.y < col*blockSize+blockSize:
                if this.yVel > 0:
                    this.y = col*blockSize-this.h
                    this.yVel = 0
                else:
                    this.y -= this.yVel*1.1
                    this.yVel = 0.5
        elif key[0] != 0:
            onCorner = False
            if key[0] == 2:
                if pointInWedge(4, row*blockSize, col*blockSize, this.x, this.y+this.h):
                    onCorner = True
            if key[0] == 3:
                if pointInWedge(5, row*blockSize, col*blockSize, this.x+this.w, this.y+this.h):
                    onCorner = True
            if key[0] == 4:
                if pointInWedge(2, row*blockSize, col*blockSize, this.x+this.w, this.y):
                    onCorner = True
            if key[0] == 5:
                if pointInWedge(3, row*blockSize, col*blockSize, this.x, this.y):
                    onCorner = True
            if pointInWedge(key[0], row*blockSize, col*blockSize, this.x, this.y) or pointInWedge(key[0], row*blockSize, col*blockSize, this.x+this.w, this.y) or pointInWedge(key[0], row*blockSize, col*blockSize, this.x, this.y+this.h) or pointInWedge(key[0], row*blockSize, col*blockSize, this.x+this.w, this.y+this.h) or onCorner:
                if this.yVel > 0:
                    this.y -= this.yVel*1.1
                    this.yVel = 0
                else:
                    this.y -= this.yVel*1.1
                    this.yVel = 0.5
        
            
    

class Gun:

    def __init__(this, name, scale, translation, **kwargs):
        this.scale = scale
        this.translation = translation
        this.damage = kwargs.get("damage", 10)
        this.firerate = kwargs.get("firerate", 10)
        this.bulletspeed = kwargs.get("bulletspeed", 3)
        this.spread = kwargs.get("spread", 0)
        this.shots = kwargs.get("shots", 1)
        this.name = name
        this.shapes = pygame.image.load("guns/" + this.name + ".png")
        
        
    def draw(this, surface, scale, translation, rotation):
        while rotation > math.pi:
            rotation -= 2*math.pi
        while rotation < -math.pi:
            rotation += 2*math.pi
        originalRect = this.shapes.get_rect()
        if (rotation > -math.pi/2 and rotation < math.pi/2):
            flip = 1
            gunImage = pygame.transform.rotate(pygame.transform.flip(pygame.transform.scale(this.shapes, (round(originalRect.width*this.scale*scale), round(originalRect.height*this.scale*scale))), 0, 0), -rotation*180/math.pi)
        else:
            flip = -1
            gunImage = pygame.transform.rotate(pygame.transform.flip(pygame.transform.scale(this.shapes, (round(originalRect.width*this.scale*scale), round(originalRect.height*this.scale*scale))), 0, 1), -rotation*180/math.pi)
        gunRect = gunImage.get_rect()
        gunRect.center = (translation[0] + (math.cos(rotation)*this.translation[0]+math.cos(rotation+math.pi/2)*this.translation[1]*flip)*scale*this.scale, translation[1] + (math.sin(rotation)*this.translation[0]+math.sin(rotation+math.pi/2)*this.translation[1]*flip)*scale*this.scale)
        surface.blit(gunImage, gunRect)


guns = [
    Gun("Glock 19", 0.8, [300, 50], damage=5, firerate=20, bulletspeed=7, spread=3),
    Gun("Spas 12", 1, [300, -10], damage=4, firerate=40, bulletspeed=6, spread=10, shots=10),
    Gun("Howa 1500", 1.2, [300, -10], damage=20, firerate=30, bulletspeed=10, spread=1),
    Gun("PLR-16", 1, [300, -10], damage=3, firerate=1, bulletspeed=7, spread=20),
    Gun("AWM", 1.2, [300, -10], damage=45, firerate=80, bulletspeed=15, spread=1),
    Gun("AK-47", 0.9, [300, 100], damage=2, firerate=2, bulletspeed=7, spread=6),
]  
