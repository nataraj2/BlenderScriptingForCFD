import bpy

bpy.context.scene.render.engine = 'CYCLES'

bpy.ops.object.delete(use_global=False)
bpy.ops.wm.open_mainfile(filepath="DropScene.blend")

for i in range(0,5,1):

	file_loc='plic_mesh_%0.2d.stl'%i
	drop=bpy.ops.import_mesh.stl(filepath=file_loc)
	mat_drop = bpy.data.materials.get("Drop")
	if mat_drop is None:
		# create material
		mat_drop = bpy.data.materials.new(name="Drop")

	mat_drop.use_nodes=True
	nodes=mat_drop.node_tree.nodes
	for node in nodes:
	    nodes.remove(node)

	refractionshader = nodes.new(type='ShaderNodeBsdfRefraction')
	glossyshader = nodes.new(type='ShaderNodeBsdfGlossy')
	glossyshader.inputs[1].default_value=0.0
	mixshader = nodes.new(type='ShaderNodeMixShader')
	dropoutput = nodes.new(type='ShaderNodeOutputMaterial')

	links = mat_drop.node_tree.links
	link = links.new(refractionshader.outputs[0], mixshader.inputs[1])
	link = links.new(glossyshader.outputs[0], mixshader.inputs[2])
	link = links.new(mixshader.outputs[0], dropoutput.inputs[0])
	#objname = "Plic Mesh %02d"%i
	#bpy.data.objects[objname].scale[0]=1.0

	 # Get material
	ob = bpy.context.active_object
	if ob.data.materials:
	# assign to 1st material slot
		ob.data.materials[1] = mat_drop
	else:
	# no slots
		ob.data.materials.append(mat_drop)
#bpy.context.scene.objects.active = ob

	for area in bpy.context.screen.areas:
		if area.type == 'VIEW_3D':
			area.spaces[0].viewport_shade = 'RENDERED'
       
	bpy.context.scene.render.image_settings.file_format='JPEG'
	bpy.context.scene.render.filepath = "pic%0.2d.jpg"%i
	bpy.ops.render.render(use_viewport = True, write_still=True)
	bpy.ops.object.select_all(action='DESELECT')
	bpy.data.objects[3].select=True
	bpy.ops.object.delete() 
	#bpy.data.objects.remove(ob,do_unlink=True)

