import math

class Bullet:

    def __init__(self, x, y, dx, dy, power, distance, radius):
        self.x        = x        # float, grids 
        self.y        = y        # float, grids 
        self.dx       = dx       # float, grids per second
        self.dy       = dy       # float, grids per second
        self.power    = power    # float, damage in hit points
        self.distance = distance # float, grids
        self.radius   = radius   # float, grids
        self.alive    = True
        self.old_x    = x
        self.old_y    = y
        return

    def getPower(self):
        return self.power
    
    def getAlive(self):
        return self.alive
    
    def setDead(self):
        self.alive = False
        return

    def getPosition(self):
        return self.x, self.y
    
    def getOldPosition(self):
        return self.old_x, self.old_y

    def getRadius(self):
        return self.radius

    # this is called when the bullet hits a baddie
    # special actions should go here
    def explode(self):
        return

    #
    # move bullet
    #
    def evolve(self, dt, width, height):
        # amount moved this frame
        ddx = self.dx * dt
        ddy = self.dy * dt

        # remember old position
        self.old_x = self.x
        self.old_y = self.y

        # update position
        self.x += ddx
        self.y += ddy
        
        # update total distance traveled by bullet
        self.distance -= math.sqrt(ddx*ddx + ddy*ddy)

        # if off-screen, remove it
        if self.x < 0 or self.x > width or self.y < 0 or self.y > height or self.distance < 0.:
            self.alive = False
        return
