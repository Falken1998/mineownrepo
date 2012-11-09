from tower_tower import Tower


class TowerType:
    def __init__(self, name, cost, width, height, fire_rate, fire_range, fire_power, fire_speed, bullet_size, tower_type):
        self.name        = name          # string, name of tower
        self.cost        = cost          # float, cost in points
        self.width       = width         # float, width in grids
        self.height      = height        # float, height in grids
        self.fire_rate   = fire_rate     # float, shots per second
        self.fire_range  = fire_range    # float, radius of fire, in grids
        self.fire_power  = fire_power    # float, damage per shot in hit points
        self.fire_speed  = fire_speed    # float, speed of bullets in grids, per second
        self.bullet_size = bullet_size   # float, radius of bullets in grids
        self.tower_type  = tower_type    # integer, index in list
        return
    
    def getName(self):
        return self.name
    
    def getCost(self):
        return self.cost
    
    def getDimensions(self):
        return self.width, self.height
    
    def getFireRate(self):
        return self.fire_rate
    
    def getFireRange(self):
        return self.fire_range
    
    def getFirePower(self):
        return self.fire_power
    
    def getFireSpeed(self):
        return self.fire_speed
    
    def getBulletSize(self):
        return self.bullet_size
    
    def getTowerType(self):
        return self.tower_type
    
    def newTower(self):
        t = Tower(self.fire_rate, self.fire_range, self.fire_power, self.fire_speed, self.tower_type)
        t.width = self.width
        t.height = self.height
        t.bullet_radius = self.bullet_size
        return t
        
