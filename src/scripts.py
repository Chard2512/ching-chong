def circle_in_the_center(context):
    circle = context.factory.new('Circle')
    circle.position = context.screen_vector2(0.5, 0.5)
    circle.radius = context.screen_unit(0.05)
    context.add_object(circle)