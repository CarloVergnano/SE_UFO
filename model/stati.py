from dataclasses import dataclass

@dataclass()
class Stato:
    id : str
    name : str
    #capital
    #lat
    #lng
    #area
    #population
    #neighbors

    def __str__(self):
        return f"Stati({self.id}, {self.name})"


    def __hash__(self):
        return hash(self.id)