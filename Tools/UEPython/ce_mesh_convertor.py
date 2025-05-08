import os
import subprocess

CRY_ENGINE_OUTPUT_FOLDER_ROOT = "D:/temp/rataja"
LEVEL_ROOT_FOLDER = "data/levels"  # Removed leading slash for consistency
LEVEL_LAYERS_FOLDER = "layers"
LEVEL_EDITOR_XML = "level.editor_xml"
PREFAB_ROOT_FOLDER = 'prefabs'

LEVEL_NAME = "rataje"

def convert_meshes_from_list(file_path):
    """
    Reads a list of mesh paths from a file and converts each using the cgf-converter tool.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    converter_exe = os.path.join(script_dir, "../cgf-converter.exe")
    with open(file_path, 'r') as file:
        for line in file:
            mesh_path = line.strip()
            if not mesh_path:
                continue
            full_mesh_path = os.path.join(CRY_ENGINE_OUTPUT_FOLDER_ROOT, mesh_path.replace("/", os.sep))
            command = [converter_exe, full_mesh_path, "-dae", "-group"]
            try:
                print(f"Executing: {' '.join(command)}")
                subprocess.run(command, check=True)
            except subprocess.CalledProcessError as e:
                print(f"Error converting {mesh_path}: {e}")




def import_meshes_to_unreal(file_path):
    import unreal
    import asset_import_utils
    with open(file_path, 'r') as file:
        tasks = []
        for line in file:
            mesh_path = line.strip()
            if not mesh_path:
                continue
            mesh_path = mesh_path.replace(".cgf", ".fbx")
            fbx_path = os.path.join(CRY_ENGINE_OUTPUT_FOLDER_ROOT, mesh_path.replace("/", os.sep))
            
            package_name = f"/Game/Old/{mesh_path.replace('.fbx', '')}"
            package_path = package_name[:package_name.rfind("/")]
            name = package_name.split("/")[-1]
            if os.path.exists(fbx_path):
                option = asset_import_utils.build_staticmesh_import_options()
                task = asset_import_utils.build_input_task_simple(fbx_path, package_path, name, option)
                tasks.append(task)
            else:
                unreal.log_error("File not found: {}".format(fbx_path))
        asset_import_utils.execute_import_tasks(tasks)
        
if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    mesh_list_file = os.path.join(script_dir, "convert_mesh_list.txt")
    convert_meshes_from_list(mesh_list_file)
    # import_meshes_to_unreal(mesh_list_file)


