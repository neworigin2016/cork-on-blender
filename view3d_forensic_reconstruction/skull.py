import bpy

from .exceptions import *

def skull_import(context, filepath, decimate_factor):
    try:
        bpy.ops.import_mesh.stl.poll()
    except AttributeError:
        raise ImportSTLException()

    # import STL mesh
    res = bpy.ops.import_mesh.stl(filepath=filepath)

    if res != {'FINISHED'}:
        raise ImportSkullException()

    skull = context.object
    decimate = skull.modifiers.new('Decimate', type='DECIMATE')
    decimate.ratio = decimate_factor

    # apply the modifier
    res = {'CANCELLED'}
    if bpy.ops.object.modifier_apply.poll():
        res = bpy.ops.object.modifier_apply(apply_as='DATA', modifier='Decimate')

    if res != {'FINISHED'}:
        raise ImportSkullDecimateException(skull.name)

    # expand the view to the new object
    res = {'CANCELLED'}
    if bpy.ops.view3d.view_all.poll():
        res = bpy.ops.view3d.view_all()

    if res != {'FINISHED'}:
        raise ImportSkullViewAllException()

