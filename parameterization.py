#usage: /Applications/blender.app/Contents/MacOS/blender -b empty.blend -P parameterization.py > log
#para_into: input, output obj mesh

import os
import sys
import bpy

task_info=open('para_info','r')
#task_info=open('/Users/tuanfeng/Documents/ResearchWork/project_2/code/texture_transfer/para_info','r')

task_info_ = task_info.read().splitlines();

input_file = task_info_[0]
output_file = task_info_[1]

Scenename = 'Scene'

#input_file = "/Users/tuanfeng/Documents/ResearchWork/project_2/code/texture_transfer/model_clean.obj"

bpy.ops.import_scene.obj(filepath=input_file)
obj_name = os.path.splitext(os.path.basename(input_file))[0]

for objs in bpy.data.objects:
	objs.select = False

for objs in bpy.data.objects:
	if objs.type == 'MESH':
		objs.select = True
		bpy.context.scene.objects.active = objs
		bpy.ops.object.mode_set(mode = 'EDIT')#bpy.ops.object.editmode_toggle()
		bpy.ops.mesh.normals_make_consistent(inside=False)
		bpy.ops.object.mode_set(mode = 'OBJECT')
		bpy.ops.uv.smart_project(angle_limit=66.0, island_margin=0.0, user_area_weight=0.0)
		objs.select = False

bpy.ops.export_scene.obj(filepath=output_file,check_existing=False,use_materials=False)