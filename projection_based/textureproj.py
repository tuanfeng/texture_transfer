#usage: python textureproj.py image.png mask.png model_t.obj view_estimate.txt

import sys
import os
from PIL import Image

import scipy.io as spio
import numpy as np

image_file = sys.argv[1]
mask_file = sys.argv[2]
model_file = sys.argv[3]
ve_file = sys.argv[4]

rimg = Image.open(image_file)

rimg_mask = Image.open(mask_file)

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

def crossproduct3d(u1,u2,u3,v1,v2,v3):
	s1=u2*v3-u3*v2
	s2=u3*v1-u1*v3
	s3=u1*v2-u2*v1
	return (s1,s2,s3)

def pointproduct3d(u1,u2,u3,v1,v2,v3):
	return u1*v1+u2*v2+u3*v3

def normalize3d(x1,y1,z1):
	n=pow(x1*x1+y1*y1+z1*z1,0.5)
	if n != 0:
		return (x1/n,y1/n,z1/n)
	else:
		return 1

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
					
		v3d_base_x=arrayv[fv[order[0]],1]
		v3d_base_y=arrayv[fv[order[0]],2]
		v3d_base_z=arrayv[fv[order[0]],3]
		v3d_1_x=arrayv[fv[order[1]],1]
		v3d_1_y=arrayv[fv[order[1]],2]
		v3d_1_z=arrayv[fv[order[1]],3]
		v3d_2_x=arrayv[fv[order[2]],1]
		v3d_2_y=arrayv[fv[order[2]],2]
		v3d_2_z=arrayv[fv[order[2]],3]


		fn=crossproduct3d(v3d_1_x-v3d_base_x,v3d_1_y-v3d_base_y,v3d_1_z-v3d_base_z,v3d_2_x-v3d_base_x,v3d_2_y-v3d_base_y,v3d_2_z-v3d_base_z)
		facenormal=normalize3d(fn[0],fn[1],fn[2])

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
				for lj in range(q1_,q2_+1):
					px = li-vit_[1,1]
					py = lj-vit_[1,2]
					mu=(t1y*px-t1x*py)/(t1y*t2x-t1x*t2y)
					lam=(t2y*px-t2x*py)/(t2y*t1x-t2x*t1y)

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
							dv=normalize3d((v3d_x-cx),(v3d_y-cy),(v3d_z-cz))
							#if pointproduct3d(facenormal[0],facenormal[1],facenormal[2],dv[0],dv[1],dv[2]) > 0.8:
								#dpt=0
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
		v3d_base_x=arrayv[fv[order[2]],1]
		v3d_base_y=arrayv[fv[order[2]],2]
		v3d_base_z=arrayv[fv[order[2]],3]
		v3d_1_x=arrayv[fv[order[1]],1]
		v3d_1_y=arrayv[fv[order[1]],2]
		v3d_1_z=arrayv[fv[order[1]],3]
		v3d_2_x=arrayv[fv[order[0]],1]
		v3d_2_y=arrayv[fv[order[0]],2]
		v3d_2_z=arrayv[fv[order[0]],3]

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
							dv=normalize3d((v3d_x-cx),(v3d_y-cy),(v3d_z-cz))
							#if pointproduct3d(facenormal[0],facenormal[1],facenormal[2],dv[0],dv[1],dv[2]) > 0.8:
								#dpt=0
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
		if rimg_pd[i,j]>dpt_max and rimg_pd[i,j]<100000:
			dpt_max = rimg_pd[i,j]
		if rimg_pd[i,j]<dpt_min:
			dpt_min = rimg_pd[i,j]

print 'depth range: ',dpt_min,dpt_max

dimg = Image.new( 'RGB', rimg.size, "green") # create a new black image
pixels = dimg.load() # create the pixel map

for i in range(dimg.size[0]):   
    for j in range(dimg.size[1]):
        if rimg_pd[i,j]<100000:
        	pixels[i,j] = (int((rimg_pd[i,j]-dpt_min)/(dpt_max-dpt_min)*255),int((rimg_pd[i,j]-dpt_min)/(dpt_max-dpt_min)*255),int((rimg_pd[i,j]-dpt_min)/(dpt_max-dpt_min)*255)) # set the colour accordingly
        else:
        	pixels[i,j] = (255,0,0)


