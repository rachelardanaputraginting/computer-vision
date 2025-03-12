from PIL import Image, ImageFilter
import matplotlib.pyplot as plt  # You need pyplot specifically, not just matplotlib

img1 = Image.open("images/image.png").convert('L')

img2 = img1.filter(ImageFilter.MaxFilter(size=3))

fig = plt.figure()
plt.gray()
ax1 = fig.add_subplot(121)  # First subplot
ax2 = fig.add_subplot(122)  # Second subplot (you had ax1 twice)

ax1.imshow(img1)
ax2.imshow(img2)  # This should use ax2, not ax1 again
plt.show()

img2.save("output/median_output.png")