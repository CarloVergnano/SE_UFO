from dataclasses import dataclass

@dataclass()
class Connessione:
    state1: str
    state2 : str

    def __str__(self):
        return f"Vicini({self.state1}, {self.state2})"


    def __hash__(self):
        return hash(self.state1)