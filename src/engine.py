import pygame as pg
import sys
from scripts import engine_scripts
from context import GameEditorContext

pg.init()

class Game:
    def __init__(self):
        self.screen = pg.display.set_mode((800, 600))
        self.clock = pg.time.Clock()
        self.render_step = 0
        self.frame_rate = 60

        self.objects = []
        self.gravity = self.screen_proportional_vector2(0, 1)
        self.delta_time = 0

        self.context = GameEditorContext(self)

    def handle_tick_loop_script(self, script, render_steps_per_tick):
        if (self.render_step + 1) % render_steps_per_tick == 0:
            script()

    def handle_tick_loop_bool(self, render_steps_per_tick):
        if (self.render_step + 1) % render_steps_per_tick == 0:
            return True
        else:
            return False

    def handle_scripts(self):
        for script in engine_scripts:
            script(self.context)
        
    def handle_quit_button(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

    #WIP
    def get_events_bool_array(self, events_requested):
        bool_array = []
        
        return bool_array
    
    #WIP
    def handle_player_move_ws_binds(self, player_rectangle):
        bind_w_pressed, bind_s_pressed = self.get_events_bool_array([pg.K_w, pg.K_s])

        def handle_w_bind_move_up():
            player_rectangle.position.y = self.screen_proportional_vector2(0, -0.1) * self.delta_time
        def handle_s_bind_move_down():
            player_rectangle.position.y = self.screen_proportional_vector2(0, 0.1) * self.delta_time

        if bind_w_pressed:
            handle_w_bind_move_up()
        if bind_s_pressed:
            handle_s_bind_move_down()
        
    def clear_graphics(self):
        self.screen.fill((0,0,0))

    def handle_physics(self):
        for object in self.objects:
            if object.anchored == False:
                object.velocity += self.gravity * self.delta_time
                object.position += object.velocity * self.delta_time

    def handle_wall_colision(self):
        for object in self.objects:
            if object.anchored == False:
                if isinstance(object, Object.Circle):
                    self.handle_bottom_collision(object)
                    self.handle_top_collision(object)
                    self.handle_right_collision(object)
                    self.handle_left_collision(object)

    def handle_left_player_collision(self, obj, player_rectangle):
        x_hits_player = (obj.position.x - obj.radius < player_rectangle.position.x)
        y_hits_player_upper_bound = (obj.position.y > player_rectangle.position.y) 
        y_hits_player_lower_bound = (obj.position.y < player_rectangle.position.y + player_rectangle.size.y)
        if x_hits_player and y_hits_player_upper_bound and y_hits_player_lower_bound:
            obj.position.x = player_rectangle.position.x + player_rectangle.size.x
            obj.velocity.x = -obj.velocity.x

    def handle_bottom_collision(self, obj):
        screen_height = self.screen.get_height()
        if obj.position.y + obj.radius > screen_height:
            obj.position.y = screen_height - obj.radius
            obj.velocity.y = -obj.velocity.y

    def handle_top_collision(self, obj):
        if obj.position.y - obj.radius < 0:
            obj.position.y = obj.radius
            obj.velocity.y = -obj.velocity.y

    def handle_right_collision(self, obj):
        screen_width = self.screen.get_width()
        if obj.position.x + obj.radius > screen_width:
            obj.position.x = screen_width - obj.radius
            obj.velocity.x = -obj.velocity.x

    def handle_left_collision(self, obj):
        if obj.position.x - obj.radius < 0:
            obj.position.x = obj.radius
            obj.velocity.x = -obj.velocity.x

    def render_objects(self):
        for object in self.objects:
            if isinstance(object, Object.Rectangle):
                pg.draw.rect(self.screen, object.color, pg.Rect(object.position, object.size), object.width)
            elif isinstance(object, Object.Circle):
                pg.draw.circle(self.screen, object.color, object.position, object.radius, object.width)

    def display_graphics(self):
        pg.display.flip()
        self.delta_time = self.clock.tick(self.frame_rate) / 1000
        self.render_step += 1

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
