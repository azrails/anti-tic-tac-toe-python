import click
import random

def check_diagonals(game_map: 'list[list[str]]', size_to_victory:int, hight_left: 'list[int]')-> bool:
    """Checked lost the game on the diagonals"""
    toright = set()
    toleft = set()
    for i in range(size_to_victory):
        toright.add(game_map[hight_left[0] + i][hight_left[1] + i])
        toleft.add(game_map[hight_left[0] + i][hight_left[1] + size_to_victory - i])
    if (len(toright) == 1 and (' ' in toright) == False) or (len(toleft) == 1 and (' ' in toleft) == False):
        return True
    return False

def check_lines(game_map: 'list[list[str]]', size_to_victory: int, hight_left: 'list[int]')-> bool:
    """Checked lost the game on the lines\columns"""
    line = set()
    column = set()
    i,j = hight_left[0],hight_left[1]
    while (i <= (hight_left[0] + size_to_victory - 1)):
        while (j <= (hight_left[1] + size_to_victory - 1)):
            line.add(game_map[i][j])
            column.add(game_map[j][i])
            j += 1
        if len(line) == 1 and (' ' in line) == False:
            return True
        if len(column) == 1 and (' ' in column) == False:
            return True
        line.clear()
        column.clear()
        i += 1
    return False

def winlose(size_of_map: int, size_to_victory: int, game_map: 'list[list[str]]')-> int:
    """Check end game."""
    for i in range(size_of_map - size_to_victory):
        for j in range(size_of_map - size_to_victory):
            if (check_lines(game_map, size_to_victory, hight_left=[i,j])) == True \
                or (check_diagonals(game_map, size_to_victory, hight_left=[i,j])) == True:
                return True
    return False

def empty_cell(game_map: 'list[list[str]]')->'list[list[int]]':
    """Create map of empty cells"""
    empty_c = []
    for i in range(len(game_map)):
        empty_c.append([])
        for j in range(len(game_map[i])):
            if game_map[i][j] == ' ':
                empty_c[i].append(j)
    return empty_c

def go_random(game_map: 'list[list[str]]', size_of_map: int, size_to_victory: int, computer_symbol: str): 
    """Chose a random cell for computer move"""
    empt = empty_cell(game_map)
    count = 0
    while True:
        x = random.randrange(0, len(empt))
        if (len(empt[x]) == 0):
            continue
        y = random.choice(empt[x])
        if game_map[x][y] == ' ':
            game_map[x][y] = computer_symbol
            if winlose(size_of_map, size_to_victory, game_map) == True and count < 3:
                game_map[x][y] = ' '
                count += 1
                continue
            else:
                break

def draw_terminal(d_map: 'list[list[str]]')-> None:
    """The function draws a tic-tac-toe map of any rectangular field in the terminal.""" 
    len_map = len(d_map[0])
    for i in range(len(d_map)):
        for j in range(len(d_map[i])):
            print(f'{d_map[i][j]}', end='')
            print('|',end='') if j < (len_map - 1) else print()
        for j in range(len(d_map[i]) + 1):
            print('{0:2}'.format("_"), end='') if j < (len_map) else print()

def chose_symbol()-> 'list[str]':
    """The function gets from the user what sign he wants to play."""
    while True:
        player_symbol = str(input("Chose X or O\n"))
        if player_symbol == 'X' or player_symbol == 'O':
            break
        print("Please, try again")
    return player_symbol, 'X' if player_symbol == 'O' else 'O'

def player_move(game_map: 'list[list[str]]', size_of_map: int, player_symbol: str)-> None:
    """Function processes the player move"""
    while True:
        inp = input(f'Chose the move in ranger ({size_of_map},{size_of_map})\n')
        position = inp.split(',')
        try:
            for i in range(2):
                position[i] = int(position[i]) - 1
        except IndexError:
            continue
        if game_map[position[0]][position[1]] != ' ':
            continue
        if (position[0] >= size_of_map or position[1] >= size_of_map) or (position[0] < 0 or position[1] < 0):
            continue
        else:
            break
    game_map[position[0]][position[1]] = player_symbol

"""def minimax(game_map, size_of_map, size_to_victory, computer_symbol):
    empty_c = empty_cell(game_map)
    pass"""
    
def tictactoe(size_of_map: int, size_to_victory: int)-> None:
    """The starting function of the game of tic-tac-toe."""
    count = 0
    player_symbol, computer_symbol = chose_symbol()
    game_map = [[' ' for i in range(size_of_map)] for i in range(size_of_map)]
    draw_terminal(game_map)
    while True:
        if count == (size_of_map * size_of_map):
            print("Draw X and O")
        if count >= ((size_to_victory * 2) - 2):
            if winlose(size_of_map, size_to_victory, game_map) == True:
                print("LOSE X") if (count % 2) == 1 else print("LOSE O")
                break
        if (player_symbol == 'X' and (count % 2) == 0) or (player_symbol == 'O' and (count % 2) == 1):
            print('Turn Player:')
            player_move(game_map, size_of_map, player_symbol)
            draw_terminal(game_map)
        else:
            #if count <= ((size_of_map * size_of_map) - 20):
            go_random(game_map, size_of_map, size_to_victory, computer_symbol)
            #else:
            #    minimax(game_map, size_of_map, size_to_victory, computer_symbol)
            print('Turn Computer:')
            draw_terminal(game_map)
        count+=1

@click.command()
def main():
    tictactoe(10, 5)

if __name__ == '__main__':
    main()