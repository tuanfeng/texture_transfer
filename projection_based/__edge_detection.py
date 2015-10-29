#usage: python edge_detection.py image

# need to link cv2 to right python

import cv2
import numpy as np
from matplotlib import pyplot as plt
import sys

image_file = sys.argv[1]

img = cv2.imread(image_file,0)

edges = cv2.Canny(img,100,200)

plt.subplot(121),plt.imshow(img,cmap = 'gray')

plt.title('Original Image'), plt.xticks([]), plt.yticks([])
plt.subplot(122),plt.imshow(edges,cmap = 'gray')
plt.title('Edge Image'), plt.xticks([]), plt.yticks([])

plt.show()

