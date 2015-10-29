# projection


data format 
	
	texture_m.mat: group_number,name[i],size_x[i],size_y[i],pixel[i,x,y,0:2]


clean obj file (clean_info)

	python clean.py ../../../data/model/model.obj ../../../data/model/model_c.obj 

parameterization: generate uv coordinate, update para_info first

	para_info

	/Applications/blender.app/Contents/MacOS/blender -b empty.blend -P parameterization.py > log

initial texture image

	python textureinit.py ../../../data/model/model_p.obj ../../../data/model/model_t.obj

get est-view.txt
	
	python ../../../RenderForCNN-master/demo_render/run_demo.py (est-view.txt on desktop)

creat mask

	matlab >> polygon_mask('../../../data/model6/image.jpg','../../../data/model6/mask.png',true);

project texture image
	
	python textureproj.py ../../../data/model/image.png ../../../data/model/mask.png ../../../data/model/model_t.obj ../../../data/model/est-view.txt

	python textureproj.py ../../../data/fabricut_based/case0/image.jpg ../../../data/fabricut_based/case0/mask.png ../../../data/fabricut_based/case0/model_t.obj ../../../data/fabricut_based/case0/est-view.txt

texture_m.mat to texture images

	python texturem2t.py ./matfile.mat

graph based completion (based on Image Completion Approaches Using the Statistics of Similar Patches)
	
	python completion_offset.py ../../../data/model/texture_m.mat ../../../data/model/texture_m_c.mat

	python completion_.py ../../../data/model/texture_m_c.mat ../../../data/model/texture_m_c2.mat