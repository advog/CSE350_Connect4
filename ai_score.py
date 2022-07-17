COLUMN_COUNT = 7
ROW_COUNT = 6

WINDOW_LENGTH = 4

PLAYER_PIECE = 0
AI_PIECE = 1

EMPTY = 0

def evaluate_window(window, piece):
    score = 0
    opp_piece = PLAYER_PIECE
    if piece == PLAYER_PIECE:
        opp_piece = AI_PIECE
    #If this window has a winning position for us, give it a very high score
    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(EMPTY) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        SCORE += 2

    # avoid situations where the opponent is close to winning
    if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
        score -= 4

    return score
#-------------------------------------------------------


def score_position(board, piece):
    score = 0
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

    return score

