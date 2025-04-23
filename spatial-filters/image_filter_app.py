import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageFilter
import os
from datetime import datetime

class ImageFilterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Filter Application")
        self.root.geometry("1000x800")
        
        # Create output directory if it doesn't exist
        os.makedirs("output", exist_ok=True)
        
        # Initialize variables
        self.image_path = None
        self.original_image = None
        self.filtered_image = None
        
        self.create_widgets()
        
    def create_widgets(self):
        # Create main frames
        self.top_frame = tk.Frame(self.root)
        self.top_frame.pack(pady=10)
        
        self.middle_frame = tk.Frame(self.root)
        self.middle_frame.pack(pady=10)
        
        self.bottom_frame = tk.Frame(self.root)
        self.bottom_frame.pack(pady=10)
        
        # Image selection button
        tk.Button(self.top_frame, text="Choose Image", command=self.choose_image).pack(side=tk.LEFT, padx=10)
        
        # Filter selection
        self.filter_var = tk.StringVar()
        self.filter_var.set("canny")  # Default filter
        
        filters = [
            ("Canny Edge Detection", "canny"),
            ("Max Filter", "max"),
            ("Min Filter", "min"),
            ("Median Filter", "median"),
            ("Sobel Edge Detection", "sobel"),
            ("Prewitt Horizontal", "prewitt_h"),
            ("Prewitt Vertical", "prewitt_v"),
            ("Prewitt Combined", "prewitt_combined")
        ]
        
        # Create radio buttons for filter selection
        for text, value in filters:
            tk.Radiobutton(self.top_frame, text=text, variable=self.filter_var,
                          value=value, command=self.apply_filter).pack(side=tk.LEFT, padx=10)
        
        # Image display areas
        self.original_label = tk.Label(self.middle_frame, text="Original Image")
        self.original_label.pack(side=tk.LEFT, padx=20)
        
        self.filtered_label = tk.Label(self.middle_frame, text="Filtered Image")
        self.filtered_label.pack(side=tk.LEFT, padx=20)
        
        # Apply filter button
        tk.Button(self.bottom_frame, text="Apply Filter", command=self.apply_filter).pack(pady=10)
        
    def choose_image(self):
        file_path = filedialog.askopenfilename(
            title="Select Image",
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.gif")]
        )
        if file_path:
            self.image_path = file_path
            self.load_image(file_path)
            
    def load_image(self, path):
        try:
            self.original_image = Image.open(path)
            # Resize image to fit in the window
            self.original_image.thumbnail((400, 400))
            photo = ImageTk.PhotoImage(self.original_image)
            self.original_label.configure(image=photo)
            self.original_label.image = photo
            self.apply_filter()  # Apply default filter
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load image: {str(e)}")
            
    def apply_filter(self):
        if not self.original_image:
            return
            
        try:
            # Convert to grayscale
            img = self.original_image.convert('L')
            
            # Get current date for filename
            current_date = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Apply selected filter
            filter_type = self.filter_var.get()
            
            if filter_type == 'canny':
                # Canny edge detection using Sobel and thresholding
                sobel = img.filter(ImageFilter.FIND_EDGES)
                threshold = 100
                filtered = sobel.point(lambda x: 255 if x > threshold else 0)
                output_path = f"output/canny_{current_date}.png"
                
            elif filter_type == 'max':
                filtered = img.filter(ImageFilter.MaxFilter(size=3))
                output_path = f"output/max_{current_date}.png"
                
            elif filter_type == 'min':
                filtered = img.filter(ImageFilter.MinFilter(size=3))
                output_path = f"output/min_{current_date}.png"
                
            elif filter_type == 'median':
                filtered = img.filter(ImageFilter.MedianFilter(size=3))
                output_path = f"output/median_{current_date}.png"
                
            elif filter_type == 'sobel':
                filtered = img.filter(ImageFilter.FIND_EDGES)
                output_path = f"output/sobel_{current_date}.png"
                
            elif filter_type == 'prewitt_h':
                prewitt_h = ImageFilter.Kernel((3, 3), [-1, 0, 1, -1, 0, 1, -1, 0, 1], 1)
                filtered = img.filter(prewitt_h)
                output_path = f"output/prewitt_h_{current_date}.png"
                
            elif filter_type == 'prewitt_v':
                prewitt_v = ImageFilter.Kernel((3, 3), [-1, -1, -1, 0, 0, 0, 1, 1, 1], 1)
                filtered = img.filter(prewitt_v)
                output_path = f"output/prewitt_v_{current_date}.png"
                
            elif filter_type == 'prewitt_combined':
                prewitt_h = ImageFilter.Kernel((3, 3), [-1, 0, 1, -1, 0, 1, -1, 0, 1], 1)
                prewitt_v = ImageFilter.Kernel((3, 3), [-1, -1, -1, 0, 0, 0, 1, 1, 1], 1)
                h_filtered = img.filter(prewitt_h)
                v_filtered = img.filter(prewitt_v)
                filtered = Image.blend(h_filtered, v_filtered, 0.5)
                output_path = f"output/prewitt_combined_{current_date}.png"
            
            # Save the filtered image
            filtered.save(output_path)
            
            # Display the filtered image
            filtered.thumbnail((400, 400))
            photo = ImageTk.PhotoImage(filtered)
            self.filtered_label.configure(image=photo)
            self.filtered_label.image = photo
            
            messagebox.showinfo("Success", f"Filter applied and saved to: {output_path}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to apply filter: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageFilterApp(root)
    root.mainloop() 