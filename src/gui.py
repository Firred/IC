import tkinter as tk
from enum import Enum
import algorithm as al, utils
import numpy as np


class ActiveButton(Enum):
    none = 0
    start_button = 1
    goal_button = 2
    obstacle_button = 3
    clear_button = 4


class App(tk.Tk):
    def __init__(self, a_star):
        self.window = tk.Tk()
        self.window.title("A*")
        self.canvas = tk.Canvas(self.window, width=1000, height=800, borderwidth=0, highlightthickness=0)
        self.canvas.pack(side="left", fill="both", expand=1, ipadx=2, ipady=2, padx=20, pady=5)

        self.cellWidth = 25
        self.cellHeight = 25

        self.active = ActiveButton.none

        self.board = a_star.get_board()

        def canvas_click(event):
            x, y = event.x, event.y
            ids = self.canvas.find_overlapping(x, y, x, y)

            if len(ids) == 1:
                pos = ids[0]-1
                shape = np.shape(self.rect)
                row = int(pos/shape[1])
                col = pos % shape[1]

                if self.active == ActiveButton.obstacle_button:
                    self.canvas.itemconfig(ids, fill="red", tags="red")
                    a_star.add_obstacle(row, col)
                elif self.active == ActiveButton.start_button:
                    self.canvas.itemconfig(ids, fill="grey", tags="grey")
                    result = a_star.add_start(row, col)

                    if result is not None:
                        self.canvas.itemconfig(result[0]*shape[1]+result[1]+1, fill="white", tags="white")
                elif self.active == ActiveButton.goal_button:
                    self.canvas.itemconfig(ids, fill="green", tags="green")
                    result = a_star.add_goal(row, col)

                    if result is not None:
                        self.canvas.itemconfig(result[0]*shape[1]+result[1]+1, fill="white", tags="white")
                elif self.active == ActiveButton.clear_button:
                    self.canvas.itemconfig(ids, fill="white", tags="white")
                    a_star.clear_cell(row, col)

        def canvas_held(event):
            x, y = event.x, event.y
            ids = self.canvas.find_overlapping(x, y, x, y)

            if len(ids) == 1:
                pos = ids[0]-1
                shape = np.shape(self.rect)
                row = int(pos/shape[1])
                col = pos % shape[1]

                if self.active == ActiveButton.obstacle_button:
                    self.canvas.itemconfig(ids, fill="red", tags="red")
                    a_star.add_obstacle(row, col)
                elif self.active == ActiveButton.clear_button:
                    self.canvas.itemconfig(ids, fill="white", tags="white")
                    a_star.clear_cell(row, col)

        def execute():
            reset()

            result = a_star.exec()

            if result == -1:
                self.message['text'] = "Es necesario introducir un \n punto de inicio y otro de meta."
            elif result[0] is None:
                self.message['text'] = "No se pudo encontrar un camino \n desde el origen al destino."
            else:
                self.message['text'] = display_result(result[0], result[1], result[2])
                self.message['fg'] = "green"

        def new_board(rows, columns):
            self.board = al.Board(rows, columns)
            a_star.set_board(self.board)

            if rows > 0 and columns > 0:
                if rows <= 100 and columns <= 100:
                    size = self.canvas.winfo_screenwidth(), self.canvas.winfo_screenheight()
                    self.canvas.destroy()
                    self.canvas = tk.Canvas(self.window, width=size[0], height=size[1], borderwidth=0,
                                            highlightthickness=0)
                    self.rect = np.empty((rows, columns))

                    cell_size = (size[0]-300)/columns if (size[0]-300)/columns < (size[1]-100)/rows else (size[1]-100)/rows

                    for row in range(rows):
                        for column in range(columns):
                            x1 = column * cell_size
                            y1 = row * cell_size
                            x2 = x1 + cell_size
                            y2 = y1 + cell_size
                            self.rect[row, column] = self.canvas.create_rectangle(x1, y1, x2, y2,
                                                                                  fill="white", tags="rect")

                    self.canvas.pack(side="left", fill="both", expand=1, ipadx=2, ipady=2, padx=20, pady=5)
                    self.canvas.bind("<Button-1>", canvas_click)
                    self.canvas.bind("<B1-Motion>", canvas_held)

                else:
                    return -1

        self.right_panel = tk.Frame(self.window, borderwidth=2)
        self.control_panel = tk.Frame(self.right_panel, borderwidth=2)

        size_panel = tk.Frame(self.control_panel)
        x_panel = tk.Frame(size_panel)
        y_panel = tk.Frame(size_panel)

        tk.Label(x_panel, text="Filas", borderwidth=2, relief="groove").pack(side="left", fill="x", expand=1)
        x_entry = tk.Entry(x_panel)
        x_entry.pack(side="right", expand=1)

        tk.Label(y_panel, text="Columnas", borderwidth=2, relief="groove").pack(side="left", fill="x", expand=1)
        y_entry = tk.Entry(y_panel)
        y_entry.pack(side="right", expand=1)

        x_panel.pack(side="top", expand=1)
        y_panel.pack(side="top", expand=1)

        size_panel.pack(side="top", fill="x", expand=1)

        tk.Button(self.control_panel, text="Generar", bg="grey", fg="black",
                  command=lambda: (self.message.config(text="El valor de fila y columna \n debe de ser inferior a 100")
                    if new_board(int(x_entry.get()), int(y_entry.get())) == -1 else None)
                  if utils.is_int(x_entry.get()) and utils.is_int(x_entry.get()) else
                  self.message.config(text="El valor de fila y columna \n debe de ser un número"))\
            .pack(side="top")

        self.control_panel.pack(side="top", fill="x", expand=1, pady=20)

        buttons = tk.Frame(self.right_panel)

        start_button = tk.Button(buttons, text="Agregar inicio", bg="grey", fg="black", borderwidth=2,
                                 command=lambda: set_button(start_button))
        start_button.name = 'start_button'
        start_button.pack(side="top", fill="x", expand=0)
        button_list = [start_button]

        goal_button = tk.Button(buttons, text="Agregar meta", bg="green", fg="white", borderwidth=2,
                                command=lambda: set_button(goal_button))
        goal_button.name = 'goal_button'
        goal_button.pack(side="top", fill="x", expand=0)
        button_list.append(goal_button)

        obstacle_button = tk.Button(buttons, text="Agregar obstáculo", bg="red", fg="white", borderwidth=2,
                                    command=lambda: set_button(obstacle_button))
        obstacle_button.name = 'obstacle_button'
        obstacle_button.pack(side="top", fill="x", expand=0)
        button_list.append(obstacle_button)

        clear_button = tk.Button(buttons, text="Limpiar celda", bg="white", fg="black", borderwidth=2,
                                 command=lambda: set_button(clear_button))
        clear_button.name = 'clear_button'
        clear_button.pack(side="top", fill="x", expand=0)
        button_list.append(clear_button)

        exec_button = tk.Button(buttons, text="Ejecutar", bg="white", fg="black", command=execute)
        exec_button.pack(side="top", fill="x", expand=0)

        buttons.pack(side="left", fill="x", expand=0)

        message_panel = tk.Frame(self.control_panel)
        self.message = tk.Label(message_panel, fg="red")\

        self.message.pack(side="bottom", fill="x", expand=1)
        message_panel.pack(side="bottom", fill="x", expand=1)
        self.right_panel.pack(side="right")

        b_rows, b_columns = self.board.get_size()
        new_board(b_rows, b_columns)

        self.window

        def reset():
            self.message['text'] = ''
            self.message['fg'] = 'red'

            self.canvas.itemconfig("path", fill="white", tags="white")

        def display_result(result, goal, start, dflt_jump=4):
            string = ''
            jump = dflt_jump
            shape = np.shape(self.rect)

            while not result.empty():
                pos = tuple(result.get())

                if pos != start and pos != goal:
                    self.canvas.itemconfig(pos[0] * shape[1] + pos[1] + 1, fill="dark blue", tags="path")

                string += str(pos) + " -> "

                jump -= 1

                if jump == 0:
                    string += '\n'
                    jump = dflt_jump

            if jump == dflt_jump:
                return string[:-5]
            else:
                return string[:-4]

        def set_button(button):
            for b in button_list:
                colors = utils.get_color(b.name, False)
                b['bg'] = colors[0]
                b['fg'] = colors[1]
                b['borderwidth'] = colors[2]
                b['relief'] = colors[3]

            self.active = ActiveButton[button.name]
            colors = utils.get_color(button.name, True)
            button['bg'] = colors[0]
            button['fg'] = colors[1]
            button['borderwidth'] = colors[2]
            button['relief'] = colors[3]
