import flet as ft

class Controller:
    def __init__(self, view, model):
        self._view = view
        self._model = model
        self.anno_selezionato = None

    def on_anno_change(self, e):
        if e.control.value is None:
            return
        self.anno_selezionato = int(e.control.value)
        self.popola_dropdown_forme()

    def populate_dd_anni(self):
        """Popola il menu a tendina delle regioni."""
        self._view.dd_year.options.clear()

        anni = self._model.get_anni()

        if anni:
            for anno in anni:
                self._view.dd_year.options.append(ft.dropdown.Option(key=anno, text=anno))
        else:
            self._view.show_alert("Errore nel caricamento anni.")

        self._view.update()


    def handle_graph(self, e):
        self.anno_selezionato = int(self._view.dd_year.value)
        self.forma_selezionata =  self._view.dd_shape.value
        self.grafo = self._model.crea_grafo(int(self.anno_selezionato), self.forma_selezionata)
        num_nodi = self.grafo.number_of_nodes()
        num_rami = self.grafo.number_of_edges()

        self._view.lista_visualizzazione_1.controls.clear()
        self._view.lista_visualizzazione_1.controls.append(
            ft.Text(f"Numero di vertici: {num_nodi}. Numero di archi: {num_rami}")
        )

        for nodo, somma_pesi in self.grafo.degree(weight="weight"):
            self._view.lista_visualizzazione_1.controls.append(
                ft.Text(f"Nodo {nodo}, somma pesi su archi = {somma_pesi}")
            )

        self._view.update()


    def on_forma_change(self, e):
        self.forma_selezionata = e.control.value

    def popola_dropdown_forme(self):

        self._view.dd_shape.options.clear()



        if self._view.dd_year.value is None:
            self._view.show_alert("Seleziona prima un anno")
            return

        self.anno_selezionato = int(self._view.dd_year.value)


        self.forme = self._model.get_forme(self.anno_selezionato)

        if not self.forme:
            self._view.show_alert("Nessuna forma trovata per l'anno selezionato")
            return
        if self.forme:
            for forma in self.forme:
                self._view.dd_shape.options.append(
                    ft.dropdown.Option(
                        key=forma,
                        text=forma
                )
            )
        else:
            self._view.show_alert("Errore nel caricamento forme.")


        self._view.update()



    def handle_path(self, e):
        """ Handler per gestire il problema ricorsivo di ricerca del cammino """
        # TODO
