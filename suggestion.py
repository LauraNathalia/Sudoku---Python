import tkinter as tk

def showSuggestion(value, row, col, mainWindow, editableCells):
    suggestionWindow = tk.Toplevel(mainWindow)
    suggestionWindow.overrideredirect(True)  # remove borders and title bar
    suggestionWindow.config(bg="lavender", relief="solid", bd=1)

    # position the window right next to the selected cell
    x = editableCells[row][col].winfo_rootx() + editableCells[row][col].winfo_width() + 10
    y = editableCells[row][col].winfo_rooty()
    suggestionWindow.geometry(f"+{x}+{y}")

    # show the suggested value
    label = tk.Label(suggestionWindow, text=f"{value}", bg="lavender", fg="slateblue", font=("Comic Sans MS", 12), padx=10, pady=5)
    label.pack()
    
    # close the suggestion popup when clicking outside to avoid issues
    def closeSuggestion(event):
        clickedWidget = event.widget.winfo_containing(event.x_root, event.y_root)
        if clickedWidget is None or not str(clickedWidget).startswith(str(suggestionWindow)):
            suggestionWindow.destroy()
            mainWindow.unbind_all("<Button-1>")

    # detect outside click
    mainWindow.after_idle(lambda: mainWindow.bind_all("<Button-1>", closeSuggestion))
