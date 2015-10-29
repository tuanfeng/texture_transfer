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

vertices = {}
v_flag = {}
faces = {}
objs = {}
obj_id = 0
v_id = 0
f_id = 0

f2 = open(input_file,'r')
f3 = open(output_file,'w')

for line in f2.readlines():
	linet = line.split()
	if len(linet) == 0:
		continue
	if linet[0] == argvs[0]:
		f3.write(line)
	if linet[0] == argvs[1]:
		fa1 = linet[1].split('/')[0]
		fa2 = linet[2].split('/')[0]
		fa3 = linet[3].split('/')[0]
		st='f '+fa1+' '+fa2+' '+fa3+'\n'
		f3.write(st)
	if linet[0] == argvs[2]:
		f3.write(line)


f2.close()
f3.close()

