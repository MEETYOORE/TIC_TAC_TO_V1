import copy
import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 800    # set window size leave space for buttons also
LINE_COLOR = (0, 0, 0)      
BG_COLOR = (50, 255, 50)
GRID_SIZE = 3
CELL_SIZE = WIDTH // GRID_SIZE  # cell size is floor of (width/grid_size)

# Initialize the window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe")


# Function to draw the grid lines
def draw_grid():
    for i in range(1, GRID_SIZE+1):
        pygame.draw.line(screen, LINE_COLOR, (0, i * CELL_SIZE), (WIDTH, i * CELL_SIZE))    # 4 horizontal line from (0,y) to (horizontal_dge,y)

    for i in range(1, GRID_SIZE):
        pygame.draw.line(screen, LINE_COLOR, (i * CELL_SIZE, 0), (i * CELL_SIZE, CELL_SIZE*3))  # 3 vertical line from (x,0) to (x,vertical_edge)


# Function to draw the X or O in the cell
def draw_symbol(row, col, symbol):
    font = pygame.font.Font(None,100)                     #select default font,size=100   
    if(symbol=='O'):                                      #for O set blue color
        text = font.render(symbol, True, (0, 0, 255))     #render the symbol using font ,set anti aliasing True , color rgb
    else:                                                 #for X set red color
        text = font.render(symbol, True, (255, 0, 0))     #render the symbol using font ,set anti aliasing True , color rgb

    text_rectangle = text.get_rect(center=(col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2)) # set the text surface at the mid_point of the cell
    screen.blit(text, text_rectangle)   # blit used to draw one image on top of another 


# Create buttons
button_width=200
button_height=100
x_button_rect = pygame.Rect(0, HEIGHT-button_height, button_width, button_height)   # top left corner (x,y,width,height)
o_button_rect = pygame.Rect(WIDTH-button_width, HEIGHT-button_height, button_width, button_height)    # top left corner (x,y,width,height)


# Function to handle button click events
def handle_button_click(symbol):
    global current_player
    current_player = symbol


# create empty 2d array of 3 X 3 and initial player is X default unless O button selected 
grid = [[" " for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
current_player = " " # remains " " unless selected X or O 


# checks for a win IN GRID
def check_win(grid):
    for i in range(0,3):
        if grid[i][0] == grid[i][1] == grid[i][2] != " " : # if 3 in  a column then win
            return grid[i][0]
    for j in range(0,3):
        if grid[0][j] == grid[1][j] == grid[2][j] != " " : # if 3 in  a row then win
            return grid[0][j]
    
    if grid[0][0]==grid[1][1] and grid[1][1]==grid[2][2]:   # if 3 in  a diag then win
        return grid[0][0]
    
    if grid[0][2]==grid[1][1] and grid[1][1]==grid[2][0]:   # if 3 in  a diag then win
        return grid[0][2]

    else:
        if not any(" " in row for row in grid):
            return "DRAW"   #if NOTA then drawn game


def display_win(msg):
    winner_text = msg_font.render(msg , True, (100, 100, 100))
    screen.blit(winner_text, (WIDTH // 2 - winner_text.get_width() // 2, HEIGHT//2 - winner_text.get_height()))  # Display winner message at the bottom
    pygame.display.flip()
    pygame.time.delay(2000)  # Delay for 5 seconds before continuing



PLAY_HUMAN=True
player_selected=False

# Main game loop
while PLAY_HUMAN:
    screen.fill(BG_COLOR)
    draw_grid()

    # Draw buttons
    pygame.draw.rect(screen, (255, 0, 0), x_button_rect)    # draw button on screen object and set color (rgb) 
    pygame.draw.rect(screen, (0, 0, 255), o_button_rect)    # draw button on screen object and set color (rgb) 

    # Add button labels
    font = pygame.font.Font(None, 30)
    x_text = font.render("X", True, (255, 255, 255))
    o_text = font.render("O", True, (255, 255, 255))
    screen.blit(x_text, (x_button_rect.centerx - x_text.get_width() // 2, x_button_rect.centery - x_text.get_height() // 2)) # draw the text on nbutton center
    screen.blit(o_text, (o_button_rect.centerx - o_text.get_width() // 2, o_button_rect.centery - o_text.get_height() // 2)) # draw the text on nbutton center

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if x_button_rect.collidepoint(event.pos) and player_selected==False:   # check if mouse click inside boudary of x_button
                handle_button_click("X")    # current player= X
                player_selected=True
            elif o_button_rect.collidepoint(event.pos) and player_selected==False: # check if mouse click inside boudary of y_button
                handle_button_click("O")    # current player= O
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
                draw_symbol(row, col, grid[row][col])
    
    winner = check_win(grid) 
    winner_text = None
    msg_font = pygame.font.Font(None, 100)


    if winner == "DRAW":
        display_win("DRAWN GAME")
        PLAY_COMPUTER=False

    elif winner == "X":
        display_win("X WINS !")
        PLAY_COMPUTER=False

    elif winner == "O":
        display_win("O WINS !")
        PLAY_COMPUTER=False

    
    pygame.display.flip() # all changes are collected in a back buffer and are performed at once when flip called


