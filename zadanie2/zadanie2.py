import random
import math

rounds_number = 50
sheeps_number = 15
init_pos_limit = 10.0
sheep_move_dist = 0.5
wolf_move_dist = 1.0


class Sheep:
    # atrybuty klasowe, czyli wspoldzielona przez wszystkie obiekty klasy:

    # atrybuty instancyjne, czyli związane z okreslonym obiektem:
    def __init__(self, identify_number, x, y, direction='N'):
        self.identify_number = identify_number
        self.x = random.uniform(-init_pos_limit, init_pos_limit)
        self.y = random.uniform(-init_pos_limit, init_pos_limit)
        self.direction = direction
        self.status = 'alive'


# Byc moze w owcy wystarczą atrybuty x i y, jeszcze to przemysle

class Wolf:
    # atrybuty klasowe (z góry mamy powiedziane, że będzie jeden wilk zatem będa tylko atrybuty klasowe)
    x = 0.0
    y = 0.0


wolf = Wolf()  # globalna zmienna wilk (nie wiem czy to poprawna konwencja)


# metoda inicjalizujace owce ze wstepnymi wartosciami:
def sheeps_init():
    sheeps_list = []  # lista owiec, które będdą brały udział w symulacji
    # petla, która wstawia owce do listy, ze wstepnie zainicjalizowanymi losowymi wartosicam
    for i in range(sheeps_number):
        sheeps_list.append(Sheep(i, random.uniform(-init_pos_limit, init_pos_limit),
                                 random.uniform(-init_pos_limit, init_pos_limit)))

    for index, sheep in enumerate(sheeps_list):  # dzięki enumerate dostajemy indeks owcy w tablicy
        print("START Owca nr.", sheep.identify_number, "x:", sheep.x, "y:", sheep.y, "direction:", sheep.direction,
              "status:", sheep.status)
    return sheeps_list  # zwracamy listę owiec


# metoda odpowiadająca za ruch owcy:
def sheeps_move(sheeps_list):
    directions = ["N", "S", "E", "W"]  # tablica odpowiadająca za kierunki
    # pętla, w której losujemy kierunek dla każdej owcy w liście przed każdą rundą:
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
    return sheeps_list


# funkcja majaca na celu policzenie odleglosci pomiedzy wilkiem a żyjacymi owcami i wskazanie najblizszej:
def find_nearest_distance(sheeps_list):
    distances = {}  # słownik, w którym klucze toindeksy owiec, a wartosci to odleglosci pomiedzy owca(zyjaca), a wilkiem
    for sheep in sheeps_list:
        if sheep.status == 'alive':
            distances[sheep.identify_number] = math.sqrt((Wolf.x - sheep.x) ** 2 + (Wolf.y - sheep.y) ** 2)
    min_distance_index = min(distances.keys(), key=(lambda k: distances[k]))  # min_distance_index jest to indeks
    # owcy, do której wilkowi najbliżej
    return min_distance_index, distances[
        min_distance_index]  # zwracamy indeks najblizszej owcy oraz tą najbliżsszą odległość


def wolf_move(index, nearest_distance, sheeps_list):
    if nearest_distance < wolf_move_dist:
        wolf.x = sheeps_list[index].x
        wolf.y = sheeps_list[index].y
        sheeps_list[index].status = 'dead'


def main():
    start_sheeps = sheeps_init()
    for i in range(rounds_number):
        print("--------------------RUNDA:", i, "--------------------")
        sheeps_list = sheeps_move(start_sheeps)  # lista owiec po przemieszczeniu się
        index_of_sheep_with_nearest_distance, nearest_distance = find_nearest_distance(
            sheeps_list)  # odleglosc pomiedzy wilkiem a
        # najblizsza z owiec (tak wiem, tworcza nazwa)
        wolf_move(index_of_sheep_with_nearest_distance, nearest_distance, sheeps_list)


if __name__ == "__main__":
    main()
