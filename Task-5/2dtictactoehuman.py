# Make a copy of this file
# and Add a class called AI Agent 

import sys

from gym_tictactoe.envs.tictactoe_env2D import TicTacToeEnv, after_action_state, check_game_status, agent_by_mark

class HumanAgent(object):
    def __init__(self, mark):
        self.mark = mark

    def act(self, ava_actions):
        while True:
            uloc = input("Enter location[00 - 22], q for quit: ")
            if uloc.lower() == 'q':
                return None
            try:
                action = uloc
                if action not in ava_actions:
                    raise ValueError()
            except ValueError:
                print("Illegal location: '{}'".format(uloc))
            else:
                break

        return self.mark + action

def play():
    env = TicTacToeEnv()
    agents = [HumanAgent('1'),
              HumanAgent('2')]
    episode = 0
    done = False
    while not done:
        agent = agent_by_mark(agents, str(env.show_turn()))
        ava_actions = env.available_actions()
        print("Available actions = ", ava_actions)
        if ava_actions:
            action = agent.act(ava_actions)
        else:
            action = '200'
        if action is None:
            sys.exit()
        state, reward, done, info = env.step(action)
        print("Done or not env = ", env._done) # 1 for x, 2 for o, -1 for none
        print("done =", done, "| reward =", reward, "| result = ", env._result)
        print()
        env.render()
        if done:
            env.show_result()
            break
    episode += 1


if __name__ == '__main__':
    play()