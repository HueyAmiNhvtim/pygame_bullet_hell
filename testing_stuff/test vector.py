from pygame import Vector2

test_vector = Vector2(16, 9)
another = Vector2(12, 13)
print(test_vector.angle_to(another))
print(test_vector.rotate(30))