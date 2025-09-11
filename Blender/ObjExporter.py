## TODO: Add suport for models with multiple materials.
    # index = 0
    # for mat in obj.data.materials:
    #     imgMat = mat.node_tree.nodes[-1]
    #     srcPath = imgMat.image.filepath
    #     newPath = os.path.join(filePath, f"texture_diffuse{index}.png")
    #     imgMat.image.save(filepath = newPath, quality=0, save_copy=True)

## exports each selected object into its own file.
import bpy
import os

def ObjExport(obj):
    '''
    For each object in the selection: 
    - Set that object as the only selected object.
    - Make a new directory with the object's name.
    - Make a copy of textures in the new directory.
    - Set material to use texture in new directory.
    - Export model.
    - Reset material attributes.
    '''
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj

    name = bpy.path.clean_name(obj.name)
    filePath = baseDir + '/' + name
    os.mkdir(filePath)

    srcImgPath = obj.data.materials[0].node_tree.nodes[-1].image.filepath
    newImgPath = os.path.join(filePath, "texture_diffuse.png")
    obj.data.materials[0].node_tree.nodes[-1].image.save(filepath=newImgPath, quality=0, save_copy=True)
    obj.data.materials[0].node_tree.nodes[-1].image.filepath = newImgPath

    fn = os.path.join(filePath, name)
    bpy.ops.wm.obj_export(filepath=fn + '.obj', export_selected_objects=True)
    obj.data.materials[0].node_tree.nodes[-1].image.filepath = srcImgPath
    obj.select_set(False)
    print("written:", fn)

def ObjExportPIL(obj):
    '''
    For each object in the selection: 
    - Set that object as the only selected object.
    - Make a new directory with the object's name.
    - Make a copy of textures in the new directory.
    - Set material to use texture in new directory.
    - Export model.
    - Reset material attributes.
    '''
    from PIL import Image
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj

    name = bpy.path.clean_name(obj.name)
    filePath = baseDir + '/' + name
    os.mkdir(filePath)

    texPath = obj.data.materials[0].node_tree.nodes[-1].image.filepath_from_user()
    newPath = os.path.join(filePath, "texture_diffuse.png")
    txDiff = Image.open(texPath)
    txDiff.save(newPath)

    srcImgPath = obj.data.materials[0].node_tree.nodes[-1].image.filepath
    obj.data.materials[0].node_tree.nodes[-1].image.filepath = newPath

    fn = os.path.join(filePath, name)
    bpy.ops.wm.obj_export(filepath=fn + '.obj', export_selected_objects=True)
    obj.data.materials[0].node_tree.nodes[-1].image.filepath = texPath
    obj.select_set(False)
    print("written:", fn)

## Check if blender version is above 4.4. This is because the image.save function only allows saving as a copy in versions 4.4 and above.
version = bpy.app.version
valid = False
if(version[0] >=4 and version[1] >= 4):
    valid = True

## Check if user has installed PIL.
if(not valid):
    print("Blender version below 4.4, attempting export using PIL module.")
    modPath = bpy.utils.user_resource("SCRIPTS", path="modules")
    if not os.path.isdir(os.path.join(modPath, "PIL")):
        error = f'Missing PIL module. Install module to blender modules directory using the command: pip install pillow --target="{modPath}"'
        raise Exception(error)

## export to blend file location.
baseDir = os.path.dirname(bpy.data.filepath)
if not baseDir:
    raise Exception("Blend file is not saved")

## Get selected objects in scene.
selection = bpy.context.selected_objects
bpy.ops.object.select_all(action='DESELECT')

for obj in selection:
    if valid:
        ObjExport(obj)
    else:
        ObjExportPIL(obj)

## Reset selection.
for obj in selection:
    obj.select_set(True)

print("Export complete.")