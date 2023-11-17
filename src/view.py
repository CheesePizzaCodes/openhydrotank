from model import CurvesBunch

import tkinter as tk



class GUI(tk.Tk):
    def __init__(self, model: CurvesBunch) -> None:
        super().__init__()
        self.model = model
        