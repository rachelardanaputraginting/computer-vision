import numpy as np

def transformasi_pixel(img_array, offset=50):
    """Menerapkan transformasi piksel T(x) = x + offset menggunakan perulangan"""
    # Membuat array baru dengan ukuran yang sama
    transformed = np.zeros_like(img_array)
    
    # Melakukan transformasi piksel per piksel
    for i in range(img_array.shape[0]):  # baris
        for j in range(img_array.shape[1]):  # kolom
            # Menerapkan transformasi dan memastikan nilai tetap dalam range 0-255
            new_value = img_array[i, j] + offset
            if new_value > 255:
                new_value = 255
            elif new_value < 0:
                new_value = 0
            transformed[i, j] = new_value
    
    return transformed 