#usage: python clean.py input_file.obj output_file.obj v f s o

#todo: clean degenerate triangle and unused vertex


import sys

input_file = sys.argv[1]
output_file = sys.argv[2]

#info_file = "clean_info"
argvs = sys.argv[3:]
#f1 = open(info_file,'r')
#tmp = f1.readlines()
#argvs = tmp[0].split()
#f1.close()

f2 = open(input_file,'r')
f3 = open(output_file,'w')
for line in f2.readlines():
	linet = line.split()
	if linet[0] in argvs:
		f3.write(line)

f2.close()
f3.close()

