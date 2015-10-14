# projection


data format 
	
	texture_m.mat: t_size_x,t_size_y,label[i][x,y],pixel[i][x,y]
	image_m.mat: size_x,size_y,depth[x,y]


clean obj file (clean_info)

	python clean.py ../../../data/model/model.obj ../../../data/model/model_c.obj 

parameterization: generate uv coordinate, update para_info first

	para_info

	/Applications/blender.app/Contents/MacOS/blender -b empty.blend -P parameterization.py > log

texture_m to texture images
	
	python texturegen.py ../data/model/texture_m.mat ../data/model/texture/








initial texture image

	python textureinit.py ../data/model/model_p.obj ../data/model/model_t.obj

get est-view.txt
	
	python ./../../../RenderForCNN-master/demo_render/run_demo.py (est-view.txt on desktop)

project texture image
	
	python textureproj.py ../data/model/image.png ../data/model/model_t.obj ../data/model/est-view.txt
