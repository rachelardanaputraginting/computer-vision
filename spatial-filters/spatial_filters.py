from PIL import Image, ImageFilter
import os
from datetime import datetime

def apply_spatial_filter(image_path, filter_type):

    # Create output directory if it doesn't exist
    os.makedirs("output", exist_ok=True)
    
    # Open and convert image to grayscale
    img = Image.open(image_path).convert('L')
    
    # Get current date for filename
    current_date = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Apply different filters based on filter_type
    if filter_type == 'canny':
        # Canny edge detection using Sobel and thresholding
        sobel = img.filter(ImageFilter.FIND_EDGES)
        # Apply threshold
        threshold = 100
        canny = sobel.point(lambda x: 255 if x > threshold else 0)
        output_path = f"output/canny_{current_date}.png"
        canny.save(output_path)
        return canny
        
    elif filter_type == 'max':
        filtered = img.filter(ImageFilter.MaxFilter(size=3))
        output_path = f"output/max_{current_date}.png"
        filtered.save(output_path)
        return filtered
        
    elif filter_type == 'min':
        filtered = img.filter(ImageFilter.MinFilter(size=3))
        output_path = f"output/min_{current_date}.png"
        filtered.save(output_path)
        return filtered
        
    elif filter_type == 'median':
        filtered = img.filter(ImageFilter.MedianFilter(size=3))
        output_path = f"output/median_{current_date}.png"
        filtered.save(output_path)
        return filtered
        
    elif filter_type == 'sobel':
        filtered = img.filter(ImageFilter.FIND_EDGES)
        output_path = f"output/sobel_{current_date}.png"
        filtered.save(output_path)
        return filtered
        
    elif filter_type == 'prewitt_h':
        prewitt_h = ImageFilter.Kernel((3, 3), [-1, 0, 1, -1, 0, 1, -1, 0, 1], 1)
        filtered = img.filter(prewitt_h)
        output_path = f"output/prewitt_h_{current_date}.png"
        filtered.save(output_path)
        return filtered
        
    elif filter_type == 'prewitt_v':
        prewitt_v = ImageFilter.Kernel((3, 3), [-1, -1, -1, 0, 0, 0, 1, 1, 1], 1)
        filtered = img.filter(prewitt_v)
        output_path = f"output/prewitt_v_{current_date}.png"
        filtered.save(output_path)
        return filtered
        
    elif filter_type == 'prewitt_combined':
        prewitt_h = ImageFilter.Kernel((3, 3), [-1, 0, 1, -1, 0, 1, -1, 0, 1], 1)
        prewitt_v = ImageFilter.Kernel((3, 3), [-1, -1, -1, 0, 0, 0, 1, 1, 1], 1)
        h_filtered = img.filter(prewitt_h)
        v_filtered = img.filter(prewitt_v)
        combined = Image.blend(h_filtered, v_filtered, 0.5)
        output_path = f"output/prewitt_combined_{current_date}.png"
        combined.save(output_path)
        return combined
        
    else:
        raise ValueError(f"Unknown filter type: {filter_type}")

# Example usage:
if __name__ == "__main__":
    # Example image path
    image_path = "images/2.PNG"
    
    filters = [
        'canny',
        'max',
        'min',
        'median',
        'sobel',
        'prewitt_h',
        'prewitt_v',
        'prewitt_combined'
    ]
    
    for filter_type in filters:
        try:
            filtered_image = apply_spatial_filter(image_path, filter_type)
            print(f"Successfully applied {filter_type} filter")
        except Exception as e:
            print(f"Error applying {filter_type} filter: {str(e)}") 