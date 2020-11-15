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


# wolf = Wolf()  # globalna zmienna wilk (nie wiem czy to poprawna konwencja)


# metoda inicjalizujace owce ze wstepnymi wartosciami:
def sheeps_init():
    sheeps_list = []  # lista owiec, które będdą brały udział w symulacji
    # petla, która wstawia owce do listy, ze wstepnie zainicjalizowanymi losowymi wartosicam
    for i in range(sheeps_number):
        sheeps_list.append(Sheep(i, random.uniform(-init_pos_limit, init_pos_limit),
                                 random.uniform(-init_pos_limit, init_pos_limit)))
    # # wyswietlenie owiec startowych
    # for sheep in sheeps_list:  # dzięki enumerate dostajemy indeks owcy w tablicy
    #     print("START Owca nr.", sheep.identify_number, "x:", sheep.x, "y:", sheep.y, "direction:", sheep.direction,
    #           "status:", sheep.status)
    return sheeps_list  # zwracamy listę owiec


# metoda odpowiadająca za ruch owcy:
def sheeps_move(sheeps_list):
    directions = ["N", "S", "E", "W"]  # tablica odpowiadająca za kierunki
    # pętla, w której losujemy kierunek dla każdej owcy w liście przed każdą rundą:
    for sheep in sheeps_list:
        if sheep.status == 'alive':
            sheep.direction = random.choice(directions)
            if sheep.direction == 'N':
                sheep.y = sheep.y + sheep_move_dist
            elif sheep.direction == 'S':
                sheep.y = sheep.y - sheep_move_dist
            elif sheep.direction == 'E':
                sheep.x = sheep.x + sheep_move_dist
            elif sheep.direction == 'W':
                sheep.x = sheep.x - sheep_move_dist
    # # wyswietlenie owiec:
    # for index, sheep in enumerate(sheeps_list):  # dzięki enumerate dostajemy indeks owcy w tablicy
    #     print("Owca nr.", index, "x:", sheep.x, "y:", sheep.y, "direction:", sheep.direction, "status:",
    #           sheep.status)
    return sheeps_list  # chyba nie musimy w sumie zwracac sheeps_list


# funkcja majaca na celu policzenie odleglosci pomiedzy wilkiem a żyjacymi owcami i wskazanie najblizszej:
def find_nearest_distance(sheeps_list, wolf):
    distances = {}  # słownik, w którym klucze to indeksy owiec, a wartosci to odleglosci pomiedzy owca(zyjaca),
    # a wilkiem
    for sheep in sheeps_list:
        if sheep.status == 'alive':  # oczywiscie zwracamy tylko odleglość pomiędzy wilkiem a owcami żyjącymi
            # wstawiamy dystanse wraz z odpowiadającymi im indeksami owiec do słownika:
            distances[sheep.identify_number] = math.sqrt((wolf.x - sheep.x) ** 2 + (wolf.y - sheep.y) ** 2)
    min_distance_index = min(distances.keys(), key=(lambda k: distances[k]))  # min_distance_index jest to indeks
    # owcy, do której wilkowi najbliżej
    return min_distance_index, distances[
        min_distance_index]  # zwracamy indeks najblizszej owcy oraz tą najbliżsszą odległość


# funkcja odpowiedzialna za ruch wilka
def wolf_move(index, nearest_distance, sheeps_list, wolf):
    # Jeśli owca w zasięgu to wilk ją zjada (przesuwa się na jej mmiejsce, a status owcy zmienia się na 'dead':
    if nearest_distance < wolf_move_dist:
        wolf.x = sheeps_list[index].x
        wolf.y = sheeps_list[index].y
        sheeps_list[index].status = 'dead'
        print("Pozarto owce nr.", sheeps_list[index].identify_number)  # informacja ktora owce pozarto
    else:
        wolf.x = wolf.x + (wolf_move_dist * (sheeps_list[index].x - wolf.x) / nearest_distance)  # nowe położenie
        # wilka obliczone ze wzoru: x + dystans_ataku_wilka * (xOwcy - xWilka) / dystans_miedzy_wilkiem_i_owcą
        wolf.y = wolf.y + (wolf_move_dist * (sheeps_list[index].y - wolf.y) / nearest_distance)  # analogicznie jw.
    print("WILK: x:", format(wolf.x, '.3f'), "y:", format(wolf.y, '.3f'))  # wyswietlenie info o wilku


# dunkcja sprawdzająca czy wszystkie owce są martwe:
def check_if_all_sheeps_are_dead(sheeps_list):
    for sheep in sheeps_list:
        if sheep.status == 'alive':  # jeśli jest jakakolwiek żywa zwracamy True
            return False
    return True


# funkcja do liczenia żywych owiec
def count_alive_sheeps(sheeps_list):
    alive_sheeps_list = []  # lista żywych owiec
    for sheep in sheeps_list:
        if sheep.status == 'alive':
            alive_sheeps_list.append(sheep)
    return len(alive_sheeps_list)

# funkcja, która sporządzi listę gotową do zapisania w pliku pos.json
def prepare_list_to_export_to_json(round_no, wolf_pos_x, wolf_pos_y, sheeps_list):
    list_of_dictionaries = [] # lista, która bedzie przechowywała słowniki
    sheeps_pos_list = [] # lista zawierajaca pary liczb - pozycje owiec dla owcy żywych lub null dla pożartych
    for sheep in sheeps_list:
        sheeps_pos_list.append(sheep.x + ", " + sheep.y)
    list_of_dictionaries.append({
        "round_no": round_no,
        "wolf pos": wolf_pos_x + ", " + wolf_pos_y
        "sheep_pos": sheeps_pos_list
    })

def export_to_json(file_name,sheeps_list):
    return

def main():
    start_sheeps = sheeps_init()  # owce ze wstępnie zainicjalizowanymi atrybutami
    wolf = Wolf()  # zmienna reprezentujaca wilka (domyslnie znajduje sie w (0,0))
    # petla, w której jedna iteracja odpowiada jednej rundzie:
    for i in range(rounds_number):
        print("--------------------RUNDA:", i + 1, "--------------------")
        sheeps_list = sheeps_move(start_sheeps)  # lista owiec po przemieszczeniu się
        index_of_sheep_with_nearest_distance, nearest_distance = find_nearest_distance(
            sheeps_list, wolf)  # indeks owcy, do której wilk ma najbliżej i odleglosc pomiedzy wilkiem a najblizsza
        # z owiec
        # print("nearest distance:", nearest_distance, "index:", index_of_sheep_with_nearest_distance)
        wolf_move(index_of_sheep_with_nearest_distance, nearest_distance, sheeps_list, wolf)  # ruch wilka
        if check_if_all_sheeps_are_dead(sheeps_list):  # sprawdzamy czy wszystkie owce są martwe
            print("All sheeps are dead after round", i + 1)
            break
        else:
            print("Zywych owiec:", count_alive_sheeps(sheeps_list))  # liczymy zywe owce
        prepare_list_to_export_to_json(i+1, wolf.x, wolf.y, sheeps_list)

if __name__ == "__main__":
    main()
