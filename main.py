import tkinter
from tkinter import ttk

# GLOBAL VARIABLES
    # GUI proportion modification
BUTTON_WIDTH = 100
BUTTON_HEIGHT = 50

# Modifying these cause GUI to not work
GUI_COLUMNS = 4 
GUI_ROWS_AFTER_HEADER = 5

# Postionally modifyable globals
OPERATION_TYPES = ["/", "*", "-", "+"]
LABELS = ["C", " ", " ", OPERATION_TYPES[0], 
           "7", "8", "9", OPERATION_TYPES[1], 
           "4", "5", "6", OPERATION_TYPES[2], 
           "1", "2", "3", OPERATION_TYPES[3], 
           "0", " ", ".", "="]

# Order of Operations bool for multiple operations at once
USE_PEMDAS = True


class CalcObj:
    def __init__(self, in_root):
        self.root = in_root
        self.buttons = []

        # display variable storage
        self.header_label = ttk.Label()

        # init GUI and reset it
        self.init_window()
        self.reset_header()

        # operational variable storage
        self.first_number = 0
        self.second_number = 0
        self.operation = str("0")

        # logical variable storage
        self.header_text = str(0)
        self.is_reset = True
        self.first_number_set = False
        self.last_operation_equals = False
        self.operation_amount = 0

        
    def init_window(self):
        self.root.title("Calculator: Made by ZachG1235")
        # self.root.geometry(f"{X_WINDOW_PIXELS}x{Y_WINDOW_PIXELS}")
        self.root.configure(bg="white")
        header_label = ttk.Label(self.root, text=str("N/A"), 
                                                 style="White.TLabel", width=0, 
                                                    font=("Courier New", 24, "bold"), 
                                             anchor="center", justify="center")
        header_label.grid(row=0, column=0, columnspan=GUI_COLUMNS, padx=0, pady=0, sticky="nesw", ipady=10)
        self.header_label = header_label
        label_index = 0
        clear_index = 0
        zero_index = 0
        for i in range(GUI_ROWS_AFTER_HEADER):
            # init header (for caluclation results)
            row_buttons = []   
            row_label = ttk.Label(self.root, text=str(i), 
                                                 style="White.TLabel", width=0, 
                                                    font=("Courier New", 24, "bold"), 
                                             anchor="center", justify="center")
            row_label.grid(row=i+1, column=0, padx=0, pady=0, sticky="nesw")
            # init buttons
            for j in range(GUI_COLUMNS):
                # // logic here could be optimized // # 
                btn_text = str()
                canvas = tkinter.Canvas(self.root, width=BUTTON_WIDTH, height=BUTTON_HEIGHT, bg="white", highlightthickness=1)
                if clear_index < 3:
                    if clear_index == 0: # clear
                        canvas.grid(row=i+1, column=j, columnspan=3, padx=0, pady=0, sticky="nesw")
                        btn_text = str(LABELS[label_index])
                        canvas.create_text((BUTTON_WIDTH*3)//2, BUTTON_HEIGHT//2, text=btn_text, font=("Courier New", 16), fill="black")
                elif zero_index > 15 and zero_index < 18: #16 or 17
                    if zero_index == 16: # only 16, so 0
                        canvas.grid(row=i+1, column=j, columnspan=2, padx=0, pady=0, sticky="nesw")
                        btn_text = str(LABELS[label_index])
                        canvas.create_text((BUTTON_WIDTH*2)//2, BUTTON_HEIGHT//2, text=btn_text, font=("Courier New", 16), fill="black")
                else:
                    canvas.grid(row=i+1, column=j, padx=0, pady=0, sticky="nesw")
                    btn_text = str(LABELS[label_index])
                    canvas.create_text(BUTTON_WIDTH//2, BUTTON_HEIGHT//2, text=btn_text, font=("Courier New", 16), fill="black")
                canvas.bind("<Button-1>", lambda event, row_param=i, col_param=j:self.onButtonClick(row_param, col_param))
                new_button = MyButton(data=canvas, row=i, col=j, text=btn_text)
                row_buttons.append(new_button)
                label_index += 1
                clear_index += 1
                zero_index += 1
            self.buttons.append(row_buttons)
    
    def onButtonClick(self, row_param : int, col_param : int):
        button_text = self.buttons[row_param][col_param].text
        if self.is_num(button_text): # is a number
            if self.last_operation_equals:
                self.reset_header()
                self.append_to_header(button_text)
            elif not (self.is_reset and button_text == "0"):  
                self.append_to_header(button_text)
            self.last_operation_equals = False
        else: 
            if button_text == "C": # clear
                self.reset_header()
            elif button_text == "=": 
                self.process_equals()
            else: # is an operation
                if self.is_num(self.header_text):
                    self.first_number = float(self.header_text)
                self.append_to_header(button_text, True)
                if button_text in OPERATION_TYPES: # excludes decimal point button
                    self.operation = button_text
                    self.operation_amount += 1
                    self.first_number_set = True
                    self.last_operation_equals = False
        
    def set_header_to(self, text_to_update : str):
        self.header_text = str(text_to_update)
        self.header_label.config(text=self.header_text)
    
    def append_to_header(self, text_to_append: str, override = False):
        if self.is_reset and not override:
            self.set_header_to(text_to_append)
        else: # override used to force appendation when self.is_reset is true
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
        self.first_number_set = False
        self.first_number = 0
        self.second_number = 0
        self.last_operation_equals = False
    
    def run_operation(self) -> int | float:
        op = self.operation
        output_result = 0
        match op:
            case "+":
                output_result = self.first_number + self.second_number
            case "-":
                output_result = self.first_number - self.second_number
            case "*":
                output_result = self.first_number * self.second_number
            case "/":
                output_result = self.first_number / self.second_number
            case _:
                self.set_header_to_error("Invalid Operation")
        return output_result

    def process_equals(self):
        # process operations where only two int/floats being equals'ed
        if self.operation_amount < 2:
            if self.last_operation_equals: # if user pressed equals after doing equals
                potential_second_num = self.second_number
                self.first_number = float(self.header_text)
            else:
                potential_second_num = self.header_text.split(self.operation)[1]
            
            if self.is_num(str(potential_second_num)):
                self.second_number = float(potential_second_num)
                result = str(self.run_operation())
                result = self.fix_float_output(str(result))
                self.set_header_to(str(result))
                self.last_operation_equals = True
                self.operation_amount = 0
            else: 
                self.set_header_to_error("2nd num isn't a num")
        # multiple operations
        else: 
            # parse the data
            result = 0
            temp_str = ""
            num_list = []
            op_list = []
            num_list_index = 1
            for each_char in self.header_text:
                if each_char in OPERATION_TYPES:
                    num_list.append(temp_str)
                    op_list.append(each_char)
                    temp_str = ""
                else:
                    temp_str = temp_str + each_char
            num_list.append(temp_str) 
            # num_list now contains each number and op_list contains each operation
            # ex. "3+5*5.2/8-7" turns into 
            # num_list = ['3', '5', '5.2', '8', '7'] and op_list = ['+', '*', '/', '-']
            
            # check for error (multiple empty list indicies)
            error_found = False
            bad_num_counter = 0
            for each_num in num_list[1:]:
                if len(each_num) == 0:
                    bad_num_counter += 1
            error_found = bad_num_counter != 0 

            if (len(num_list) - 1 == len(op_list)) and not USE_PEMDAS and not error_found: # if valid operations
                if len(num_list[0]) == 0: # fixes leading operation of num_list
                    num_list[0] = 0
                result = float(num_list[0]) 
                for each_op in op_list:
                    next_num = float(num_list[num_list_index])
                    if each_op == "+":
                        result += next_num
                    elif each_op == "-":
                        result -= next_num
                    elif each_op == "*":
                        result *= next_num
                    else: # must be division:
                        result /= next_num
                    num_list_index += 1
                result = self.fix_float_output(str(result))
                self.set_header_to(result)
                self.last_operation_equals = True
                self.operation_amount = 0
            elif (len(num_list) - 1 == len(op_list)) and USE_PEMDAS and not error_found:
                if len(num_list[0]) == 0: # fixes leading operation of num_list
                    num_list[0] = 0
                result = float(num_list[0]) 
                new_op_list = []
                num_index = 0
                # modifies num_list and multiplies/divides adjacent numbers, leaving only addition/subtraction left
                for each_op in op_list:
                    if each_op == "-" or each_op == "+":
                        new_op_list.append(each_op)
                        num_index += 1
                    elif each_op == "*":
                        num_list[num_index] = float(num_list[num_index]) * float(num_list[num_index + 1])
                        num_list.pop(num_index + 1)
                    elif each_op == "/":
                        num_list[num_index] = float(num_list[num_index]) / float(num_list[num_index + 1])
                        num_list.pop(num_index + 1)

                # new_op_list should only have + and -, do those next  
                for each_op in new_op_list:
                    next_num = float(num_list[num_list_index])
                    if each_op == "+":
                        result += next_num
                    elif each_op == "-":
                        result -= next_num
                    # last loop got rid of * and /, so shouldn't need to have those cases
                    else: 
                        self.set_header_to_error("OoO Failure")
                        return
                    num_list_index += 1
                result = self.fix_float_output(str(result))
                self.set_header_to(result)
                self.last_operation_equals = True
                self.operation_amount = 0        
            else: 
                # error
                self.set_header_to_error("Bad Operation Quantity")

    def fix_float_output(self, string_to_fix : str) -> str:
        # removes tails such as .0 or more 0s the occur after a decimal point 
        # ex. 42.0 -> 42, 21. -> 21, 17.0300 -> 17.03
        while str(string_to_fix).find(".") != -1 and (str(string_to_fix).endswith("0") or str(string_to_fix).endswith(".")):
            string_to_fix = str(string_to_fix)[:-1]
        return string_to_fix

    def set_header_to_error(self, error_string = "Undefined Error"):
        err_str = "Err: " + str(error_string)
        self.header_text = err_str
        self.header_label.config(text=self.header_text)


class MyButton:
    def __init__(self, data, row : int, col : int, text : str):
        self.data = data
        self.row = row
        self.col = col
        self.text = text


def main():
    root_content = tkinter.Tk()
    calc_obj = CalcObj(root_content)
    print("Thank you for checking out my calculator!")
    print("Feel free to try to break it, let me know what doesn't work!")
    print("Made by: @ZachG1235 on Github")
    calc_obj.root.mainloop()

main()