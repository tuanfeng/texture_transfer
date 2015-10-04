#usage: python textureinit.py input_file.obj output_file.obj

import sys
import os
from PIL import Image

input_file = sys.argv[1]
output_file = sys.argv[2]

obj_name = os.path.splitext(os.path.basename(output_file))[0]

mtl_file = obj_name + '.mtl'

mesh_name ={}

f2 = open(input_file,'r')
f3 = open(output_file,'w')

f3.write('mtllib '+mtl_file+'\n')

group_count = 0

for line in f2.readlines():
	linet = line.split()
	if not linet[0] == 's':
		f3.write(line)
	if linet[0] == 'o':
		group_count = group_count + 1
		mesh_name[group_count] = linet[1]
		f3.write('usemtl texture_'+linet[1]+'\n')
	if linet[0] == 's':
		f3.write('s off\n')

f2.close()
f3.close()

#os.remove(input_file)
#os.rename(output_file, input_file)

newpath = os.path.dirname(output_file)+'/texture/' 
if not os.path.exists(newpath): os.makedirs(newpath)

f4 = open(os.path.dirname(output_file) + '/' + mtl_file,'w')

for i in range(1,group_count+1):
	f4.write('newmtl texture_'+mesh_name[i]+'\n')
	f4.write('Ns 0\n')
	f4.write('Ka 0.000000 0.000000 0.000000\n')
	f4.write('Kd 0.8 0.8 0.8\n')
	f4.write('Ks 0.8 0.8 0.8\n')
	f4.write('d 1\n')
	f4.write('illum 2\n')
	f4.write('map_Kd ./texture/texture_'+mesh_name[i]+'.png\n')
	f4.write('\n')

f4.close()

img = Image.new('RGB',(1000,1000),(0,255,0))
#img = Image.open('checkerboard.jpg')

#img.putdata(my_list)
for i in range(1,group_count+1):
	img.save(newpath + 'texture_'+mesh_name[i]+'.png')




