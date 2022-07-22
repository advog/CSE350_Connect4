import random

COLUMN_COUNT = 7
ROW_COUNT = 6

WINDOW_LENGTH = 4

PLAYER_PIECE = 1
AI_PIECE = 2

EMPTY = 0

def evaluate_window(window, turn):
    score = 0
    player = turn
    opp_player = 1 if turn == 2 else 2
    #If this window has a winning position for us, give it a very high score
    if window.count(player) == 4:
        score += 100
    elif window.count(player) == 3 and window.count(EMPTY) == 1:
        score += 5
    #elif window.count(player) == 2 and window.count(EMPTY) == 2:
     #   score += 2

    # avoid situations where the opponent is close to winning
    if window.count(opp_player) == 3 and window.count(EMPTY) == 1:
        score -= 5
    if window.count(opp_player) == 4:
        score -= 100

    return score
#-------------------------------------------------------


def score_position(board,turn):
    #score = random.randrange(0,7,1)
    '''
#score center columns
    center_array = [int(i) for i in list(board[:, COLUMN_COUNT/2])]
    center_count = center_array.count(piece)
    score += center_count * 3

#score horizontal
    for r in range(ROW_COUNT):
        row_array = [int(i) for i in list(board[r,:])]
        for c in range(COLUMN_COUNT - 3):
            window = row_array[c:c+WINDOW_LENGTH] # not sure what this is
            score += evaluate_window(window, piece)

#score positively sloped diagonal
    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT-3):
            window = [board[r+i][c+i] for i in range[WINDOW_LENGTH]]
            score += evaluate_window(window, piece)

#score negetively sloped diagonal
    for r in range(ROW_COUNT-3):
        for c in range(COLUMN_COUNT-3):
            window = [board[r+3][c+i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)
'''

    score_total=0
    for x in range(7):
        for y in range(6):
            #vertical
            if(y > 2):
                curr_window = [board[x][y],board[x][y-1],board[x][y-2],board[x][y-3]]
                score_total += evaluate_window(curr_window,turn)
            #up diagonal
            if (y > 2 and x < 4):
                curr_window = [board[x][y], board[x+1][y - 1], board[x+2][y - 2], board[x+3][y - 3]]
                score_total += evaluate_window(curr_window, turn)
            #horizontal
            if (x < 4):
                curr_window = [board[x][y], board[x+1][y], board[x+2][y], board[x+3][y]]
                score_total += evaluate_window(curr_window, turn)
            #down diagnal
            if (x < 4 and y < 3):
                curr_window = [board[x][y], board[x+1][y + 1], board[x+2][y + 2], board[x+3][y + 3]]
                score_total += evaluate_window(curr_window, turn)
    return score_total

