import tkinter as tk
from main_gui import CaroApp


def main():
    root = tk.Tk()
    app = CaroApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
