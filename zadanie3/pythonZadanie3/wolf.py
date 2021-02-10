class Wolf:
    # atrybuty klasowe (z góry mamy powiedziane, że będzie jeden wilk zatem będa tylko atrybuty klasowe)
    x = 145.0
    y = 145.0
    wolf_color = "tomato2"
    wolf_move_dist = 20.0

    # funkcja odpowiedzialna za ruch wilka
    def wolf_move(self, index_of_sheep, nearest_distance, sheep_list, points_list, wolf, meadow):
        # Jeśli owca w zasięgu to wilk ją zjada (przesuwa się na jej miejsce, a status owcy zmienia się na 'dead':
        if nearest_distance < self.wolf_move_dist:
            wolf.x = sheep_list[index_of_sheep].x
            wolf.y = sheep_list[index_of_sheep].y
            sheep_list[index_of_sheep].status = 'dead'
        else:
            wolf.x = wolf.x + (
                    self.wolf_move_dist * (sheep_list[index_of_sheep].x - wolf.x) / nearest_distance)  # nowe położenie
            # wilka obliczamy ze wzoru: x + dystans_ataku_wilka * (xOwcy - xWilka) / dystans_miedzy_wilkiem_i_owcą
            wolf.y = wolf.y + (
                    self.wolf_move_dist * (sheep_list[index_of_sheep].y - wolf.y) / nearest_distance)


def draw_wolf(canvas, x0, y0, color, power):
    # dane do narysowania punktu o okreslonych wymiarach, zalozylam, ze wilk jest troche wiekszy od owcy,
    # odpowiednio przeskalowany, w przypadku zoomowania (stąd 1.2 do potęgi skali (od 1 do 10))
    oval_width = 15 * 1.25 ** power.get()
    oval_height = 15 * 1.25 ** power.get()

    x1 = x0 + oval_width
    y1 = y0 + oval_height
    drawn_wolf = canvas.create_oval(x0, y0, x1, y1, fill=color)

    return drawn_wolf
