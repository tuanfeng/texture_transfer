# projection


clean obj file (clean_info)

	python clean.py ../data/model/model.obj ../data/model/model_c.obj v f s o

parameterization: generate uv coordinate, using para_info

	/Applications/blender.app/Contents/MacOS/blender -b empty.blend -P parameterization.py > log

initial texture image

	python textureinit.py ../data/model/model_p.obj ../data/model/model_t.obj

get est-view.txt
	
	python ./../../../RenderForCNN-master/demo_render/run_demo.py (est-view.txt on desktop)

project texture image
	
	python textureproj.py ../data/model/image.png ../data/model/model_t.obj ../data/model/est-view.txt
