# Make a copy of this file
# and Add a class called AI Agent 

import sys
from gym_tictactoe.envs.tictactoe_env2D import TicTacToeEnv, after_action_state, check_game_status, agent_by_mark
player = '1'

class AIAgent(object):
    def __init__(self, mark):
        self.mark = mark

    def act(self, ava_actions):
        while True:
            uloc = None
            try:
                action = uloc
                if action not in ava_actions:
                    raise ValueError()
            except ValueError:
                print("Illegal location: '{}'".format(uloc))
            else:
                break

        return self.mark + action

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

def minimax(board, depth, maximisingPlayer):
    if board._result and maximisingPlayer: # 10 for o, -10 fro x, None for game in progress, 0 for draw
        return board._result + depth
    elif board._result and not maximisingPlayer:
        return board._result - depth
    if not board.available_actions():
        return 0
    if maximisingPlayer:
        maxEval = -float('inf')
        ava_actions = board.available_actions()
        for newaction in ava_actions:
            state, reward, done, info = board.step('2' + newaction)
            maxEval = max(maxEval, minimax(board, depth + 1, not maximisingPlayer))
            state[int(newaction[0])][int(newaction[1])] = 0 # Undo Action
            board._round -= 1 #Undo round
        return maxEval
    else:
        minEval = float('inf')
        ava_actions = board.available_actions()
        for newaction in ava_actions:
            state, reward, done, info = board.step('1' + newaction)
            minEval = min(minEval, minimax(board,depth + 1, not maximisingPlayer))
            state[int(newaction[0])][int(newaction[1])] = 0 # Undo Action
            board._round -= 1 #Undo round
        return minEval

def bestMove(board):
    bestVal = -float('inf')
    bestMove = ''
    ava_actions = board.available_actions()
    for action in ava_actions:
        state, reward, done, info = board.step('2'+ action)
        moveVal = minimax(board, 0, False)
        state[int(action[0])][int(action[1])] = 0 # Undo Action
        board._round -= 1 #Undo round
        if (moveVal > bestVal) :               
            bestMove = action
            bestVal = moveVal
    return bestMove

def play():
    env = TicTacToeEnv()
    agents = [HumanAgent('1'), AIAgent('2')]
    episode = 0
    turn = 0
    done = False
    while not done:
        agent = agent_by_mark(agents, str(env.show_turn()))
        print(agent.mark)
        if(agent.mark == '2'): # AI turn
            action = bestMove(env)
            print("|Best action identifies =", action)
            action = '2' + action
        else:
            ava_actions = env.available_actions()
            print("available moves =",ava_actions)
            action = agent.act(ava_actions)
        
        print(action)
        if action is None:
            sys.exit()

        turn += 1
        if turn != 10:
            state, reward, done, info = env.step(action)
        else:
            state, reward, done, info = env.step('200')
        print()
        print("Done = ", done, "| reward = ", reward, "| info = ", info)
        env.render()
        if done:
            env.show_result()
            break
    episode += 1


if __name__ == '__main__':
    play()