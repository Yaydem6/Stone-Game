MIN_LENGTH = 4 #row and column number of the playing field must be between 4-8.
MAX_LENGTH = 8
MIN_STONE = 2 #players must have at least 2 stones or the game is finished.
def input_movement(length,stone_list, column_dict, char): #take input of movement from the user
    try:
        turn = input(f"Player {char}, please enter the position of your own stone you want to move and the target position:")
        row_of_stone = int(turn[0]) #row of the stone user wants to move
        column_of_stone = column_dict[turn[1].upper()] #column of the stone user wants to move
        while stone_list[row_of_stone - 1][column_of_stone - 1] != char: #if the stone user want to move is not in given position
            turn = input("You have any stone there. Try again:")
            row_of_stone = int(turn[0])
            column_of_stone = column_dict[turn[1].upper()]
        row_of_target = int(turn[3]) #row of the position user wants to go
        column_of_target = column_dict[turn[4].upper()] #column of the position user wants to go
        if 0 > column_of_target or column_of_target > length or 0 > row_of_target or row_of_target > length:
            print("Incorrect data entry.Try again.")
            row_of_stone, column_of_stone, row_of_target, column_of_target=input_movement(length,stone_list,column_dict,char)
    except ValueError:
        print("Incorrect data entry. Try again.")
        row_of_stone, column_of_stone, row_of_target, column_of_target = input_movement(length,stone_list, column_dict,char)
    except KeyError:
        print("Incorrect data entry. Try again.")
        row_of_stone, column_of_stone, row_of_target, column_of_target = input_movement(length,stone_list, column_dict,char)
    except IndexError:
        print("Incorrect data entry. Try again.")
        row_of_stone, column_of_stone, row_of_target, column_of_target = input_movement(length,stone_list, column_dict,char)
    return row_of_stone, column_of_stone, row_of_target, column_of_target

def input_length(): #take input of table's length
    try:
        length = int(input("Enter the row/column number of the playing field(4-8):"))
        while length < MIN_LENGTH or length > MAX_LENGTH:
            length = int(input("Row/column number must be between 4 and 8. Try again:"))
    except ValueError:
        print("Incorrect data entry.")
        length = input_length()
    return length

def field(char1, char2, stone_list, length, column_alphabet): #print the playing field
    print("    ", end="")
    for index in range(0, length):
        print(f"{column_alphabet[index]:3}", end=" ")
    print()
    print("  ", end="")
    for i in range(length * 3 + length + 1):
        print("-", end="")
    print()
    for row in range(0, length):
        print(f"{row + 1:1}", end=" | ")
        for column in range(0, length):
            print(f"{stone_list[row][column]:1}", end=" | ")
        print(f"{row + 1:1}")
        print("  ", end="")
        for i in range(length * 3 + length + 1):
            print("-", end="")
        print()
    print("    ", end="")
    for index in range(0, length):
        print(f"{column_alphabet[index]:3}", end=" ")
    print()

def player1(stone_list, char1, char2, length, column_dict, column_alphabet): #first player's turn
    row_of_stone, column_of_stone, row_of_target, column_of_target = input_movement(length,stone_list, column_dict, char1)
    check = if_move(row_of_stone, row_of_target, column_of_stone, column_of_target, stone_list)
    while not check: #if player can't do that move, take input until a right move
        row_of_stone, column_of_stone, row_of_target, column_of_target = input_movement(length,stone_list, column_dict, char1)
        check = if_move(row_of_stone, row_of_target, column_of_stone, column_of_target, stone_list)

    stone_list[row_of_stone - 1][column_of_stone - 1] = " " #stone removed from current position
    stone_list[row_of_target - 1][column_of_target - 1] = char1 #stone goes to target position
    remove_row, remove_column = if_remove(column_alphabet,stone_list, length, row_of_target, column_of_target, char1, char2)
    field(char1, char2, stone_list, length, column_alphabet)
    if remove_row != -1:  # if it is not default value, print removed stone's position
        print(f"The stone at position {remove_row}{remove_column} was locked and removed.")
    if if_finish(length, stone_list, char1, char2) == "continue": #if game continues, opponent makes a move
        player2(stone_list, char1, char2, length, column_dict, column_alphabet)
    else:
        print(f"Player {char1} won the game.")  #print the winner

