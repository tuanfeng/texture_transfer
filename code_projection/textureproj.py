#usage: python textureproj.py image.png model_t.obj view_estimate.txt

import sys
import os
from PIL import Image

image_file = sys.argv[1]
model_file = sys.argv[2]
ve_file = sys.argv[3]

rimg = Image.open(image_file)
rimg_pd={}

#upsam=10

for i in range(0,rimg.size[0]):
	for j in range(0,rimg.size[1]):
		rimg_pd[i,j]=1000000.0

#rimg_p = rimg.load()
#for i in range(100,400):
#	for j in range(200,400):
#		rimg_p[i,j] = (255,0,0)

#rimg.show()

fve = open(ve_file,'r')
lfve=fve.readlines()
cx=float(lfve[0].split()[0])
cy=float(lfve[0].split()[1])
cz=float(lfve[0].split()[2])
qw=float(lfve[0].split()[3])
qx=float(lfve[0].split()[4])
qy=float(lfve[0].split()[5])
qz=float(lfve[0].split()[6])
foc=float(lfve[0].split()[7])
fve.close()

#print cx,cy,cz

R11=qw*qw+qx*qx-qz*qz-qy*qy
R21=2*qx*qy-2*qz*qw
R31=2*qy*qw+2*qx*qz
R12=2*qx*qy+2*qz*qw
R22=qy*qy+qw*qw-qx*qx-qz*qz
R32=2*qz*qy-2*qx*qw
R13=2*qx*qz-2*qy*qw 
R23=2*qy*qz+2*qw*qx
R33=qz*qz+qw*qw-qx*qx-qy*qy

#print R11,R12,R13
#print R21,R22,R23
#print R31,R32,R33

focal = float(rimg.size[0])*foc/32.0


#v3d_x=0.1
#v3d_y=0.0
#v3d_z=0.0
#ppx=R11*(v3d_x-cx)+R12*(v3d_y-cy)+R13*(v3d_z-cz)
#ppy=R21*(v3d_x-cx)+R22*(v3d_y-cy)+R23*(v3d_z-cz)
#ppz=R31*(v3d_x-cx)+R32*(v3d_y-cy)+R33*(v3d_z-cz)
#pfx=int(rimg.size[0]/2-focal*ppx/ppz)
#pfy=int(rimg.size[1]/2-focal*ppy/ppz)

#print ppx,ppy,ppz,pfx,pfy



#exit()


obj_name = os.path.splitext(os.path.basename(model_file))[0]
mtl_file = model_file[:-3]+'mtl'


#load_mesh

f1 = open(model_file,'r')

arrayv_={}
cv_=0
arrayf_={}
cf_=0

for line in f1.readlines():
	linet = line.split()
	if linet[0] == 'v':
		cv_ = cv_ + 1
		arrayv_[cv_,1] = float(linet[1])
		arrayv_[cv_,2] = float(linet[2])
		arrayv_[cv_,3] = float(linet[3])
	if linet[0] == 'f':
		cf_ = cf_ + 1
		arrayf_[cf_,1] = int(linet[1].split('/')[0])
		arrayf_[cf_,2] = int(linet[2].split('/')[0])
		arrayf_[cf_,3] = int(linet[3].split('/')[0])
		

f1.close()



f2 = open(model_file,'r')

arrayv={}
cv=0
arrayvt={}
cvt=0

img_name={}
img={}
img_p={}
img_rx={} #x location on refimg
img_ry={} #y location on refimg
img_rd={} #depth


cim=0

