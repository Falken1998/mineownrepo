import random
import math
from tower_configuration import g_BADDIE_WIGGLE,g_BADDIE_MAX_WIGGLE

EPSILON = 0.00001

class Baddie:

    def __init__(self, x, y, speed, hp, radius):
        self.x = x
        self.y = y
        self.speed = speed
        self.hp = hp
        self.radius = radius
        self.alive = True
        self.distance = 0.
        self.dx = 0.
        self.dy = 0.
        self.pdx = 0.
        self.pdy = 0.
        return

    def getPosition(self):
        return self.x, self.y

    def getDirection(self):
        return self.dx, self.dy

    def getAlive(self):
        return self.alive

    def getRadius(self):
        return self.radius

    def setDead(self):
        self.alive = False
        return

    def takeDamage(self, damage):
        self.hp -= damage
        if self.hp <= EPSILON:
            self.setDead()
        return

    def getDistance(self):
        return self.distance

    #
    # moves the baddie a little along the path
    #
    def evolve(self, dt, maps, width, height):
        
        # get map direction
        i, j = int(self.x), int(self.y)
        if maps[j][i]:
            dx, dy = maps[j][i].getDirection()
        else:
            dx, dy = 0, 0

        # modify personal direction with minor wiggle
        self.pdx += random.uniform(-g_BADDIE_WIGGLE, g_BADDIE_WIGGLE)
        self.pdy += random.uniform(-g_BADDIE_WIGGLE, g_BADDIE_WIGGLE)
        if self.pdx < -g_BADDIE_MAX_WIGGLE: self.pdx = -g_BADDIE_MAX_WIGGLE
        if self.pdx >  g_BADDIE_MAX_WIGGLE: self.pdx =  g_BADDIE_MAX_WIGGLE
        if self.pdy < -g_BADDIE_MAX_WIGGLE: self.pdy = -g_BADDIE_MAX_WIGGLE
        if self.pdy >  g_BADDIE_MAX_WIGGLE: self.pdy =  g_BADDIE_MAX_WIGGLE
        
        # modify direction by personal direction
        dx += self.pdx
        dy += self.pdy

        # update personal velocity
        self.dx = dx * self.speed
        self.dy = dy * self.speed

        # update personal position
        ddx = dt * self.dx
        ddy = dt * self.dy
        self.x += ddx
        self.y += ddy

        # update distance traveled by baddie
        self.distance += math.sqrt(ddx*ddx + ddy*ddy)
        
        # off the map border
        if self.x < 0 or self.x > width or self.y < 0 or self.y > height:
            self.alive = False
            
        return
