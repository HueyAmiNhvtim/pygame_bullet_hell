from pygame import Vector2

test_vector = Vector2(100, 150)
test_vector[0] = 69
print(test_vector.normalize())
print(test_vector.rotate(-90))