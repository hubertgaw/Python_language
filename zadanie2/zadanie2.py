import random

rounds_number = 50
sheeps_number = 15
init_pos_limit = 10.0
sheep_move_dist = 0.5


class Sheep:
    # atrybuty klasowe, czyli wspoldzielona przez wszystkie obiekty klasy:

    # atrybuty instancyjne, czyli związane z okreslonym obiektem:
    def __init__(self, x, y, direction='N'):
        self.x = random.uniform(-init_pos_limit, init_pos_limit)
        self.y = random.uniform(-init_pos_limit, init_pos_limit)
        self.direction = direction
        self.status = 'alive'


# Byc moze w owcy wystarczą atrybuty x i y, jeszcze to przemysle

class Wolf:
    # atrybuty klasowe (z góry mamy powiedziane, że będzie jeden wilk zatem będa tylko atrybuty klasowe)
    wolf_move_dist = 1.0
    x = 0.0
    y = 0.0


def main():
    sheeps_list = []
    for i in range(sheeps_number):
        sheeps_list.append(Sheep(random.uniform(-init_pos_limit, init_pos_limit),
                                 random.uniform(-init_pos_limit, init_pos_limit)))
    licznik = 1
    for sheep in sheeps_list:
        print("Owca nr.", licznik, "x:", sheep.x, "y:", sheep.y, "direction:", sheep.direction, "status:", sheep.status)
        licznik = licznik + 1


if __name__ == "__main__":
    main()
