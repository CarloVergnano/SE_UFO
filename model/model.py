from database.dao import DAO
import networkx as nx
from operator import itemgetter

class Model:
    def __init__(self):
        self.G = nx.Graph()
        self.anni = []
        self.forme = []
        self.stati = []
        self.stati_confinanti = []
        self.avvistamenti = []

    def get_anni(self):
        self.anni = DAO.get_anni()
        return self.anni

    def get_forme(self, anno_selezionato):
        self.forme = DAO.get_forme(anno_selezionato)
        return self.forme

    def crea_grafo(self, anno_selezionato, forma_selezionata):
        self.G.clear()
        self.stati = DAO.get_all_stati()
        self.stati_confinanti = DAO.get_all_neighbors()
        for stato in self.stati_confinanti:
            if stato.state1 != stato.state2:
                peso1 = DAO.get_avvistamenti(anno_selezionato, forma_selezionata, stato.state1)
                peso2 = DAO.get_avvistamenti(anno_selezionato, forma_selezionata, stato.state2)
                try:
                    peso = int(peso1 + peso2)
                except ValueError:
                    print("Errore formato peso tra archi del grafo")
                    return
                self.G.add_edge(stato.state1, stato.state2, weight = peso)
                print(stato.state1, stato.state2, peso)
        nodi = list(self.G.nodes())
        for stato_ in self.stati:
            if stato_.id not in nodi:
                self.G.add_node(stato_.id)
        return self.G.number_of_nodes(), self.G.number_of_edges()

    def get_risultati(self):
        risultati = []
        for nodo in list(self.G.nodes()):
            vicini = self.G.neighbors(nodo)
            peso = 0
            for vicino in vicini:
                peso_vicino = self.G[nodo][vicino]['weight']
                peso += peso_vicino
            risultati.append((nodo, peso))
        risultati = sorted(risultati, key=itemgetter(0))
        return risultati


    def calcola_percorso_ottimo(self):
        self.best_solution = []
        self.best_value = 0 #float("inf") se percorso min - oppure float("-inf") se percorso max

        for nodo in self.G.nodes():
            self._ricorsione(
                parziale=[nodo],
                visitati={nodo},
                valore_corrente=0,
                ultimo_peso=-1
            )
        self.stampa_percorso()
        return self.best_solution, self.best_value

    def _ricorsione(self, parziale, visitati, valore_corrente, ultimo_peso):

        # aggiorna sempre il best (> percorso max, < percorso min) oppure (len(parziale) == L)  oppure  (parziale[-1] == nodo_finale)
        if valore_corrente > self.best_value:
            self.best_value = valore_corrente
            self.best_solution = parziale[:]

        nodo_corrente = parziale[-1]

        for vicino in self.G.neighbors(nodo_corrente):

            if vicino in visitati:
                continue

            peso = self.G[nodo_corrente][vicino]["weight"]

            # vincolo: pesi crescenti
            if peso <= ultimo_peso:
                continue

            parziale.append(vicino)
            visitati.add(vicino)

            self._ricorsione(
                parziale,
                visitati,
                valore_corrente + peso,
                peso
            )

            visitati.remove(vicino)
            parziale.pop()

    def stampa_percorso(self):
        for i in range(len(self.best_solution) - 1):
            u = self.best_solution[i]
            v = self.best_solution[i + 1]

            peso = self.G[u][v]["weight"]
            print(f"{u} -> {v} | peso={peso}")

