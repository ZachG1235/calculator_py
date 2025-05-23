import tkinter
from tkinter import ttk


BUTTON_WIDTH = 100
BUTTON_HEIGHT = 50

class CalcObj:
    def __init__(self, in_root):
        self.root = in_root
        self.buttons = []
        self.init_window()
        
    
    def init_window(self):
        self.root.title("Caluclator")
        # self.root.geometry(f"{X_WINDOW_PIXELS}x{Y_WINDOW_PIXELS}")
        self.root.configure(bg="white")
        for i in range(4):
            row_buttons = []

            row_label = ttk.Label(self.root, text=str(i), 
                                                 style="White.TLabel", width=0, 
                                                    font=("Arial", 24, "bold"), 
                                             anchor="center", justify="center")
            row_label.grid(row=i, column=0, padx=0, pady=0, sticky="nesw")

            for j in range(3):
                canvas = tkinter.Canvas(self.root, width=BUTTON_WIDTH, height=BUTTON_HEIGHT, bg="white",highlightthickness=1)
                canvas.grid(row=i, column=j, padx=0, pady=0, sticky="nesw")
                canvas.bind("<Button-1>", lambda event, row_param=i, col_param=j:self.onButtonClick(row_param, col_param))
                new_button = MyButton(data=canvas, row=i, col=j)
                row_buttons.append(new_button)
            self.buttons.append(row_buttons)
    
    def onButtonClick(self, row_param, col_param):
        print(f"{row_param},{col_param}")
    
class MyButton:
    def __init__(self, data, row, col):
        self.data = data
        self.row = row
        self.col = col


def main():
    root_content = tkinter.Tk()
    calc_obj = CalcObj(root_content)
    calc_obj.root.mainloop()

main()