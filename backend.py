# backend of the program:
from tkinter import messagebox, filedialog
import tkinter as tk
from suggestion import showSuggestion

# list with game history:
history = []

# function to read the file and create a 9x9 matrix:
def gameBoardMatrix():
    matrix = []
    filePath = filedialog.askopenfilename(
        title="Select a configuration file",
        filetypes=[("Text files", "*.txt")]
    )

    if not filePath:
        messagebox.showerror("Error", "No file was selected.")
        exit()

    with open(filePath, "r") as file:
        for line in file:  # rows
            row = []
            for value in line.strip():  # columns
                if value.isdigit() or value == "-":
                    row.append(value)
            matrix.append(row)

    return matrix  # return the 9x9 matrix


# load the 9x9 game board:
gameBoard = gameBoardMatrix()

# to manage the board updated by moves, we use a copy:
currentBoard = [row.copy() for row in gameBoard]

# validate that input is a number from 1 to 9:
def validateValue(v):
    v = str(v)
    return v == "" or (v.isdigit() and 1 <= int(v) <= 9)

# validate a move:
def validateMove(r, c, v):
    if v == "":
        return True
    for i in range(9):  # check row
        if currentBoard[r][i] == v:
            return False
    for i in range(9):  # check column
        if currentBoard[i][c] == v:
            return False
    regionRow = (r // 3) * 3
    regionCol = (c // 3) * 3
    for i in range(3):
        for j in range(3):
            currentR = regionRow + i
            currentC = regionCol + j
            if (currentR != r or currentC != c) and (currentBoard[currentR][currentC] == v):
                return False
    return True

# combine value and move validation:
def fullValidation(r, c, v):
    return validateValue(v) and validateMove(r, c, v)

# add a valid move to history
def pushHistory(value, row, col, action):
    move = f"{value}{row}{col}{action}"
    history.append(move)

# undo last move
def undoMove(editableCells):
    if not history:
        messagebox.showerror("Error", "There are no previous moves!")
        return

    lastMove = history[-1]
    val, r, c = lastMove[0], int(lastMove[1]), int(lastMove[2])

    if lastMove[3:] == "undo":
        messagebox.showerror("Error", "Cannot undo a move that was already undone!")
        return

    if len(history) >= 2:
        prevMove = history[-2]
        if int(prevMove[1]) == r and int(prevMove[2]) == c:
            val = prevMove[0]
        else:
            val = ' '
    else:
        val = ' '
    newMove = f"{val}{r}{c}undo"
    history.append(newMove)
    editableCells[r][c].delete(0, tk.END)
    editableCells[r][c].insert(0, val)

# redo last undone move
def redoMove(editableCells):
    if not history:
        messagebox.showerror("Error", "There are no previous moves!")
        return

    lastMove = history[-1]
    val, r, c = lastMove[0], int(lastMove[1]), int(lastMove[2])

    if lastMove[3:] != "undo":
        messagebox.showerror("Error", "Last move was not an undo!")
        return

    prevMove = history[-2]
    if int(prevMove[1]) == r and int(prevMove[2]) == c:
        val = prevMove[0]
    else:
        val = ' '

    newMove = f"{val}{r}{c}redo"
    history.append(newMove)

    currentBoard[r][c] = val
    editableCells[r][c].delete(0, tk.END)
    editableCells[r][c].insert(0, val)

# check if Sudoku is complete
def isSudokuComplete():
    for row in currentBoard:
        if "-" in row or "" in row:
            return False

    for row in currentBoard:
        if sorted(row) != [str(i) for i in range(1, 10)]:
            return False

    for c in range(9):
        column = [currentBoard[r][c] for r in range(9)]
        if sorted(column) != [str(i) for i in range(1, 10)]:
            return False

    for regionR in range(0, 9, 3):
        for regionC in range(0, 9, 3):
            region = []
            for i in range(3):
                for j in range(3):
                    region.append(currentBoard[regionR + i][regionC + j])
            if sorted(region) != [str(i) for i in range(1, 10)]:
                return False

    return True

# handle user input on a cell
def handleMove(event, r, c):
    entry = event.widget
    value = entry.get()
    if value == "":
        return
    if currentBoard[r][c] == value:
        return
    if not fullValidation(r, c, value):
        messagebox.showerror("Error", "Invalid move!")
        entry.delete(0, tk.END)
    else:
        currentBoard[r][c] = value
        pushHistory(value, r, c, "new")
    if isSudokuComplete():
        messagebox.showinfo("Congratulations!", "You completed the Sudoku! You're amazing (•̀ ω •́ )✧")

# check if a value was previously deleted
def wasValueDeletedBefore(v, r, c):
    reversedHistory = list(reversed(history))
    if not history:
        return False
    for i in range(len(reversedHistory) - 1):
        move = reversedHistory[i]
        prevMove = reversedHistory[i + 1]
        row, col, action = move[1], move[2], move[3:]
        prevValue = prevMove[0]
        if row == r and col == c:
            if action == "undo" and prevValue == v:
                return True
    return False

# suggest a valid move for the currently selected cell
def suggestMove(mainWindow, editableCells):
    activeCell = mainWindow.focus_get()
    r, c = -1, -1
    for i in range(9):
        for j in range(9):
            if editableCells[i][j] == activeCell:
                r = i
                c = j
    if r == -1 and c == -1:
        messagebox.showerror("Error", "Please select a cell to get a suggestion!")
        return

    for i in range(1, 10):
        value = str(i)
        if fullValidation(r, c, value) and not wasValueDeletedBefore(value, str(r), str(c)):
            showSuggestion(i, r, c, mainWindow, editableCells)
            return

    messagebox.showerror("Error", "There are no valid suggestions for this cell.")
