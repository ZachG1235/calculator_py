import tkinter
from tkinter import ttk


BUTTON_WIDTH = 100
BUTTON_HEIGHT = 50
GUI_COLUMNS = 4
GUI_ROWS_AFTER_HEADER = 5
LABELS = ["t1", "t2", "C", "/", "7", "8", "9", "*", "4", "5", "6", "-", "1", "2", "3", "+", "0", ".", "t4", "="]

class CalcObj:
    def __init__(self, in_root):
        self.root = in_root
        self.buttons = []
        self.header_label = ttk.Label()
        self.header_text = str(0)
        self.is_reset = True
        self.init_window()
        self.reset_header()
        
    
    def init_window(self):
        self.root.title("Caluclator")
        # self.root.geometry(f"{X_WINDOW_PIXELS}x{Y_WINDOW_PIXELS}")
        self.root.configure(bg="white")
        header_label = ttk.Label(self.root, text=str("N/A"), 
                                                 style="White.TLabel", width=0, 
                                                    font=("Arial", 24, "bold"), 
                                             anchor="center", justify="center")
        header_label.grid(row=0, column=0, columnspan=GUI_COLUMNS, padx=0, pady=0, sticky="nesw")
        self.header_label = header_label
        label_index = 0
        for i in range(GUI_ROWS_AFTER_HEADER):
            row_buttons = []   


            row_label = ttk.Label(self.root, text=str(i), 
                                                 style="White.TLabel", width=0, 
                                                    font=("Arial", 24, "bold"), 
                                             anchor="center", justify="center")
            row_label.grid(row=i+1, column=0, padx=0, pady=0, sticky="nesw")

            for j in range(GUI_COLUMNS):
                canvas = tkinter.Canvas(self.root, width=BUTTON_WIDTH, height=BUTTON_HEIGHT, bg="white", highlightthickness=1)
                canvas.grid(row=i+1, column=j, padx=0, pady=0, sticky="nesw")
                btn_text = str(LABELS[label_index])
                label_index += 1
                canvas.create_text(BUTTON_WIDTH//2, BUTTON_HEIGHT//2, text=btn_text, font=("Arial", 16), fill="black")
                canvas.bind("<Button-1>", lambda event, row_param=i, col_param=j:self.onButtonClick(row_param, col_param))
                new_button = MyButton(data=canvas, row=i, col=j, text=btn_text)
                row_buttons.append(new_button)
            self.buttons.append(row_buttons)
    
    def onButtonClick(self, row_param : int, col_param : int):
        button_text = self.buttons[row_param][col_param].text
        print(button_text)
        if self.is_num(button_text):
            if not (self.is_reset and button_text == "0"):  
                self.append_to_header(button_text)
        else:
            if button_text == "C":
                self.reset_header()
            elif button_text == "=":
                self.set_header_to("idk how to do that yet")
            else:
                self.append_to_header(button_text)
        
    def set_header_to(self, text_to_update : str):
        self.header_text = str(text_to_update)
        self.header_label.config(text=self.header_text)
    
    def append_to_header(self, text_to_append: str):
        if self.is_reset:
            self.set_header_to(text_to_append)
        else:
            self.header_text = self.header_text + text_to_append
            self.header_label.config(text=self.header_text)
        self.is_reset = False
        
    def is_num(self, data_to_check : str) -> bool:
        try:
            float(data_to_check)
            return True
        except ValueError:
            return False
    
    def reset_header(self):
        self.set_header_to("0")
        self.is_reset = True

class MyButton:
    def __init__(self, data, row : int, col : int, text : str):
        self.data = data
        self.row = row
        self.col = col
        self.text = text


def main():
    root_content = tkinter.Tk()
    calc_obj = CalcObj(root_content)
    calc_obj.root.mainloop()

main()