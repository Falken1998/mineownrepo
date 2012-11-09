import math
from tower_bullet import Bullet

class Tower:
    def __init__(self, fire_rate, fire_range, fire_power, fire_speed, tower_type):
        self.fire_rate      = fire_rate  # float, shots per second
        self.fire_range     = fire_range # float, radius of fire, in grids
        self.fire_power     = fire_power # float, damage per shot in hit points
        self.fire_speed     = fire_speed # float, speed of bullets in grids per second
        self.tower_type     = tower_type # integer number
        self.last_fire_time = 0.         # float, time of last shot in seconds
        self.x        = 0  # int, x location of top left corner in grids
        self.y        = 0  # int, y location of top left corner in grids
        self.width    = 3  # int, width in grids
        self.height   = 4  # int, width in grids
        self.direction = 0. # float, radians
        self.bullet_radius = 0.5 # float, grids
        self.map = None
        return

    def getPosition(self):
        return self.x, self.y
    
    def getFirePosition(self):
        return self.x+self.width/2., self.y+self.height/2.
    
    def getDimensions(self):
        return self.width, self.height
    
    def move(self, x, y):
        self.x = x
        self.y = y
        return

    def setMap(self, map_object):
        self.map = map_object
        return
    
    def getFireRate(self):
        return self.fire_rate
    
    def getFireRange(self):
        return self.fire_range
    
    def getFirePower(self):
        return self.fire_power
    
    def getFireSpeed(self):
        return self.fire_speed
    
    def getTowerType(self):
        return self.tower_type
    
    def getLastFireTime(self):
        return self.last_fire_time

    def getDirection(self):
        return self.direction
    
    #
    # find direction to shoot baddie, with approximation prediction
    # find time to hit baddie if they stand still
    # use this time to find where baddie will actually be
    # use this position to find the angle to hit the baddie
    # this works if the bullets are fast enough compared to the baddie speed
    #
    # this could iterate for higher accuracy
    #
    def findDirectionAux(self, baddie):
        # current position and direction of baddie
        x0p, y0p   = baddie.getPosition()
        dx0p, dy0p = baddie.getDirection()
        # tower position and bullet speed
        x1p, y1p   = self.getFirePosition()
        s1         = self.getFireSpeed()

        # distance(dp), time(tp), and angle(angle2) to baddie's current position
        dxp = x0p - x1p
        dyp = y0p - y1p
        dp  = math.sqrt(dxp*dxp + dyp*dyp)
        tp  = dp/s1
        angle2 = math.atan2(dyp, dxp)

        # baddies position at time(tp)
        x0  = x0p + dx0p*tp
        y0  = y0p + dy0p*tp
        
        # check if baddie is on a straight path at that position
        xx = int(x0)
        yy = int(y0)
        mo = self.map.getMap()
        if yy >= 0 and yy < len(mo) and xx >= 0 and xx < len(mo[yy]):
            p = mo[yy][xx]
            if (not p) or (p.dx != 0 and p.dy != 0):
                # baddie will have turned before we hit it
                return -1.0, -1.0

        # distance(distance) and angle(angle) to baddie's future position
        dx  = x0 - x1p
        dy  = y0 - y1p
        distance = math.sqrt(dx*dx + dy*dy)
        angle = math.atan2(dy, dx)
        
        return angle, distance

    # find direction to oldest baddie within range
    def findDirection(self, baddies):
        d = -1.0
        age = -1.0
        for b in baddies:
            if b.getDistance() > age:
                angle, distance = self.findDirectionAux(b)
                if distance > 0 and distance < self.fire_range:
                    age = b.getDistance()
                    d = angle
                    # make radians positive
                    while d < 0:
                        d += 2*math.pi
        return d

    # fire a bullet, if enough time has passed
    def fire(self, baddies):
        ok     = False
        bullet = None
        if self.fire_rate * self.last_fire_time >= 1.0:
            ok = True
            self.last_fire_time = 0
            # aim the gun
            direction = self.findDirection(baddies)
            if direction >= 0.:
                # found a target, shoot
                dx = math.cos(direction) * self.fire_speed
                dy = math.sin(direction) * self.fire_speed
                x = self.x+self.width/2.
                y = self.y+self.height/2.
                bullet = Bullet(x, y, dx, dy, self.fire_power, self.fire_range, self.bullet_radius)
                self.direction = direction
        return ok, bullet

    # fire a bullet if it's ok
    def evolve(self, dt, baddies):
        self.last_fire_time += dt
        ok, bullet = self.fire(baddies)
        return ok, bullet
