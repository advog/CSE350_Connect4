import random
import gamelogic
import ai_score
import math

#constants
beginner = 0
easy = 1
medium = 2
hard = 3
ai_player = 1
human = 0
columns = 7

def minimax(board, depth, turn, alpha, beta, maximizing): # turn = AI retruns the max value to the min function
    #establish players
    player = turn
    opp_player = 1 if turn == 2 else 2


    #base cases for recursion
    if depth==0:#end recursion
        return(None, ai_score.score_position(board,turn))
    if gamelogic.check_win(board,player)==player: #win for us
        return (None,1e10)
    if gamelogic.check_win(board,opp_player)==opp_player: #win for them
        return (None,-1e10)
    if sum(x.count(0) for x in board)==0: #tie
        return (None,0)


    # create 7 different boards and add a AI piece to each column
    new_board = []
    for i in range(columns):
        y = [row[:] for row in board]
        new_board.append(y)


    #max and min steps
    if maximizing:
        curr_score = -math.inf
        final_col = -1
        column = 0
        for item in new_board:
            if (gamelogic.check_valid(item, column)):

                #create possible board and score
                gamelogic.add_piece(item,column, player)
                new_score = minimax(item,depth-1,player, alpha, beta, False)[1]

                if(new_score>curr_score):
                    curr_score=new_score
                    final_col=column

                """
                #alpha-beta pruning:
                alpha = max(alpha,curr_score)
                if alpha >= beta:
                    break
                """
            column += 1
        return (final_col,curr_score)

    else:

        curr_score = math.inf
        final_col = -1
        column = 0
        for item in new_board:
            if (gamelogic.check_valid(item, column)):
                # create possible board and score
                gamelogic.add_piece(item, column, opp_player)
                new_score = minimax(item, depth - 1, opp_player, alpha, beta, True)[1]

                if (new_score < curr_score):
                    curr_score = new_score
                    final_col = column

                """
                # alpha-beta pruning:
                beta=min(beta,curr_score)
                if alpha >= beta:
                    break
                """
            column += 1
        return (final_col, curr_score)

def request_move_AI(board, difficulty, turn):
    if difficulty==0:
        return random.randrange(0,7,1)
    difficulty = difficulty * 2
    if difficulty > 6: difficulty = difficulty - 1
    value = minimax(board,difficulty,turn,-math.inf,math.inf,True)[0]
    return value
    print("Difficulty initialization Error")