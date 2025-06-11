import numpy as np

def image_inverse(img_array):
    """Menerapkan transformasi inverse pada gambar menggunakan perulangan"""
    # Membuat array baru dengan ukuran yang sama
    transformed = np.zeros_like(img_array)
    
    # Melakukan transformasi piksel per piksel
    for i in range(img_array.shape[0]):  # baris
        for j in range(img_array.shape[1]):  # kolom
            # Menerapkan transformasi inverse
            transformed[i, j] = 255 - img_array[i, j]
    
    return transformed 