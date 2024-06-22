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

        self.events = []

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

    def get_events(self):
        self.events = pg.event.get()
        
    def handle_quit_button(self):
        event_types = (event.type for event in self.events)
        if pg.QUIT in event_types:
            pg.quit()
            sys.exit()

    def handle_player_move_mouse(self, player_rectangle):
        _, mouse_pos_y = pg.mouse.get_pos()

        player_rectangle.position.y = mouse_pos_y

    def get_key_events(self):
        event_key = []
        for event in self.events:
            if event.type == pg.KEYDOWN:
                event_key.append(event.key)
        
        return event_key
    
    def handle_player_move_ws_binds(self, player_rectangle):
        event_key = self.get_key_events()

        if pg.K_w in event_key:
            self.handle_w_bind_player_move_up(player_rectangle)
        if pg.K_s in event_key:
            self.handle_s_bind_player_move_down(player_rectangle)
    
    def handle_w_bind_player_move_up(self, player_rectangle):
            player_rectangle.position.y += self.screen_height_proportional_unit(-5) * self.delta_time

    def handle_s_bind_player_move_down(self, player_rectangle):
        player_rectangle.position.y += self.screen_height_proportional_unit(5) * self.delta_time
        
    def clear_graphics(self):
        self.screen.fill((0,0,0))

    def handle_physics(self):
        for object in self.objects:
            if object.anchored == False:
                object.velocity += self.gravity * self.delta_time
                object.position += object.velocity * self.delta_time

    def handle_wall_colision(self):
        for obj in self.objects:
            if obj.anchored == False:
                if isinstance(obj, Object.Circle):
                    self.handle_bottom_collision(obj)
                    self.handle_top_collision(obj)
                    self.handle_right_collision(obj)
                    self.handle_left_collision(obj)

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

    def get_balls(self):
        balls = []
        for obj in self.objects:
            if isinstance(obj, Object.Circle):
                balls.append(obj)

        return balls

    def handle_left_player_collision(self, player_rectangle):
        for ball in self.get_balls():
            ball_left_extremity = ball.position.x - ball.radius
            rectangle_right_extremity = player_rectangle.position.x + player_rectangle.size.x/2
            rectangle_upper_extremity = player_rectangle.position.y - player_rectangle.size.y/2
            rectangle_lower_extremity = player_rectangle.position.y + player_rectangle.size.y/2

            x_hits_rectangle = ball_left_extremity < rectangle_right_extremity
            y_hits_rectangle_upper_bound = ball.position.y > rectangle_upper_extremity                         
            y_hits_rectangle_lower_bound = ball.position.y < rectangle_lower_extremity

            if x_hits_rectangle and y_hits_rectangle_upper_bound and y_hits_rectangle_lower_bound:
                ball.position.x = player_rectangle.position.x + player_rectangle.size.x
                ball.velocity.x = -ball.velocity.x

    def render_objects(self):
        for obj in self.objects:
            if isinstance(obj, Object.Rectangle):
                rect_centered_position = pg.Vector2(obj.position.x - obj.size.x/2,
                                                    obj.position.y - obj.size.y/2)
                pg.draw.rect(self.screen, obj.color, pg.Rect(rect_centered_position, obj.size), obj.width)
            elif isinstance(obj, Object.Circle):
                pg.draw.circle(self.screen, obj.color, obj.position, obj.radius, obj.width)

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
