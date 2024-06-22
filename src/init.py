import engine
import loader

game = engine.Game()
player, ball = loader.init(game)

running = True
while running:
    game.handle_quit_button()
    game.handle_scripts()
    game.handle_physics()
    game.handle_wall_colision()
    game.handle_left_player_collision(ball, player)
    game.clear_graphics()
    game.render_objects()
    game.display_graphics()