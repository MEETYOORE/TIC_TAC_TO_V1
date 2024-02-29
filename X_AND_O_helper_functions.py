import pygame
import sys


# Function to draw the grid lines
def draw_grid(screen, GRID_SIZE, CELL_SIZE, LINE_COLOR):
    for i in range(1, GRID_SIZE+1):
        pygame.draw.line(screen, LINE_COLOR, (0, i * CELL_SIZE), (CELL_SIZE*3, i * CELL_SIZE))    # 4 horizontal line from (0,y) to (horizontal_dge,y)

    for i in range(1, GRID_SIZE):
        pygame.draw.line(screen, LINE_COLOR, (i * CELL_SIZE, 0), (i * CELL_SIZE, CELL_SIZE*3))  # 3 vertical line from (x,0) to (x,vertical_edge)


# Function to draw the X or O in the cell
def draw_symbol(screen, CELL_SIZE, row, col, symbol):
    font = pygame.font.Font(None,100)                     #select default font,size=100   
    if(symbol=='O'):                                      #for O set blue color
        text = font.render(symbol, True, (0, 0, 255))     #render the symbol using font ,set anti aliasing True , color rgb
    else:                                                 #for X set red color
        text = font.render(symbol, True, (255, 0, 0))     #render the symbol using font ,set anti aliasing True , color rgb

    text_rectangle = text.get_rect(center=(col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2)) # set the text surface at the mid_point of the cell
    screen.blit(text, text_rectangle)   # blit used to draw one image on top of another 


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


def display_win(msg, screen, WIDTH, HEIGHT):
    msg_font = pygame.font.Font(None, 100)

    winner_text = msg_font.render(msg , True, (100, 100, 100))
    screen.blit(winner_text, (WIDTH // 2 - winner_text.get_width() // 2, HEIGHT//2 - winner_text.get_height()))  # Display winner message at the bottom
    pygame.display.flip()

