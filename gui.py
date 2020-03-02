import tkinter as tk
from enum import Enum
import algorithm as al
import numpy as np
import utils


class ActiveButton(Enum):
    NONE = 0
    START = 1
    GOAL = 2
    OBSTACLE = 3
    CLEAR = 4


class App(tk.Tk):
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("A*")
        self.canvas = tk.Canvas(self.window, width=500, height=500, borderwidth=0, highlightthickness=0)
        self.canvas.pack(side="left", fill="both", expand=1, ipadx=2, ipady=2, padx=20, pady=5)

        self.rows = 100
        self.columns = 100
        self.cellWidth = 25
        self.cellHeight = 25

        self.active = ActiveButton.NONE

        self.rect = np.empty((5, 5))

        for row in range(5):
            for column in range(5):
                x1 = column * self.cellWidth
                y1 = row * self.cellHeight
                x2 = x1 + self.cellWidth
                y2 = y1 + self.cellHeight
                self.rect[row, column] = self.canvas.create_rectangle(x1, y1, x2, y2, fill="white", tags="rect")

        def add_start():
            if utils.start == 0:
                self.active = ActiveButton.START

        def add_goal():
            if utils.goal == 0:
                self.active = ActiveButton.GOAL
                goal_button['bg'] = utils.get_goal_color()


        def add_obstacle():
            self.active = ActiveButton.OBSTACLE

        def clear():
            self.active = ActiveButton.CLEAR

        def new_board(rows, columns):
            self.rect = np.empty((rows, columns))

            cell_width = 500/columns
            cell_height = 500/rows
            for row in range(rows):
                for column in range(columns):
                    x1 = column * cell_width
                    y1 = row * cell_height
                    x2 = x1 + cell_width
                    y2 = y1 + cell_height
                    self.rect[row, column] = self.canvas.create_rectangle(x1, y1, x2, y2, fill="white", tags="rect")

        self.right_panel = tk.Frame(self.window, borderwidth=2)
        self.control_panel = tk.Frame(self.right_panel, borderwidth=2)

        size_panel = tk.Frame(self.control_panel)
        x_panel = tk.Frame(size_panel)
        y_panel = tk.Frame(size_panel)

        tk.Label(x_panel, text="X", borderwidth=2, relief="groove").pack(side="left", fill="x", expand=1)
        x_entry = tk.Entry(x_panel)
        x_entry.pack(side="right", expand=1)

        tk.Label(y_panel, text="Y", borderwidth=2, relief="groove").pack(side="left", fill="x", expand=1)
        y_entry = tk.Entry(y_panel)
        y_entry.pack(side="right", expand=1)

        x_panel.pack(side="top", expand=1)
        y_panel.pack(side="top", expand=1)

        size_panel.pack(side="top", fill="x", expand=1)

        tk.Button(self.control_panel, text="Generar", bg="grey", fg="black",
                  command=lambda: new_board(int(x_entry.get()), int(y_entry.get()))
                  if x_entry.get() and y_entry.get() else None)\
            .pack(side="top")

        self.control_panel.pack(side="top", fill="x", expand=1, pady=20)

        buttons = tk.Frame(self.right_panel)

        tk.Button(buttons, text="Agregar inicio", bg="grey", fg="black", command=add_start)\
            .pack(side="top", fill="x", expand=0)

        goal_button = tk.Button(buttons, text="Agregar meta", bg="green", fg="white", command=add_goal)
        goal_button.pack(side="top", fill="x", expand=0)

        tk.Button(buttons, text="Agregar obstáculo", bg="red", fg="white", command=add_obstacle)\
            .pack(side="top", fill="x", expand=0)

        tk.Button(buttons, text="Limpiar celda", bg="white", fg="black", command=clear)\
            .pack(side="top", fill="x", expand=0)

        buttons.pack(side="left", fill="x", expand=0)
        self.right_panel.pack(side="right", fill="x", expand=1)

        def canvas_click(event):
            x, y = event.x, event.y
            ids = self.canvas.find_overlapping(x, y, x, y)

            if len(ids) == 1:
                if self.active == ActiveButton.OBSTACLE:
                    self.canvas.itemconfig(ids, fill="red", tag="red")

                elif self.active == ActiveButton.START:
                    self.canvas.itemconfig(ids, fill="grey", tag="grey")

                elif self.active == ActiveButton.GOAL:
                    self.canvas.itemconfig(ids, fill="green", tag="green")

                elif self.active == ActiveButton.CLEAR:
                    self.canvas.itemconfig(ids, fill="white", tag="white")

        self.canvas.bind("<Button-1>", canvas_click)

        self.window


if __name__ == "__main__":
    app = App()
    app.window.mainloop()