for line in f2.readlines():
	linet = line.split()
	if linet[0] == 'usemtl':
		f3 = open(mtl_file,'r')
		flag = 0
		for l_ in f3.readlines():
			lt_ = l_.split()			
			if len(lt_)>1 and lt_[0] == 'newmtl' and lt_[1] == linet[1]:
				flag = 1
			if flag == 1 and lt_[0] == 'map_Kd':
				cim=cim+1
				img_name[cim] = model_file[:-(4+len(obj_name))]+lt_[1]
				print img_name[cim]
				img[cim] = Image.open(img_name[cim])
				img_p[cim] = img[cim].load()
				(img_size_x, img_size_y) = img[cim].size
				img_rx[cim]={}
				img_ry[cim]={}
				img_rd[cim]={}
				for lsi in range(0,img_size_x):
					for lsj in range(0,img_size_y):
						img_rd[cim][lsi,lsj] = -1.0
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
		vit = {} #get real texture coordinate location and sort
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

		t1x=vit_[2,1]-vit_[1,1]
		t1y=vit_[2,2]-vit_[1,2]
		t2x=vit_[3,1]-vit_[1,1]
		t2y=vit_[3,2]-vit_[1,2]

		if int(vit_[1,1]) < int(vit_[2,1]) and t1y*t2x-t1x*t2y != 0:
			frx=int(vit_[1,1])
			ftx=int(vit_[2,1])
			for li in range(frx,ftx+1):
				p1=(li-vit_[1,1])/(t1x)
				q1=vit_[1,2]+(t1y)*p1
				p2=(li-vit_[1,1])/(t2x)
				q2=vit_[1,2]+(t2y)*p2
				q1_=int(min(q1,q2))
				q2_=int(max(q1,q2))
				#if q1_>0:
				#	q1_=q1_-1
				#if q2_<img_size_y-1:
				#	q2_=q2_+1
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
					v3d_x_=v3d_base_x+lam*(v3d_1_x-v3d_base_x)+mu*(v3d_2_x-v3d_base_x)
					v3d_y_=v3d_base_y+lam*(v3d_1_y-v3d_base_y)+mu*(v3d_2_y-v3d_base_y)
					v3d_z_=v3d_base_z+lam*(v3d_1_z-v3d_base_z)+mu*(v3d_2_z-v3d_base_z)
					v3d_x=v3d_x_
					v3d_y=-v3d_z_
					v3d_z=v3d_y_
					ppx=R11*(v3d_x-cx)+R12*(v3d_y-cy)+R13*(v3d_z-cz)
					ppy=R21*(v3d_x-cx)+R22*(v3d_y-cy)+R23*(v3d_z-cz)
					ppz=R31*(v3d_x-cx)+R32*(v3d_y-cy)+R33*(v3d_z-cz)
					pfx=int(rimg.size[0]/2-focal*ppx/ppz)
					pfy=int(rimg.size[1]/2+focal*ppy/ppz)
					pfx_=rimg.size[0]/2-focal*ppx/ppz
					pfy_=rimg.size[1]/2+focal*ppy/ppz
					if pfx>=0 and pfx<rimg.size[0] and pfy>=0 and pfy<rimg.size[1]:
						if pfx == rimg.size[0]-1 or pfy == rimg.size[1]-1:
							pix = rimg.getpixel((pfx,pfy))
						else:
							d00=(pfx_-pfx)*(pfx_-pfx)+(pfy_-pfy)*(pfy_-pfy)
							d01=(pfx_-pfx)*(pfx_-pfx)+(pfy_-pfy-1)*(pfy_-pfy-1)
							d10=(pfx_-pfx-1)*(pfx_-pfx-1)+(pfy_-pfy)*(pfy_-pfy)
							d11=(pfx_-pfx-1)*(pfx_-pfx-1)+(pfy_-pfy-1)*(pfy_-pfy-1)
							w00=1/d00/(1/d00+1/d10+1/d01+1/d11)
							w01=1/d01/(1/d00+1/d10+1/d01+1/d11)
							w10=1/d10/(1/d00+1/d10+1/d01+1/d11)
							w11=1/d11/(1/d00+1/d10+1/d01+1/d11)
							pix0 = w00*rimg.getpixel((pfx,pfy))[0]+w10*rimg.getpixel((pfx+1,pfy))[0]+w01*rimg.getpixel((pfx,pfy+1))[0]+w11*rimg.getpixel((pfx+1,pfy+1))[0]
							pix1 = w00*rimg.getpixel((pfx,pfy))[1]+w10*rimg.getpixel((pfx+1,pfy))[1]+w01*rimg.getpixel((pfx,pfy+1))[1]+w11*rimg.getpixel((pfx+1,pfy+1))[1]
							pix2 = w00*rimg.getpixel((pfx,pfy))[2]+w10*rimg.getpixel((pfx+1,pfy))[2]+w01*rimg.getpixel((pfx,pfy+1))[2]+w11*rimg.getpixel((pfx+1,pfy+1))[2]
							pix = (int(pix0),int(pix1),int(pix2))
						if li>=0 and li<img_size_x and lj>=0 and lj<img_size_y:
							dpt=(v3d_x-cx)*(v3d_x-cx)+(v3d_y-cy)*(v3d_y-cy)+(v3d_z-cz)*(v3d_z-cz)
							if rimg_pd[pfx,pfy]>dpt:
								rimg_pd[pfx,pfy] = dpt
							img_p[cim][li,img_size_y-lj-1]=pix
							img_rd[cim][li,img_size_y-lj-1]=dpt
							img_rx[cim][li,img_size_y-lj-1]=pfx
							img_ry[cim][li,img_size_y-lj-1]=pfy

		t1x=vit_[2,1]-vit_[3,1]
		t1y=vit_[2,2]-vit_[3,2]
		t2x=vit_[1,1]-vit_[3,1]
		t2y=vit_[1,2]-vit_[3,2]

		if int(vit_[2,1]) < int(vit_[3,1]) and t1y*t2x-t1x*t2y != 0:
			frx=int(vit_[2,1])
			ftx=int(vit_[3,1])
			for li in range(frx,ftx+1):
				p1=(li-vit_[3,1])/(t1x)
				q1=vit_[3,2]+(t1y)*p1
				p2=(li-vit_[3,1])/(t2x)
				q2=vit_[3,2]+(t2y)*p2
				q1_=int(min(q1,q2))
				q2_=int(max(q1,q2))
				#if q1_>0:
				#	q1_=q1_-1
				#if q2_<img_size_y-1:
				#	q2_=q2_+1
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
					v3d_x_=v3d_base_x+lam*(v3d_1_x-v3d_base_x)+mu*(v3d_2_x-v3d_base_x)
					v3d_y_=v3d_base_y+lam*(v3d_1_y-v3d_base_y)+mu*(v3d_2_y-v3d_base_y)
					v3d_z_=v3d_base_z+lam*(v3d_1_z-v3d_base_z)+mu*(v3d_2_z-v3d_base_z)
					v3d_x=v3d_x_
					v3d_y=-v3d_z_
					v3d_z=v3d_y_
					ppx=R11*(v3d_x-cx)+R12*(v3d_y-cy)+R13*(v3d_z-cz)
					ppy=R21*(v3d_x-cx)+R22*(v3d_y-cy)+R23*(v3d_z-cz)
					ppz=R31*(v3d_x-cx)+R32*(v3d_y-cy)+R33*(v3d_z-cz)
					pfx=int(rimg.size[0]/2-focal*ppx/ppz)
					pfy=int(rimg.size[1]/2+focal*ppy/ppz)
					pfx_=rimg.size[0]/2-focal*ppx/ppz
					pfy_=rimg.size[1]/2+focal*ppy/ppz
					if pfx>=0 and pfx<rimg.size[0] and pfy>=0 and pfy<rimg.size[1]:
						if pfx == rimg.size[0]-1 or pfy == rimg.size[1]-1:
							pix = rimg.getpixel((pfx,pfy))
						else:
							d00=(pfx_-pfx)*(pfx_-pfx)+(pfy_-pfy)*(pfy_-pfy)
							d01=(pfx_-pfx)*(pfx_-pfx)+(pfy_-pfy-1)*(pfy_-pfy-1)
							d10=(pfx_-pfx-1)*(pfx_-pfx-1)+(pfy_-pfy)*(pfy_-pfy)
							d11=(pfx_-pfx-1)*(pfx_-pfx-1)+(pfy_-pfy-1)*(pfy_-pfy-1)
							w00=1/d00/(1/d00+1/d10+1/d01+1/d11)
							w01=1/d01/(1/d00+1/d10+1/d01+1/d11)
							w10=1/d10/(1/d00+1/d10+1/d01+1/d11)
							w11=1/d11/(1/d00+1/d10+1/d01+1/d11)
							pix0 = w00*rimg.getpixel((pfx,pfy))[0]+w10*rimg.getpixel((pfx+1,pfy))[0]+w01*rimg.getpixel((pfx,pfy+1))[0]+w11*rimg.getpixel((pfx+1,pfy+1))[0]
							pix1 = w00*rimg.getpixel((pfx,pfy))[1]+w10*rimg.getpixel((pfx+1,pfy))[1]+w01*rimg.getpixel((pfx,pfy+1))[1]+w11*rimg.getpixel((pfx+1,pfy+1))[1]
							pix2 = w00*rimg.getpixel((pfx,pfy))[2]+w10*rimg.getpixel((pfx+1,pfy))[2]+w01*rimg.getpixel((pfx,pfy+1))[2]+w11*rimg.getpixel((pfx+1,pfy+1))[2]
							pix = (int(pix0),int(pix1),int(pix2))
						if li>=0 and li<img_size_x and lj>=0 and lj<img_size_y:
							dpt=(v3d_x-cx)*(v3d_x-cx)+(v3d_y-cy)*(v3d_y-cy)+(v3d_z-cz)*(v3d_z-cz)
							if rimg_pd[pfx,pfy]>dpt:
								rimg_pd[pfx,pfy] = dpt
							img_p[cim][li,img_size_y-lj-1]=pix
							img_rd[cim][li,img_size_y-lj-1]=dpt
							img_rx[cim][li,img_size_y-lj-1]=pfx
							img_ry[cim][li,img_size_y-lj-1]=pfy



