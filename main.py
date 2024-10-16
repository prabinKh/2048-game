# Import necessary modules from tkinter
from tkinter import *
from tkinter import messagebox
import random

# Define the Board class
class Board:
    # Define background colors for different tile values
    bg_color = {
        '2': '#eee4da', '4': '#ede0c8', '8': '#edc850', '16': '#edc53f',
        '32': '#f67c5f', '64': '#f65e3b', '128': '#edcf72', '256': '#edcc61',
        '512': '#f2b179', '1024': '#f59563', '2048': '#edc22e',
    }
    # Define text colors for different tile values
    color = {
        '2': '#776e65', '4': '#f9f6f2', '8': '#f9f6f2', '16': '#f9f6f2',
        '32': '#f9f6f2', '64': '#f9f6f2', '128': '#f9f6f2', '256': '#f9f6f2',
        '512': '#776e65', '1024': '#f9f6f2', '2048': '#f9f6f2',
    }

    # Initialize the Board
    def __init__(self):
        self.n = 4  # Set grid size to 4x4
        self.window = Tk()  # Create main window
        self.window.title('2048 Game')  # Set window title
        self.gameArea = Frame(self.window, bg='azure3')  # Create game area frame
        self.board = []  # Initialize board list
        self.gridCell = [[0]*4 for _ in range(4)]  # Create 4x4 grid of zeros
        self.compress = self.merge = self.moved = False  # Initialize game state flags
        self.score = 0  # Initialize score

        # Create and place labels for each grid cell
        for i in range(4):
            rows = []
            for j in range(4):
                l = Label(self.gameArea, text='', bg='azure4',
                          font=('arial', 22, 'bold'), width=4, height=2)
                l.grid(row=i, column=j, padx=7, pady=7)
                rows.append(l)
            self.board.append(rows)
        self.gameArea.grid()  # Place the game area in the window

    # Reverse the order of elements in each row
    def reverse(self):
        for ind in range(4):
            i, j = 0, 3
            while i < j:
                self.gridCell[ind][i], self.gridCell[ind][j] = self.gridCell[ind][j], self.gridCell[ind][i]
                i += 1
                j -= 1

    # Transpose the grid (swap rows and columns)
    def transpose(self):
        self.gridCell = [list(t) for t in zip(*self.gridCell)]

    # Compress the grid by moving all non-zero elements to one side
    def compressGrid(self):
        self.compress = False
        temp = [[0] * 4 for _ in range(4)]
        for i in range(4):
            cnt = 0
            for j in range(4):
                if self.gridCell[i][j] != 0:
                    temp[i][cnt] = self.gridCell[i][j]
                    if cnt != j:
                        self.compress = True
                    cnt += 1
        self.gridCell = temp

    # Merge adjacent cells with the same value
    def mergeGrid(self):
        self.merge = False
        for i in range(4):
            for j in range(3):
                if self.gridCell[i][j] == self.gridCell[i][j + 1] and self.gridCell[i][j] != 0:
                    self.gridCell[i][j] *= 2
                    self.gridCell[i][j + 1] = 0
                    self.score += self.gridCell[i][j]
                    self.merge = True

    # Add a new '2' tile to a random empty cell
    def random_cell(self):
        cells = [(i, j) for i in range(4) for j in range(4) if self.gridCell[i][j] == 0]
        curr = random.choice(cells)
        self.gridCell[curr[0]][curr[1]] = 2

    # Check if any cells can be merged
    def can_merge(self):
        for i in range(4):
            for j in range(3):
                if self.gridCell[i][j] == self.gridCell[i][j+1]:
                    return True
        for i in range(3):
            for j in range(4):
                if self.gridCell[i+1][j] == self.gridCell[i][j]:
                    return True
        return False

    # Update the visual representation of the grid
    def paintGrid(self):
        for i in range(4):
            for j in range(4):
                if self.gridCell[i][j] == 0:
                    self.board[i][j].config(text='', bg='azure4')
                else:
                    self.board[i][j].config(text=str(self.gridCell[i][j]),
                        bg=self.bg_color.get(str(self.gridCell[i][j])),
                        fg=self.color.get(str(self.gridCell[i][j])))

# Define the Game class
class Game:
    # Initialize the Game
    def __init__(self, gamepanel):
        self.gamepanel = gamepanel
        self.end = self.won = False

    # Start the game
    def start(self):
        self.gamepanel.random_cell()
        self.gamepanel.random_cell()
        self.gamepanel.paintGrid()
        self.gamepanel.window.bind('<Key>', self.link_keys)
        self.gamepanel.window.mainloop()

    # Handle key press events
    def link_keys(self, event):
        if self.end or self.won:
            return
        self.gamepanel.compress = self.gamepanel.merge = self.gamepanel.moved = False
        pressed_key = event.keysym
        if pressed_key == 'Up':
            self.gamepanel.transpose()
            self.gamepanel.compressGrid()
            self.gamepanel.mergeGrid()
            self.gamepanel.moved = self.gamepanel.compress or self.gamepanel.merge
            self.gamepanel.compressGrid()
            self.gamepanel.transpose()
        elif pressed_key == 'Down':
            self.gamepanel.transpose()
            self.gamepanel.reverse()
            self.gamepanel.compressGrid()
            self.gamepanel.mergeGrid()
            self.gamepanel.moved = self.gamepanel.compress or self.gamepanel.merge
            self.gamepanel.compressGrid()
            self.gamepanel.reverse()
            self.gamepanel.transpose()
        elif pressed_key == 'Left':
            self.gamepanel.compressGrid()
            self.gamepanel.mergeGrid()
            self.gamepanel.moved = self.gamepanel.compress or self.gamepanel.merge
            self.gamepanel.compressGrid()
        elif pressed_key == 'Right':
            self.gamepanel.reverse()
            self.gamepanel.compressGrid()
            self.gamepanel.mergeGrid()
            self.gamepanel.moved = self.gamepanel.compress or self.gamepanel.merge
            self.gamepanel.compressGrid()
            self.gamepanel.reverse()
        else:
            return
        self.gamepanel.paintGrid()
        print(self.gamepanel.score)
        if any(2048 in row for row in self.gamepanel.gridCell):
            self.won = True
            messagebox.showinfo('2048', 'You Won!')
            print("won")
            return
        if not any(0 in row for row in self.gamepanel.gridCell) and not self.gamepanel.can_merge():
            self.end = True
            messagebox.showinfo('2048', 'Game Over!')
            print("Over")
        if self.gamepanel.moved:
            self.gamepanel.random_cell()
        self.gamepanel.paintGrid()

# Create game board and start the game
gamepanel = Board()
game2048 = Game(gamepanel)
game2048.start()