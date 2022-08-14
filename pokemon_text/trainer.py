from .pokemon import Pokemon


class CurrentPokemon:
    def __init__(self):
        self.pokemon1: Pokemon | None = None
        self.pokemon2: Pokemon | None = None
        self.pokemon3: Pokemon | None = None
        self.pokemon4: Pokemon | None = None
        self.pokemon5: Pokemon | None = None
        self.pokemon6: Pokemon | None = None


class Trainer:
    def __init__(self, name):
        self.name = name
        self.pokemon = CurrentPokemon()

    def add_pokemon(self, slot: int, pokemon: Pokemon):
        self.pokemon.pokemon1 = pokemon
