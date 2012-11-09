from tower_type import TowerType

# name, cost, width, height, fire_rate, fire_range, fire_power, fire_speed, bullet_size, type
g_ALL_TOWER_TYPES = [ TowerType("Speedy",     100, 3, 3, 5.0, 10.0, 0.50, 20.0, 0.20, 0),
                      TowerType("Slow",       200, 4, 4, 1.0, 20.0, 2.00, 20.0, 0.75, 1),
                      TowerType("Average",    150, 3, 4, 2.5, 15.0, 1.00, 17.0, 0.50, 2),
                      TowerType("Long Range", 300, 4, 4, 1.0, 40.0, 1.00, 60.0, 0.50, 3),
                      ]
# the "type" numbers 0, 1, 2, 3, etc. must be in order.

# the number of colors must match the number of towers
#                   body,        gun
g_TOWER_COLORS = [ [(0, 0, 0),   (100, 100, 0)],
                   [(0, 100, 0), (100, 100, 0)],
                   [(255, 0, 0), (100, 100, 0)],
                   [(0, 0, 255), (100, 100, 0)],
                   ]


# Baddie personal direction wiggle
g_BADDIE_WIGGLE     = 0.001
g_BADDIE_MAX_WIGGLE = 0.1


# Baddie spawn rate in baddies per second
g_BADDIE_SPAWN_RATE = 5.
