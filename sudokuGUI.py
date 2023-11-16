import pygame
import sys
from solver import is_valid, find_empty_cell, solve_sudoku, generate_sudoku

# Moved pygame initialization to start_game() so pygame doesn't open automatically
# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHTGRAY = (200, 200, 200)
RED = (255, 0, 0)
GREEN = (34,139,34)
LIGHTRED = (255, 182, 193)
LIGHTBLUE = (173, 216, 230)

# Screen dimensions
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600

def draw_grid(screen, puzzle, playable_field):
    # Draw minor lines
    for x in range(0, SCREEN_WIDTH, SCREEN_WIDTH // 9):  # Vertical lines
        pygame.draw.line(screen, LIGHTGRAY, (x, 0), (x, SCREEN_HEIGHT))
    for y in range(0, SCREEN_HEIGHT, SCREEN_HEIGHT // 9):  # Horizontal lines
        pygame.draw.line(screen, LIGHTGRAY, (0, y), (SCREEN_WIDTH, y))

    # Draw major lines
    for x in range(0, SCREEN_WIDTH, SCREEN_WIDTH // 3):  # Vertical lines
        pygame.draw.line(screen, BLACK, (x, 0), (x, SCREEN_HEIGHT))
    for y in range(0, SCREEN_HEIGHT, SCREEN_HEIGHT // 3):  # Horizontal lines
        pygame.draw.line(screen, BLACK, (0, y), (SCREEN_WIDTH, y))

    # Highlight the selected cell with a light blue background
    if selected_cell:
        x, y = selected_cell[1] * (SCREEN_WIDTH // 9), selected_cell[0] * (SCREEN_HEIGHT // 9)
        pygame.draw.rect(screen, LIGHTBLUE, (x, y, SCREEN_WIDTH // 9, SCREEN_HEIGHT // 9))

    # Draw the numbers from the sudoku_puzzle
    font = pygame.font.Font(None, 36)
    for i in range(9):
        for j in range(9):
            if puzzle[i][j] > 0:
                # TODO: Add logic for detecting incorrect inputs here
                if playable_field[i][j]:  # Differentiating between user input and computer-generated puzzle
                    text = font.render(str(puzzle[i][j]), True, GREEN)
                else:
                    text = font.render(str(puzzle[i][j]), True, BLACK)
                screen.blit(text, (j * (SCREEN_WIDTH // 9) + 15, i * (SCREEN_HEIGHT // 9) + 15))



def get_clicked_pos(pos, playable_field):
    x, y = pos
    row = y // (SCREEN_HEIGHT // 9)
    col = x // (SCREEN_WIDTH // 9)
    print(f"Calculated cell: (row={row}, col={col})")   #debugging print statement
    if playable_field[row][col]:
        return row, col
    else:
        print("You cannot select this cell.")  #debugging print statement
        return None


selected_cell = None

def get_playable_field(board):
    playable_field = [[True if board[i][j] == 0 else False for j in range(9)] for i in range(9)]
    return playable_field


def start_game():
    # Initialize pygame
    ico = pygame.image.load("sudokuIcon.ico")
    pygame.display.set_icon(ico)
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Sudoku')

    # Generate a random Sudoku puzzle for the player
    sudoku_puzzle = generate_sudoku()
    playable_field = get_playable_field(sudoku_puzzle)

    global selected_cell
    print("Starting game loop...")
    while True:
        screen.fill(WHITE)  # Fill the screen with a white background to start off
        draw_grid(screen, sudoku_puzzle, playable_field)  #  Drawing the sudoku grid on top of the white background
        # pygame.draw.rect(screen, RED, (50, 50, 100, 100)) # what is this red box for? - howard

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:  # Click
                pos = pygame.mouse.get_pos()
                print(f"Mouse clicked at position: {pos}")  #debugging print statement
                selected_cell = get_clicked_pos(pos, playable_field)    #debugging print statement
                print(f"Selected cell: {selected_cell}")
            if event.type == pygame.KEYDOWN:  # Number key is pressed
                if event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7,
                                 pygame.K_8, pygame.K_9]:
                    if selected_cell:
                        row, col = selected_cell
                        num = event.key - pygame.K_0
                        if is_valid(sudoku_puzzle, row, col, num):  # Assuming sudoku_puzzle is your board
                            sudoku_puzzle[row][col] = num
                        else:
                            sudoku_puzzle[row][col] = -1
                            pygame.time.wait(500)
                            sudoku_puzzle[row][col] = 0
                            pass
        pygame.display.flip()  # Displays board after taking all events into consideration
