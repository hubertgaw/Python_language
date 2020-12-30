import random
import math
import json
import os
import csv
import argparse
import logging
import distutils
from configparser import ConfigParser


# Co do zastosowanej notacji przy wypisywaniu i przy eksportowaniu do plików - jesli owca zostanie zjedzona w danej
# rundzie, nie jest ona wypisywana, np w rundzie 23 wilk zjada owce nr 2 - czyli wypisujemy pozycje owcy w rundzie
# 22, potem w rundzie 23 przesuwa się ona i wilk ją zjada - ale jej pozycji w tej rundzie nie wypisujemy, jako,
# że na koniec rundy jest martwa, a założyłem ze wypisywane informacje odnoszą się do momentu zakończenia rundy.
# Jesli stwierdzimy inaczej moge to zmienic

class Sheep:

    # atrybuty instancyjne, czyli związane z okreslonym obiektem:
    def __init__(self, identify_number, x, y, direction='N'):
        self.identify_number = identify_number  # identify_number to numer owcy w kolejnosci(od 0)
        self.x = x  # losujemy x i y
        self.y = y
        self.direction = direction  # ustawiamy wstępny domyślny kierunek na N (mozna go zmienic
        # przekazujac inny w konstruktorze)
        self.status = 'alive'  # ustawiamy wstepny status na alive (jego w konnstruktorze nie zmienimy)


class Wolf:
    # atrybuty klasowe (z góry mamy powiedziane, że będzie jeden wilk zatem będa tylko atrybuty klasowe)
    x = 0.0
    y = 0.0


# metoda inicjalizujace owce ze wstepnymi wartosciami:
def sheeps_init(sheeps_number, init_pos_limit):
    sheeps_list = []  # lista owiec, które będdą brały udział w symulacji
    # petla, która wstawia owce do listy, ze wstepnie zainicjalizowanymi losowymi wartosicam
    logging.info("initialisation of sheep list, primary coordinates:")
    for i in range(sheeps_number):
        sheeps_list.append(
            Sheep(i, random.uniform(-init_pos_limit, init_pos_limit), random.uniform(-init_pos_limit, init_pos_limit)))
        logging.info("sheep nr " + str(sheeps_list[i].identify_number) + " with position (" + str(sheeps_list[i].x) + ", " + str(sheeps_list[i].y) + ")")
    logging.debug("sheeps_init(" + str(sheeps_number) + str(init_pos_limit) + ") called, returned " + str(sheeps_list))

    return sheeps_list  # zwracamy listę owiec


# metoda odpowiadająca za ruch owcy:
def sheeps_move(sheeps_list, sheep_move_dist):
    directions = ["N", "S", "E", "W"]  # tablica odpowiadająca za kierunki
    # pętla, w której losujemy kierunek dla każdej owcy w liście przed każdą rundą:
    logging.info("movement of sheeps:")
    for sheep in sheeps_list:
        if sheep.status == 'alive':
            sheep.direction = random.choice(directions)  # tutaj odbywa się losowanie kierunku
            # po wylosowaniu kierunku "poruszamy" owce
            if sheep.direction == 'N':
                sheep.y = sheep.y + sheep_move_dist
            elif sheep.direction == 'S':
                sheep.y = sheep.y - sheep_move_dist
            elif sheep.direction == 'E':
                sheep.x = sheep.x + sheep_move_dist
            elif sheep.direction == 'W':
                sheep.x = sheep.x - sheep_move_dist
        logging.info("sheep nr " + str(sheep.identify_number) + " with position (" + str(sheep.x) + ", " + str(sheep.y) + ")")
    logging.debug("sheeps_move(" + str(sheeps_list) + str(sheep_move_dist) + ") called, returned " + str(sheeps_list))
    return sheeps_list


# funkcja majaca na celu policzenie odleglosci pomiedzy wilkiem a żyjacymi owcami i wskazanie najblizszej:
def find_nearest_distance(sheeps_list, wolf):
    distances = {}  # słownik, w którym klucze to indeksy owiec, a wartosci to odleglosci
    # pomiedzy owca(zyjaca), a wilkiem
    for sheep in sheeps_list:
        if sheep.status == 'alive':  # oczywiscie zwracamy tylko odleglość pomiędzy wilkiem a owcami żyjącymi
            # wstawiamy dystanse wraz z odpowiadającymi im indeksami owiec do słownika:
            distances[sheep.identify_number] = math.sqrt((wolf.x - sheep.x) ** 2 + (wolf.y - sheep.y) ** 2)
    min_distance_index = min(distances.keys(), key=(
        lambda k: distances[k]))  # min_distance_index jest to indeks owcy, do której wilkowi najbliżej
    logging.debug("find_nearest_distance(" + str(sheeps_list) + wolf.__str__() + ") called, returned " + str(
        min_distance_index) + str(distances[min_distance_index]))
    return min_distance_index, distances[
        min_distance_index]  # zwracamy indeks najblizszej owcy oraz tą najbliżsszą odległość


