from PIL import Image, ImageFilter
import matplotlib.pyplot as plt
import os

os.makedirs("output", exist_ok=True)

# Open image
img1 = Image.open("images/image.png").convert('L')

# Sobel filter
img_sobel = img1.filter(ImageFilter.FIND_EDGES)

# Prewitt filters
prewitt_h = ImageFilter.Kernel((3, 3), [-1, 0, 1, -1, 0, 1, -1, 0, 1], 1)
prewitt_v = ImageFilter.Kernel((3, 3), [-1, -1, -1, 0, 0, 0, 1, 1, 1], 1)

img_prewitt_h = img1.filter(prewitt_h)
img_prewitt_v = img1.filter(prewitt_v)

fig = plt.figure(figsize=(12, 8))
plt.gray()

ax1 = fig.add_subplot(231)  
ax2 = fig.add_subplot(232)  
ax3 = fig.add_subplot(233)  
ax4 = fig.add_subplot(234)  
ax5 = fig.add_subplot(235)  

ax1.imshow(img1)
ax1.set_title('Original')
ax2.imshow(img_sobel)
ax2.set_title('Sobel')
ax3.imshow(img_prewitt_h)
ax3.set_title('Prewitt Horizontal')
ax4.imshow(img_prewitt_v)
ax4.set_title('Prewitt Vertical')
ax5.imshow(Image.blend(img_prewitt_h, img_prewitt_v, 0.5))
ax5.set_title('Prewitt Combined')

plt.tight_layout()
plt.show()

# Save images
img_sobel.save("output/sobel_output.png")
img_prewitt_h.save("output/prewitt_h_output.png")
img_prewitt_v.save("output/prewitt_v_output.png")
Image.blend(img_prewitt_h, img_prewitt_v, 0.5).save("output/prewitt_combined_output.png")