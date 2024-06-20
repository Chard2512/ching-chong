import pygame as pg
import sys

pg.init()

class Game:
    def __init__(self):
        self.screen = pg.display.set_mode((800, 600))
        self.clock = pg.time.Clock()
        self.frame_rate = 60

        self.objects = []
        self.gravity = pg.Vector2(0, 20)
        self.delta_time = 0
        
    def handle_quit_button(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

    def clear_graphics(self):
        self.screen.fill((0,0,0))

    def render_physics(self):
        for object in self.objects:
            if object.anchored == False:
                object.velocity += self.gravity * self.delta_time
                object.position += object.velocity * self.delta_time

    def render_objects(self):
        for object in self.objects:
            if isinstance(object, Object.Rectangle):
                pg.draw.rect(self.screen, object.color, pg.Rect(object.position, object.size), object.width)
            elif isinstance(object, Object.Circle):
                pg.draw.circle(self.screen, object.color, object.position, object.radius, object.width)

    def display_graphics(self):
        pg.display.flip()
        self.delta_time = self.clock.tick(self.frame_rate) / 1000

    def screen_proportional_vector2(self, x, y, x_pixels = 0, y_pixels = 0):
        return pg.Vector2(x * self.screen.get_width() + x_pixels,
                          y * self.screen.get_height() + y_pixels)
    
    def screen_width_proportional_unit(self, x):
        return x * self.screen.get_width()
    
    def screen_height_proportional_unit(self, x):
        return x * self.screen.get_height()

class Object:

    class Rectangle:
        def __init__(self, game_instance):       
            self.color = pg.Color(255, 255, 255)
            self.velocity = pg.Vector2(0, 0)
            self.position = pg.Vector2(0, 0)
            self.size = pg.Vector2(0, 0)
            self.width = 0
            self.anchored = False

    class Circle:
        def __init__(self, game_instance):
            self.color = pg.Color(255, 255, 255)
            self.velocity = pg.Vector2(0, 0)
            self.position = pg.Vector2(0, 0)
            self.radius = pg.Vector2(0, 0)
            self.width = 0
            self.anchored = False

class ObjectFactory:
    def __init__(self, game_instance):
        self.game_instance = game_instance
    
    def new(self, type_name):
        object_class = getattr(Object, type_name)
        return object_class(self.game_instance)
