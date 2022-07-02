def check_valid(board, column):
    if(column == -1):
        value = False
    elif(board[column][get_open_row(board, column)][1] == 0):
        value = True
    else:
        value = False
    return value

def get_open_row(board, col):
    row = -1
    for i in range(6):
        if(board[col][i][1]==0):
            row = i
    return row

def upadate_board(board, column, turn):
    if(turn%2 == 1):
        player_value = 1
    else:
        player_value = 2
    for row in range(0,6):
        if(board[column][row][1] != 0):
            board[column][row-1] = player_value
            return
        elif(row == 5):
            board[column][row-1] = player_value
            return

def check_win(board, turn, start_column):
    if(turn%2 == 1):
        player_value = 1
    else:
        player_value = 2
    next_turn = 0
    win = 1
    tie = 2
    start_row = 0
    count = 0

    # Checking Down Win
    for row in range(0,6):
        if(board[start_column][row][1] == player_value):
            if(count == 0):
                start_row = row
            count += 1
            if(count == 4):
                return win
        elif(board[start_column][row][1] == 0):
            continue
        elif(board[start_column][row][1] != player_value):
            break

    # Checking Across Win
    count = 0
    for column in range(start_column,-1, -1):
        if(board[column][start_row] == player_value):
            count += 1
            if(count == 4):
                return win
        else:
            break
    for column in range(start_column+1, 7):
        if(board[column][start_row] == player_value):
            count += 1
            if(count == 4):
                return win
        else:
            break

    #Checking Positive Diagonal Win
    count = 0
    row = start_row
    column = start_column
    while(row < 6 and column > -1):
        if(board[column][row][1] == player_value):
            count += 1
            if(count == 4):
                return win
        else:
            break
        row += 1
        column -= 1
    row = start_row - 1
    column = start_column + 1
    while(row > -1  and column < 7):
        if(board[column][row][1] == player_value):
            count += 1
            if(count == 4):
                return win
        else:
            break
        row -= 1
        column += 1

    #Checking Negative Diagonal Win
    count = 0
    row = start_row
    column = start_column
    while(column > -1 and row > -1):
        if(board[column][row][1] == player_value):
            count += 1
            if(count == 4):
                return win
        else:
            break
        row -= 1
        column -= 1
    row = start_row + 1
    column = start_column + 1
    while(row < 6  and column < 7):
        if(board[column][row][1] == player_value):
            count += 1
            if(count == 4):
                return win
        else:
            break
        row += 1
        column += 1
    if(turn == 42):
        return tie
    else:
        return next_turn
