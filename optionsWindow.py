import sudokuGUI
import tkinter
from tkinter import *
from tkinter import ttk

class OptionsWindow:
    def __init__(self):
        # Creating main window
        self.win = tkinter.Tk()
        self.win.geometry("400x300")
        self.win.minsize(400, 300)
        self.win.title("Sudoku")

        tkinter.Tk.grid_columnconfigure(self.win, 0, weight=1)

        # variable that controls start/stop flow of the program
        self.start_button_clicked = False

        self.difficulty = IntVar()
        welcomeLabel = ttk.Label(self.win, text="Welcome to Sudoku!\n"
                                           "To begin, select a difficulty and click the Start Game button.")
        welcomeLabel.grid(row=0, column=0, columnspan=2)

        diff1 = ttk.Radiobutton(self.win, text="Easy", value=1, variable=self.difficulty, command=self.buttonEnabler)
        diff2 = ttk.Radiobutton(self.win, text="Normal", value=2, variable=self.difficulty, command=self.buttonEnabler)
        diff3 = ttk.Radiobutton(self.win, text="Hard", value=3, variable=self.difficulty, command=self.buttonEnabler)

        difficulties = [diff1, diff2, diff3]
        for each in range(0, 3):
            difficulties[each].grid(row=each + 1, column=0, sticky="w")

        self.startButton = ttk.Button(self.win, text="Start Game", state="disabled",
                                      command=self.start_button_pressed)

        self.startButton.grid(row=4, column=1, padx=10, pady=(0, 10), sticky="e")

    def buttonEnabler(self):
        if int(self.difficulty.get()) != 0:
            self.startButton.config(state="normal")
            self.start_button_clicked = True  # once all choices are selected, status of button click changed to true

    def start_button_pressed(self, event=None):
        # if the button is clicked, get the value of each option and put it into list
        if self.start_button_clicked:
            difficulty = int(self.difficulty.get())
            if difficulty != 0:
                # TODO: Have sudoku GUI implement difficulty
                self.win.destroy()
                sudokuGUI.start_game()

    def run(self):
        try:
            # Running Window
            self.win.mainloop()
        except UnicodeDecodeError:  # if error occurs, let user exit the app gui. needs to rerun and try again
            error_msg = "\nPlease re-run the program."
            print(error_msg)
            input("Press any key to exit")
            pass