def player2(stone_list, char1, char2, length, column_dict, column_alphabet): #second player's turn
    row_of_stone, column_of_stone, row_of_target, column_of_target = input_movement(length,stone_list, column_dict, char2)
    check = if_move(row_of_stone, row_of_target, column_of_stone, column_of_target, stone_list)
    while not check: #if player can't do that move, take input until a right move
        row_of_stone, column_of_stone, row_of_target, column_of_target = input_movement(length,stone_list, column_dict, char2)
        check =if_move(row_of_stone, row_of_target, column_of_stone, column_of_target, stone_list)

    stone_list[row_of_stone - 1][column_of_stone - 1] = " " #stone removed from current position
    stone_list[row_of_target - 1][column_of_target - 1] = char2 #stone goes to target position
    remove_row, remove_column = if_remove(column_alphabet,stone_list,length,row_of_target, column_of_target,char2,char1)
    field(char1, char2, stone_list, length, column_alphabet)
    if remove_row != -1: #if it is not default value, print removed stone's position
        print(f"The stone at position {remove_row}{remove_column} was locked and removed.")
    if if_finish(length, stone_list, char1, char2) == "continue": #if game continues, opponent makes a move
        player1(stone_list, char1, char2, length, column_dict, column_alphabet)
    else:
        print(f"Player {char2} won the game.")  #print the winner

def if_move(row_of_stone, row_of_target, column_of_stone, column_of_target, stone_list): #control whether the player can make the move
    check = True
    message = "" #the message to show when the move is wrong
    if row_of_stone == row_of_target and column_of_stone == column_of_target:
        message = "Your target and location can't be same."
        check = False
    elif row_of_stone == row_of_target:  # moves horizontally
        if column_of_target > column_of_stone: #goes to right
            for column in range(column_of_stone, column_of_target):
                if stone_list[row_of_stone - 1][column] != " ":
                    message = "You can't go there."
                    check = False
        elif column_of_target < column_of_stone: #goes to left
            for column in range(column_of_stone - 2, column_of_target - 2, -1):
                if stone_list[row_of_stone - 1][column] != " ":
                    message = "You can't go there."
                    check = False
    elif column_of_stone == column_of_target:  #moves vertically
        if row_of_target > row_of_stone:  #goes to down
            for row in range(row_of_stone, row_of_target):
                if stone_list[row][column_of_stone - 1] != " ":
                    message = "You can't go there."
                    check = False
        elif row_of_target < row_of_stone: #goes to up
            for row in range(row_of_stone - 2, row_of_target - 2, -1):
                if stone_list[row][column_of_stone - 1] != " ":
                    message = "You can't go there."
                    check = False
    else: #wants to move diagonally
        message = "You must go vertically or horizontally."
        check = False
    print(message)
    return check

