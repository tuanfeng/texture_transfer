#usage: python clean.py input_file.obj output_file.obj

#todo: clean degenerate triangle and unused vertex


import sys

input_file = sys.argv[1]
output_file = sys.argv[2]

#info_file = "clean_info"
argvs = ['v','f','o']
#f1 = open(info_file,'r')
#tmp = f1.readlines()
#argvs = tmp[0].split()
#f1.close()

file2 = open(input_file,'r')
file3 = open(output_file,'w')

v1={}
v2={}
v3={}
vm={}
f1={}
f2={}
f3={}
vid=0
fid=0
stb=0
vn=0
vn2=0

for line in file2.readlines():
	linet = line.split()
	if len(linet) == 0:
		continue
	if linet[0] == 'o':

		vn=0
		if len(v1) != 0:
			#clean vertise
			for i in range(1,vid):
				for j in range(i+1,vid+1):
					if (v1[i]-v1[j])*(v1[i]-v1[j])+(v2[i]-v2[j])*(v2[i]-v2[j])+(v3[i]-v3[j])*(v3[i]-v3[j])<0.000001:
						#print 'duplicate vertices detected'
						for p in range(1,fid+1):
							if f1[p]==j: f1[p]=i
							if f2[p]==j: f2[p]=i
							if f3[p]==j: f3[p]=i
						vm[j] = -1000000
						vn=vn+1
						for p in range(j+1,vid+1):
							vm[p]=vm[p]+1
			vn2=vn2+vn
			for i in range(1,vid+1):
				st='v '+str(v1[i])+' '+str(v2[i])+' '+str(v3[i])+'\n'
				if vm[i] >= 0: file3.write(st)

			#clean faces
			for i in range(1,fid+1):

				x1=v1[f2[i]]-v1[f1[i]]
				x2=v2[f2[i]]-v2[f1[i]]
				x3=v3[f2[i]]-v3[f1[i]]
				y1=v1[f3[i]]-v1[f1[i]]
				y2=v2[f3[i]]-v2[f1[i]]
				y3=v3[f3[i]]-v3[f1[i]]

				area=0.5*pow(pow(x2*y3-x3*y2,2)+pow(x3*y1-x1*y3,2)+pow(x1*y2-x2*y1,2),0.5)
				#if 1000*area<=0.000001:
				#	print 'degenearte face detected'

				st='f '+str(f1[i]+stb-(vn2-vn)-vm[f1[i]])+' '+str(f2[i]+stb-(vn2-vn)-vm[f2[i]])+' '+str(f3[i]+stb-(vn2-vn)-vm[f3[i]])+'\n'
				
				for j in range(1,i):
					if f1[i]+f2[i]+f3[i] == f1[j]+f2[j]+f3[j] and f1[i]*f1[i]+f2[i]*f2[i]+f3[i]*f3[i] == f1[j]*f1[j]+f2[j]*f2[j]+f3[j]*f3[j] and f1[i]*f1[i]*f1[i]+f2[i]*f2[i]*f2[i]+f3[i]*f3[i]*f3[i] == f1[j]*f1[j]*f1[j]+f2[j]*f2[j]*f2[j]+f3[j]*f3[j]*f3[j]:
						area=0
						#print 'duplicate face detected'
						break

				if 1000*area>0.000001: file3.write(st)

		file3.write(line)		
		v1={}
		v2={}
		v3={}
		vm={}
		f1={}
		f2={}
		f3={}
		stb=stb+vid
		vid=0
		fid=0

	if linet[0] == 'f':
		fid=fid+1
		f1[fid] = int(linet[1].split('/')[0])-stb
		f2[fid] = int(linet[2].split('/')[0])-stb
		f3[fid] = int(linet[3].split('/')[0])-stb
		
	if linet[0] == 'v':
		vid=vid+1
		v1[vid] = float(linet[1])
		v2[vid] = float(linet[2])
		v3[vid] = float(linet[3])
		vm[vid] = 0

vn=0
if len(v1) != 0:
	for i in range(1,vid):
		for j in range(i+1,vid+1):
			if (v1[i]-v1[j])*(v1[i]-v1[j])+(v2[i]-v2[j])*(v2[i]-v2[j])+(v3[i]-v3[j])*(v3[i]-v3[j])<0.000001:
				#print i,j
				for p in range(1,fid+1):
					if f1[p]==j: f1[p]=i
					if f2[p]==j: f2[p]=i
					if f3[p]==j: f3[p]=i
				vm[j] = -1000000
				vn=vn+1
				for p in range(j+1,vid+1):
					vm[p]=vm[p]+1
	vn2=vn2+vn
	for i in range(1,vid+1):
		st='v '+str(v1[i])+' '+str(v2[i])+' '+str(v3[i])+'\n'
		if vm[i] >= 0: file3.write(st)
	for i in range(1,fid+1):
		st='f '+str(f1[i]+stb-(vn2-vn)-vm[f1[i]])+' '+str(f2[i]+stb-(vn2-vn)-vm[f2[i]])+' '+str(f3[i]+stb-(vn2-vn)-vm[f3[i]])+'\n'
		file3.write(st)


file2.close()
file3.close()

