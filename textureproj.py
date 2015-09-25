#usage: python textureproj.py image.png model_t.obj view_estimate.txt

import sys
import os
from PIL import Image

image_file = sys.argv[1]
model_file = sys.argv[2]
ve_file = sys.argv[3]

obj_name = os.path.splitext(os.path.basename(model_file))[0]
mtl_file = model_file[:-3]+'mtl'

f2 = open(model_file,'r')

img_name=''

arrayv={}
cv=0
arrayvt={}
cvt=0

for line in f2.readlines():
	linet = line.split()
	if linet[0] == 'usemtl':
		if not img_name=='':
			img.save(img_name)
		f3 = open(mtl_file,'r')
		flag = 0
		for l_ in f3.readlines():
			lt_ = l_.split()			
			if len(lt_)>1 and lt_[0] == 'newmtl' and lt_[1] == linet[1]:
				flag = 1
			if flag == 1 and lt_[0] == 'map_Kd':
				img_name = model_file[:-(4+len(obj_name))]+lt_[1]
				print img_name
				img = Image.open(img_name)
				img_p = img.load()
				(img_size_x, img_size_y) = img.size
				break
		f3.close()
	if linet[0] == 'v':
		cv = cv + 1
		arrayv[cv,1] = float(linet[1])
		arrayv[cv,2] = float(linet[2])
		arrayv[cv,3] = float(linet[3])
	if linet[0] == 'vt':
		cvt = cvt + 1
		arrayvt[cvt,1] = float(linet[1])
		arrayvt[cvt,2] = float(linet[2])
	if linet[0] == 'f':
		fv={}
		fvt={}
		fv[1] = int(linet[1].split('/')[0])
		fvt[1] = int(linet[1].split('/')[1])
		fv[2] = int(linet[2].split('/')[0])
		fvt[2] = int(linet[2].split('/')[1])
		fv[3] = int(linet[3].split('/')[0])
		fvt[3] = int(linet[3].split('/')[1])
		if img_name == '':
			print('Error: no material!\n')
			exit()
		vit = {}
		vit[1,1] = (float(arrayvt[fvt[1],1])*float(img_size_x))
		vit[1,2] = (float(arrayvt[fvt[1],2])*float(img_size_y))
		vit[2,1] = (float(arrayvt[fvt[2],1])*float(img_size_x))
		vit[2,2] = (float(arrayvt[fvt[2],2])*float(img_size_y))
		vit[3,1] = (float(arrayvt[fvt[3],1])*float(img_size_x))
		vit[3,2] = (float(arrayvt[fvt[3],2])*float(img_size_y))
		if vit[1,1] <= vit[2,1] and vit[2,1] <= vit[3,1]:
			order = [1,2,3]
		if vit[1,1] <= vit[3,1] and vit[3,1] <= vit[2,1]:
			order = [1,3,2]
		if vit[2,1] <= vit[1,1] and vit[1,1] <= vit[3,1]:
			order = [2,1,3]
		if vit[2,1] <= vit[3,1] and vit[3,1] <= vit[1,1]:
			order = [2,3,1]
		if vit[3,1] <= vit[1,1] and vit[1,1] <= vit[2,1]:
			order = [3,1,2]
		if vit[3,1] <= vit[2,1] and vit[2,1] <= vit[1,1]:
			order = [3,2,1]
		vit_ = {}
		vit_[1,1] = vit[order[0],1]
		vit_[1,2] = vit[order[0],2]
		vit_[2,1] = vit[order[1],1]
		vit_[2,2] = vit[order[1],2]
		vit_[3,1] = vit[order[2],1]
		vit_[3,2] = vit[order[2],2]
		if int(vit_[1,1]) < int(vit_[2,1]):
			t1x=vit_[2,1]-vit_[1,1]
			t1y=vit_[2,2]-vit_[1,2]
			t2x=vit_[3,1]-vit_[1,1]
			t2y=vit_[3,2]-vit_[1,2]
			frx=int(vit_[1,1])
			#if frx>0:
			#	frx=frx-1
			ftx=int(vit_[2,1])
			#if ftx<img_size_y-1:
			#	ftx=ftx+1
			for li in range(frx,ftx+1):
				p1=(li-vit_[1,1])/(t1x)
				q1=vit_[1,2]+(t1y)*p1
				p2=(li-vit_[1,1])/(t2x)
				q2=vit_[1,2]+(t2y)*p2
				q1_=int(min(q1,q2))
				q2_=int(max(q1,q2))
				if q1_>0:
					q1_=q1_-1
				if q2_<img_size_y-1:
					q2_=q2_+1
				for lj in range(q1_,q2_+1):
					px = li-vit_[1,1]
					py = lj-vit_[1,2]
					mu=(t1y*px-t1x*py)/(t1y*t2x-t1x*t2y)
					lam=(t2y*px-t2x*py)/(t2y*t1x-t2x*t1y)
					v3d_base_x=arrayv[fv[order[0]],1]
					v3d_base_y=arrayv[fv[order[0]],2]
					v3d_base_z=arrayv[fv[order[0]],3]
					v3d_1_x=arrayv[fv[order[1]],1]
					v3d_1_y=arrayv[fv[order[1]],2]
					v3d_1_z=arrayv[fv[order[1]],3]
					v3d_2_x=arrayv[fv[order[2]],1]
					v3d_2_y=arrayv[fv[order[2]],2]
					v3d_2_z=arrayv[fv[order[2]],3]
					v3d_x=v3d_base_x+lam*(v3d_1_x-v3d_base_x)+mu*(v3d_2_x-v3d_base_x)
					v3d_y=v3d_base_y+lam*(v3d_1_y-v3d_base_y)+mu*(v3d_2_y-v3d_base_y)
					v3d_z=v3d_base_z+lam*(v3d_1_z-v3d_base_z)+mu*(v3d_2_z-v3d_base_z)
					if li>=0 and li<img_size_x and lj>=0 and lj<img_size_y:
						img_p[li,lj]=(255,0,0)
					#do some thing
		if int(vit_[2,1]) < int(vit_[3,1]):
			t1x=vit_[2,1]-vit_[3,1]
			t1y=vit_[2,2]-vit_[3,2]
			t2x=vit_[1,1]-vit_[3,1]
			t2y=vit_[1,2]-vit_[3,2]
			frx=int(vit_[2,1])
			#if frx>0:
			#	frx=frx-1
			ftx=int(vit_[3,1])
			#if ftx<img_size_y-1:
			#	ftx=ftx+1
			for li in range(frx,ftx+1):
				p1=(li-vit_[3,1])/(t1x)
				q1=vit_[3,2]+(t1y)*p1
				p2=(li-vit_[3,1])/(t2x)
				q2=vit_[3,2]+(t2y)*p2
				q1_=int(min(q1,q2))
				q2_=int(max(q1,q2))
				if q1_>0:
					q1_=q1_-1
				if q2_<img_size_y-1:
					q2_=q2_+1
				for lj in range(q1_,q2_+1):
					px = li-vit_[3,1]
					py = lj-vit_[3,2]
					mu=(t1y*px-t1x*py)/(t1y*t2x-t1x*t2y)
					lam=(t2y*px-t2x*py)/(t2y*t1x-t2x*t1y)
					v3d_base_x=arrayv[fv[order[2]],1]
					v3d_base_y=arrayv[fv[order[2]],2]
					v3d_base_z=arrayv[fv[order[2]],3]
					v3d_1_x=arrayv[fv[order[1]],1]
					v3d_1_y=arrayv[fv[order[1]],2]
					v3d_1_z=arrayv[fv[order[1]],3]
					v3d_2_x=arrayv[fv[order[0]],1]
					v3d_2_y=arrayv[fv[order[0]],2]
					v3d_2_z=arrayv[fv[order[0]],3]
					v3d_x=v3d_base_x+lam*(v3d_1_x-v3d_base_x)+mu*(v3d_2_x-v3d_base_x)
					v3d_y=v3d_base_y+lam*(v3d_1_y-v3d_base_y)+mu*(v3d_2_y-v3d_base_y)
					v3d_z=v3d_base_z+lam*(v3d_1_z-v3d_base_z)+mu*(v3d_2_z-v3d_base_z)
					if li>=0 and li<img_size_x and lj>=0 and lj<img_size_y:
						img_p[li,lj]=(255,0,0)
					#do some thing

if not img_name=='':
	img.save(img_name)


f2.close()




