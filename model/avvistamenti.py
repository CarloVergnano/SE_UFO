from dataclasses import dataclass

@dataclass()
class Avvistamento:
    state: str
    num_avvistamenti : int

    def __str__(self):
        return f"Avvistamenti({self.state}, {self.num_avvistamenti})"


    def __hash__(self):
        return hash(self.state)