def if_remove(column_alphabet,stone_list,length,row_of_target,column_of_target,player,opponent):
    remove_row, remove_column = -1, -1  # default value
    #player = the character of the player whose turn, opponent = that player's opponent's character
    #check if there is a locked stone to the left of the played stone
    if column_of_target > 2: #if played stone's column is 1 or 2, there is no locked stone on the left.
        #if there is opponent's stone on the left of the played stone and there is player's stone on the left of opponent, opponent is removed.
        if stone_list[row_of_target-1][column_of_target-2] == opponent and stone_list[row_of_target-1][column_of_target-3] == player:
            stone_list[row_of_target-1][column_of_target-2] = " "
            remove_row, remove_column = row_of_target, column_alphabet[column_of_target-2]
    #check if there is a locked stone to the right of the played stone
    if column_of_target < length-1: #if played stone's column is equal to length or length-1, there is no locked stone on the right.
        #if there is opponent's stone on the right of the played stone and there is player's stone on the right of opponent, opponent is removed.
        if stone_list[row_of_target-1][column_of_target] == opponent and stone_list[row_of_target-1][column_of_target+1] == player:
            stone_list[row_of_target-1][column_of_target] = " "
            remove_row, remove_column = row_of_target, column_alphabet[column_of_target]
    #check if there is a locked stone above of the played stone
    if row_of_target > 2: #moved stone's row must be at least 2 to lock
        #if there is opponent's stone above of the played stone and there is player's stone on the above of opponent, opponent is removed.
        if stone_list[row_of_target-2][column_of_target-1] == opponent and stone_list[row_of_target-3][column_of_target-1] == player:
            stone_list[row_of_target-2][column_of_target-1] = " "
            remove_row, remove_column = row_of_target-1, column_alphabet[column_of_target-1]
    #check if there is a locked stone under the played stone
    if row_of_target < length-1:
        # if there is opponent's stone under the played stone and there is player's stone under the opponent, opponent is removed.
        if stone_list[row_of_target][column_of_target-1] == opponent and stone_list[row_of_target+1][column_of_target-1] == player:
            stone_list[row_of_target][column_of_target-1] = " "
            remove_row, remove_column = row_of_target+1, column_alphabet[column_of_target-1]

    #check if there is a locked stone at the corners.
    if stone_list[0][0] == opponent:
        if stone_list[0][1] == player and stone_list[1][0]== player:
            stone_list[0][0] = " " #remove the locked stone
            remove_row, remove_column = 1,column_alphabet[0]
    if stone_list[0][length-1] == opponent:
        if stone_list[0][length-2] == player and stone_list[1][length-1] == player:
            stone_list[0][length-1] = " "
            remove_row, remove_column = 1,column_alphabet[length-1]
    if stone_list[length-1][0] == opponent:
        if stone_list[length-1][1] == player and stone_list[length-2][0] == player:
            stone_list[length-1][0] = " "
            remove_row, remove_column = length,column_alphabet[0]
    if stone_list[length-1][length-1] == opponent:
        if stone_list[length-1][length-2] == player and stone_list[length-2][length-1] == player:
            stone_list[length-1][length-1] = " "
            remove_row, remove_column = length, column_alphabet[length-1]
    return remove_row,remove_column


def if_finish(length, stone_list, char1, char2): #check if the game is finished
    count1 = 0 #first player's stone count
    count2 = 0 #second player's stone count
    for i in range(0, length):
        for j in range(0, length):
            if stone_list[i][j] == char1: #if there is 1. player's stone increase counter
                count1 += 1
            elif stone_list[i][j] == char2: #if there is 2. player's stone increase counter
                count2 += 1
    if count1 < MIN_STONE or count2 < MIN_STONE: #if one of the players have one stone finish the game
        return "finish"
    else:
        return "continue"

def main():
    column_dict = {"A": 1, "B": 2, "C": 3, "D": 4, "E": 5, "F": 6, "G": 7, "H": 8}
    column_alphabet = ["A", "B", "C", "D", "E", "F", "G", "H"]
    char1 = input("Enter a character to represent player 1:").upper()
    while len(char1) != 1:
        char1 = input("The length of your character must be 1. Try again:").upper()
    char2 = input("Enter a character to represent player 2:").upper()
    while len(char2) != 1:
        char2 = input("The length of your character must be 1. Try again:").upper()
    answer = "Y"
    while answer in ["Y","y"]:
        length = input_length()
        #make a list of stones
        stone_list = []
        for i in range(length):
            a_row = [" "] * length
            stone_list.append(a_row)
        #stones at the beginning
        for column in range(0, length):
            stone_list[0][column] = char1
        for column in range(0, length):
            stone_list[length - 1][column] = char2

        field(char1, char2, stone_list, length, column_alphabet) #print the table at the beginning
        player1(stone_list, char1, char2, length, column_dict, column_alphabet) #start the game
        answer = input("Would you like to play again(Y,y,N,n):")
        while answer not in ["Y", "y", "N", "n"]:
            answer = input("Incorrect data entry. Try again(Y,y,N,n):")

main()
