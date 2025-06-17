from tkinter import Toplevel, Scrollbar, ttk, RIGHT, Y, BOTH
from backend import history
import tkinter as tk


def showHistory():
    historyWindow = tk.Toplevel()
    historyWindow.title("History")
    historyWindow.resizable(False, False)

    # Display the history in a table format for better organization
    tree = ttk.Treeview(historyWindow, columns=("Value", "Row", "Column", "Action"), show="headings", height=10)

    # Define column properties
    tree.column("Value", width=80, anchor="center")
    tree.column("Row", width=80, anchor="center")
    tree.column("Column", width=80, anchor="center")
    tree.column("Action", width=100, anchor="center")

    # Define column headers
    tree.heading("Value", text="Value", anchor=tk.CENTER)
    tree.heading("Row", text="Row", anchor=tk.CENTER)
    tree.heading("Column", text="Column", anchor=tk.CENTER)
    tree.heading("Action", text="Action", anchor=tk.CENTER)

    # Add a vertical scrollbar if the table becomes too long
    scrollbar = Scrollbar(historyWindow, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)

    tree.pack(side="left", fill=BOTH)
    scrollbar.pack(side=RIGHT, fill=Y)

    # Populate the table with historical moves
    for move in history:
        value, row, column, action = move[0], move[1], move[2], move[3:]
        tree.insert("", "end", values=(value, row, column, action))
