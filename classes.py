class Station:
    def __init__(self, id, pos, trains, size=1) -> None:
        self.id = id
        self.pos = pos
        self.trains = trains
        self.size = size

    def __str__(self) -> str:
        return f'Station {self.id} at {self.pos} with {len(self.trains)} trains'

class Train:
    def __init__(self, pos, route) -> None:
        self.pos = pos
        self.route = route