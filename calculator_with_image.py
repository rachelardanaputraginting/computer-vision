import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os

class CalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculator with Image Input")
        self.root.geometry("800x600")
        
        # Create menu frame
        self.menu_frame = tk.Frame(root)
        self.menu_frame.pack(pady=20)
        
        # Create calculator frame
        self.calc_frame = tk.Frame(root)
        self.calc_frame.pack(pady=20)
        
        # Create image frame
        self.image_frame = tk.Frame(root)
        self.image_frame.pack(pady=20)
        
        # Initialize variables
        self.num1 = tk.StringVar()
        self.num2 = tk.StringVar()
        self.result = tk.StringVar()
        self.image_path = None
        
        self.create_widgets()
        
    def create_widgets(self):
        # Menu buttons
        tk.Button(self.menu_frame, text="Calculator", command=self.show_calculator).pack(side=tk.LEFT, padx=10)
        tk.Button(self.menu_frame, text="Image Input", command=self.show_image_input).pack(side=tk.LEFT, padx=10)
        
        # Calculator widgets
        self.calc_widgets = []
        
        # Number 1
        tk.Label(self.calc_frame, text="Number 1:").grid(row=0, column=0, padx=5, pady=5)
        tk.Entry(self.calc_frame, textvariable=self.num1).grid(row=0, column=1, padx=5, pady=5)
        
        # Number 2
        tk.Label(self.calc_frame, text="Number 2:").grid(row=1, column=0, padx=5, pady=5)
        tk.Entry(self.calc_frame, textvariable=self.num2).grid(row=1, column=1, padx=5, pady=5)
        
        # Operation buttons
        operations = ['+', '-', '*', '/', '%', '^', '√']
        for i, op in enumerate(operations):
            btn = tk.Button(self.calc_frame, text=op, command=lambda o=op: self.calculate(o))
            btn.grid(row=2, column=i, padx=5, pady=5)
            self.calc_widgets.append(btn)
        
        # Result
        tk.Label(self.calc_frame, text="Result:").grid(row=3, column=0, padx=5, pady=5)
        tk.Entry(self.calc_frame, textvariable=self.result, state='readonly').grid(row=3, column=1, padx=5, pady=5)
        
        # Image input widgets
        self.image_widgets = []
        
        # Image selection button
        tk.Button(self.image_frame, text="Choose Image", command=self.choose_image).pack(pady=10)
        
        # Image display
        self.image_label = tk.Label(self.image_frame)
        self.image_label.pack(pady=10)
        self.image_widgets.append(self.image_label)
        
        # Initially hide calculator and image frames
        self.calc_frame.pack_forget()
        self.image_frame.pack_forget()
        
    def show_calculator(self):
        self.image_frame.pack_forget()
        self.calc_frame.pack(pady=20)
        
    def show_image_input(self):
        self.calc_frame.pack_forget()
        self.image_frame.pack(pady=20)
        
    def choose_image(self):
        file_path = filedialog.askopenfilename(
            title="Select Image",
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.gif")]
        )
        if file_path:
            self.image_path = file_path
            self.display_image(file_path)
            
    def display_image(self, path):
        try:
            image = Image.open(path)
            # Resize image to fit in the window
            image.thumbnail((400, 400))
            photo = ImageTk.PhotoImage(image)
            self.image_label.configure(image=photo)
            self.image_label.image = photo
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load image: {str(e)}")
            
    def calculate(self, operation):
        try:
            num1 = float(self.num1.get())
            num2 = float(self.num2.get())
            
            if operation == '+':
                result = num1 + num2
            elif operation == '-':
                result = num1 - num2
            elif operation == '*':
                result = num1 * num2
            elif operation == '/':
                if num2 == 0:
                    raise ValueError("Division by zero")
                result = num1 / num2
            elif operation == '%':
                if num2 == 0:
                    raise ValueError("Modulus by zero")
                result = num1 % num2
            elif operation == '^':
                result = num1 ** num2
            elif operation == '√':
                if num1 < 0:
                    raise ValueError("Cannot calculate square root of negative number")
                result = num1 ** 0.5
                
            self.result.set(str(result))
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = CalculatorApp(root)
    root.mainloop() 