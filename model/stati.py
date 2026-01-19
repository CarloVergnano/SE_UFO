from dataclasses import dataclass

@dataclass()
class Stato:
    id: str
    name : str


    def __str__(self):
        return f"Stato(id={self.id})"

    def __repr__(self):
        return f"Stato(id={self.id})"

    def __hash__(self):
        return hash(self.id)