#usage: python completion_.py texture_m_c.mat texture_m_c2.mat

import os
import sys
import scipy.io as spio
import numpy as np
from subprocess import call

#from pygco.pygco import cut_simple
#from PIL import Image

matfile = sys.argv[1]
output = sys.argv[2]

mat = spio.loadmat(matfile)
name = mat['name']
group_number = mat['group_number']
size_x = mat['size_x']
size_y = mat['size_y']
pixel = mat['pixel']
pixel_ori = mat['pixel_ori']

new_size = 250

pixel_=np.zeros((group_number[0],new_size,new_size,3),dtype='u2')

for img_id in range(0,group_number[0]):
	#size_x[0,img_id] = new_size
	#size_y[0,img_id] = new_size

	for pi in range(0,new_size):#size_x[0,img_id]):
		for pj in range(0,new_size):#size_y[0,img_id]):
			pixel_[img_id,pi,pj]=pixel[img_id,pi,pj]

offset = mat['offset']
peak = 50

for img_id in range(0,group_number[0]):

	
	sortx = np.zeros((peak,3),int)
	
	for pi in range(0,2*size_x[0,img_id]):
		for pj in range(0,2*size_y[0,img_id]):
			ids=peak-1
			while ids>=0 and sortx[ids,0]<offset[img_id,pi,pj]:
				if ids == peak-1:
					sortx[ids,0]=offset[img_id,pi,pj]
					sortx[ids,1]=pi-250
					sortx[ids,2]=pj-250
					ids = ids - 1
				else:
					sortx[ids+1,0]=sortx[ids,0]
					sortx[ids+1,1]=sortx[ids,1]
					sortx[ids+1,2]=sortx[ids,2]					
					sortx[ids,0]=offset[img_id,pi,pj]
					sortx[ids,1]=pi-250
					sortx[ids,2]=pj-250
					ids = ids - 1		


	offs = np.zeros((peak*8,2),int)
	for iii in range(0,peak):
		offs[iii,0]=sortx[iii,1]*int(new_size/250)
		offs[iii,1]=sortx[iii,2]*int(new_size/250)
		offs[iii+peak,0]=sortx[iii,1]*2*int(new_size/250)
		offs[iii+peak,1]=sortx[iii,2]*2*int(new_size/250)
		offs[iii+2*peak,0]=sortx[iii,1]*3*int(new_size/250)
		offs[iii+2*peak,1]=sortx[iii,2]*3*int(new_size/250)
		offs[iii+3*peak,0]=sortx[iii,1]*4*int(new_size/250)
		offs[iii+3*peak,1]=sortx[iii,2]*4*int(new_size/250)
		offs[iii+4*peak,0]=sortx[iii,1]*5*int(new_size/250)
		offs[iii+4*peak,1]=sortx[iii,2]*5*int(new_size/250)
		offs[iii+5*peak,0]=sortx[iii,1]*6*int(new_size/250)
		offs[iii+5*peak,1]=sortx[iii,2]*6*int(new_size/250)
		offs[iii+6*peak,0]=sortx[iii,1]*7*int(new_size/250)
		offs[iii+6*peak,1]=sortx[iii,2]*7*int(new_size/250)
		offs[iii+7*peak,0]=sortx[iii,1]*8*int(new_size/250)
		offs[iii+7*peak,1]=sortx[iii,2]*8*int(new_size/250)


	flag_all = True
	count_all = 0

	size_x[0,img_id] = new_size
	size_y[0,img_id] = new_size

	while flag_all:
	
		reglabel = np.zeros((size_x[0,img_id],size_y[0,img_id]),'u2')
		reglabel_ = np.zeros((size_x[0,img_id],size_y[0,img_id]),'u2')

		count_before = count_all
		count_all=0

		for pi in range(0,size_x[0,img_id]):
			for pj in range(0,size_y[0,img_id]):
				if pixel_[img_id,pi,pj,0]>255:
					reglabel[pi,pj]=3
					count_all = count_all + 1
				elif pixel_[img_id,pi,pj,1]>255:
					reglabel[pi,pj]=4
				else:
					reglabel[pi,pj]=0
	
		print count_all, "pixels to compelet"

		if count_all < 50 or count_all == count_before:
			flag_all = False
			continue

		for pi in range(0,size_x[0,img_id]):
			for pj in range(0,size_y[0,img_id]):
				reglabel_[pi,pj] = reglabel[pi,pj]


		for pi in range(0,size_x[0,img_id]):
			for pj in range(0,size_y[0,img_id]):
				if reglabel[pi,pj] == 0:
					flag = False
					for di in range(-1,2):
						for dj in range(-1,2):
							if pi+di>=0 and pi+di<size_x[0,img_id] and pj+dj>=0 and pj+dj<size_y[0,img_id]:
								if reglabel[pi+di,pj+dj] == 3:
									flag = True
					if flag:
						for di in range(-9,10):
							for dj in range(-9,10):
								if pi+di>=0 and pi+di<size_x[0,img_id] and pj+dj>=0 and pj+dj<size_y[0,img_id]:
									if reglabel[pi+di,pj+dj] == 0 and di*di+dj*dj<=4:
										reglabel_[pi+di,pj+dj] = 1
									if reglabel[pi+di,pj+dj] == 3 and di*di+dj*dj<=81:
										reglabel_[pi+di,pj+dj] = 2

		fid = open('tmp_1','w')
		fid.write(str(size_x[0,img_id])+' '+str(size_y[0,img_id])+' '+str(peak*16)+'\n')
		for pi in range(0,size_x[0,img_id]):
			for pj in range(0,size_y[0,img_id]):
				fid.write(str(pixel_[img_id,pi,pj,0])+' '+str(pixel_[img_id,pi,pj,1])+' '+str(pixel_[img_id,pi,pj,2])+' '+str(reglabel_[pi,pj])+'\n')
	
		for offid in range(0,peak*8):
			fid.write(str(offs[offid,0])+' '+str(offs[offid,1])+'\n')		 
		for offid in range(0,peak*8):
			fid.write(str(-offs[offid,0])+' '+str(-offs[offid,1])+'\n')		 

		fid.close()

		call(["./gco-v3/main"])
	
		fid2 = open('tmp_2','r')
		for line in fid2.readlines():
			linet = line.split()
			pix_loc_1=int(linet[0])
			pix_loc_2=int(linet[1])
			off_1=int(linet[2])
			off_2=int(linet[3])
			new_loc_1=pix_loc_1+off_1
			new_loc_2=pix_loc_2+off_2
			if new_loc_1>=0 and new_loc_1<size_x[0,img_id] and new_loc_2>=0 and new_loc_2<size_y[0,img_id]:
				if reglabel_[new_loc_1,new_loc_2] < 2:
					pixel_[img_id,pix_loc_1,pix_loc_2,0]=pixel_[img_id,new_loc_1,new_loc_2,0]
					pixel_[img_id,pix_loc_1,pix_loc_2,1]=pixel_[img_id,new_loc_1,new_loc_2,1]
					pixel_[img_id,pix_loc_1,pix_loc_2,2]=pixel_[img_id,new_loc_1,new_loc_2,2]

		fid2.close()

	print "+++++++++++++++++++++++++++++",count_all
	#delete tmp_1,tmp_2


spio.savemat(output,{'pixel':pixel,'pixel_':pixel_,'reglabel':reglabel,'reglabel_':reglabel_})






