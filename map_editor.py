#
# 
#

import pygame
import pygame.locals
import math
import random
import game_mouse
from tower_map import Map,PathCell

TEXT_COLOR = 0

class Editor(game_mouse.Game):

    def __init__(self, filename, grid_size):
        self.map = Map(filename)
        width  = self.map.getWidth()
        height = self.map.getHeight()
        self.map_width  = width * grid_size
        self.map_height = height * grid_size
        game_mouse.Game.__init__(self, "Map Editor",
                                 self.map_width,
                                 self.map_height,
                                 30)
        self.grid_size = grid_size

        self.font_height = 12
        self.font = pygame.font.SysFont("Courier New", self.font_height)
        
        self.color = [ (0, 0, 0), # TEXT_COLOR
                       ]
        
        self.mouse_x = 0
        self.mouse_y = 0
        self.dx      = 1
        self.dy      = 1
        
        self.t1 = pygame.time.get_ticks()
        return
        
    def game_logic(self, keys, newkeys, buttons, newbuttons, mouse_position):
        x = mouse_position[0]
        y = mouse_position[1]

        self.mouse_x = x
        self.mouse_y = y

        if pygame.K_UP in keys and pygame.K_LEFT in keys:
            self.dx = -1
            self.dy = -1
        elif pygame.K_UP in keys and pygame.K_RIGHT in keys:
            self.dx = 1
            self.dy = -1
        elif pygame.K_DOWN in keys and pygame.K_RIGHT in keys:
            self.dx = 1
            self.dy = 1
        elif pygame.K_DOWN in keys and pygame.K_LEFT in keys:
            self.dx = -1
            self.dy = 1
        elif pygame.K_LEFT in keys:
            self.dx = -1
            self.dy = 0
        elif pygame.K_RIGHT in keys:
            self.dx = 1
            self.dy = 0
        elif pygame.K_UP in keys:
            self.dx = 0
            self.dy = -1
        elif pygame.K_DOWN in keys:
            self.dx = 0
            self.dy = 1
        else:
            self.dx = 0
            self.dy = 0
        
        if 1 in buttons and (self.dx or self.dy):
            cell_x = x/self.grid_size
            cell_y = y/self.grid_size
            cell = PathCell(cell_x, cell_y, self.dx, self.dy)
            self.map.setCell(cell_x, cell_y, cell)
        if (2 in buttons) or (3 in buttons):
            cell_x = x/self.grid_size
            cell_y = y/self.grid_size
            self.map.setCell(cell_x, cell_y, None)
        if ((pygame.K_LCTRL in keys) or (pygame.K_RCTRL in keys)) and (pygame.K_c in newkeys):
            self.map.clear()

        if ((pygame.K_LCTRL in keys) or (pygame.K_RCTRL in keys)) and (pygame.K_s in newkeys):
            self.map.saveMapFile("map2.txt")
            
        t2 = pygame.time.get_ticks()
        dt = (t2 - self.t1)/1000.
        self.t1 = t2
        
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

    def drawPath(self, surface):
        for row in self.map.getMap():
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
        return

def main():
    pygame.font.init()
    e = Editor("map1.txt", 10)
    e.main_loop()
    return
    
if __name__ == "__main__":
    main()

