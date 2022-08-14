from .pokemon import Pokemon
from .attacks import attack_hits
from .scene import choose_pokemon, choose_pokemon2, Text, TextResponse, pokemon_fight
from .trainer import Trainer
import numpy as np


class game_states:
    init = 1
    fight = 2
    finish = 3


class Game:
    def __init__(self, player_name):
        self.state = game_states.init
        self.state_index = 1
        self.player_name = player_name
        self.trainer = Trainer(name=player_name)
        self.pokemon_starter = [Pokemon(dex_id=1), Pokemon(dex_id=4), Pokemon(dex_id=7)]

        self.enemy = Trainer('Gary')

    def get_starter(self) -> dict:
        response = {}
        for i in range(len(self.pokemon_starter)):
            response.update({
                self.pokemon_starter[i].name: {
                    'KP': self.pokemon_starter[i].stats.kp,
                    'Angr': self.pokemon_starter[i].stats.angriff,
                    'Vert': self.pokemon_starter[i].stats.verteidigung,
                    'Spez': self.pokemon_starter[i].stats.spezial,
                    'Init': self.pokemon_starter[i].stats.initiative,
                }
            })
        return response

    def choose_pokemon(self, command):
        if command in ['1', '2', '3']:
            self.state = game_states.fight
            self.trainer.add_pokemon(1, self.pokemon_starter[int(command)-1])
            index = 0 if command == '3' else 1 if command == '1' else 2
            self.enemy.add_pokemon(1, self.pokemon_starter[index])

    def use_command(self, command) -> TextResponse:
        if self.state == game_states.init:
            self.choose_pokemon(command)
            return choose_pokemon2(command)
        else:
            return self.pokemon_fight(command)

    def pokemon_fight(self, command) -> TextResponse:
        if self.state_index == 1:
            player = Text(speaker=self.trainer.name, text=self.trainer.pokemon.pokemon1.get_fight_display())
            enemy = Text(speaker=self.enemy.name, text=self.enemy.pokemon.pokemon1.get_fight_display(enemy=True))
            attacks = Text(speaker='Attacken', text=self.trainer.pokemon.pokemon1.get_4attack_options())
            self.state_index += 1
            return TextResponse(player=player, enemy=enemy, attacks=attacks)
        else:
            allowed_command = [str(i) for i in range(len(self.trainer.pokemon.pokemon1.attacken))]
            if command in allowed_command:
                return self.choose_attack(int(command))
            else:
                text = Text("Giovanni's Snobilikat", f'Miau! Nur {", ".join(allowed_command)}!!')
                return TextResponse(info=text)

    def choose_attack(self, command):
        battle_text = ''

        # check who is first
        if self.trainer_first_turn():
            turns = [self.trainer, self.enemy]
        else:
            turns = [self.enemy, self.trainer]

        for trainer in turns:
            if trainer.name == self.player_name:
                attack_index = command
                enemy = self.enemy
            else:
                attack_index = np.random.choice(range(len(trainer.pokemon.pokemon1.attacken)), p=[0.8, 0.2])
                enemy = self.trainer
            pokemon = trainer.pokemon.pokemon1
            enemy_pokemon = enemy.pokemon.pokemon1
            attack = pokemon.attacken[attack_index]

            battle_text += f'{pokemon.name} setzt {attack.name} ein!\n'
            if attack_hits(attack):
                damage, critical = pokemon.use_attack(attack, enemy=enemy_pokemon)
                if critical:
                    battle_text += 'Volltreffer!\n'
                battle_text += f'{damage} Schaden verursacht\n'
                enemy_pokemon.receive_damage(damage=damage)
                if enemy_pokemon.stats.kp_momentan <= 0:
                    self.state = game_states.finish
                    battle_text += f'{enemy_pokemon.name} wurde besiegt. {enemy.name} wurde ohnmächtig\n'
                    del games[self.player_name]
                    break
            else:
                battle_text += 'Die Attacke ging daneben\n'
            battle_text += '\n'

        battle = Text(speaker="Giovanni's Snobilikat", text=battle_text)
        player = Text(speaker=self.trainer.name, text=self.trainer.pokemon.pokemon1.get_fight_display())
        enemy = Text(speaker=self.enemy.name, text=self.enemy.pokemon.pokemon1.get_fight_display(enemy=True))
        attacks = Text(speaker='Attacken', text=self.trainer.pokemon.pokemon1.get_4attack_options())
        return TextResponse(battle_info=battle, player=player, enemy=enemy, attacks=attacks)

    def trainer_first_turn(self) -> bool:
        return self.trainer.pokemon.pokemon1.stats.initiative >= self.enemy.pokemon.pokemon1.stats.initiative


games = {}


def init(player_name: str) -> TextResponse:
    games[player_name] = Game(player_name=player_name)
    response = choose_pokemon(player_name)
    return response


def use_command(player_name: str, arg: str) -> TextResponse:
    return games[player_name].use_command(arg)


if __name__ == '__main__':
    init('Ash')
