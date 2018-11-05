import bpy

bpy.context.scene.render.engine = 'CYCLES'

bpy.ops.object.delete(use_global=False)
bpy.ops.mesh.primitive_plane_add(view_align=False, enter_editmode=False, location=(0, 0, 0), layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))
bpy.ops.transform.resize(value=(30, 30, 30), constraint_axis=(False, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
bpy.ops.transform.rotate(value=1.57, axis=(1.0, 0.0, 0.0), constraint_axis=(False, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
bpy.ops.transform.translate(value=(10.0, 10.0, -0.0), constraint_axis=(False, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)

obj_camera = bpy.context.scene.camera
obj_camera.location[0]=10.0
obj_camera.location[1]=-10.0
obj_camera.location[2]=0.0
obj_camera.rotation_mode='XYZ'

obj_camera.rotation_euler[0]=1.57
obj_camera.rotation_euler[1]=0.0
obj_camera.rotation_euler[2]=0.523

obj_camera.scale[0]=10
obj_camera.scale[1]=10
obj_camera.scale[2]=10

# Get material
mat_plane = bpy.data.materials.get("Plane")
if mat_plane is None:
    # create material
    mat_plane = bpy.data.materials.new(name="Plane")

mat_plane.use_nodes=True
nodes=mat_plane.node_tree.nodes
for node in nodes:
    nodes.remove(node)

# create emission node
node_emission = nodes.new(type='ShaderNodeEmission')
node_emission.inputs[0].default_value = (0,1,0,1)  # green RGBA
node_emission.inputs[1].default_value = 4.0 # strength
node_emission.location = 0,0

# create output node
node_output = nodes.new(type='ShaderNodeOutputMaterial')
#node_output.location = 100,0
node_checker=nodes.new(type='ShaderNodeTexChecker')
node_checker.inputs[2].default_value=(0,0,0,1)
node_checker.inputs[3].default_value=20
# link nodes
links = mat_plane.node_tree.links
link = links.new(node_emission.inputs[0], node_checker.outputs[0])
link = links.new(node_emission.outputs[0], node_output.inputs[0])
# Get material
ob = bpy.context.active_object
if ob.data.materials:
    # assign to 1st material slot
    ob.data.materials[0] = mat_plane
else:
    # no slots
    ob.data.materials.append(mat_plane)

for i in range(0,5,1):

        file_loc='/Users/natarajan/Desktop/BlenderTesting/plic_mesh_%0.2d.stl'%i
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
        bpy.context.scene.render.filepath = "./pic%0.2d.jpg"%i
        bpy.ops.render.render(use_viewport = True, write_still=True)
        bpy.data.objects.remove(ob,do_unlink=True)
