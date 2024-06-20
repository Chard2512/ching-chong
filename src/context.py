import engine

class GameContext:
    def __init__(self, game_instance):
        self.game = game_instance
        self.factory = engine.ObjectFactory(game_instance)
        self.screen_vector2 = game_instance.screen_proportional_vector2
        self.screen_unit = game_instance.screen_height_proportional_unit
        self.add_object = game_instance.objects.append