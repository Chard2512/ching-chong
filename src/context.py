import engine

#Used on script construction for name shortening
class GameEditorContext:
    def __init__(self, game_instance):
        self.add_object = game_instance.objects.append
        self.delete_object = game_instance.objects.remove
        self.factory = engine.ObjectFactory(game_instance)
        self.game = game_instance
        self.loop_ticks = game_instance.handle_tick_loop_bool
        self.screen_vector2 = game_instance.screen_proportional_vector2
        self.screen_unit = game_instance.screen_height_proportional_unit
        