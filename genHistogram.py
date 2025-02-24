import numpy as np
import cv2
import matplotlib.pyplot as plt

image = cv2.imread("1P0A0010.JPG")

image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

histogram, bin_edges = np.histogram(image, bins=256, range=(0, 256))

# configure and draw the histogram figure
plt.figure()
plt.title("Grayscale Histogram")
plt.xlabel("grayscale value")
plt.ylabel("pixel count")
plt.xlim([0.0, 256])  # <- named arguments do not work here

plt.plot(bin_edges[0:-1], histogram)  # <- or here
plt.show()
