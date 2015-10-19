#usage: python completion_offset.py texture_m.mat texture_m_c.mat

import os
import sys
import scipy.io as spio
import numpy as np
#from PIL import Image

matfile = sys.argv[1]
output = sys.argv[2]

mat = spio.loadmat(matfile)
name = mat['name']
group_number = mat['group_number']
size_x = mat['size_x']
size_y = mat['size_y']
pixel = mat['pixel']

ou_size_x=np.zeros((group_number[0]),dtype=int)
ou_size_y=np.zeros((group_number[0]),dtype=int)
ou_pixel=np.zeros((group_number[0],250,250,3),dtype='u2')
ou_offset=np.zeros((group_number[0],500,500),dtype='u2')

dis_limit = 5.0


for i in range(0,group_number[0]):
	print name[i]
	patch_size=5
	patch_count=0
	patch_set={}
	patch_dis={}
	patch_tid={}
	offset=np.zeros((size_x[0,i],size_y[0,i]),'u2')

	ou_size_x[i]=250
	ou_size_y[i]=250
	
	#pixels=pixel[i]

	tp=np.zeros((500,500,3),dtype='u2')

	for pi in range(0,500):
		for pj in range(0,500):
			tp[pi,pj,0]=int(float(pixel[i,pi*2,pj*2,0]+pixel[i,pi*2+1,pj*2,0]+pixel[i,pi*2,pj*2+1,0]+pixel[i,pi*2+1,pj*2+1,0])/4.0)
			tp[pi,pj,1]=int(float(pixel[i,pi*2,pj*2,1]+pixel[i,pi*2+1,pj*2,1]+pixel[i,pi*2,pj*2+1,1]+pixel[i,pi*2+1,pj*2+1,1])/4.0)
			tp[pi,pj,2]=int(float(pixel[i,pi*2,pj*2,2]+pixel[i,pi*2+1,pj*2,2]+pixel[i,pi*2,pj*2+1,2]+pixel[i,pi*2+1,pj*2+1,2])/4.0)
			if pixel[i,pi*2,pj*2,0]>255 or pixel[i,pi*2+1,pj*2,0]>255 or pixel[i,pi*2,pj*2+1,0]>255 or pixel[i,pi*2+1,pj*2+1,0]>255:
				tp[pi,pj,0]=256
				tp[pi,pj,1]=0
				tp[pi,pj,2]=0
			if pixel[i,pi*2,pj*2,1]>255 or pixel[i,pi*2+1,pj*2,1]>255 or pixel[i,pi*2,pj*2+1,1]>255 or pixel[i,pi*2+1,pj*2+1,1]>255:
				tp[pi,pj,0]=0
				tp[pi,pj,1]=256
				tp[pi,pj,2]=0


	for pi in range(0,250):
		for pj in range(0,250):
			ou_pixel[i,pi,pj,0]=int(float(tp[pi*2,pj*2,0]+tp[pi*2+1,pj*2,0]+tp[pi*2,pj*2+1,0]+tp[pi*2+1,pj*2+1,0])/4.0)
			ou_pixel[i,pi,pj,1]=int(float(tp[pi*2,pj*2,1]+tp[pi*2+1,pj*2,1]+tp[pi*2,pj*2+1,1]+tp[pi*2+1,pj*2+1,1])/4.0)
			ou_pixel[i,pi,pj,2]=int(float(tp[pi*2,pj*2,2]+tp[pi*2+1,pj*2,2]+tp[pi*2,pj*2+1,2]+tp[pi*2+1,pj*2+1,2])/4.0)
			if tp[pi*2,pj*2,0]>255 or tp[pi*2+1,pj*2,0]>255 or tp[pi*2,pj*2+1,0]>255 or tp[pi*2+1,pj*2+1,0]>255:
				ou_pixel[i,pi,pj,0]=256
				ou_pixel[i,pi,pj,1]=0
				ou_pixel[i,pi,pj,2]=0
			if tp[pi*2,pj*2,1]>255 or tp[pi*2+1,pj*2,1]>255 or tp[pi*2,pj*2+1,1]>255 or tp[pi*2+1,pj*2+1,1]>255:
				ou_pixel[i,pi,pj,0]=0
				ou_pixel[i,pi,pj,1]=256
				ou_pixel[i,pi,pj,2]=0

	for pi in range(patch_size,ou_size_x[i]-patch_size-1,2):
		#print pi,patch_count
		for pj in range(patch_size,ou_size_y[i]-patch_size-1,2):
			if ou_pixel[i,pi,pj,0]>255 or ou_pixel[i,pi,pj,1]>255:
				continue
			if ou_pixel[i,pi,pj-patch_size,0]>255 or ou_pixel[i,pi,pj-patch_size,1]>255:
				continue
			if ou_pixel[i,pi,pj+patch_size+1,0]>255 or ou_pixel[i,pi,pj+patch_size+1,1]>255:
				continue
			if ou_pixel[i,pi-patch_size,pj,0]>255 or ou_pixel[i,pi-patch_size,pj,1]>255:
				continue
			if ou_pixel[i,pi-patch_size,pj-patch_size,0]>255 or ou_pixel[i,pi-patch_size,pj-patch_size,1]>255:
				continue
			if ou_pixel[i,pi-patch_size,pj+patch_size+1,0]>255 or ou_pixel[i,pi-patch_size,pj+patch_size+1,1]>255:
				continue
			if ou_pixel[i,pi+patch_size+1,pj,0]>255 or ou_pixel[i,pi+patch_size+1,pj,1]>255:
				continue
			if ou_pixel[i,pi+patch_size+1,pj-patch_size,0]>255 or ou_pixel[i,pi+patch_size+1,pj-patch_size,1]>255:
				continue
			if ou_pixel[i,pi+patch_size+1,pj+patch_size+1,0]>255 or ou_pixel[i,pi+patch_size+1,pj+patch_size+1,1]>255:
				continue


			flag = True
			for ti in range(pi-patch_size,pi+patch_size+1,2):
				for tj in range(pj-patch_size,pj+patch_size+1,2):
					#print i,ti,tj
					if ti<0 or ti>=size_x[0,i] or tj<0 or tj>=size_y[0,i]:
						flag = False
					elif ou_pixel[i,ti,tj,0]>255 or ou_pixel[i,ti,tj,1]>255:
						flag = False
					if not flag:
						break
				if not flag:
					break
			if flag:
				patch_count = patch_count + 1
				patch_set[patch_count] = (pi,pj)
				patch_dis[patch_count] = 100000000
				patch_tid[patch_count] = -1
					#print '++++++',pi,pj
	print 'patch number: ', patch_count 

	for di in range(1,patch_count):
		#print di
		for dj in range(di+1,patch_count+1):
			di0=patch_set[di][0]
			dj0=patch_set[dj][0]
			di1=patch_set[di][1]
			dj1=patch_set[dj][1]
			ddi=patch_dis[di]
			ddj=patch_dis[dj]

			if (di0-dj0)*(di0-dj0)+(di1-dj1)*(di1-dj1)<dis_limit*dis_limit:
				continue

			diff=0.0
			flag=True
			for pi in range(-patch_size, patch_size+1):
				for pj in range(-patch_size, patch_size+1):

					def getabs(a,b):
						if a>b:
							return a-b
						else:
							return b-a

					diff=diff+getabs(ou_pixel[i,di0+pi,di1+pj,0],ou_pixel[i,dj0+pi,dj1+pj,0])
					diff=diff+getabs(ou_pixel[i,di0+pi,di1+pj,1],ou_pixel[i,dj0+pi,dj1+pj,1])
					diff=diff+getabs(ou_pixel[i,di0+pi,di1+pj,2],ou_pixel[i,dj0+pi,dj1+pj,2])
					if diff>ddi:
						flag = False
					if diff>ddj:
						flag = False
					if not flag:
						break
				if not flag:
					break

			if diff<patch_dis[di]:
				patch_dis[di] = diff
				patch_tid[di] = dj
			if diff<patch_dis[dj]:
				patch_dis[dj] = diff
				patch_tid[dj] = di


	for di in range(1,patch_count+1):
		tag_x=patch_set[patch_tid[di]][0]-patch_set[di][0]
		tag_y=patch_set[patch_tid[di]][1]-patch_set[di][1]
#		if tag_x<0:
#			tag_x = -tag_x
#			tag_y = - tag_y
		ou_offset[i,tag_x+250,tag_y+250] = ou_offset[i,tag_x+250,tag_y+250]+1

spio.savemat(output,{'group_number':group_number,'name':name,'size_x':ou_size_x,'size_y':ou_size_y,'pixel':ou_pixel,'offset':ou_offset})

		













