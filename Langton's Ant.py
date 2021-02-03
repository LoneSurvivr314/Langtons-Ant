import pyglet
from pyglet import shapes
from pyglet import clock
 
 
# Set up global variables
WIDTH = 250
HEIGHT = 250
SIZE = 4
COLORS = [(255,0,0), (0,0,255)]
GRID = [[COLORS[0] for y in range(HEIGHT)] for x in range(WIDTH)] # Fill Grid with first color
RULES = ['L', 'R']
# Set up pyglet window
window = pyglet.window.Window(WIDTH * SIZE, HEIGHT * SIZE)
 
fps_display = pyglet.window.FPSDisplay(window)
 
batch = pyglet.graphics.Batch()
 
class Grid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
 
        self.rects = {}
        for x in range(width):
            self.rects[x] = {}
            for y in range(height):
                self.rects[x][y] = shapes.Rectangle(
                        x * SIZE, 
                        y * SIZE,
                        SIZE,
                        SIZE,
                        color=COLORS[0],
                        batch = batch)
 
grid = Grid(WIDTH, HEIGHT)
 
# Ant
class Ant:
    buffer = []
 
    def __init__(self, x_pos, y_pos, grid):
        self.location = [x_pos, y_pos]
        self.direction = [1,0]
        self.grid = grid
    
    def turn(self, direction):
        if direction == 'R':
            self.direction = [self.direction[1], -1 * self.direction[0]]
        if direction == 'L':
            self.direction = [-1 * self.direction[1],self.direction[0]]
    
    def move(self, distance):
        self.location = [
            direction + location for direction, location in zip(
            [item * distance for item in self.direction], self.location)]
        self.location = [self.location[0] % WIDTH, self.location[1] % HEIGHT]  # Wrap over edge
    
    def iterate(self, iterations):
        for iteration in range(iterations):
            index = COLORS.index(GRID[self.location[0]][self.location[1]])  # Find index of current color
            GRID[self.location[0]][self.location[1]] = COLORS[
                    (index + 1) % len(COLORS)]  # Set cell to next color
            self.turn(RULES[index])  # Turn
            self.move(1)  # Move
            self.grid.rects[self.location[0]][self.location[1]].color = GRID[self.location[0]][self.location[1]]
 
    def debug(self):
        print('direction' + str(self.direction))
        print('location' + str(self.location))
 
my_ant = Ant(100,100, grid)
 
@window.event
def on_draw():
    window.clear()
    batch.draw()
    fps_display.draw()
 
def update(dt):
    my_ant.iterate(10)
   
pyglet.clock.schedule_interval(update, 1/1000)
 
pyglet.app.run()