import random
import gamelogic
import ai_score

#difficulty
beginner = 0
easy = 1
medium = 2
hard = 3

# determines the number of recursion
easy_depth = 3
medium_depth = 5
hard_depth = 7

AI = 1
player = 0

columns = 7
 #----------------------------------------------------   
def max(board, depth, AI): # turn = AI retruns the max value to the min function
  #store the resulting node values  
  score_max = [0] * columns
  recursion = recursion + 1  # used for node traversal
  # create 7 different boards and add a AI piece to each column
  new_board = [board] * columns
  for column in new_board:
    if(gamelogic.check_valid(new_board[column], column)):
        if(recursion < depth):
            gamelogic.add_piece(new_board[column], column, AI)
            if(gamelogic.check_win(new_board[column], AI)):
                return ai_score.score_position(min(new_board[column], player), gamelogic.add_piece(new_board[column], column, AI))
            score_max[column] = min(new_board[column], player) # switch to player
        elif(recursion == depth):
            recursion = recursion - 1
            # score the board (send the board and the piece)
            #return the value to be stored
            return ai_score.score_position(min(new_board[column], player), gamelogic.add_piece(new_board[column], column, player))

    # find the smallest value in score_min and return the value
    max_value = score_max[0]
    column = 0
    for i in score_max:
        if(score_max[i] > max_value):
            max_value = score_max[i]
            column = i

    recursion = recursion - 1

    if(recursion <= 2): # should be recursion == 2
        return column
    else:
        return max_value
#---------------------------------------------------------------

def min(board, depth, player): # turn = player returns the min value to the max function
    score_min = [0] * columns
    recursion = recursion + 1  
    new_board = [board] * columns
    for column in new_board:
        if(gamelogic.check_valid(new_board[column], column)):
            if(recursion < depth):
                gamelogic.add_piece(new_board[column], column, player)
                if(gamelogic.check_win(new_board[column], player)):
                    continue
                score_min[column] = max(new_board[column], AI) # switch to AI
            elif(recursion == depth): 
                recursion = recursion - 1
                #score the board
                #return the value to be stored
                return ai_score.score_position(min(new_board[column], AI), gamelogic.add_piece(new_board[column], column, AI))


# find the smallest value in score_min and return the value
    min_value = score_min[0]
    column = 0
    for i in score_min:
        if(score_min[i] < min_value):
            min_value = score_min[i]
            column = i

    recursion = recursion - 1

    if (recursion <= 2): # should be recursion == 2
        return column
    else:
        return min_value

 #--------------------------------------------------       

def request_move_AI(board, difficulty, turn): 
    recursion = 0  # used for tree traversal
    insert_piece_into_column = 0

    if(difficulty == beginner):
        return random.randrange(0,7,1)
    elif(difficulty == easy):
        insert_piece_into_column = max(board, easy_depth, turn)
        return insert_piece_into_column
    elif(difficulty == medium):
        insert_piece_into_column = max(board, medium_depth, turn)
        return insert_piece_into_column
    elif(difficulty == hard):
        insert_piece_into_column = max(board, hard_depth, turn)
        return insert_piece_into_column
    else:
        print("Difficulty initialization Error")
