
class Text:
    def __init__(self, speaker, text):
        self.speaker = speaker
        self.text = text


class TextResponse:
    def __init__(self, info: Text | None = None, enemy: Text | None = None, player: Text | None = None,
                 attacks: Text | None = None, battle_info: Text | None = None):
        self.info = info
        self.enemy = enemy
        self.player = player
        self.attacks = attacks
        self.battle_info = battle_info


def choose_pokemon(player_name: str) -> TextResponse:
    text = Text('Prof.Eich', f'Hallo. Dein Name ist also {player_name}!\nWähle ein Pokemon aus.')
    return TextResponse(info=text)


def choose_pokemon2(command: str) -> TextResponse:
    chosen_pokemon = {
        '1': 'Du hast dich also für Bisasam dem Pflanzenpokemon entschieden.',
        '2': 'Du hast dich also für Glumanda dem Feuerpokemon entschieden.',
        '3': 'Du hast dich also für Schiggy dem Wasserpokemon entschieden.'
    }
    if command in ['1', '2', '3']:
        text = Text('Prof.Eich', chosen_pokemon[command] + '\nBereit für einen Kampf mit meinem Enkel Gary?\n[Ja, vielleicht, Nein]')
        return TextResponse(info=text)
    else:
        text = Text("Giovanni's Snobilikat", 'Miau! Nur 1, 2 oder 3!!')
        return TextResponse(info=text)


def pokemon_fight(command:str) -> TextResponse:
    text = Text("Jemand", 'Haha')
    return TextResponse(info=text)