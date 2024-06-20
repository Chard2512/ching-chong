import engine
import loader

game = engine.Game()
loader.init(game)

running = True
while running:
    game.handle_quit_button()
    game.clear_graphics()
    game.render_physics()
    game.render_objects()
    game.display_graphics()