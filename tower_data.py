import random
import math
import sys

from tower_baddie import Baddie
from tower_bullet import Bullet
from tower_type import TowerType
from tower_tower import Tower
from tower_map import PathCell, Map
from tower_configuration import g_ALL_TOWER_TYPES, g_BADDIE_SPAWN_RATE


# sign of value
def sign(x):
    if x >= 0:
        return 1
    else:
        return -1

# distance between to points in space (p1, p2) are sequences of same length
def distance(p1, p2):
    d = 0.0
    for i in range(len(p1)):
        dx = p2[i] - p1[i]
        d += dx*dx
    return math.sqrt(d)

# square of distance between to points in space (p1, p2) are sequences of same length
def distance_sqr(p1, p2):
    d = 0.0
    for i in range(len(p1)):
        dx = p2[i] - p1[i]
        d += dx*dx
    return d

# mid point of two points in space (p1, p2, m) are sequences of same length
def midpoint(p1, p2):
    m = []
    for i in range(len(p1)):
        x = (p1[i] + p2[i])/2.
        m.append(x)
    return m
    
# dot product of two vectors (x, y) are sequences of same length
def dot(x, y):
    d = 0
    for i in range(len(x)):
        d += x[i] * y[i]
    return d

# subtract to vectors (p1, p2) which are sequences of same length
def vector(p1, p2):
    v = []
    for i in range(len(p1)):
        v.append( p2[i] - p1[i] )
    return v
    



    

        
class TowerData:

    def __init__(self, width, height, map_object):
        self.width     = width     # in grids
        self.height    = height    # in grids
        self.map       = map_object
        self.tower_types = g_ALL_TOWER_TYPES
        self.newGame()
        return

    def newGame(self):
        self.towers         = []
        self.bullets        = []
        self.baddies        = []
        self.baddie_spawns  = []

        # find points on map where Baddies can come in.
        for row in self.map.getMap():
            for p in row:
                if not p: continue
                (x, y) = p.getPosition()
                (dx, dy) = p.getDirection()
                if ((x == 0 and dx > 0 and dy == 0) or
                    (y == 0 and dy > 0 and dx == 0) or
                    (x == self.width-1 and dx < 0 and dy == 0) or
                    (y == self.height-1 and dy < 0 and dx == 0)):
                    self.baddie_spawns.append( (x, y) )
        return

    def getTowerTypes(self):
        return self.tower_types

    # add tower by index (tower_type)
    def addNewTower(self, tower_type, x, y):
        t = self.tower_types[tower_type].newTower()
        t.setMap(self.map)
        t.move(x, y)
        self.towers.append(t)
        return
    
    # add tower by type object (tower_type)
    def addNewTowerFromType(self, tower_type, x, y):
        if not self.towerPositionIsLegal(tower_type, x, y):
            return
        t = tower_type.newTower()
        t.setMap(self.map)
        t.move(x, y)
        self.towers.append(t)
        return

    def getWidth(self):
        return self.width
        
    def getHeight(self):
        return self.height

    def getTowers(self):
        return self.towers

    def getBullets(self):
        return self.bullets

    def getMap(self):
        return self.map
    
    def getBaddies(self):
        return self.baddies

    # find the closest approach of bullet to baddie
    # it's just a little trigonometry
    # used for collision detection
    def findClosestApproach(self, x1, x2, c):
        # x1 = old point of bullet
        # x2 = current point of bullet
        # c  = center of baddie
        x  = vector(x1, x2)
        a  = vector(x1, c)
        b  = vector(x2, c)
        d1 = dot(x, a)
        d2 = dot(x, b)
        if (d1 > 0 and d2 > 0) or (d1 < 0 and d2 < 0) or (distance(x1, x2) < .1):
            return min(distance(x1,c), distance(x2,c))
        else:
            mid = midpoint(x1, x2)
            g = vector(mid, c)
            d3 = dot(x, g)
            if sign(d1) == sign(d3):
                return self.findClosestApproach(mid, x2, c)
            else:
                return self.findClosestApproach(x1, mid, c)

    # check that tower isn't on the road or another tower
    # used for placing new towers
    def towerPositionIsLegal(self, tower_type, x, y):
        ok = True
        maps = self.map.getMap()
        w, h = tower_type.getDimensions()
        for dy in range(y, y+h):
            if not ok:
                break
            # off the map
            if dy < 0 or dy >= len(maps):
                ok = False
                break
            for dx in range(x, x+w):
                # off the map
                if dx < 0 or dx >= len(maps[dy]):
                    ok = False
                    break
                # on the road
                if maps[dy][dx]:
                    ok = False
                    break
                for t in self.towers:
                    tx, ty = t.getPosition()
                    tw, th = t.getDimensions()
                    if not ok:
                        break
                    for tdy in range(ty, ty+th):
                        if not ok:
                            break;
                        for tdx in range(tx, tx+tw):
                            if not ok:
                                break
                            # on another tower
                            if dx == tdx and dy == tdy:
                                ok = False
                                break
        return ok

    # check for collisions between baddies and bullets
    def collisions(self):
        new_dead = 0
        for bad in self.baddies:
            x1, y1 = bad.getPosition()
            if not bad.getAlive():
                continue
            for bul in self.bullets:
                if not bul.getAlive():
                    continue
                x2, y2 = bul.getPosition()
                x0, y0 = bul.getOldPosition()
                dist = self.findClosestApproach((x0, y0), (x2, y2), (x1, y1))
                # if their edges would have touched
                if dist < bad.getRadius() + bul.getRadius():
                    # this is where the collision occurs,
                    bul.explode()
                    bul.setDead()
                    bad.takeDamage(bul.getPower())
                    if not bad.getAlive():
                        new_dead += 1
                    break
        return new_dead

    # spawn baddies according to spawn plan
    # if there were multiple types of baddies, you could
    # randomly select the types here.
    def spawnBaddies(self, dt):
        if random.random() < g_BADDIE_SPAWN_RATE * dt:
            (x, y) = random.choice(self.baddie_spawns)
            speed = random.random() * 2. + 4.
            hp = 1.0
            radius = 1.0
            self.baddies.append( Baddie(x, y, speed, hp, radius) )
        return
    
    # process one frame of action
    def evolve(self, dt):

        # allow the towers to shoot bullets
        for t in self.towers:
            ok, bullet = t.evolve(dt, self.baddies)
            if ok and bullet:
                self.bullets.append(bullet)

        # move the bullets
        for b in self.bullets:
            b.evolve(dt, self.width, self.height)

        # create more baddies
        self.spawnBaddies(dt)
        
        # move the baddies
        for b in self.baddies:
            b.evolve(dt, self.map.getMap(), self.width, self.height)

        # check for bullet-baddie collisions
        new_dead = self.collisions()

        # remove dead bullets and baddies from the lists
        self.bullets = [ b for b in self.bullets if b.getAlive() ]
        self.baddies = [ b for b in self.baddies if b.getAlive() ]

        # return the number of baddies that died.
        return new_dead
