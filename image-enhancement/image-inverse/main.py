# Fungsi untuk melakukan inverse pada gambar
def image_inverse(input_image):
    # Mendapatkan dimensi gambar
    height = len(input_image)
    width = len(input_image[0])
    
    # Membuat array untuk menyimpan hasil inverse
    output_image = [[0 for _ in range(width)] for _ in range(height)]
    
    # Melakukan inverse pada setiap pixel
    for i in range(height):
        for j in range(width):
            # Rumus inverse: t(i,j) = L-1 - I(i,j)
            # Untuk 8-bit image, L = 255
            output_image[i][j] = 255 - input_image[i][j]
    
    return output_image

# Contoh penggunaan
if __name__ == "__main__":
    # Contoh gambar input (2D array)
    # Nilai pixel antara 0-255
    input_image = [
        [0, 50, 100],
        [150, 200, 255],
        [25, 75, 125]
    ]
    
    # Melakukan inverse pada gambar
    output_image = image_inverse(input_image)
    
    # Menampilkan hasil
    print("Gambar Input:")
    for row in input_image:
        print(row)
    
    print("\nGambar Output (Inverse):")
    for row in output_image:
        print(row)
