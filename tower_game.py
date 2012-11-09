#
# 
#

import pygame
import pygame.locals
import math
import random
import game_mouse
import tower_data
from tower_configuration import g_TOWER_COLORS

TEXT_COLOR = 0


def render_transparent_circle_aux(color, radius, width=0):
    size = radius * 2
    temp_surf = pygame.Surface((size, size), pygame.locals.SRCALPHA)
    temp_surf.fill( (0, 0, 0, 0) )
    pygame.draw.circle(temp_surf, color, (radius, radius), radius, width)
    return temp_surf

# note that color should have an alpha channel (4th element)
def render_transparent_circle(surface, color, center, radius, width=0):
    circle_surface = render_transparent_circle_aux(color, radius, width)
    (cx, cy) = center
    lx = cx - radius
    ty = cy - radius
    surface.blit(circle_surface, (lx, ty))
    return


class Tower(game_mouse.Game):

    def __init__(self, filename, grid_size):
        map_object = tower_data.Map(filename)
        width  = map_object.getWidth()
        height = map_object.getHeight()
        self.map_width  = width * grid_size
        self.map_height = height * grid_size
        self.menu_width = 100
        game_mouse.Game.__init__(self, "Tower Defense Genre",
                                 self.map_width + self.menu_width,
                                 self.map_height,
                                 30)
        self.grid_size = grid_size
        self.data = tower_data.TowerData(width, height, map_object)

        self.sound_on   = True
        self.pause      = False
        self.dead_sound = []
        self.dead_sound.append( pygame.mixer.Sound('pen.wav') )
        self.dead_sound.append( pygame.mixer.Sound('scratch.wav') )
        #self.dead_sound.append( pygame.mixer.Sound('dead.wav') )
        for d in self.dead_sound:
            d.set_volume(1.00)

        self.font_height = 12
        self.font = pygame.font.SysFont("Courier New", self.font_height)
        
        self.color = [ (0, 0, 0), # TEXT_COLOR
                       ]

        self.tower_colors = g_TOWER_COLORS

        self.drag_tower_type = None
        self.mouse_x = 0
        self.mouse_y = 0
            
        self.t1 = pygame.time.get_ticks()
        return
        
    def game_logic(self, keys, newkeys, buttons, newbuttons, mouse_position):
        x = mouse_position[0]
        y = mouse_position[1]

        self.mouse_x = x
        self.mouse_y = y
        
        if pygame.K_p in newkeys:
            self.pause = not self.pause
        if pygame.K_s in newkeys:
            self.sound_on = not self.sound_on

        if 1 in newbuttons:
            tt = self.clickToTowerMenu(x, y)
            if (not self.drag_tower_type) and tt:
                self.drag_tower_type = tt
            elif self.drag_tower_type and tt:
                self.drag_tower_type = None
            elif self.drag_tower_type and (not tt):
                self.data.addNewTowerFromType(self.drag_tower_type,
                                              int(self.mouse_x/self.grid_size),
                                              int(self.mouse_y/self.grid_size))
                self.drag_tower_type = None
        
        t2 = pygame.time.get_ticks()
        dt = (t2 - self.t1)/1000.
        self.t1 = t2
        
        if not self.pause:
            new_dead = self.data.evolve(dt)
            if self.sound_on:
                if new_dead:
                    random.choice(self.dead_sound).play()
            
        return

    # Draws text left justified at "x" using "The Font".
    # The bottom of the text is displayed at "y".
    def drawTextLeft(self, surface, text, x, y):
        textobj = self.font.render(text, False, self.color[TEXT_COLOR])
        textrect = textobj.get_rect()
        textrect.bottomleft = (x, y)
        surface.blit(textobj, textrect)
        return
    
    # Draws text right justified at "x" using "The Font".
    # The bottom of the text is displayed at "y".
    def drawTextRight(self, surface, text, x, y):
        textobj = self.font.render(text, False, self.color[TEXT_COLOR])
        textrect = textobj.get_rect()
        textrect.bottomright = (x, y)
        surface.blit(textobj, textrect)
        return

    def drawBackground(self, surface):
        rect = pygame.Rect(0,0, self.map_width, self.map_height)
        surface.fill( (200, 200, 255), rect)
        return

    def drawBullets(self, surface):
        bullets = self.data.getBullets()
        for b in bullets:
            x, y = b.getPosition()
            r = b.getRadius()
            x *= self.grid_size
            y *= self.grid_size
            x = int(x)
            y = int(y)
            pygame.draw.circle(surface, (255, 0, 0), (x, y), int(self.grid_size*r))
        return
    
    def drawBaddies(self, surface):
        baddies = self.data.getBaddies()
        for b in baddies:
            x, y = b.getPosition()
            r    = b.getRadius()
            x *= self.grid_size * r
            y *= self.grid_size * r
            x = int(x)
            y = int(y)
            pygame.draw.circle(surface, (155, 0, 155), (x, y), self.grid_size)
        return

    def drawTower(self, surface, x, y, w, h, d, body_color, gun_color):
        rect = pygame.Rect(x, y, w, h)
        pygame.draw.rect(surface, body_color, rect)
        
        dx = int(math.cos(d) * w)
        dy = int(math.sin(d) * w)
        pygame.draw.line(surface, gun_color, (x+w/2, y+h/2),
                         (x+w/2+dx, y+h/2+dy), 1)
        return
    
    def drawTowers(self, surface):
        towers = self.data.getTowers()
        for t in towers:
            x, y = t.getPosition()
            w, h = t.getDimensions()
            d    = t.getDirection()
            x = int(x * self.grid_size)
            y = int(y * self.grid_size)
            w = int(w * self.grid_size)
            h = int(h * self.grid_size)
            colors = self.tower_colors[t.getTowerType()]
            self.drawTower(surface, x, y, w, h, d, colors[0], colors[1])
        return
    
    def drawPath(self, surface):
        for row in self.data.getMap().getMap():
            for p in row:
                if not p: continue
                x, y = p.getPosition()
                dx, dy = p.getDirection()
                x = int(x * self.grid_size)
                y = int(y * self.grid_size)
                w = int(self.grid_size)
                h = int(self.grid_size)
                rect = pygame.Rect(x, y, w, h)
                pygame.draw.rect(surface, (0, 0, 255), rect)
                pygame.draw.line(surface, (255, 255, 255), (x+w/2, y+h/2),
                                 (x+w/2+int(dx*self.grid_size/2), y+h/2+int(dy*self.grid_size/2)))
        return

    def drawTowerButton(self, surface, x, y, w, h, tt):
        rect = pygame.Rect(x, y, w, h)
        pygame.draw.rect(surface, (0, 0, 0), rect, 1)

        tw, th = tt.getDimensions()
        tw, th = int(tw*self.grid_size), int(th*self.grid_size)
        tx     = x + (w-tw)/2
        ty     = y + (h-th)/2
        td     = 0.
        
        colors = self.tower_colors[tt.getTowerType()]
        self.drawTower(surface, tx, ty, tw, th, td, colors[0], colors[1])

        fx = x + self.font_height
        fy = y + self.font_height/2
        
        fy = fy + self.font_height
        s = "%s" % (tt.getName())
        self.drawTextLeft(surface, s, fx, fy)

        fy = fy + self.font_height
        s = "%d" % (tt.getCost())
        self.drawTextLeft(surface, s, fx, fy)
        
        fy = fy + self.font_height
        s = "%0.2f" % (tt.getFireRate())
        self.drawTextLeft(surface, s, fx, fy)
        
        fy = fy + self.font_height
        s = "%0.2f" % (tt.getFireRange())
        self.drawTextLeft(surface, s, fx, fy)
        
        fy = fy + self.font_height
        s = "%0.2f" % (tt.getFirePower())
        self.drawTextLeft(surface, s, fx, fy)
        
        fy = fy + self.font_height
        s = "%0.2f" % (tt.getFireSpeed())
        self.drawTextLeft(surface, s, fx, fy)
        
        return

    def clickToTowerMenu(self, click_x, click_y):
        tts = self.data.getTowerTypes()
        n = len(tts)
        h = int(self.height / n)
        w = int(self.width - self.map_width)
        left = self.map_width

        x = left
        y = 0
        for tt in tts:
            if(click_x >= x and click_x <= x + w and
               click_y >= y and click_y <= y + h):
                return tt
            y += h
        return None
    
    def drawMenu(self, surface):
        tts = self.data.getTowerTypes()
        n = len(tts)
        h = int(self.height / n)
        w = int(self.width - self.map_width)
        left = self.map_width

        rect = pygame.Rect(left, 0, w, self.height)
        surface.fill( (200, 200, 255), rect)

        x = left
        y = 0
        for tt in tts:
            self.drawTowerButton(surface, x, y, w, h, tt)
            y += h
        
        return

    
    def drawDragTower(self, surface):
        if self.drag_tower_type == None:
            return

        if self.data.towerPositionIsLegal(self.drag_tower_type,
                                          int(self.mouse_x/self.grid_size),
                                          int(self.mouse_y/self.grid_size)):
            color = (100, 200, 100, 128)
        else:
            color = (200, 100, 100, 128)
        
        tw, th = self.drag_tower_type.getDimensions()
        tw, th = int(tw*self.grid_size), int(th*self.grid_size)
        tx     = int(self.mouse_x/self.grid_size)*self.grid_size
        ty     = int(self.mouse_y/self.grid_size)*self.grid_size
        td     = 0.
        colors = self.tower_colors[self.drag_tower_type.getTowerType()]
        self.drawTower(surface, tx, ty, tw, th, td, colors[0], colors[1])
        
        fire_range = self.drag_tower_type.getFireRange()
        cx         = tx + tw/2
        cy         = ty + th/2
        render_transparent_circle(surface, color, (cx, cy), int(fire_range*self.grid_size))
        
        return
    
    def drawGrid(self, surface):
        for x in range(0, self.map_width+1, self.grid_size):
            pygame.draw.line(surface, (10, 10, 10), (x, 0), (x, self.map_height), 1)
        for y in range(0, self.map_height+1, self.grid_size):
            pygame.draw.line(surface, (10, 10, 10), (0, y), (self.map_width, y), 1)
        return
    
    def paint(self, surface):
        self.drawBackground(surface)
        self.drawGrid(surface)
        self.drawPath(surface)
        self.drawTowers(surface)
        self.drawBaddies(surface)
        self.drawBullets(surface)
        self.drawMenu(surface)
        self.drawDragTower(surface)
        return

def main():
    pygame.font.init()
    pygame.mixer.init()
    t = Tower("map1.txt", 10)
    t.main_loop()
    return
    
if __name__ == "__main__":
    main()

