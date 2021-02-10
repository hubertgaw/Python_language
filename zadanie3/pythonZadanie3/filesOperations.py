import json


# funkcja, która sporządzi slownik danych gotowy do zapisania w pliku o rozszerzeniu json
from sheep import Sheep, draw_sheep
from sheepsList import SheepList
from wolf import Wolf, draw_wolf


def prepare_list_to_export_to_json(wolf, sheeps_list, sheep_color, bgColor):
    # list_of_dicitionaries - czyli lista, która bedzie przchowyywała słowniki (ta, ktora wyeksportujemy do json)
    sheeps_pos_list = []  # lista zawierajaca pary liczb - pozycje owiec dla owcy żywych lub null dla pożartych
    for sheep in sheeps_list:
        if sheep.status == 'alive':  # zapisujemy wspolrzedne tylko zywych owiec
            sheeps_pos_list.append(str(sheep.x) + ", " + str(sheep.y))
    list_of_dictionaries = {
        "bg_color": bgColor,
        "wolf_color": wolf.wolf_color,
        "wolf_pos": str(wolf.x) + ", " + str(wolf.y),
        "sheep_color": sheep_color,
        "sheep_pos": sheeps_pos_list
    }
    return list_of_dictionaries


# funkcja, ktora eksportuje naszą liste do jsona
def export_to_json(sheep_list, f):
    # zapis do pliku
    f.write(json.dumps(sheep_list, indent=6))  # indent oznacza wciecia (aby wyswietlalo sie w pliku w ładny sposób)
    # zamkniecie pliku
    f.close()


def import_from_json(f, meadow, scale, sheep_list_sheeps, points_list):
    meadow.delete("all")
    sheep_list_sheeps.clear()
    points_list.clear()
    scale.set(0)

    # zapis danych z pliku do zmiennej
    with open(f) as json_file:
        data = json.load(json_file)

        # zapis poszczegolnych fragmentow do zmiennych
        bg_color = data['bg_color']
        wolf_color = data['wolf_color']
        wolf_pos = data['wolf_pos']
        sheep_color = data['sheep_color']
        sheep_pos = data['sheep_pos']

        # podzial zmiennej wolf_pos na liste z wspolrzednymi wilka
        wolf_after = wolf_pos.split(',')
        wolf_x = wolf_after[0]
        wolf_y = wolf_after[1]

        # przypisanie wszystkich atrybutow do wilka
        wolf = Wolf()
        wolf.x = float(wolf_x)
        wolf.y = float(wolf_y)
        wolf.wolf_color = wolf_color
        drawn_wolf = draw_wolf(meadow, wolf.x, wolf.y, wolf.wolf_color, scale)

        # ilosc owiec zapisanych w pliku
        length = len(sheep_pos)

        # stworzenie listy owiec, do ktorej zapisze sie dane z pliku
        sheep_list_sheeps = SheepList()

        for i in range(0, length):
            # dzielimy kazdy element listy na mniejsza tablice, ktorej pierwszy element to x, a drugi to y
            pom = sheep_pos[i].split(',')
            # konwertujemy elementy tablicy na float
            x = float(pom[0])
            y = float(pom[1])
            # dodajemy owce o wspolrzednych z pliku do stworzonej listy
            sheep_list_sheeps.sheep_add(Sheep(i, x, y))
            # rysujemy te owce na lace
            point = draw_sheep(meadow, x, y, sheep_color, scale)
            # dodajemy narysowane punkty do listy
            sheep_list_sheeps.point_add(point)

        # każdej owcy z listy ustawiamy kolor wczytany z pliku
        for sheep in sheep_list_sheeps.sheep_list:
            sheep.sheep_color = sheep_color

        # zwracamy te elementy, ktore sa istotne przy kolejnych krokach symulacji
        return sheep_color, wolf, drawn_wolf, bg_color