# funkcja odpowiedzialna za ruch wilka
def wolf_move(index_of_sheep, nearest_distance, sheeps_list, wolf, wolf_move_dist, round_number, list_to_json):
    logging.debug("wolf_move(" + str(index_of_sheep) + str(nearest_distance) + str(sheeps_list) + wolf.__str__() + str(
        wolf_move_dist) + ") called")
    logging.info("wolf movement from " + str(wolf.x) + ", " + str(wolf.y))
    # Jeśli owca w zasięgu to wilk ją zjada (przesuwa się na jej miejsce, a status owcy zmienia się na 'dead':
    if nearest_distance < wolf_move_dist:
        wolf.x = sheeps_list[index_of_sheep].x
        wolf.y = sheeps_list[index_of_sheep].y
        prepare_list_to_export_to_json(round_number, wolf.x, wolf.y, sheeps_list, list_to_json)
        sheeps_list[index_of_sheep].status = 'dead'
        print("Pozarto owce nr.", sheeps_list[index_of_sheep].identify_number)  # informacja ktora owce pozarto
        logging.info("wolf ate a sheep with a number " + str(sheeps_list[index_of_sheep].identify_number))
    else:
        wolf.x = wolf.x + (
                wolf_move_dist * (sheeps_list[index_of_sheep].x - wolf.x) / nearest_distance)  # nowe położenie
        # wilka obliczone ze wzoru: x + dystans_ataku_wilka * (xOwcy - xWilka) / dystans_miedzy_wilkiem_i_owcą
        wolf.y = wolf.y + (
                wolf_move_dist * (sheeps_list[index_of_sheep].y - wolf.y) / nearest_distance)  # analogicznie jw.
        prepare_list_to_export_to_json(round_number, wolf.x, wolf.y, sheeps_list, list_to_json)
    logging.info("wolf movement to " + str(wolf.x) + ", " + str(wolf.y))
    print("WILK: x:", format(wolf.x, '.3f'), "y:", format(wolf.y, '.3f'))  # wyswietlenie info o wilku


# funkcja do liczenia żywych owiec
def count_alive_sheeps(sheeps_list):
    alive_sheeps_list = []  # lista żywych owiec
    for sheep in sheeps_list:
        if sheep.status == 'alive':
            alive_sheeps_list.append(sheep)
    logging.debug("count_alive_sheeps(" + str(sheeps_list) + ") called, returned " + str(len(alive_sheeps_list)))
    logging.info("alive sheeps number is " + str(len(alive_sheeps_list)))
    return len(alive_sheeps_list)


# funkcja, która sporządzi listę gotową do zapisania w pliku pos.json
def prepare_list_to_export_to_json(round_no, wolf_pos_x, wolf_pos_y, sheeps_list, list_of_dictionaries):
    logging.debug(
        "prepare_list_to_export_to_json(" + str(round_no) + str(wolf_pos_x) + str(wolf_pos_y) + str(sheeps_list) + str(
            list_of_dictionaries) + ") called")
    # list_of_dicitionaries - czyli lista, która bedzie przchowyywała słowniki (ta, ktora wyeksportujemy do json)
    sheeps_pos_list = []  # lista zawierajaca pary liczb - pozycje owiec dla owcy żywych lub null dla pożartych
    for sheep in sheeps_list:
        if sheep.status == 'alive':  # jesli owca żywa to dodajemy jej wspołrzedne
            sheeps_pos_list.append(str(sheep.x) + ", " + str(sheep.y))
        else:
            sheeps_pos_list.append(None)  # jeśli zjedzona to None
    list_of_dictionaries.append({
        "round_no": round_no,
        "wolf pos": str(wolf_pos_x) + ", " + str(wolf_pos_y),
        "sheep_pos": sheeps_pos_list
    })


