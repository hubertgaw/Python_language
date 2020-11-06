class Sheep:
    # atrybuty klasowe, czyli wspoldzielona przez wszystkie obiekty klasy:
    init_pos_limit = 10.0
    sheep_move_dist = 0.5

    # atrybuty instancyjne, czyli związane z okreslonym obiektem:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction


# Byc moze w owcy wystarczą atrybuty x i y, jeszcze to przemysle

class Wolf:
    # atrybuty klasowe (z góry mamy powiedziane, że będzie jeden wilk zatem będa tylko atrybuty klasowe)
    wolf_move_dist = 1.0
    x = 0.0
    y = 0.0
