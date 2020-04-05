import algorithm as al
import gui

if __name__ == "__main__":
    algorithm = al.AStar(al.Board(6, 6))
    app = gui.App(algorithm)

    app.window.mainloop()
