class PathCell:
    
    def __init__(self, x, y, dx, dy):
        self.x = x   # location on grid
        self.y = y   # location on grid
        self.dx = dx # -1, 0, 1 direction of travel from here
        self.dy = dy # -1, 0, 1 direction of travel from here
        return

    def getPosition(self):
        return self.x, self.y

    def getDirection(self):
        return self.dx, self.dy

class Map:

    def __init__(self, filename):
        self.map = []
        self.width = 0
        self.height = 0
        self.readMapFile(filename)
        return

    def getWidth(self):
        return self.width

    def getHeight(self):
        return self.height

    def setCell(self, x, y, cell):
        self.map[y][x] = cell
        return
        
    def getCell(self, x, y):
        return self.map[y][x]

    def getMap(self):
        return self.map

    def clear(self):
        for j in range(len(self.map)):
            for i in range(len(self.map[j])):
                self.map[j][i] = None
        return

    def readMapFile(self, filename):
        self.map = []
        self.height = 0
        self.width  = 0
        f = open(filename, "r")
        for l in f:
            map_row = []
            l = l.strip()
            width = len(l)
            if self.width > 0 and self.width != width:
                print "Map file line widths not identical"
                sys.exit(1)
            elif self.width == 0:
                self.width = width
                
            for x in range(self.width):
                if l[x] == "v":
                    map_row.append( PathCell(x, self.height, 0, 1) )
                elif l[x] == "^":
                    map_row.append( PathCell(x, self.height, 0, -1) )
                elif l[x] == ">":
                    map_row.append( PathCell(x, self.height, 1, 0) )
                elif l[x] == "<":
                    map_row.append( PathCell(x, self.height, -1, 0) )
                elif l[x] == "L":
                    map_row.append( PathCell(x, self.height, -1, 1) )
                elif l[x] == "J":
                    map_row.append( PathCell(x, self.height, 1, 1) )
                elif l[x] == "\\":
                    map_row.append( PathCell(x, self.height, -1, -1) )
                elif l[x] == "/":
                    map_row.append( PathCell(x, self.height, 1, -1) )
                elif l[x] == ".":
                    map_row.append( None )
                else:
                    print "Map file unknown character '%s'." % (l[x])
                    sys.exit(1)
            self.map.append( map_row )
            self.height += 1
        
        f.close()
        return


    def saveMapFile(self, filename):
        f = open(filename, "w")
        for row in self.map:
            for cell in row:
                if cell:
                    dx, dy = cell.getDirection()
                else:
                    dx, dy = 0, 0
                if dx == 0 and dy == 0:
                    f.write(".")
                elif dx == 0 and dy == 1:
                    f.write("v")
                elif dx == 0 and dy == -1:
                    f.write("^")
                elif dx == 1 and dy == 0:
                    f.write(">")
                elif dx == -1 and dy == 0:
                    f.write("<")
                elif dx == -1 and dy == 1:
                    f.write("L")
                elif dx == 1 and dy == 1:
                    f.write("J")
                elif dx == -1 and dy == -1:
                    f.write("\\")
                elif dx == 1 and dy == -1:
                    f.write("/")
                else:
                    print "ERROR"
            f.write("\n")
        f.close()
        return
