import os
from tkinter import *
from tkinter import colorchooser
from tkinter import filedialog
from tkinter import ttk
from tkinter import messagebox
from time import sleep

import sheepsList
from filesOperations import prepare_list_to_export_to_json, export_to_json, import_from_json
from sheep import Sheep, draw_sheep
from wolf import draw_wolf, Wolf


class GUI:

    def __init__(self):
        # tworzenie okna:
        self.window = Tk()
        self.window.title("Python 3 Simulation")
        self.window.geometry('500x420')
        self.window.resizable(False, False)
        self.window.configure(background="grey")

        # atrybuty instancyjne:

        # zmienna z kolorem tła:
        self.bg_color = "chartreuse2"

        self.init_pos_limit = 200.0

        # tworzymy obszar, ktory bedzie łaką (meadow)
        self.meadow = Canvas(self.window, bg=self.bg_color, height=1.5 * self.init_pos_limit,
                             width=1.5 * self.init_pos_limit)

        # suwak do przyblizania / oddalania
        self.scale_variable = DoubleVar()
        self.scale = Scale(self.window, variable=self.scale_variable, command=self.zooming, activebackground="green",
                           bg="white", from_=0, to=5, label="ZOOM")

        # wartosc domyslna dla suwaka
        self.default_value = 0
        # ustawiamy na początku na 0
        self.scale.set(self.default_value)

        # tworzymy wilka na start na srodku laki
        self.wolf = Wolf()
        self.drawn_wolf = draw_wolf(self.meadow, 145, 145, self.wolf.wolf_color, self.scale_variable)

        # owca, ktora nie jest pokazywana na lace
        self.sheep = Sheep(0, 100, 100)
        self.sheep_color = "light blue"

        # utworzenie obiektu lista owiec
        self.sheep_list_object = sheepsList.SheepList()
        self.sheep_list_gui = self.sheep_list_object.sheep_list
        self.points_list_gui = self.sheep_list_object.points_list

        # etykieta z liczba zywych owiec i zmienna do zmiany wartosci
        self.variable_sheep_number = StringVar()
        self.variable_sheep_number.set("0")
        self.label_how_many_sheep = Label(self.window, textvariable=self.variable_sheep_number, bg="grey",
                                          font="calibri 20 bold")

        # menu
        self.menu_bar = Menu(self.window)

        # przycisk step
        self.step = Button(self.window, text="STEP", height=2, width=15, justify=CENTER, bg="white",
                           font="calibri 10 bold", command=self.step)

        # przycisk Reset
        self.reset = Button(self.window, text="RESET", height=2, width=15, justify=CENTER, bg="white",
                            font="calibri 10 bold", command=self.reset)

        # przycisk start/stop
        self.var = StringVar()
        self.var.set("START")
        self.start_stop = Button(self.window, textvariable=self.var, height=2, width=15, justify=CENTER, bg="white",
                                 font="calibri 10 bold", command=self.start_stop_click)

        # zmienna dla czasu pojedynczego ruchu
        self.interval = 1.0

        # flaga do tego czy ruch ma trwać
        self.perform_flag = False

    # funkcja inicjalizujaca, ktora stworzy nam interfejs graficzny
    def initialization(self):
        # czyszczenie zawartosci listy owiec, zeby po ponownym otwarciu aplikacji byla pusta
        self.sheep_list_gui.clear()
        self.points_list_gui.clear()

        self.add_canvas()
        self.add_buttons()
        self.add_menu()

        self.window.mainloop()

    def save_to_file(self):
        # dodatkowa zmienna, zeby domyslnie otwieral sie biezacy katalog
        path = os.getcwd()
        f = filedialog.asksaveasfile(initialdir=path, title="Save file", filetypes=[('Json File', ['.json'])])
        # list_for_export_to_json - slownik, który wyeksportujemy do pliku json
        list_for_export_to_json = prepare_list_to_export_to_json(self.wolf, self.sheep_list_gui,
                                                                 self.sheep_color, self.bg_color)
        if f is None:  # jesli sie zamknie okno, to wtedy asksaveasfile zwraca None
            return
        export_to_json(list_for_export_to_json, f)

    def set_colors_from_file(self):
        self.meadow.configure(bg=self.bg_color)
        # pobieramy liste punktow, a nastepnie zmieniamy ich kolor
        points_list = self.sheep_list_object.get_points()
        for point in points_list:
            self.meadow.itemconfig(point, fill=self.sheep_color)
        self.variable_sheep_number.set(str(self.sheep_list_object.count_alive_sheeps()))

    def open_file(self):
        # dodatkowa zmienna, zeby domyslnie otwieral sie biezacy katalog
        path = os.getcwd()
        # funkcja do wybierania pliku do otwarcia
        # askopenfile zwraca wlasciwy plik, a askopenfilename zwrociloby sciezke do tego pliku
        f = filedialog.askopenfilename(initialdir=path, title="Select file", filetypes=[('Json File', ['.json'])])
        if f is None:  # jesli sie zamknie okno, to wtedy askopen file zwraca None
            return
        self.sheep_color, self.wolf, self.drawn_wolf, self.bg_color = import_from_json(f, self.meadow,
                                                                                       self.scale_variable,
                                                                                       self.sheep_list_gui,
                                                                                       self.points_list_gui)
        self.scale.set(0)
        self.set_colors_from_file()

    def settings(self):
        # tutaj nowe okno do ustawien
        settings = Tk()
        settings.title("Settings")
        settings.geometry('300x210')
        settings.resizable(False, False)

        def paint_wolf_settings():
            # kolor to lista z dwoma elementami, pierwszy to informacje numeryczne w skali RGB, a drugi to kolor w
            # formacie szesnastkowym
            my_color = colorchooser.askcolor()[1]
            setattr(self.wolf, 'wolf_color', my_color)
            wolf_btn.configure(bg=self.wolf.wolf_color)
            self.meadow.itemconfig(self.drawn_wolf, fill=self.wolf.wolf_color)

        def paint_sheep_settings():
            # kolor to lista z dwoma elementami, pierwszy to informacje numeryczne w skali RGB, a drugi to kolor w
            # formacie szesnastkowym
            my_color = colorchooser.askcolor()[1]
            self.sheep_color = my_color
            sheep_btn.configure(bg=self.sheep_color)
            # pobieramy liste punktow, a nastepnie zmieniamy ich kolor
            points_list = self.sheep_list_object.get_points()
            for point in points_list:
                self.meadow.itemconfig(point, fill=self.sheep_color)
            for sheep in self.sheep_list_gui:
                sheep.sheep_color = self.sheep_color

        def paint_background_settings():
            # kolor to lista z dwoma elementami, pierwszy to informacje numeryczne w skali RGB, a drugi to kolor w
            # formacie szesnastkowym
            my_color = colorchooser.askcolor()[1]
            self.bg_color = my_color
            background_button.configure(bg=self.bg_color)  # tu moze trzeba self.bgColor
            self.meadow.configure(bg=self.bg_color)

        # ustawiamy pauze
        def set_interval(event):
            self.interval = float(chosen_number.get())

        wolf_label = Label(settings, text=" Wolf color ")
        wolf_label.place(x=20, y=20)

        wolf_btn = Button(settings, text="Choose a color", command=paint_wolf_settings, bg=self.wolf.wolf_color)
        wolf_btn.place(x=190, y=20)

        sheep_label = Label(settings, text=" Sheep color ")
        sheep_label.place(x=20, y=50)

        sheep_btn = Button(settings, text="Choose a color", command=paint_sheep_settings, bg=self.sheep_color)
        sheep_btn.place(x=190, y=50)

        background_label = Label(settings, text=" Background color ")
        background_label.place(x=20, y=80)

        background_button = Button(settings, text="Choose a color", command=paint_background_settings, bg=self.bg_color)
        background_button.place(x=190, y=80)

        time_label = Label(settings, text=" Single step time ")
        time_label.place(x=20, y=110)

        chosen_number = ttk.Combobox(settings, width=11)  # textvariable=self.number_var)
        chosen_number['justify'] = CENTER
        chosen_number['values'] = (0.5, 1, 1.5, 2)
        chosen_number.place(x=190, y=110)
        # ustawiamy index, na którym domyślnie ma byc ustawiony combobox po włączeniu ustawień
        pom = self.interval
        print(pom)
        if self.interval == 0.5:
            index = 0
        elif self.interval == 1.0:
            index = 1
        elif self.interval == 1.5:
            index = 2
        else:
            index = 3
        chosen_number.current(index)
        chosen_number.bind("<<ComboboxSelected>>", set_interval)

        # zmienna potrzebna pozniej do kontroli symulacji
        self.number_var = chosen_number.get()
        settings.mainloop()

    def add_menu(self):
        # Tworzenie paska menu
        self.window.config(menu=self.menu_bar)

        # Tworzenie menu a dodawanie do niego elementow
        # Pierwszy element z rozwijana lista
        menu_file = Menu(self.menu_bar, tearoff=0)
        menu_file.add_command(label="Open", command=self.open_file)
        menu_file.add_separator()
        menu_file.add_command(label="Save", command=self.save_to_file)
        menu_file.add_separator()
        menu_file.add_command(label="Quit", command=self.window.destroy)
        self.menu_bar.add_cascade(label="File", menu=menu_file)

        # Drugi element z rozwijana lista
        self.menu_bar.add_command(label="Settings", command=self.settings)

    def paint_sheep(self, event):
        x1, y1 = event.x, event.y
        point = draw_sheep(self.meadow, x1, y1, self.sheep_color, self.scale_variable)
        # zmienna do numerowania owiec
        number = self.sheep_list_object.count()
        # dodanie owcy do listy owiec
        self.sheep_list_object.sheep_add(Sheep(number, x1, y1))
        self.sheep_list_gui[-1].sheep_color = self.sheep_color
        # dodanie narysowanego punktu oznaczajacego owce do listy narysowanych punktow w obiekcie klasy SheepsList
        self.sheep_list_object.point_add(point)
        # aktualizacja etykiety z lista zywych owiec na podstawie liczby elementow listy owiec
        self.variable_sheep_number.set(str(self.sheep_list_object.count_alive_sheeps()))

    def move_wolf(self, event):
        x1, y1 = event.x, event.y
        # usuwany jest istniejacy wilk
        self.meadow.delete(self.drawn_wolf)
        # i rysowany nowy na podstawie wspolrzednych pobranych z klikniecia uzytkownika
        self.drawn_wolf = draw_wolf(self.meadow, x1, y1, self.wolf.wolf_color, self.scale_variable)
        # zmiana wartosci wspolrzednych wilka w logice aplikacji
        self.wolf.x = x1
        self.wolf.y = y1

    def add_canvas(self):
        self.meadow.place(x=20, y=20)
        self.meadow.bind("<ButtonPress-1>", self.paint_sheep)
        self.meadow.bind("<ButtonPress-3>", self.move_wolf)

    # funkcja wykonujaca pojedyncza ture ruchow (czyli de facto step)
    def perform_move(self):

        # ruch owiec
        self.sheep_list_object.sheep_move()

        # obliczenie indeksu najblizszej owcy i wartosci tej odleglosci
        index_of_sheep_with_nearest_distance, nearest_distance \
            = self.sheep_list_object.find_nearest_distance(self.wolf)

        # ruch wilkiem (zmiana wspolrzednych na liscie)
        self.wolf.wolf_move(index_of_sheep_with_nearest_distance, nearest_distance, self.sheep_list_gui,
                            self.points_list_gui, self.wolf, self.meadow)
        # ruch wilkiem na lace (narysowanie kropki w innym miejscu)
        self.meadow.delete(self.drawn_wolf)

        # rysowanie owiec po ruchu
        self.sheep_list_object.sheep_draw_all(self.meadow, self.scale_variable)

        # rysowanie wilka po ruchu owiec
        self.drawn_wolf = draw_wolf(self.meadow, self.wolf.x, self.wolf.y, self.wolf.wolf_color,
                                    self.scale_variable)

        # aktualizacja do etykiety wyswietlajacej zywe owce
        self.variable_sheep_number.set(str(self.sheep_list_object.count_alive_sheeps()))

    def step(self):
        if self.sheep_list_object.count_alive_sheeps() != 0:
            self.perform_move()

        else:
            messagebox.showerror("Error", "There is no simulation step, because there are no sheeps in the meadow. "
                                          "\nAdd sheep and try again!")

    def reset(self):
        # usuniecie wszytskich owiec z listy
        self.sheep_list_gui.clear()
        # usuniecie wszytkich punktow z listy
        self.points_list_gui.clear()
        # czyszczenie laki ze wszystkich elementow
        self.meadow.delete("all")
        # ustawienie wilka na srodku
        self.drawn_wolf = draw_wolf(self.meadow, 145, 145, self.wolf.wolf_color, self.scale_variable)
        # ustawienie ponownie wspolrzednych wilka na srodek laki
        self.wolf.x = 145
        self.wolf.y = 145
        # ustawienie liczby zywych owiec na zero
        self.variable_sheep_number.set("0")

    def do_nothing(self, event):
        pass

    def start_stop_click(self):
        # warunki, zeby nazwa przycisku sie zmieniala po nacisnieciu
        if self.start_stop.cget("text") == "START":
            self.var.set("STOP")

            # zablokowanie pozostalych przyciskow
            self.step["state"] = DISABLED
            self.reset["state"] = DISABLED

            # zablokowanie paska menu
            self.menu_bar.entryconfig("File", state="disabled")
            self.menu_bar.entryconfig("Settings", state="disabled")

            # zablokowanie mozliwosci dodawania owiec oraz przesuwania wilka
            self.meadow.bind("<ButtonPress-1>", self.do_nothing)
            self.meadow.bind("<ButtonPress-3>", self.do_nothing)

            self.perform_flag = True

            if self.sheep_list_object.count_alive_sheeps() == 0:
                messagebox.showerror("Add sheep", "There are no sheep on the meadow \n Add some")
            else:
                while self.sheep_list_object.count_alive_sheeps() != 0 and self.perform_flag:
                    self.perform_move()
                    self.window.update()
                    sleep(float(self.interval))
                    if self.sheep_list_object.count_alive_sheeps() == 0:
                        messagebox.showinfo("Game over", "Wolf ate all sheep ;( \n Game is over.")
                        self.stop_game()
                        break
        else:
            self.stop_game()

    def stop_game(self):
        self.var.set("START")

        # odblokowanie pozostaych przyciskow
        self.step["state"] = NORMAL
        self.reset["state"] = NORMAL

        # odblokowanie paska menu
        self.menu_bar.entryconfig("File", state="normal")
        self.menu_bar.entryconfig("Settings", state="normal")

        # ponowne umozliwienie dodawania owiec oraz przesuwania wilka
        self.meadow.bind("<ButtonPress-1>", self.paint_sheep)
        self.meadow.bind("<ButtonPress-3>", self.move_wolf)

        self.perform_flag = False

    def add_buttons(self):
        # etykiety potrzebne do wyswietlenia ilosci owiec
        how_many_label = Label(self.window, text="Number of live sheep: ", bg="grey", fg="white",
                               font="calibri 12 bold")
        how_many_label.place(x=335, y=20)

        self.label_how_many_sheep.place(x=400, y=40)

        # przycisk Step
        self.step.place(x=350, y=120)
        self.reset.place(x=350, y=180)

        # przycik Start/Stop
        self.start_stop.place(x=350, y=240)

        # suwak do przyblizania / oddalania
        self.scale.place(x=350, y=290)

    def zooming(self, event):
        # metoda do zoomowania (wzgledem srodka)
        # przyblizanie
        if float(event) > float(self.default_value):
            print(self.meadow.winfo_id())
            while float(event) > float(self.default_value):
                # self.meadow.scale("all", self.meadow.winfo_width() / 2, self.meadow.winfo_height() / 2,
                #                   1.25, 1.25)
                for point in self.points_list_gui:
                    self.meadow.delete(point)

                # pętla, w której ponownie rysujemy owce
                for sheep in self.sheep_list_gui:
                    if sheep.status == 'alive':
                        point = draw_sheep(self.meadow, sheep.x, sheep.y, sheep.sheep_color, self.scale_variable)
                        self.sheep_list_object.point_add(point)

                self.meadow.delete(self.drawn_wolf)
                self.drawn_wolf = draw_wolf(self.meadow, self.wolf.x, self.wolf.y, self.wolf.wolf_color,
                                            self.scale_variable)
                self.default_value = self.default_value + 1.0
        # oddalanie
        elif float(event) < float(self.default_value):
            while float(event) < float(self.default_value):
                # self.meadow.scale("all", self.meadow.winfo_width() / 2, self.meadow.winfo_height() / 2,
                #                   0.8, 0.8)
                for point in self.points_list_gui:
                    self.meadow.delete(point)

                    # pętla, w której ponownie rysujemy owce
                for sheep in self.sheep_list_gui:
                    if sheep.status == 'alive':
                        point = draw_sheep(self.meadow, sheep.x, sheep.y, sheep.sheep_color, self.scale_variable)
                        self.sheep_list_object.point_add(point)

                self.meadow.delete(self.drawn_wolf)
                self.drawn_wolf = draw_wolf(self.meadow, self.wolf.x, self.wolf.y, self.wolf.wolf_color,
                                            self.scale_variable)
                self.default_value = self.default_value - 1.0

        self.default_value = float(event)


if __name__ == "__main__":
    gui = GUI()
    gui.initialization()
