from sudoku_connections import SudokuConnections
import tkinter as tk
from tkinter import messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

class SudokuGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Solver")
        self.board = [[tk.StringVar() for _ in range(9)] for _ in range(9)]  
        self.create_widgets()

    def create_widgets(self):
        self.canvas = tk.Canvas(self.root, width=360, height=360)
        self.canvas.pack()

        self.solve_button = tk.Button(self.root, text="Solve", command=self.solve_sudoku)
        self.solve_button.pack()

        self.draw_board()

    def draw_board(self):
        for i in range(9):
            for j in range(9):
                x0 = j * 40
                y0 = i * 40
                x1 = x0 + 40
                y1 = y0 + 40
                self.canvas.create_rectangle(x0, y0, x1, y1, outline="black")

                entry = tk.Entry(self.root, textvariable=self.board[i][j], font=('Arial', 16), justify='center')
                entry.place(x=x0 + 10, y=y0 + 10, width=20, height=20)

    def solve_sudoku(self):
        board = [[int(entry.get()) if entry.get() else 0 for entry in row] for row in self.board]

        s = SudokuBoard(board)
        solved = s.solveGraphColoring()

        if solved:
            self.board = [[tk.StringVar(value=str(s.board[i][j])) for j in range(9)] for i in range(9)]
            self.canvas.delete("all")
            self.draw_board()

            self.plot_sudoku_solution(s.board)

            messagebox.showinfo("Sudoku Solved", "Sudoku has been solved successfully!")
        else:
            messagebox.showerror("Sudoku Solver", "Could not solve Sudoku!")

    def plot_sudoku_solution(self, solution):
        unique_numbers = np.unique(solution)
        cmap = plt.cm.get_cmap("tab10", len(unique_numbers))  # Choose a different colormap if desired
        custom_cmap = ListedColormap(cmap.colors)

        fig, ax = plt.subplots()
        im = ax.matshow(np.array(solution), cmap=custom_cmap)

        # Add grid lines
        for i in range(1, 9):
            ax.axhline(i - 0.5, color="black", linewidth=2)
            ax.axvline(i - 0.5, color="black", linewidth=2)

        # Display legend or colorbar
        cbar = plt.colorbar(im, ticks=unique_numbers)
        cbar.set_label("Number")

        plt.show()

class SudokuBoard:
    def __init__(self, board):
        self.board = board
        self.sudokuGraph = SudokuConnections()
        self.mappedGrid = self.__get_mapped_matrix()

    def __get_mapped_matrix(self):
        matrix = [[0 for _ in range(9)] for _ in range(9)]

        count = 1
        for rows in range(9):
            for cols in range(9):
                matrix[rows][cols] = count
                count += 1
        return matrix

    def print_board(self):
        print("    1 2 3     4 5 6     7 8 9")
        for i in range(len(self.board)):
            if i % 3 == 0:
                print("  - - - - - - - - - - - - - - ")

            for j in range(len(self.board[i])):
                if j % 3 == 0:
                    print(" |  ", end="")
                if j == 8:
                    print(self.board[i][j], " | ", i + 1)
                else:
                    print(f"{self.board[i][j]} ", end="")
        print("  - - - - - - - - - - - - - - ")

    def is_blank(self):
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                if self.board[row][col] == 0:
                    return (row, col)
        return None

    def is_valid(self, num, pos):
        for col in range(len(self.board[0])):
            if self.board[pos[0]][col] == num and pos[0] != col:
                return False

        for row in range(len(self.board)):
            if self.board[row][pos[1]] == num and pos[1] != row:
                return False

        x = pos[1] // 3
        y = pos[0] // 3

        for row in range(y * 3, y * 3 + 3):
            for col in range(x * 3, x * 3 + 3):
                if self.board[row][col] == num and (row, col) != pos:
                    return False

        return True

    def solve_it_naive(self):
        find_blank = self.is_blank()

        if find_blank is None:
            return True
        else:
            row, col = find_blank
        for i in range(1, 10):
            if self.is_valid(i, (row, col)):
                self.board[row][col] = i

                if self.solve_it_naive():
                    return True
                self.board[row][col] = 0
        return False

    def graph_coloring_initialize_color(self):
        color = [0] * (self.sudokuGraph.graph.totalV + 1)
        given = []
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                if self.board[row][col] != 0:
                    idx = self.mappedGrid[row][col]
                    color[idx] = self.board[row][col]
                    given.append(idx)
        return color, given

    def solveGraphColoring(self, m=9):
        color, given = self.graph_coloring_initialize_color()
        if self.__graph_color_utility(m=m, color=color, v=1, given=given) is None:
            print(":(")
            return False
        count = 1
        for row in range(9):
            for col in range(9):
                self.board[row][col] = color[count]
                count += 1
        return color

    def __graph_color_utility(self, m, color, v, given):
        if v == self.sudokuGraph.graph.totalV + 1:
            return True
        for c in range(1, m + 1):
            if self.__is_safe_to_color(v, color, c, given) == True:
                color[v] = c
                if self.__graph_color_utility(m, color, v + 1, given):
                    return True
            if v not in given:
                color[v] = 0

    def __is_safe_to_color(self, v, color, c, given):
        if v in given and color[v] == c:
            return True
        elif v in given:
            return False

        for i in range(1, self.sudokuGraph.graph.totalV + 1):
            if color[i] == c and self.sudokuGraph.graph.isNeighbour(v, i):
                return False
        return True

def test():
    board = []
    print("Enter the Sudoku board (9x9):")
    for _ in range(9):
        row = list(map(int, input().split()))
        board.append(row)

    s = SudokuBoard(board)
    print("\nBEFORE SOLVING ...")
    print("\n\n")
    s.print_board()
    print("\nSolving ...")
    print("\n\n\nAFTER SOLVING ...")
    print("\n\n")
    s.solveGraphColoring(m=9)
    s.print_board()

def test_gui():
    root = tk.Tk()
    app = SudokuGUI(root)
    root.mainloop()

if __name__ == "__main__":
    test_gui()
    test()
