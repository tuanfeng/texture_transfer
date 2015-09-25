# texture_transfer


clean obj file (clean_info)

	python clean.py model.obj model_c.obj 

parameterization: generate uv coordinate

	/Applications/blender.app/Contents/MacOS/blender -b empty.blend -P parameterization.py > log

initial texture image

	python textureinit.py model_p.obj model_t.obj