# funkcja, ktora eksportuje naszą liste do jsona
def export_to_json(file_name, sheeps_list, directory):
    logging.debug("export_to_json(" + str(file_name) + str(sheeps_list) + ") called")
    # działanie na pliku tak jak w cwiczeniu wprowadzajacym:
    with open(file_name, 'w') as f:
        f.write(
            json.dumps(sheeps_list, indent=4))  # indent oznacza wciecia (aby wyswietlalo sie w pliku w ładny sposób)


# funkcja eksportująca do csv
def export_to_csv(file_name, round_no, sheeps_no, directory):
    logging.debug("export_to_csv(" + str(file_name) + str(round_no) + str(sheeps_no) + ") called")
    if round_no == 1:  # jeśli pierwsza runda to nadpisujemy plik (mode='w')
        with open(file_name, 'w', newline='') as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            writer.writerow([round_no, sheeps_no])
    else:  # kazda nastepna to dodajemy do istniejącego pliku (mode='a')
        with open(file_name, mode='a', newline='') as csv_file:
            writer = csv.writer(csv_file, delimiter=',')  # delimiter - za pomocą czego oddzielamy wartosci
            writer.writerow([round_no, sheeps_no])


# wczytanie wartości z pliku konfiguracyjnego gdy jest argument wywołania -c/--config
def parse_config(file):
    config = ConfigParser()
    config.read(file)  # czytanie plku konfiguracyjnego
    init = config.get('Terrain', 'InitPosLimit')  # getter - pierwszy parametr to sekcja, a drugi to zmienna
    sheeps = config.get('Movement', 'SheepMoveDist')
    wolf = config.get('Movement', 'WolfMoveDist')

    if float(init) < 0 or float(sheeps) < 0 or float(wolf) < 0:  # sprawdzanie warunków dodatnich liczb z pliku
        logging.error("not positive number passed as argument")
        raise ValueError("Not positive number")
    logging.debug("parse_config(", file, ") called, returned: ", float(init), float(sheeps), float(wolf))
    return float(init), float(sheeps), float(wolf)


# funkcja sprawdzająca czy podana liczba jest dodatnia
def check_positive(value):
    ivalue = int(value)
    if ivalue <= 0:
        logging.error("argument is not a positive number")
        raise argparse.ArgumentTypeError("%s is an invalid positive int value" % value)  # raise - wyrzucenie błędu
    logging.debug("check_positive(", value, ") called, returned,", ivalue)
    return ivalue


# funkcja odpowiadająca za "właściwa symulacje":
def simulation(rounds_number, sheeps_number, init_pos_limit, sheep_move_dist, wolf_move_dist, wait, directory):
    logging.info("start a simulation")
    logging.debug(
        "simulation(" + str(rounds_number) + str(sheeps_number) + str(init_pos_limit) + str(sheep_move_dist) +
        str(wolf_move_dist) + str(wait) + str(directory) + ") called")

    start_sheeps = sheeps_init(sheeps_number, init_pos_limit)  # owce ze wstępnie zainicjalizowanymi atrybutami
    wolf = Wolf()  # zmienna reprezentujaca wilka (domyslnie znajduje sie w (0,0))
    # petla, w której jedna iteracja odpowiada jednej rundzie:
    list_for_export_to_json = []  # lista, która wyeksportujemy do pliku pos.json
    for i in range(rounds_number):
        print("--------------------RUNDA:", i + 1, "--------------------")
        sheeps_list = sheeps_move(start_sheeps, sheep_move_dist)  # lista owiec po przemieszczeniu się
        index_of_sheep_with_nearest_distance, nearest_distance = find_nearest_distance(
            sheeps_list,
            wolf)  # indeks owcy, do której wilk ma najbliżej i odleglosc pomiedzy wilkiem a najblizsza z owiec
        wolf_move(index_of_sheep_with_nearest_distance, nearest_distance, sheeps_list, wolf, wolf_move_dist, i + 1,
                  list_for_export_to_json)  # ruch wilka
        alive = count_alive_sheeps(sheeps_list)
        print("Zywych owiec:", alive)  # liczymy zywe owce
        export_to_csv('alive.csv', i + 1, alive, directory)
        if alive == 0:
            print("All sheeps are dead after round", i + 1)
            break
        if wait:
            input("\nPress a key to continue...")
    export_to_json('pos.json', list_for_export_to_json, directory)


