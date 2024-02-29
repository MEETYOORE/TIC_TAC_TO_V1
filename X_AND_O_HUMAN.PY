import X_AND_O_helper_functions 
import pygame
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


PLAY_HUMAN=True
player_selected=False

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

# Main game loop
while PLAY_HUMAN:

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
                row = event.pos[1] // CELL_SIZE # divide y position by cell size
                col = event.pos[0] // CELL_SIZE # divide x position by cell size
                if row<=2 and col<=2 and grid[row][col] == " ": # check if mouse click inside grid
                    grid[row][col] = current_player
                    current_player = "O" if current_player == "X" else "X"  # change player turn


    # Draw symbols on grid
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if grid[row][col] != " ":
                X_AND_O_helper_functions.draw_symbol(screen, CELL_SIZE, row, col, grid[row][col])
    
    winner = X_AND_O_helper_functions.check_win(grid) 
    winner_text = None


    if winner == "DRAW":
        X_AND_O_helper_functions.display_win("DRAWN GAME", screen, WIDTH, HEIGHT)
        PLAY_HUMAN=False

    elif winner == "X":
        X_AND_O_helper_functions.display_win("X WINS !", screen, WIDTH, HEIGHT)
        PLAY_HUMAN=False

    elif winner == "O":
        X_AND_O_helper_functions.display_win("O WINS !", screen, WIDTH, HEIGHT)
        PLAY_HUMAN=False

    
    pygame.display.flip() # all changes are collected in a back buffer and are performed at once when flip called



# Final event handling loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()

