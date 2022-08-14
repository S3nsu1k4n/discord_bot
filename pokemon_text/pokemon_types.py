
class Typ:
    Normal = 1
    Feuer = 2
    Wasser = 3
    Elektro = 4
    Pflanze = 5
    Flug = 6
    Kaefer = 7
    Gift = 8
    Gestein = 9
    Boden = 10
    Kampf = 11
    Eis = 12
    Psycho = 13
    Geist = 14
    Drache = 15


TYPE_EFFECTIVENESS = {
    (Typ.Normal, Typ.Gestein): 0.5,
    (Typ.Elektro, Typ.Wasser): 2,
    (Typ.Elektro, Typ.Flug): 2,
    (Typ.Elektro, Typ.Pflanze): 0.5,
    (Typ.Elektro, Typ.Elektro): 0.5,
}


POKEMON_TYP = {
    1: [Typ.Pflanze, Typ.Gift],
    2: [Typ.Pflanze, Typ.Gift],
    3: [Typ.Pflanze, Typ.Gift],
    4: [Typ.Feuer, None],
    5: [Typ.Feuer, None],
    6: [Typ.Feuer, Typ.Flug],
    7: [Typ.Wasser, None],
    8: [Typ.Wasser, None],
    9: [Typ.Wasser, None],
    25: [Typ.Elektro, None],
}


def get_attack_effectiveness(attack_type: int, enemy_type: int):
    if (attack_type, enemy_type) in TYPE_EFFECTIVENESS:
        return TYPE_EFFECTIVENESS[(attack_type, enemy_type)]
    return 1
