"""Main file wich connects to server and play"""

import argparse
from typing import Dict, Any
from gndclient import start, Action, Score, Player, State, Time, DODO_STR, GOPHER_STR
import dodo
import gopher_propre
Environment = Dict[str, Any]


def initialize(
    game: str, state: State, player: Player, hex_size: int, total_time: Time
) -> Environment:
    """initialise l'environnement"""
    print("Init")
    print(
        f"{game} you play {player} on a grid of size {hex_size}. Time remaining: {total_time}"
    )
    if game == "gopher":
        env = "gopher"
        return env
    
    print('Dodo')
    env = "dodo"
    return env

def strategy_brain(
    env: Environment, state: State, player: Player, time_left: Time
) -> tuple[Environment, Action]:
    """fonction de stratégie"""
    print(f"Temps restant : {time_left} secondes")
    if env == "gopher":
        values: tuple[Environment, Action] = gopher_propre.strategy_nega_max_alpha_beta(
            env, state, player, time_left
        )
        return values

    values: tuple[Environment, Action] = dodo.strategy_nega_max_alpha_beta(
        env, state, player, time_left
    )
    return values

def final_result(state: State, score: Score, player: Player):
    """affichage du gagnant"""
    print(f"Ending: {player} wins with a score of {score}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="ClientTesting", description="Test the IA02 python client"
    )

    parser.add_argument("group_id")
    parser.add_argument("members")
    parser.add_argument("password")
    parser.add_argument("-s", "--server-url", default="http://lchappuis.fr:8081/")
    parser.add_argument("-d", "--disable-dodo", action="store_true")
    parser.add_argument("-g", "--disable-gopher", action="store_true")
    args = parser.parse_args()

    available_games = [DODO_STR, GOPHER_STR]
    if args.disable_dodo:
        available_games.remove(DODO_STR)
    if args.disable_gopher:
        available_games.remove(GOPHER_STR)

    start(
        args.server_url,
        args.group_id,
        args.members,
        args.password,
        available_games,
        initialize,
        strategy_brain,
        final_result,
        gui=True,
    )