
# -*- coding: utf-8 -*-
import asyncio
import time

from poke_env.player.player import Player
from poke_env.player.random_player import RandomPlayer

import time


weakness_map = {
    13: [6],
    6: [8, 15, 5],
    8: [16, 4, 12],
    14: [11, 15],
    11: [18, 10, 12],
    16: [6, 11, 17, 18, 10],
    9: [9, 2],
    17: [6, 11, 7],
    7: [11, 16, 18],
    18: [10, 4],
    10: [8, 14, 1, 7, 12],
    4: [11],
    15: [1, 9, 2],
    12: [6, 16, 17, 7],
    3: [12, 3, 5],
    2: [6, 1, 5],
    5: [14, 17]
}



class MaxDamagePlayer(Player):

    def choose_move(self, battle):

        #Adding this for more observable battles!!
        # time.sleep(10)

        # print("Pokemon Class:",battle.POKEMON_CLASS)
        # print("\nActive Pokemon:",battle.active_pokemon)

        # If the player can attack, it will
        if battle.available_moves:

            # #Print Moves
            # print("Available Moves:")
            # for move in battle.available_moves:
            #     print(move," | BP:", move.base_power)

            # Finds the best move among available ones
            best_move = max(battle.available_moves, key=lambda move: move.base_power)

            return self.create_order(best_move)

        # If no attack is available, a random switch will be made
        else:
            return self.choose_random_move(battle)



class TypeMatchupPlayer(Player):

    def choose_move(self, battle):

        #Adding this for more observable battles
        # time.sleep(10)

        # print("Pokemon Class:",battle.POKEMON_CLASS)
        print("\nPlayer's Active Pokemon:", battle.active_pokemon)
        print("Opponent's Active Pokemon", battle.opponent_active_pokemon)

        # If the player can attack, it will
        if battle.available_moves:

            best_move = max(battle.available_moves, key=lambda move: move.base_power)

            #Get weaknesses of opposing Pokemon
            opp_weaknesses = []
            opp_pokemon_types = list(battle.opponent_active_pokemon.types)
            for type in opp_pokemon_types:
                try:
                    opp_weaknesses.extend(weakness_map[type.value])
                except:
                    pass
            opp_pokemon_types = set(opp_pokemon_types)
            print("Opponent Pokemon's Weaknesses:",opp_weaknesses)

            #Get player's active Pokemon's types:
            player_active_types = list(battle.active_pokemon.types)
            player_active_typeValues = []
            for type in player_active_types:
                try:
                    player_active_typeValues.append(type.value)
                except:
                    pass
            print("Player's active Pokemon's Types:",player_active_typeValues)


            try:
                #Check if any of current Pokemon's moves are viable
                current_viable = False
                moves = battle.available_moves
                for move in moves:
                    if move.type.value in opp_weaknesses and move.category.value!=3:
                        current_viable = True
                        print("Current Pokemon is viable. Effective move found")
                        best_move = move
                        return self.create_order(best_move)
            except:
                pass

            #If current Pokemon is not viable, check if any other Pokemon is viable
            if not current_viable:

                print("Current Pokemon is not viable")

                #Iterate through list of possible Pokemon to switch to
                for possible_pokemon in battle.available_switches:

                    #Get types of one possible Pokemon
                    possible_pokemon_types = possible_pokemon.types
                    possible_pokemon_typeValues = []
                    for type in possible_pokemon_types:
                        try:
                            possible_pokemon_typeValues.append(type.value)
                        except:
                            pass

                    #Check if that pokemon is viable

                    potential_viable = False

                    #Check Pokemon type
                    for type in possible_pokemon_typeValues:
                        if type in opp_weaknesses:
                            print("Pokemon with viable type found. Making switch")
                            potential_viable = True
                            return self.create_order(possible_pokemon)

                #Check Pokemon move types for viability
                # try:
                #     for possible_pokemon in battle.available_switches:
                #         moves = list(possible_pokemon.moves.values())
                #         for move in moves:
                #             if move.type.value in opp_weaknesses:
                #                 print("Pokemon with viable move type found. Making switch")
                #                 potential_viable = True
                #                 return self.create_order(possible_pokemon)
                
                # except:
                #     pass

                    # #If that Pokemon is viable, make the switch
                    # if potential_viable:
                    #     best_move = possible_pokemon
                    #     return self.create_order(best_move)

            try:
                if not potential_viable:
                    print("No Pokemon viable, playing strongest move on current pokemon")
            except:
                pass

            return self.create_order(best_move)

        # Player's active Pokemon has fainted, try to switch to a Pokemon with a good matchup, else random switch
        else:

            print("\nPreparing switch")
            
            #Get weaknesses of opposing Pokemon
            opp_weaknesses = []
            opp_pokemon_types = list(battle.opponent_active_pokemon.types)
            for type in opp_pokemon_types:
                try:
                    opp_weaknesses.extend(weakness_map[type.value])
                except:
                    pass
            opp_pokemon_types = set(opp_pokemon_types)
            print("Opponent Pokemon's Weaknesses:",opp_weaknesses)

            for possible_pokemon in battle.available_switches:
                #Check best Pokemon type

                #Get possible Pokemon type
                possible_pokemon_types = list(possible_pokemon.types)
                possible_pokemon_typeValues = []
                for type in possible_pokemon_types:
                        try:
                            possible_pokemon_typeValues.append(type.value)
                        except:
                            pass

                #Check if the type is viable
                for type in possible_pokemon_typeValues:
                    if type in opp_weaknesses:
                        print("Viable switch found")
                        return self.create_order(possible_pokemon)
                
            #Check Pokemon with best possible move
            #TODO

            print("No viable switch found, making random switch")
            return self.choose_random_move(battle)




async def main():

    start = time.time()

    # We create two players.
    random_player = RandomPlayer(battle_format="gen4randombattle")
    max_damage_player = MaxDamagePlayer(battle_format="gen4randombattle")
    typeMatchupPlayer = TypeMatchupPlayer(battle_format="gen4randombattle")


    # Now, let's evaluate our player
    await typeMatchupPlayer.battle_against(max_damage_player, n_battles=100)
    print(
        "\nAggressive Player won %d / 100 battles [this took %f seconds]"
        % (typeMatchupPlayer.n_won_battles, time.time() - start)
    )


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())