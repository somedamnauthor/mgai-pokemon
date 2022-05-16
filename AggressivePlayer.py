
# -*- coding: utf-8 -*-
import asyncio
import time

from poke_env.player.player import Player
from poke_env.player.random_player import RandomPlayer
from poke_env.server_configuration import ShowdownServerConfiguration

import time



class MaxDamagePlayer(Player):

    def choose_move(self, battle):

        #Adding this for more observable battles!!
        time.sleep(10)

        # print("Pokemon Class:",battle.POKEMON_CLASS)
        print("\nActive Pokemon:",battle.active_pokemon)

        # If the player can attack, it will
        if battle.available_moves:

            #Print Moves
            print("Available Moves:")
            for move in battle.available_moves:
                print(move," | BP:", move.base_power)

            # Finds the best move among available ones
            best_move = max(battle.available_moves, key=lambda move: move.base_power)

            return self.create_order(best_move)

        # If no attack is available, a random switch will be made
        else:
            return self.choose_random_move(battle)


class AggressivePlayer(Player):

    def choose_move(self, battle):

        #Adding this for more observable battles!!
        time.sleep(10)

        # print("Pokemon Class:",battle.POKEMON_CLASS)
        print("\nActive Pokemon:",battle.active_pokemon)

        # If the player can attack, it will
        if battle.available_moves:

            #Print Moves
            print("Available Moves:")
            for move in battle.available_moves:
                print(move," | BP:", move.base_power, " | Cat:",move.category)

            # Finds the best move among available ones
            # best_move = max(battle.available_moves, key=lambda move: move.base_power)

            #Play a super-effective move if possible
            

            return self.create_order(best_move)

        # If no attack is available, a random switch will be made
        else:
            return self.choose_random_move(battle)




async def main():
    start = time.time()

    # We create two players.
    random_player = RandomPlayer(battle_format="gen4randombattle")
    max_damage_player = MaxDamagePlayer(battle_format="gen4randombattle")
    # max_damage_player2 = MaxDamagePlayer(battle_format="gen8randombattle")


    # Now, let's evaluate our player
    await max_damage_player.battle_against(random_player, n_battles=1)

    print(
        "\n\nMax damage player won %d / 1 battles [this took %f seconds]"
        % (max_damage_player.n_won_battles, time.time() - start)
    )


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())