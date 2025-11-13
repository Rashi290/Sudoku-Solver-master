#!/usr/bin/python
# -*- coding: utf-8 -*-

from random import randint, shuffle


def print_board(board):
    """
    Prints the sudoku board.

    Args:
        board (list[list[int]]): A 9x9 sudoku board represented as a list of lists of integers.

    Returns:
        None.
    """

    boardString = ""
    for i in range(9):
        for j in range(9):
            boardString += str(board[i][j]) + " "
            if (j + 1) % 3 == 0 and j != 0 and j + 1 != 9:
                boardString += "| "

            if j == 8:
                boardString += "\n"

            if j == 8 and (i + 1) % 3 == 0 and i + 1 != 9:
                boardString += "- - - - - - - - - - - \n"
    print(boardString)


def find_empty(board):
    """
    Finds an empty cell in the sudoku board.

    Args:
        board (list[list[int]]): A 9x9 sudoku board represented as a list of lists of integers.

    Returns:
        tuple[int, int]|None: The position of the first empty cell found as a tuple of row and column indices, or None if no empty cell is found.
    """

    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return (i, j)
    return None


def valid(board, pos, num):
    """
    Checks whether a number is valid in a cell of the sudoku board.

    Args:
        board (list[list[int]]): A 9x9 sudoku board represented as a list of lists of integers.
        pos (tuple[int, int]): The position of the cell to check as a tuple of row and column indices.
        num (int): The number to check.

    Returns:
        bool: True if the number is valid in the cell, False otherwise.
    """

    for i in range(9):
        if board[i][pos[1]] == num:
            return False

    for j in range(9):
        if board[pos[0]][j] == num:
            return False

    start_i = pos[0] - pos[0] % 3
    start_j = pos[1] - pos[1] % 3
    for i in range(3):
        for j in range(3):
            if board[start_i + i][start_j + j] == num:
                return False
    return True


def solve(board):
    """
    Solves the sudoku board using the backtracking algorithm.

    Args:
        board (list[list[int]]): A 9x9 sudoku board represented as a list of lists of integers.

    Returns:
        bool: True if the sudoku board is solvable, False otherwise.
    """

    empty = find_empty(board)
    if not empty:
        return True

    for nums in range(1, 10):
        if valid(board, empty, nums):
            board[empty[0]][empty[1]] = nums

            if solve(board):  # recursive step
                return True
            board[empty[0]][empty[1]] = 0  # this number is wrong so we set it back to 0
    return False


def count_solutions(board, limit=2):
    """
    Counts the number of solutions for a sudoku board (up to a limit).
    
    Args:
        board (list[list[int]]): A 9x9 sudoku board.
        limit (int): Maximum number of solutions to count.
    
    Returns:
        int: Number of solutions found (up to limit).
    """
    solutions = 0
    
    def count_recursive(board):
        nonlocal solutions
        if solutions >= limit:
            return
        
        empty = find_empty(board)
        if not empty:
            solutions += 1
            return
        
        row, col = empty
        nums = list(range(1, 10))
        shuffle(nums)  # Try numbers in random order
        
        for num in nums:
            if valid(board, (row, col), num):
                board[row][col] = num
                count_recursive(board)
                board[row][col] = 0
                if solutions >= limit:
                    return
    
    count_recursive(board)
    return solutions


def generate_board():
    """
    Generates a random sudoku board with fewer initial numbers, ensuring unique solution.

    Returns:
        list[list[int]]: A 9x9 sudoku board represented as a list of lists of integers.
    """

    board = [[0 for i in range(9)] for j in range(9)]

    # Fill the diagonal boxes
    for i in range(0, 9, 3):
        nums = list(range(1, 10))
        shuffle(nums)
        for row in range(3):
            for col in range(3):
                board[i + row][i + col] = nums.pop()

    # Fill the remaining cells with backtracking
    def fill_cells(board, row, col):
        """
        Fills the remaining cells of the sudoku board with backtracking.

        Args:
            board (list[list[int]]): A 9x9 sudoku board represented as a list of lists of integers.
            row (int): The current row index to fill.
            col (int): The current column index to fill.

        Returns:
            bool: True if the remaining cells are successfully filled, False otherwise.
        """

        if row == 9:
            return True
        if col == 9:
            return fill_cells(board, row + 1, 0)

        if board[row][col] != 0:
            return fill_cells(board, row, col + 1)

        nums = list(range(1, 10))
        shuffle(nums)
        for num in nums:
            if valid(board, (row, col), num):
                board[row][col] = num

                if fill_cells(board, row, col + 1):
                    return True

        board[row][col] = 0
        return False

    fill_cells(board, 0, 0)
    
    # Create a solved board copy
    solved_board = [row[:] for row in board]
    
    # Remove cells while ensuring unique solution
    attempts = 0
    cells_to_remove = randint(40, 50)  # Reasonable difficulty
    removed = 0
    
    # Create list of all cell positions and shuffle
    positions = [(i, j) for i in range(9) for j in range(9)]
    shuffle(positions)
    
    for row, col in positions:
        if removed >= cells_to_remove:
            break
        
        if board[row][col] != 0:
            # Try removing this cell
            original_value = board[row][col]
            board[row][col] = 0
            
            # Check if solution is still unique
            test_board = [row[:] for row in board]
            solution_count = count_solutions(test_board, limit=2)
            
            if solution_count == 1:
                # Unique solution, keep it removed
                removed += 1
            else:
                # Multiple solutions, restore the value
                board[row][col] = original_value
            
            attempts += 1
            if attempts > 200:  # Safety limit
                break

    return board


if __name__ == "__main__":
    board = generate_board()
    print_board(board)
    solve(board)
    print_board(board)
