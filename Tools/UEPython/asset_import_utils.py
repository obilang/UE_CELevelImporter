import unreal


def build_input_task_simple(filename, destination_path, destination_name='', option=None):
    unreal.log("Build Import Task: {} to {} as {}".format(filename, destination_path, destination_name))
    
    task = unreal.AssetImportTask()
    task.set_editor_property('automated', True)
    task.set_editor_property('destination_name', destination_name)
    task.set_editor_property('destination_path', destination_path)
    task.set_editor_property('filename', filename)
    task.set_editor_property('replace_existing', True)
    task.set_editor_property('save', True)
    if option:
        task.set_editor_property('options', option)
    return task


def execute_import_tasks(tasks=[]):
    unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks(tasks)
    imported_asset_paths = []
    for task in tasks:
        for imported_object in task.get_objects():
            imported_asset_paths.append(imported_object.get_package().get_path_name())

    return imported_asset_paths


def build_staticmesh_import_options():
    options = unreal.FbxImportUI()
    # unreal.FbxImportUI
    options.set_editor_property('import_mesh', True)
    options.set_editor_property('import_textures', False)
    options.set_editor_property('import_materials', False)
    options.set_editor_property('import_as_skeletal', False)  # Static Mesh
    # unreal.FbxMeshImportData
    options.static_mesh_import_data.set_editor_property('import_translation', unreal.Vector(0.0, 0.0, 0.0))
    options.static_mesh_import_data.set_editor_property('import_rotation', unreal.Rotator(0.0, 0.0, 0.0))
    options.static_mesh_import_data.set_editor_property('import_uniform_scale', 1.0)
    # unreal.FbxStaticMeshImportData
    options.static_mesh_import_data.set_editor_property('combine_meshes', True)
    options.static_mesh_import_data.set_editor_property('generate_lightmap_u_vs', False)
    options.static_mesh_import_data.set_editor_property('auto_generate_collision', True)
    options.static_mesh_import_data.set_editor_property('one_convex_hull_per_ucx', True)
    options.static_mesh_import_data.set_editor_property('build_nanite', True)
    # force fix the normal from cgf
    options.static_mesh_import_data.set_editor_property('recompute_normals', True)
    
    return options


def open_editor_for_asset(asset_path):
    if not unreal.EditorAssetLibrary.does_asset_exist(asset_path):
        raise Exception('Fail to find asset: {}'.format(asset_path))
    asset_obj = unreal.load_asset(asset_path)
    # close the editor if opened or it won't refresh
    asset_subsystem = unreal.get_editor_subsystem(unreal.AssetEditorSubsystem)
    asset_subsystem.close_all_editors_for_asset(asset_obj)
    asset_subsystem.open_editor_for_assets([asset_obj])