import X_AND_O_helper_functions 
import pygame
import copy
import sys


# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 800    # set window size leave space for buttons also
LINE_COLOR = (50, 50, 50)    
BG_COLOR = (194, 240, 194)
GRID_SIZE = 3
CELL_SIZE = WIDTH // GRID_SIZE  # cell size is floor of (width/grid_size)

# Initialize the window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe")


# Create buttons
button_width=200
button_height=100
x_button_rect = pygame.Rect(0, HEIGHT-button_height, button_width, button_height)   # top left corner (x,y,width,height)
o_button_rect = pygame.Rect(WIDTH-button_width, HEIGHT-button_height, button_width, button_height)    # top left corner (x,y,width,height)



# create empty 2d array of 3 X 3 and initial player is X default unless O button selected 
grid = [[" " for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
current_player = " " # remains " " unless selected X or O 

########################################################################################################################################################################
            
def next_turn(current_player):
    if current_player== "X":
        return "O"

    return "X"


# calculates the total possible number of wins out of all possible combinations of moves for player from this grid position
def calc_num_of_wins_possible(grid, current_player, arr, computer_player):   # we use a list so we  can pass by reference
    # player is the one we calculate wins for
    if X_AND_O_helper_functions.check_win(grid) == computer_player:
        arr[0] += 1
        return arr
    if X_AND_O_helper_functions.check_win(grid) == next_turn(computer_player):
        arr[0] -= 0.5
        return arr
    if X_AND_O_helper_functions.check_win(grid) == "DRAW":
        return arr

    for i in range(0, 3):
        for j in range(0, 3):
            if grid[i][j] == " ":
                grid[i][j] = current_player
                calc_num_of_wins_possible(grid, next_turn(current_player), arr, computer_player)
                grid[i][j] = " "

    return arr


# checks if player has a win in immediate next move and blocks it
def next_move_opponent_win(grid, opponent_player):    
    for row in range(0, 3):
        for col in range(0, 3):
            
            if grid[row][col] == ' ':   # if tile empty
                grid[row][col] = opponent_player # fill player in the tile
                
                if X_AND_O_helper_functions.check_win(grid) == opponent_player: 
                    grid[row][col] = ' '    # make tile empty again
                    return (row, col)# if the player has a win then return this position
                
                grid[row][col] = ' '    # make tile empty again

    return  # if no immediate win for opponent return NULL

                                        
def best_move_grid(grid, computer_player):

    max_win = 0
    max_win_grid = []

    for i in range(0, 3):
        for j in range(0, 3):

            human_player = next_turn(computer_player)
            row_col = next_move_opponent_win(grid, human_player)   # check if opponent has a win next move
            
            if row_col:
                row = row_col[0]
                col = row_col[1]
                
                grid[row][col] = computer_player    # if opponent has a win next move,just block that move and return 
                return grid

            # check all possibilties to find max wins and min losses
            if grid[i][j] == " ":
                grid[i][j] = computer_player
                
                arr = [0]
                wins_possible_with_this_grid = calc_num_of_wins_possible(grid, next_turn(computer_player), arr, computer_player)
                if wins_possible_with_this_grid[0] > max_win:
                    max_win = wins_possible_with_this_grid[0]
                    max_win_grid = copy.deepcopy(grid)

                grid[i][j] = " "


    if max_win > 0: return max_win_grid # check if there is even a possibility of win in position


    # if reached here means all combinations lead to draw so just fill the first blank you see 
    for row in range(0, 3):
        for col in range(0, 3):
            if grid[row][col] == ' ':
                grid[row][col] = computer_player
                return grid
    
    return


# Test the function
grid = [[' ', ' ', ' '],
        [' ', ' ', ' '],
        [' ', ' ', ' ']]

max_win_grid = best_move_grid(grid, 'X')

for row in max_win_grid:
    print(row)


################################################################################################################################################    

screen.fill(BG_COLOR)
X_AND_O_helper_functions.draw_grid(screen, GRID_SIZE, CELL_SIZE, LINE_COLOR)

# Draw buttons
pygame.draw.rect(screen, (255, 0, 0), x_button_rect)    # draw button on screen object and set color (rgb) 
pygame.draw.rect(screen, (0, 0, 255), o_button_rect)    # draw button on screen object and set color (rgb) 


# Add button labels
font = pygame.font.Font(None, 30)
x_text = font.render("X", True, (255, 255, 255))
o_text = font.render("O", True, (255, 255, 255))
screen.blit(x_text, (x_button_rect.centerx - x_text.get_width() // 2, x_button_rect.centery - x_text.get_height() // 2)) # draw the text on nbutton center
screen.blit(o_text, (o_button_rect.centerx - o_text.get_width() // 2, o_button_rect.centery - o_text.get_height() // 2)) # draw the text on nbutton center


# Create name labels
font = pygame.font.Font(None, 40)
COMPUTER = font.render("COMPUTER", True, (255, 0, 0))
HUMAN = font.render("HUMAN", True, (0, 0, 255))

# Position computer label
label_x = x_button_rect.centerx - COMPUTER.get_width() // 2
label_y = x_button_rect.top - COMPUTER.get_height() - 10  # Adjusted to place the label above the button

# Blit labels to the screen
screen.blit(COMPUTER, (label_x, label_y))

# Position human label
label_x = o_button_rect.centerx - HUMAN.get_width() // 2
label_y = o_button_rect.top - HUMAN.get_height() - 10  # Adjusted to place the label above the button

# Blit labels to the screen
screen.blit(HUMAN, (label_x, label_y))

PLAY_COMPUTER=True
current_player="X"
player_selected=False

# Main game loop
while PLAY_COMPUTER:

    # Handle events
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if x_button_rect.collidepoint(event.pos) and player_selected==False:   # check if mouse click inside boudary of x_button
                current_player="X"    # current player= X
                player_selected=True

            elif o_button_rect.collidepoint(event.pos) and player_selected==False: # check if mouse click inside boudary of y_button
                current_player="O"    # current player= O
                player_selected=True

            elif player_selected:

                if current_player=="O": # humans turn
                    row = event.pos[1] // CELL_SIZE # divide y position by cell size
                    col = event.pos[0] // CELL_SIZE # divide x position by cell size

                    if row<=2 and col<=2 and grid[row][col] == " ": # check if mouse click inside grid
                        grid[row][col] = current_player
                        current_player = "X"  # change player turn to computer

                if current_player=="X": # computer turn
                    # now let engine play move  
                    grid = best_move_grid(grid, 'X')    # (i,j)
                    current_player = "O"  # change player turn to human

    # Draw symbols on grid
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if grid[row][col] != " ":
                X_AND_O_helper_functions.draw_symbol(screen, CELL_SIZE, row, col, grid[row][col])
    
    winner = X_AND_O_helper_functions.check_win(grid) 
    winner_text = None


    if winner == "DRAW":
        X_AND_O_helper_functions.display_win("DRAWN GAME", screen, WIDTH, HEIGHT)
        PLAY_COMPUTER=False

    elif winner == "X":
        X_AND_O_helper_functions.display_win("COMPUTER WINS !", screen, WIDTH, HEIGHT)
        PLAY_COMPUTER=False

    elif winner == "O":
        X_AND_O_helper_functions.display_win("HUMAN WINS !", screen, WIDTH, HEIGHT)
        PLAY_COMPUTER=False

    
    pygame.display.flip() # all changes are collected in a back buffer and are performed at once when flip called


# Final event handling loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()

