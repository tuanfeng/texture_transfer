#usage: import texturem2t
#		texturem2t.texturem2t(mat_file_name)

#usage2: python texturem2t.py matfile.mat

import os
import sys
import scipy.io as spio
from PIL import Image

class texturem2t:
	def __init__(self,filename):

		newpath = os.path.dirname(filename)+'/texture/' 
		if not os.path.exists(newpath): os.makedirs(newpath)

		filepath=os.path.dirname(filename)+'/'
		mat = spio.loadmat(filename)
		name = mat['name']
		group_number = mat['group_number']
		size_x = mat['size_x']
		size_y = mat['size_y']
		pixel = mat['pixel']

		for i in range(0,group_number[0]):
			name_i = name[i]
			img = Image.new("RGB",(size_x[0,i],size_y[0,i]),"green")
			pixels = img.load()
			for pi in range(0,size_x[0,i]):
				for pj in range(0,size_y[0,i]):
					if pixel[i,pi,pj,0] > 255:
						pixels[pi,pj]=(255,0,0)
					elif pixel[i,pi,pj,1] > 255:
						pixels[pi,pj]=(0,255,0)
					else:
						pixels[pi,pj]=(pixel[i,pi,pj,0],pixel[i,pi,pj,1],pixel[i,pi,pj,2])

			print filepath+name_i.rstrip()
			img.save(filepath+name_i.rstrip())

if __name__ == "__main__":
	texturem2t(sys.argv[1])