import random
import gamelogic
import ai_score

#difficulty
beginner = 0
easy = 1
medium = 2
hard = 3

recursion = 0
# determines the number of recursion
easy_depth = 3
medium_depth = 5
hard_depth = 7

ai_player = 1
human = 0

columns = 7
 #----------------------------------------------------   
def max(board, depth, AI): # turn = AI retruns the max value to the min function
  #store the resulting node values 
  global recursion 
  score_max = [0] * columns
  # create 7 different boards and add a AI piece to each column
  new_board = []
  for i in range(columns):
      new_board.append(board.copy())
  column = 0
  for item in new_board:
    if(gamelogic.check_valid(item, column)):
        if(recursion < depth):
            recursion = recursion + 1  
            print(recursion)
            gamelogic.add_piece(item, column, AI)
            if(gamelogic.check_win(item, AI) == AI):
                return ai_score.score_position()
            score_max[column] = min(item, depth, human) # switch to player
        elif(recursion == depth):
            recursion = recursion - 1
            print(recursion)
            # score the board (send the board and the piece)
            #return the value to be stored
            return ai_score.score_position()
        column += 1
    # find the smallest value in score_min and return the value
    max_value = score_max[0]
    column = 0
    for i in score_max:
        if(i > max_value):
            max_value = i
            column = score_max.index(i)

    recursion = recursion - 1

    if(recursion == 2): # should be recursion == 2
        return column
    else:
        return max_value
#---------------------------------------------------------------

def min(board, depth, player): # turn = player returns the min value to the max function
    global recursion
    score_min = [0] * columns
    #new_board = [board for i in range(columns)]
    new_board = []
    for i in range(columns):
        new_board.append(board.copy())
    column = 0
    for item in new_board:
        if(gamelogic.check_valid(item, column)):
            if(recursion < depth):
                recursion = recursion + 1  
                print(recursion)
                gamelogic.add_piece(item, column, player)
                if(gamelogic.check_win(item, player) == player):
                    continue
                score_min[column] = max(item, depth, ai_player) # switch to AI
            elif(recursion == depth): 
                recursion = recursion - 1
                print(recursion)
                #score the board
                #return the value to be stored
                return ai_score.score_position()
            column += 1

# find the smallest value in score_min and return the value
    min_value = score_min[0]
    column = 0
    for i in score_min:
        if(i < min_value):
            min_value = i
            column = score_min.index(i)

    recursion = recursion - 1

    if (recursion == 2): # should be recursion == 2
        return column
    else:
        return min_value

 #--------------------------------------------------       

def request_move_AI(board, difficulty, turn): 
    global recursion
    recursion = 1  # used for tree traversal
    insert_piece_into_column = 0

    if(difficulty == beginner):
        return random.randrange(0,7,1)
    elif(difficulty == easy):
        insert_piece_into_column = max(board, easy_depth, turn)
        print("disk ", insert_piece_into_column)
        return insert_piece_into_column
    elif(difficulty == medium):
        insert_piece_into_column = max(board, medium_depth, turn)
        return insert_piece_into_column
    elif(difficulty == hard):
        insert_piece_into_column = max(board, hard_depth, turn)
        return insert_piece_into_column
    else:
        print("Difficulty initialization Error")
