import math

from sheep import draw_sheep


class SheepList:
    sheep_list = []  # lista owiec, które będdą brały udział w symulacji
    points_list = []  # lista punktów reprezentujących owce na mapie

    # metoda dodajaca owce do listy:
    def sheep_add(self, sheep):
        self.sheep_list.append(sheep)

    def count(self):
        return len(self.sheep_list)

    # funkcja do liczenia żywych owiec
    def count_alive_sheeps(self):
        alive_sheeps_list = []  # lista żywych owiec

        for sheep in self.sheep_list:
            if sheep.status == 'alive':
                alive_sheeps_list.append(sheep)

        return len(alive_sheeps_list)

    def sheep_move(self):
        # pętla, w której losujemy kierunek dla każdej owcy w liście przed każdą rundą
        for sheep in self.sheep_list:
            sheep.move()

    def sheep_draw_all(self, meadow, power):
        for point in self.points_list:
            meadow.delete(point)

        for sheep in self.sheep_list:
            if sheep.status == "alive":
                point = draw_sheep(meadow, sheep.x, sheep.y, sheep.sheep_color, power)
                self.point_add(point)

    # funkcja majaca na celu policzenie odleglosci pomiedzy wilkiem a żyjacymi owcami i wskazanie najblizszej
    def find_nearest_distance(self, wolf):
        distances = {}  # słownik, w którym klucze to indeksy owiec, a wartosci to odleglosci

        # pomiedzy owca(zyjaca), a wilkiem
        for sheep in self.sheep_list:
            if sheep.status == 'alive':  # oczywiscie zwracamy tylko odleglość pomiędzy wilkiem a owcami żyjącymi
                # wstawiamy dystanse wraz z odpowiadającymi im indeksami owiec do słownika:
                distances[sheep.identify_number] = math.sqrt((wolf.x - sheep.x) ** 2 + (wolf.y - sheep.y) ** 2)

        min_distance_index = min(distances.keys(), key=(
            lambda k: distances[k]))  # min_distance_index jest to indeks owcy, do której wilkowi najbliżej

        return min_distance_index, distances[
            min_distance_index]  # zwracamy indeks najblizszej owcy oraz tą najbliżsszą odległość

    # metoda dodająca punkty do listy
    def point_add(self, point):
        self.points_list.append(point)

    # metoda pobierająca punkty z listy
    def get_points(self):
        return self.points_list