dpt_min=100000.0
dpt_max=-1.0

for i in range(0,rimg.size[0]):
	for j in range(0,rimg.size[1]):
		if rimg_pd[i,j]>dpt_max and rimg_pd[i,j]<1000:
			dpt_max = rimg_pd[i,j]
		if rimg_pd[i,j]<dpt_min:
			dpt_min = rimg_pd[i,j]

print dpt_min,dpt_max

dimg = Image.new( 'RGB', rimg.size, "green") # create a new black image
pixels = dimg.load() # create the pixel map

for i in range(dimg.size[0]):    # for every pixel:
    for j in range(dimg.size[1]):
        if rimg_pd[i,j]<1000:
        	pixels[i,j] = (int(rimg_pd[i,j]/dpt_max*255),int(rimg_pd[i,j]/dpt_max*255),int(rimg_pd[i,j]/dpt_max*255)) # set the colour accordingly
        if rimg_pd[i,j]>1000:
        	pixels[i,j] = (255,0,0)

#dimg.show()
dimg.save(model_file[:-(4+len(obj_name))] + 'depth.png')


ep = 0.02
for i in range(1,cim+1):
	for li in range(0,img[i].size[0]):
		for lj in range(0,img[i].size[1]):
			if img_rd[i][li,lj]>0:
				px=img_rx[i][li,lj]
				py=img_ry[i][li,lj]
				if px<img_size_x-1:
					px_=px+1
				else:
					px_=px
				if py<img_size_y-1:
					py_=py+1
				else:
					py_=py
				if px>0:
					px__=px-1
				else:
					px__=px
				if py>0:
					py__=py-1
				else:
					py__=py

				dpt=max(rimg_pd[px__,py__],rimg_pd[px__,py_],rimg_pd[px__,py],rimg_pd[px_,py__],rimg_pd[px_,py_],rimg_pd[px_,py],rimg_pd[px,py__],rimg_pd[px,py_],rimg_pd[px,py])
				if img_rd[i][li,lj]>dpt+ep:
					img_p[i][li,lj]=(255,0,0)

if True: # naive completion
	for i in range(1,cim+1):
		#print img_p[i][1,1]
		avgx = 0.0
		avgy = 0.0
		avgz = 0.0
		count = 0.0
		for li in range(0,img[i].size[0]):
			for lj in range(0,img[i].size[1]):
				if img_p[i][li,lj] != (255,0,0) and img_p[i][li,lj] != (0,255,0):
					count += 1.0
					avgx += img_p[i][li,lj][0]
					avgy += img_p[i][li,lj][1]
					avgz += img_p[i][li,lj][2]

		avgx = int(avgx/count)
		avgy = int(avgy/count)
		avgz = int(avgz/count)
		for li in range(0,img[i].size[0]):
			for lj in range(0,img[i].size[1]):
				if img_p[i][li,lj] != (0,255,0):
					img_p[i][li,lj] = (avgx,avgy,avgz)



for i in range(1,cim+1):
	img[i].save(img_name[i])

f2.close()




