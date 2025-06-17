# frontend of the program:
from tkinter import messagebox
import tkinter as tk
from backend import gameBoardMatrix, fullValidation, handleMove, undoMove, redoMove, suggestMove, gameBoard
from functools import partial  # to call functions with arguments from buttons
from history import showHistory

# create the main GUI window:
mainWindow = tk.Tk()
mainWindow.title("Final Project - SUDOKU")

# define a special matrix for the editable cells:
editableCells = []


def renderGameBoard(matrix):
    for i in range(9):  # rows
        rowEditable = []
        for j in range(9):  # columns
            value = matrix[i][j]
            entry = tk.Entry(mainWindow, width=2, font=("Comic Sans MS", 18), justify="center")
            entry.grid(row=i, column=j, padx=2, pady=2)

            if value != "-":
                entry.insert(0, value)
                entry.config(state="disabled", disabledforeground="purple")  # pre-filled cells are locked
            else:
                entry.bind("<FocusOut>", lambda e, r=i, c=j: handleMove(e, r, c))

            rowEditable.append(entry)
        editableCells.append(rowEditable)


renderGameBoard(gameBoard)

# Game buttons:
buttonUndo = tk.Button(
    mainWindow, text="↩", command=partial(undoMove, editableCells),
    width=5, height=2, bg="lavender", fg="slateblue", font=("Comic Sans MS", 15, "normal")
)
buttonRedo = tk.Button(
    mainWindow, text="↪", command=partial(redoMove, editableCells),
    width=5, height=2, bg="lavender", fg="slateblue", font=("Comic Sans MS", 15, "normal")
)
buttonSuggest = tk.Button(
    mainWindow, text="💡", command=partial(suggestMove, mainWindow, editableCells),
    width=5, height=2, bg="lavender", fg="slateblue", font=("Comic Sans MS", 15, "normal")
)
buttonHistory = tk.Button(
    mainWindow, text="📖", command=showHistory,
    width=5, height=2, bg="lavender", fg="slateblue", font=("Comic Sans MS", 15, "normal")
)

# Button placement:
buttonUndo.grid(row=10, column=1, columnspan=2, pady=5)
buttonRedo.grid(row=10, column=3, columnspan=2, pady=5)
buttonSuggest.grid(row=10, column=5, columnspan=2, pady=5)
buttonHistory.grid(row=10, column=7, columnspan=2, pady=5)

mainWindow.resizable(False, False)
mainWindow.mainloop()
