def create_ball(context):
    ball = context.factory.new('Circle')
    ball.position = context.screen_vector2(0.2, 0.5)
    ball.radius = context.screen_unit(0.01)

    ball.velocity = context.screen_vector2(0.5, 0.3)

    context.add_object(ball)

    return ball

def player_rectangle(context):
    rectangle = context.factory.new('Rectangle')
    rectangle.position = context.screen_vector2(0.0495, 0.4)
    rectangle.size = context.screen_vector2(0.01, 0.2)

    context.add_object(rectangle)

    return rectangle

def zero_gravity(context):
    context.game.gravity = context.screen_vector2(0, 0)

engine_scripts = []