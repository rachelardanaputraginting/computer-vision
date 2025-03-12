from PIL import Image, ImageFilter
import matplotlib.pyplot as plt
import os

if not os.path.exists("output"):
    os.makedirs("output")

def apply_filter(filter_type):    
    if filter_type == "min":
        img = Image.open("images/image.png").convert('L')
        filtered_img = img.filter(ImageFilter.MinFilter(size=3))
        output_path = "output/min_output.png"
    elif filter_type == "max":
        img = Image.open("images/image.png").convert('L')
        filtered_img = img.filter(ImageFilter.MaxFilter(size=3))
        output_path = "output/max_output.png"
    elif filter_type == "median":
        img = Image.open("images/image_median.png").convert('L')
        filtered_img = img.filter(ImageFilter.MedianFilter(size=3))
        output_path = "output/median_output.png"
    
    filtered_img.save(output_path)
    
    fig = plt.figure()
    plt.gray()
    
    ax1 = fig.add_subplot(121)
    ax2 = fig.add_subplot(122)
    
    ax1.imshow(img)
    ax2.imshow(filtered_img)
    
    plt.show()
    
    return "Image saved as " + output_path

# Example usage
filter_type = input("Choose filter (min, max, median): ")
result = apply_filter(filter_type)
print(result)