#dimg.show()
dimg.save(model_file[:-(4+len(obj_name))] + 'depth.png')
'''
dc_img = Image.new( 'RGB', rimg.size, (255,255,255))
pixdc = dc_img.load()

#depth jump
for i in range(1,dimg.size[0]):   
    for j in range(1,dimg.size[1]):
    	def dis2d(a,b):
    		#print a[0],a[1],a[2],b[0],b[1],b[2]
    		return (a[0]-b[0])*(a[0]-b[0])+(a[1]-b[1])*(a[1]-b[1])+(a[2]-b[2])*(a[2]-b[2])
    	if pixels[i,j] == (255,0,0):
    		pixdc[i,j] = (0,0,0)
    		continue
    	if dis2d(pixels[i,j],pixels[i-1,j])+dis2d(pixels[i,j],pixels[i,j-1])>100:
    		pixdc[i,j] = (0,0,0)

dc_img.save(model_file[:-(4+len(obj_name))] + 'depth_1.png')

#gradient jump
for i in range(2,dimg.size[0]):   
    for j in range(2,dimg.size[1]):
      	if pixels[i,j] == (255,0,0):
    		pixdc[i,j] = (0,0,0)
    		continue
    	g1x=abs(rimg_pd[i-2,j]-rimg_pd[i-1,j])
    	g1y=abs(rimg_pd[i-1,j-1]-rimg_pd[i-1,j])
    	g2x=abs(rimg_pd[i,j-2]-rimg_pd[i,j-1])
    	g2y=abs(rimg_pd[i-1,j-1]-rimg_pd[i,j-1])
    	g3x=abs(rimg_pd[i-1,j]-rimg_pd[i,j])
    	g3y=abs(rimg_pd[i,j-1]-rimg_pd[i,j])
    	gax=(g1x+g2x+g3x)/3.0
    	gay=(g1y+g2y+g3y)/3.0
    	#print abs(gax-g1x)+abs(gax-g2x)+abs(gax-g3x)+abs(gay-g1y)+abs(gay-g2y)+abs(gay-g3y)
    	if abs(gax-g1x)+abs(gax-g2x)+abs(gax-g3x)+abs(gay-g1y)+abs(gay-g2y)+abs(gay-g3y)>10:
    		pixdc[i,j] = (0,0,0)

dc_img.save(model_file[:-(4+len(obj_name))] + 'depth_2.png')

dc_img_2 = Image.new( 'RGB', rimg.size, (255,255,255))
pixdc_2 = dc_img_2.load()
for i in range(0,dimg.size[0]):   
    for j in range(0,dimg.size[1]):
    	pixdc_2[i,j]=pixdc[i,j]

border = 8
for i in range(1,dimg.size[0]-1):   
    for j in range(1,dimg.size[1]-1):
    	if pixdc[i,j] == (0,0,0) and (pixdc[i-1,j] != (0,0,0) or pixdc[i-1,j-1] != (0,0,0) or pixdc[i-1,j+1] != (0,0,0) or pixdc[i,j-1] != (0,0,0) or pixdc[i,j+1] != (0,0,0) or pixdc[i+1,j-1] != (0,0,0) or pixdc[i+1,j] != (0,0,0) or pixdc[i+1,j+1] != (0,0,0)):
    		for pi in range(-border,border+1):
    			for pj in range(-border,border+1):
    				if pi*pi+pj*pj<2*border*border and i+pi>=0 and i+pi<dimg.size[0] and j+pj>=0 and j+pj<dimg.size[1]:
    					pixdc_2[i+pi,j+pj]=(0,0,0)

dc_img_2.save(model_file[:-(4+len(obj_name))] + 'depth-jump.png')
'''

group_number=np.zeros((1),dtype=int)
group_number[0]=cim
texture_name=np.zeros((cim),dtype='S300')
t_size_x=np.zeros((cim),dtype=int)
t_size_y=np.zeros((cim),dtype=int)
label=np.zeros((cim,1000,1000,2),dtype='u2')
pixel=np.zeros((cim,1000,1000,3),dtype='u2')

ep = 0.02
for i in range(1,cim+1):
	t_size_x[i-1]=1000
	t_size_y[i-1]=1000
	texture_name[i-1]=img_name[i][len(model_file[:-(4+len(obj_name))]):]
	for li in range(0,img[i].size[0]):
		for lj in range(0,img[i].size[1]):

			if img_rd[i][li,lj]>0:
				px=img_rx[i][li,lj]
				py=img_ry[i][li,lj]
				label[i-1,li,lj,0] = px
				label[i-1,li,lj,1] = py
				pixel[i-1,li,lj,0] = img_p[i][li,lj][0]
				pixel[i-1,li,lj,1] = img_p[i][li,lj][1]
				pixel[i-1,li,lj,2] = img_p[i][li,lj][2]

				if px<rimg.size[0]-1:
					px_=px+1
				else:
					px_=px
				if py<rimg.size[1]-1:
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

				#print img_size_x,img_size_y,px,py,px_,py_,px__,py__
				dpt=max(rimg_pd[px__,py__],rimg_pd[px__,py_],rimg_pd[px__,py],rimg_pd[px_,py__],rimg_pd[px_,py_],rimg_pd[px_,py],rimg_pd[px,py__],rimg_pd[px,py_],rimg_pd[px,py])
				
				if img_rd[i][li,lj]>dpt+ep:
					img_p[i][li,lj]=(255,0,0)
					pixel[i-1,li,lj,0] = 256
					pixel[i-1,li,lj,1] = 0
					pixel[i-1,li,lj,2] = 0

				#print px,py,rimg_mask.getpixel((px,py))[0]

				if rimg_mask.getpixel((px,py))[0]<100:
					img_p[i][li,lj]=(255,0,0)
					label[i-1,li,lj,0] = 60000
					label[i-1,li,lj,1] = 60000
					pixel[i-1,li,lj,0] = 256
					pixel[i-1,li,lj,1] = 0
					pixel[i-1,li,lj,2] = 0					
			else:
				label[i-1,li,lj,0] = 60000
				label[i-1,li,lj,1] = 60000
				pixel[i-1,li,lj,0] = 0
				pixel[i-1,li,lj,1] = 256
				pixel[i-1,li,lj,2] = 0

'''
if False: # naive completion
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
'''


for i in range(1,cim+1):
	img[i].save(img_name[i])

spio.savemat(os.path.dirname(model_file)+'/texture_m.mat',{'group_number':group_number,'name':texture_name,'size_x':t_size_x,'size_y':t_size_y,'pixel':pixel,'label':label})

f2.close()




