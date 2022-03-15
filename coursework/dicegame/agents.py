from dice_game import DiceGame
import numpy as np
from abc import ABC, abstractmethod



class DiceGameAgent(ABC):
    def __init__(self, game):
        self.game = game
    
    @abstractmethod
    def play(self, state):
        pass



class AlwaysHoldAgent(DiceGameAgent):
    def play(self, state):
        return (0, 1, 2)

class PerfectionistAgent(DiceGameAgent):
    def play(self, state):
        if state == (1, 1, 1) or state == (1, 1, 6):
            return (0, 1, 2)
        else:
            return ()

class HybridAgent(DiceGameAgent):
    def __init__(self, game, num = 11):
        self.game = game
        self.num = num

    def play(self, state):
        current_score = self.game.get_dice_score()
        
        if current_score > self.num:
            return (0, 1, 2)
        else:
            return ()



def play_game_with_agent(agent, game, verbose=False):
    state = game.reset()
    
    if(verbose): print(f"Testing agent: \n\t{type(agent).__name__}")
    if(verbose): print(f"Starting dice: \n\t{state}\n")
    
    game_over = False
    actions = 0
    while not game_over:
        action = agent.play(state)
        actions += 1
        
        if(verbose): print(f"Action {actions}: \t{action}")
        _, state, game_over = game.roll(action)
        if(verbose and not game_over): print(f"Dice: \t\t{state}")

    if(verbose): print(f"\nFinal dice: {state}, score: {game.score}")
        
    return game.score

if __name__ == "__main__":
    np.random.seed()
    game = DiceGame()
    iterations = 100000
    agent = HybridAgent(game)
    total = 0
    for i in range(iterations):
        total += play_game_with_agent(agent, game)
    print(f"average score = {total/iterations}")