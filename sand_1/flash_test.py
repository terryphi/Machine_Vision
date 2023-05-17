import bpy
from mathutils import Vector
import random
import shutil

#prepare the output folder
shutil.rmtree('C:/Users/robot22/Documents/beacon_locate/Machine_Vision/sand_1/img/', ignore_errors=True)

# Generate random coordinates and save to file
num_coords = 1
coords = [(round(random.uniform(-0.5, 0.5), 3), round(random.uniform(-0.5, 0.5), 3), round(random.uniform(-0.5, 0.5), 3)) for _ in range(num_coords)]

for coord in coords:
    # Delete all objects
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    #print the coordinate with the text "the coordinate is: " before it
    print("the coordinate is: ", coord)
    # Create a sphere with red material
    bpy.ops.mesh.primitive_uv_sphere_add(location=coord)
    bpy.ops.transform.resize(value=(0.01, 0.01, 0.01))
    sphere = bpy.context.object
    mat = bpy.data.materials.new(name="RedMaterial")
    mat.diffuse_color = (1, 0, 0, 1)
    sphere.data.materials.append(mat)

    # Make the sphere flash at 30 Hz
    bpy.context.scene.frame_end = 30#120  # Set the end frame for a 2-second animation at 60 fps
    for frame in range(120):  # Loop through each frame
        sphere.hide_render = frame % 2 == 0  # Hide the sphere every other frame
        sphere.keyframe_insert(data_path="hide_render", frame=frame)  # Insert a keyframe
    # Create a cube with semi-transparent blue material
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0))
    cube = bpy.context.object
    cube.scale = (1, 1, 1)
    mat = bpy.data.materials.new(name="Cube_Material")
    cube.data.materials.append(mat)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    nodes.clear()
    principled_node = nodes.new(type='ShaderNodeBsdfPrincipled')
    principled_node.inputs['Base Color'].default_value = (0, 0, 1, 1)
    principled_node.inputs['Alpha'].default_value = 0.05
    output_node = nodes.new(type='ShaderNodeOutputMaterial')
    mat.node_tree.links.new(principled_node.outputs['BSDF'], output_node.inputs['Surface'])
    cube.data.materials[0].blend_method = 'BLEND'
    # Create a camera and set it to look at a specific point
    bpy.ops.object.camera_add(location=(0,3.5,1))
    camera = bpy.context.object
    bpy.context.scene.camera = camera
    direction = Vector((0,0,0)) - camera.location
    rot_quat = direction.to_track_quat('-Z', 'Y')
    camera.rotation_euler = rot_quat.to_euler()
    # Create a light source and a checkerboard plane
    bpy.ops.object.light_add(type='SUN', location=(4, -4, 4))
    bpy.ops.mesh.primitive_plane_add(size=10, location=(0, 0, -1))
    plane = bpy.context.object
    plane_mat = bpy.data.materials.new(name="Plane_Material")
    plane.data.materials.append(plane_mat)
    plane_mat.use_nodes = True
    nodes = plane_mat.node_tree.nodes
    links = plane_mat.node_tree.links
    nodes.clear()
    output = nodes.new("ShaderNodeOutputMaterial")
    diffuse = nodes.new("ShaderNodeBsdfDiffuse")
    checker = nodes.new("ShaderNodeTexChecker")
    checker.inputs["Scale"].default_value = 1000
    links.new(diffuse.inputs["Color"], checker.outputs["Color"])
    links.new(output.inputs["Surface"], diffuse.outputs["BSDF"])
    # Set up rendering of 3D scene and render
    bpy.context.scene.render.image_settings.file_format = 'AVI_JPEG'
    filename = "C:/Users/robot22/Documents/beacon_locate/Machine_Vision/sand_1/img/" + str(coord[0]) + "_" + str(coord[1]) + "_" + str(coord[2]) + ".avi"
    # bpy.context.scene.render.filepath = filename
    bpy.context.scene.render.fps = 60  # Set the frame rate to 60 fps
    bpy.ops.render.render(animation=True, write_still=True)  # Render the animation
