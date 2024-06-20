from context import GameContext
import scripts

def init(game_instance):
    context = GameContext(game_instance)

    scripts.circle_in_the_center(context)