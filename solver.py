import random

def is_valid(board, row, col, num):
  # This function checks the constraints of Sudoku

  # Check if 'num' is not in the current row and column
  for i in range(9):
      if board[row][i] == num or board[i][col] == num:
          return False

  # Check if 'num' is not in the current 3x3 box
  start_row, start_col = 3 * (row // 3), 3 * (col // 3)
  for i in range(3):
      for j in range(3):
          if board[i + start_row][j + start_col] == num:
              return False

  return True

def solve_sudoku(board):
  # This function primarily implements backtracking

  empty_cell = find_empty_cell(board)
  if not empty_cell:
      return True  # Puzzle solved
  row, col = empty_cell

  for num in range(1, 10):  # Sudoku numbers: 1 to 9
      if is_valid(board, row, col, num):  # Check constraints before placing a number
          board[row][col] = num
          if solve_sudoku(board):  # Recursive backtracking step
              return True  # Continue with this choice
          board[row][col] = 0  # Reset cell and backtrack

  return False  # Trigger backtracking

def find_empty_cell(board):
  # This function finds the next empty cell to be filled
  for i in range(9):
      for j in range(9):
          if board[i][j] == 0:
              return (i, j)  # Return row, col tuple for the empty cell
  return None

def generate_sudoku(num_clues=20):
    # Start with an empty board
    board = [[0 for _ in range(9)] for _ in range(9)]

    # Fill the board completely
    solve_sudoku(board)

    # Remove numbers to create the puzzle
    attempts = 81 - num_clues
    while attempts > 0:
        row = random.randint(0, 8)
        col = random.randint(0, 8)

        while board[row][col] == 0:
            row = random.randint(0, 8)
            col = random.randint(0, 8)

        backup = board[row][col]
        board[row][col] = 0

        # Make a copy of the board to test it
        board_copy = [row.copy() for row in board]

        # Count the number of solutions
        counter = [0]
        count_solutions(board_copy, counter)

        if counter[0] != 1:
            board[row][col] = backup
            attempts -= 1

    return board

def count_solutions(board, counter):
    if counter[0] > 1:
        return  # Already found multiple solutions, no need to continue

    empty_cell = find_empty_cell(board)
    if not empty_cell:
        counter[0] += 1
        return
    row, col = empty_cell

    for num in range(1, 10):
        if is_valid(board, row, col, num):
            board[row][col] = num
            count_solutions(board, counter)
            board[row][col] = 0

# Generate a random Sudoku puzzle
sudoku_puzzle = generate_sudoku()
for row in sudoku_puzzle:
    print(row)
