import flet as ft
from database.DB_connect import DBConnect

class Controller:
    def __init__(self, view, model):
        self._view = view
        self._model = model
        self.anni = []
        self.anno_selezionato = None
        self.forme = []
        self.forma_selezionata = None

        self._connessione_db = DBConnect.get_connection()
        if self._connessione_db is None:
            self._view.show_alert("❌ Errore di connessione al database")

    def populate_dd(self):
        """ Metodo per popolare i dropdown """
        if self._connessione_db is None:
            self._view.show_alert("❌ Errore di connessione al database")
            return
        self.anni = self._model.get_anni()
        self._view.dd_year.options.clear()
        if self.anni:
            for anno in self.anni:
                self._view.dd_year.options.append(
                    ft.dropdown.Option(anno, f"{anno}"))
        else:
            self._view.show_alert("Errore nel caricamento degli anni.")
        self._view.update()

    def seleziona_anno(self, e):
        self.anno_selezionato = self._view.dd_year.value
        if self.anno_selezionato is None:
            self._view.show_alert("Selezionare un anno.")
            return

        if self.anno_selezionato is not None:
            self.forme = self._model.get_forme(self.anno_selezionato)
            self._view.dd_shape.disabled = False
            self._view.dd_shape.options.clear()
            if len(self.forme) != 0:
                for forma in self.forme:
                    self._view.dd_shape.options.append(
                        ft.dropdown.Option(forma, f"{forma}"))
            else:
                self._view.show_alert("Errore nel caricamento delle forme.")
            self._view.update()

    def handle_graph(self, e):
        """ Handler per gestire creazione del grafo """
        self.forma_selezionata = self._view.dd_shape.value
        if self.forma_selezionata is None:
            self._view.show_alert("Selezionare un forma.")
            return
        vertici, archi = self._model.crea_grafo(self.anno_selezionato, self.forma_selezionata)
        self._view.lista_visualizzazione_1.controls.clear()
        self._view.lista_visualizzazione_1.controls.append(ft.Text(f"Numero di vertici: {vertici} - Numero di archi: {archi}"))
        self._view.update()
        risultati = (self._model.get_risultati())
        for nodo, avvistamento in risultati:
            self._view.lista_visualizzazione_1.controls.append(
                ft.Text(f"{nodo} {avvistamento}"))
        self._view.update()

    def handle_path(self, e):
        """ Handler per gestire il problema ricorsivo di ricerca del cammino """
        best_solution, best_value = (self._model.calcola_percorso_ottimo())
        self._view.lista_visualizzazione_2.controls.clear()
        for i in range(len(best_solution) - 1):
            u = best_solution[i]
            v = best_solution[i + 1]

            peso = self._model.G[u][v]["weight"]
            self._view.lista_visualizzazione_2.controls.append(
                ft.Text(f"{u} -> {v} | peso={peso}"))
        self._view.update()