import networkx as nx
from database.dao import DAO

class Model:
    def __init__(self):
        self.G = nx.Graph()
        self.anni = []
        self.connessioni = []
        self.avvistamenti = {}
        self.stati = []
        self.forme = []
        for o in self.stati:
            self.avvistamenti[o.id] = o


    def get_anni(self):
        self.anni = DAO.get_anni()
        return self.anni

    def get_connessione(self, anno):
        self.connessioni = DAO.get_connesioni()
        return self.connessioni

    def get_avvistamenti (self, anno, forma):
        self.avvistamenti = DAO.get_avvistamenti(anno, forma)

    def get_stati(self):
        self.stati = DAO.get_stati()

    def get_forme(self, anno):
        self.forme = DAO.get_forme(anno)
        return self.forme

    def crea_grafo (self, anno, forma):
        self.G.clear()
        self.avvistamenti = DAO.get_avvistamenti(anno, forma)
        self.connessioni = DAO.get_connesioni()
        peso1 = 0
        peso2 = 0
        for c in self.connessioni:
            for c.state1 in self.avvistamenti.keys():
                peso1 = int(self.avvistamenti[c.state1])
            for c.state2 in self.avvistamenti.keys():
                peso2 = int (self.avvistamenti[c.state2])
            peso = peso1 + peso2
            self.G.add_edge(c.state1, c.state2, weight = peso)

        return self.G

