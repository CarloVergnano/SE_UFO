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



    def get_anni(self):
        self.anni = DAO.get_anni()
        return self.anni

    def get_connessione(self, anno):
        self.connessioni = DAO.get_connesioni()
        return self.connessioni

    def get_avvistamenti (self, anno, forma):
        self.avvistamenti = DAO.get_avvistamenti(anno, forma)
        return self.avvistamenti

    def get_stati(self):
        self.stati = DAO.get_stati()
        return self.stati

    def get_forme(self, anno):
        self.forme = DAO.get_forme(anno)
        return self.forme

    def crea_grafo(self, anno, forma):
        self.G.clear()

        self.stati = DAO.get_stati()
        for s in self.stati:
            self.G.add_node(s.id)


        self.avvistamenti = DAO.get_avvistamenti(anno, forma)
        print(self.avvistamenti)

        self.connessioni = DAO.get_connesioni()

        for c in self.connessioni:
            s1 = c.state1
            s2 = c.state2

            peso = self.avvistamenti.get(s2, 0)


            self.G.add_edge(s1, s2, weight=peso)

        return self.G


