import bpy
from mathutils import Vector
import random
import shutil
import os

def prepare_output_folder(folder_path):
    shutil.rmtree(folder_path, ignore_errors=True)
    os.makedirs(folder_path, exist_ok=True)

def create_random_coordinates(num_coords=1):
    return [(round(random.uniform(-0.5, 0.5), 3), round(random.uniform(-0.5, 0.5), 3), round(random.uniform(-0.5, 0.5), 3)) for _ in range(num_coords)]

def delete_all_objects():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

def create_sphere(coord):
    bpy.ops.mesh.primitive_uv_sphere_add(location=coord)
    bpy.ops.transform.resize(value=(0.01, 0.01, 0.01))
    sphere = bpy.context.object
    mat = bpy.data.materials.new(name="RedMaterial")
    mat.diffuse_color = (1, 0, 0, 1)
    sphere.data.materials.append(mat)
    return sphere

def make_sphere_flash(sphere):
    bpy.context.scene.frame_end = 30
    for frame in range(120):
        sphere.hide_render = frame % 2 == 0
        sphere.keyframe_insert(data_path="hide_render", frame=frame)

def create_cube():
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
    return cube

def create_camera_and_light():
    bpy.ops.object.camera_add(location=(0,3.5,1))
    camera = bpy.context.object
    bpy.context.scene.camera = camera
    direction = Vector((0,0,0)) - camera.location
    rot_quat = direction.to_track_quat('-Z', 'Y')
    camera.rotation_euler = rot_quat.to_euler()

    bpy.ops.object.light_add(type='SUN', location=(4, -4, 4))
    return camera

def create_plane():
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
    return plane

def render_scene(filename):
    bpy.context.scene.render.image_settings.file_format = 'AVI_JPEG'
    bpy.context.scene.render.fps = 60
    bpy.ops.render.render(animation=True, write_still=True)

def main():
    output_folder = 'C:/Users/robot22/Documents/beacon_locate/Machine_Vision/sand_1/img/'
    prepare_output_folder(output_folder)
    coords = create_random_coordinates()
    for coord in coords:
        delete_all_objects()
        print("the coordinate is: ", coord)
        sphere = create_sphere(coord)
        make_sphere_flash(sphere)
        create_cube()
        create_camera_and_light()
        create_plane()
        filename = output_folder + str(coord[0]) + "_" + str(coord[1]) + "_" + str(coord[2]) + ".avi"
        render_scene(filename)

main()