# funkcja do tworzenia katalogow na pliki powstale w ramach symulacji
def create_directory(directory):
    # tu nie ma logging.debug bo porzy wywolywaniu tej funkcji jeszcze nie mamy zrobionego logging.basicConfig,
    # a jak tu zostawimy debuga to sie wgl plik nie tworzy
    # logging.debug(
    #     "create_directory(" + str(directory) + ") called")
    try:
        direct = os.getcwd()  # pobranie bieżącej ścieżki
        path = direct + '\\' + directory
        direct_path = os.path.dirname(path)
        if not os.path.exists(direct_path):  # jeśli katalog nie istnieje
            print("Create a directory")
            logging.info("create a new directory to sava files")
            os.mkdir(directory)  # to go tworzymy
        os.chdir(directory)  # katalog biezacy na nowo stworzony
    except IOError:
        print("Error with directory occured!")
        logging.error("error with directory occured")


def main():
    rounds_number = 50
    sheeps_number = 15
    init_pos_limit = 10.0
    sheep_move_dist = 0.5
    wolf_move_dist = 1.0
    wait = False
    directory = None
    # komendy do lini poleceń
    parser = argparse.ArgumentParser()
    # dodanie argumentu, pierwsze dwa parametry to nazwa skrócona i długa, później jest opis
    # wyświetlany w help'ie, action = store określa, że wartość ma zostać zapisana po ewentualnej konwersji
    # dest określa nazwę argumentu, dzięki której możemy się do niego odwołać w kodzie, metavar określa
    # nazwę oczekiwanej wartości po wywołaniu przetwarzanego argumentu
    parser.add_argument('-c', '--config', help='set config file', action='store', dest='config', metavar='FILE')
    parser.add_argument('-d', '--dir', help='choose place to save files pos.json, alive.csv and chase.log (if -c '
                                            'option given)', action='store', dest='directory', metavar='DIR')
    parser.add_argument('-l', '--log', help='defines the level of events to be recorded in the log',
                        action='store', dest='log_level', metavar="LEVEL", )
    # type - określa typ wprowadzonej wartości, my potrzebujemy dodatnie, co jest sprawdzane przez odpowiednią funkcję
    parser.add_argument('-r', '--rounds', help='defines the number of turns', action='store', dest='rounds_number',
                        metavar='NUM', type=check_positive)
    parser.add_argument('-s', '--sheep', help='defines the number of sheeps', action='store', dest='sheeps_number',
                        metavar='NUM', type=check_positive)
    # store_true zapisuje odpowiednią wartość boolean
    parser.add_argument('-w', '--wait',
                        help='wait for keystroke to be pressed after displaying basic information about the simulation status at the end od each turn',
                        action='store_true', dest='waiting')
    args = parser.parse_args()  # przetwarzanie argumentów, sprawdzenie wiersza poleceń i konwersja, a następnie wywołanie odpowiedniej akcji
    # wszystkie if'y odwołują się do parametru 'dest' i spełniają odpowiednie kryteria, np. ustawianie wartości
    if args.config:
        init_pos_limit, sheep_move_dist, wolf_move_dist = parse_config(args.config)
    if args.directory:
        directory = args.directory
        create_directory(directory)  # jak mamy podana directory z cmd to od razu ja tworzymy
    if args.log_level:  # wszystkie if'y sprawdzają, czy wartość zmiennej LEVEL jest zgodna z oczekiwaną, jesli nie, to wywala błąd
        if args.log_level == "DEBUG":
            level = logging.DEBUG
        elif args.log_level == "INFO":
            level = logging.INFO
        elif args.log_level == "WARNING":
            level = logging.WARNING
        elif args.log_level == "ERROR":
            level = logging.ERROR
        elif args.log_level == "CRITICAL":
            level = logging.CRITICAL
        else:
            raise ValueError("Invalid log level!")
        logging.basicConfig(level=level,
                            # wykonuje podstawową konfigurację systemu logowania, z określonym poziomem i nazwą pliku
                            filename='chase.log',
                            filemode='w')
    if args.rounds_number:
        rounds_number = args.rounds_number
    if args.sheeps_number:
        sheeps_number = args.sheeps_number
    if args.waiting:
        wait = args.waiting

    simulation(rounds_number, sheeps_number, init_pos_limit, sheep_move_dist, wolf_move_dist, wait, directory)


if __name__ == "__main__":
    main()
