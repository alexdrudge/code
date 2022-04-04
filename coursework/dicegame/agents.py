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

# unimplemented
class ManualAgent(DiceGameAgent):
    
    def __init__(self, game):
        super().__init__(game)
    
    def play(self, state):
        # Your Code Here.
        pass

class OneStepValueIterationAgent(DiceGameAgent):
    def __init__(self, game):
        """
        If your code does any pre-processing on the game, you can do it here.
        
        You can always access the game with self.game
        """
        super().__init__(game)
        self.gamma = 1
        
        self.policy = {state: None for state in game.states}
        self.values = {state: 0 for state in game.states}

        delta = 1
        theta = 10 ** (-400)
        while delta > theta:
            delta, self.values = self.perform_single_value_iteration()
        
    
    def perform_single_value_iteration(self):
        new_values = {state: 0 for state in game.states}
        delta = 0
        for state in game.states:
            max_value = -100000000000000
            for action in game.actions:
                next_states, game_over, reward, probabilities = game.get_next_states(action, state)
                value = 0
                if not game_over:
                    for i in range(len(next_states)):
                        value += probabilities[i] * (reward + self.gamma * self.values[next_states[i]])
                else:
                    value = reward
                if value > max_value:
                    max_value = value
                    self.policy[state] = action
            new_values[state] = max_value
            delta = max(delta, abs(self.values[state] - new_values[state]))
        return delta, new_values
    
    def play(self, state):
        """
        given a state, return the chosen action for this state
        at minimum you must support the basic rules: three six-sided fair dice
        
        if you want to support more rules, use the values inside self.game, e.g.
            the input state will be one of self.game.states
            you must return one of self.game.actions
        
        read the code in dicegame.py to learn more
        """
        return self.policy[state]



class ValueIterationAgent(DiceGameAgent):
    def __init__(self, game):
        """
        If your code does any pre-processing on the game, you can do it here
        
        You can always access the game with self.game
        """
        super().__init__(game)
        
        # These are default values, you can play around with these to improve your agents performance.
        self.theta = 10 ** (-500)
        self.gamma = 1
        
        self.policy = {state: None for state in self.game.states}
        self.values = {state: 0 for state in self.game.states}

        self.value_iteration()
        
    
    def perform_single_value_iteration(self):
        # We advice you use the function from the previous assignment. You do not have to if you don't want to but it should save you alot of time.
        
        new_values = {state: 0 for state in self.game.states}
        delta = 0
        for state in self.game.states:
            max_value = -100000000000000
            for action in self.game.actions:
                next_states, game_over, reward, probabilities = self.game.get_next_states(action, state)
                value = 0
                if not game_over:
                    for i in range(len(next_states)):
                        value += probabilities[i] * (reward + self.gamma * self.values[next_states[i]])
                else:
                    value = reward
                if value > max_value:
                    max_value = value
                    self.policy[state] = action
            new_values[state] = max_value
            delta = max(delta, abs(self.values[state] - new_values[state]))
        
        return delta, new_values
    
    def value_iteration(self):
        delta = 1
        while delta > self.theta:
            delta, self.values = self.perform_single_value_iteration()
    
    def play(self, state):
        """
        given a state, return the chosen action for this state
        at minimum you must support the basic rules: three six-sided fair dice
        
        if you want to support more rules, use the values inside self.game, e.g.
            the input state will be one of self.game.states
            you must return one of self.game.actions
        
        read the code in dicegame.py to learn more
        """
        return self.policy[state]


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
    np.random.seed(300)
    game = DiceGame()
    iterations = 100000
    agent = ValueIterationAgent(game)
    total = 0
    for i in range(iterations):
        total += play_game_with_agent(agent, game)
    print(f"average score = {total/iterations}")