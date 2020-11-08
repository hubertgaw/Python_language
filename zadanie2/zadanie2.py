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


# metoda inicjalizujace owce ze wstepnymi wartosciami:
def sheeps_init():
    sheeps_list = []
    for i in range(sheeps_number):
        sheeps_list.append(Sheep(random.uniform(-init_pos_limit, init_pos_limit),
                                 random.uniform(-init_pos_limit, init_pos_limit)))

    for index, sheep in enumerate(sheeps_list):  # dzięki enumerate dostajemy indeks owcy w tablicy
        print("Owca nr.", index, "x:", sheep.x, "y:", sheep.y, "direction:", sheep.direction, "status:", sheep.status)
    return sheeps_list


# metoda odpowiadająca za ruch owcy:
def sheeps_move(sheeps_list):
    directions = ["N", "S", "E", "W"]
    for i in range(rounds_number):
        print("--------------------RUNDA:", i, "--------------------")
        for sheep in sheeps_list:
            sheep.direction = random.choice(directions)
            if sheep.direction == 'N':
                sheep.y = sheep.y + sheep_move_dist
            elif sheep.direction == 'S':
                sheep.y = sheep.y - sheep_move_dist
            elif sheep.direction == 'E':
                sheep.x = sheep.x + sheep_move_dist
            elif sheep.direction == 'W':
                sheep.x = sheep.x - sheep_move_dist
        for index, sheep in enumerate(sheeps_list):  # dzięki enumerate dostajemy indeks owcy w tablicy
            print("Owca nr.", index, "x:", sheep.x, "y:", sheep.y, "direction:", sheep.direction, "status:",
                  sheep.status)


def main():
    sheeps_move(sheeps_init())


if __name__ == "__main__":
    main()
