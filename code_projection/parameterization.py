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
base_path = os.path.dirname(task_info_[1])

Scenename = 'Scene'

#input_file = "/Users/tuanfeng/Documents/ResearchWork/project_2/code/texture_transfer/model_clean.obj"

bpy.ops.import_scene.obj(filepath=input_file)

for objs in bpy.data.objects:
	objs.select = False


newpath = base_path + '/uv_layout/' 
if not os.path.exists(newpath): os.makedirs(newpath)

cc=0
for objs in bpy.data.objects:
	if objs.type == 'MESH':
		
		cc=cc+1
		objs.select = True
		bpy.context.scene.objects.active = objs
		bpy.ops.object.mode_set(mode = 'EDIT')#bpy.ops.object.editmode_toggle()
		bpy.ops.mesh.normals_make_consistent(inside=False)
		bpy.ops.mesh.quads_convert_to_tris()
		bpy.ops.object.mode_set(mode = 'OBJECT')
		bpy.ops.uv.smart_project(angle_limit=66.0, island_margin=0.0, user_area_weight=0.0)
		bpy.ops.uv.export_layout(filepath=newpath + "uv_"+objs.name + ".png", check_existing=False, export_all=False, mode='PNG', size=(1024,1024), opacity=0.25)
		objs.select = False

bpy.ops.export_scene.obj(filepath=output_file,check_existing=False,use_materials=False)