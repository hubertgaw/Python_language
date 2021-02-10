import random


class Sheep:
    sheep_color = "light blue"
    sheep_move_dist = 10.0

    # atrybuty instancyjne, czyli związane z okreslonym obiektem:
    def __init__(self, identify_number, x, y, direction='N'):
        self.identify_number = identify_number  # identify_number to numer owcy w kolejnosci(od 0)
        self.x = x  # losujemy x i y
        self.y = y
        self.direction = direction  # ustawiamy wstępny domyślny kierunek na N (mozna go zmienic
        # przekazujac inny w konstruktorze)
        self.status = 'alive'  # ustawiamy wstepny status na alive (jego w konnstruktorze nie zmienimy)

    # metoda odpowiadająca za ruch owcy:
    def move(self):
        directions = ["N", "S", "E", "W"]  # tablica odpowiadająca za kierunki

        if self.status == 'alive':
            self.direction = random.choice(directions)  # tutaj odbywa się losowanie kierunku
            # po wylosowaniu kierunku "poruszamy" owce
            if self.direction == 'N':
                self.y = self.y + self.sheep_move_dist
            elif self.direction == 'S':
                self.y = self.y - self.sheep_move_dist
            elif self.direction == 'E':
                self.x = self.x + self.sheep_move_dist
            elif self.direction == 'W':
                self.x = self.x - self.sheep_move_dist


def draw_sheep(canvas, x0, y0, color, power):
    # dane do rysowania punktu o okreslonej wielkosci, odpowiednio przeskalowany, w przypadku zoomowaniu (stąd
    # 1.2 do potęgi skali (od 1 do 10)
    oval_width = 12 * 1.25 ** power.get()
    oval_height = 12 * 1.25 ** power.get()

    x1 = x0 + oval_width
    y1 = y0 + oval_height
    point = canvas.create_oval(x0, y0, x1, y1, fill=color)

    return point
