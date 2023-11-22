# Sudoku Solver

## Overview

This is a Sudoku Solver project that uses graph coloring to find a solution for a given Sudoku puzzle. The solver employs a graph-based approach to represent and solve the Sudoku puzzle. All code is in the 'master' branch.

## Features

- **Graph-Based Approach**: The Sudoku puzzle is represented as a graph, and the solver uses graph coloring to find a solution.
- **Graph Connections**: The graph is connected based on the rules of Sudoku, ensuring that each row, column, and block contains unique numbers.
- **GUI Interface**: The project includes a graphical user interface (GUI) built with Tkinter for user interaction.
- **Visualization**: The solution is visualized using Matplotlib, with different colors representing different numbers.

## How to Use

1. Run the `main.py` file.
2. Input the Sudoku puzzle manually or load an example.
3. Click the "Solve" button to find the solution.
4. Optionally, use the "Load Example" button to load a predefined Sudoku puzzle.
5. The solution will be displayed visually, and a message will indicate whether the Sudoku was solved successfully.

## Requirements

- Python 3.x
- Matplotlib
- Tkinter (usually included with Python)

## Usage

```bash
python3 main.py
