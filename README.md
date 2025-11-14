# 🎮 Sudoku Solver

A modern, interactive Sudoku game and solver built with Python and Pygame. Features a beautiful GUI with real-time validation, visual solving animation, and more!

## ✨ Features

- 🎯 **Random Puzzle Generation**: Automatically generates unique, solvable Sudoku puzzles
- 🎨 **Modern GUI**: Beautiful, vibrant interface with smooth animations
- ⚡ **Visual Solver**: Watch the backtracking algorithm solve puzzles step-by-step
- 💡 **Hint System**: Get hints when you're stuck
- ✅ **Real-time Validation**: Instant feedback on correct/incorrect moves
- ⏱️ **Timer**: Track your solving time
- 📊 **Score Tracking**: Monitor correct moves, wrong moves, and empty cells
- 🔄 **New Puzzle**: Generate a fresh puzzle anytime
- 🎯 **Submit Solution**: Check if your solution is correct

## 📋 Requirements

- Python 3.6 or higher
- Pygame 2.0.1

## 🚀 Installation

1. Clone or download this repository
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

Or install Pygame directly:

```bash
pip install pygame==2.0.1
```

## 🎮 How to Run

Simply run the main Python file:

```bash
python SudokuGUI.py
```

## 🎯 How to Play

1. **Select a Cell**: Click on any empty cell to select it
2. **Enter Numbers**: Type numbers 1-9 to fill the selected cell
3. **Delete Numbers**: Press `DELETE` or `BACKSPACE` to clear a cell
4. **Get Hints**: Click the "💡 Show Answer" button to reveal all solutions
5. **Submit**: Click "✓ Submit" to check if your solution is correct
6. **New Puzzle**: Click "🔄 New Puzzle" to generate a fresh puzzle

## 🎨 Controls

- **Mouse Click**: Select a cell
- **Number Keys (1-9)**: Enter numbers in selected cell
- **DELETE/BACKSPACE**: Clear selected cell
- **Arrow Keys**: Navigate between cells

## 🏗️ Project Structure

```
Sudoku-Solver/
│
├── SudokuGUI.py      # Main GUI application
├── sudokutools.py    # Core Sudoku solving algorithms
├── requirements.txt  # Python dependencies
└── README.md         # This file
```

## 🔧 Technical Details

### Algorithms Used

- **Backtracking Algorithm**: Used for solving Sudoku puzzles
- **Constraint Satisfaction**: Validates numbers based on Sudoku rules (row, column, 3x3 box)

### Key Functions

- `generate_board()`: Creates a random, solvable Sudoku puzzle with unique solution
- `solve(board)`: Solves the puzzle using backtracking
- `valid(board, pos, num)`: Checks if a number is valid at a given position
- `find_empty(board)`: Finds the next empty cell to fill

## 🎨 Color Scheme

The application uses a modern, vibrant color palette:
- Background: Light gray-blue
- Board: White with subtle shadows
- Correct moves: Green highlights
- Incorrect moves: Red highlights
- Selected cell: Blue highlight
- Buttons: Purple/indigo with hover effects

## 📝 License

This project is open source and available for educational purposes.

## 🤝 Contributing

Feel free to fork this project and submit pull requests for any improvements!

## 📧 Support

If you encounter any issues or have suggestions, please open an issue on the repository.

---

**Enjoy solving Sudoku puzzles! 🎉**


