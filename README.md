# texture_transfer


clean obj file (clean_info)

	python clean.py model.obj model_c.obj 

parameterization: generate uv coordinate

	/Applications/blender.app/Contents/MacOS/blender -b empty.blend -P parameterization.py > log

initial texture image

	python textureinit.py model_p.obj model_t.obj

get est-view.txt
	
	/../RenderForCNN-master/demo_render/run_demo.py (est-view.txt on desktop)

project texture image
	
	python image.png model_t.obj est_view.txt
