import tkinter as tk
from enum import Enum
import algorithm as al


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
        self.canvas.pack(side="left", fill="both", expand="true")
        self.rows = 100
        self.columns = 100
        self.cellWidth = 25
        self.cellHeight = 25

        self.active = ActiveButton.NONE

        self.rect = {}
        for column in range(20):
            for row in range(20):
                x1 = column * self.cellWidth
                y1 = row * self.cellHeight
                x2 = x1 + self.cellWidth
                y2 = y1 + self.cellHeight
                self.rect[row, column] = self.canvas.create_rectangle(x1, y1, x2, y2, fill="white", tags="rect")

        def add_start():
            self.active = ActiveButton.START

        def add_goal():
            self.active = ActiveButton.GOAL

        def add_obstacle():
            self.active = ActiveButton.OBSTACLE

        def clear():
            self.active = ActiveButton.CLEAR

        self.rightpanel = tk.Frame(self.window)

        self.btn = tk.Button(self.rightpanel, text="Agregar inicio", bg="grey", fg="black", command=add_start)
        self.btn.pack(side="top", fill="x", expand="false")

        self.btn = tk.Button(self.rightpanel, text="Agregar meta", bg="green", fg="white", command=add_goal)
        self.btn.pack(side="top", fill="x", expand="false")

        self.btn = tk.Button(self.rightpanel, text="Agregar obstáculo", bg="red", fg="white", command=add_obstacle)
        self.btn.pack(side="top", fill="x", expand="false")

        self.btn = tk.Button(self.rightpanel, text="Limpiar celda", bg="white", fg="black", command=clear)
        self.btn.pack(side="top", fill="x", expand="false")

        self.rightpanel.pack(side="right")

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

        '''self.redraw(1000)'''

    def redraw(self, delay):
        self.after(delay, lambda: self.redraw(delay))


if __name__ == "__main__":
    app = App()
    app.window.mainloop()
