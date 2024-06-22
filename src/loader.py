from context import GameEditorContext
import scripts

def init(game_instance):
    context = GameEditorContext(game_instance)

    player = scripts.player_rectangle(context)
    ball = scripts.create_ball(context)

    
    scripts.zero_gravity(context)

    return player, ball