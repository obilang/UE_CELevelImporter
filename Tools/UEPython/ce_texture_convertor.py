import os
import shutil
import subprocess
import ce_path_utils
# import dds2png


def copy_dds_files_with_structure(source_dir, target_dir):
    for root, _, files in os.walk(source_dir):
        # Filter for .dds and its variants
        dds_files = [f for f in files if f.endswith('.dds') or '.dds.' in f]
        
        for dds_file in dds_files:
            base_name = dds_file.split('.dds')[0]  # Extract base name
            base_path = os.path.join(root, base_name + '.dds')
            
            # Determine relative path for subfolder structure
            relative_path = os.path.relpath(root, source_dir)
            target_subfolder = os.path.join(target_dir, relative_path)
            os.makedirs(target_subfolder, exist_ok=True)
            
            # Copy all files with the same base name
            for variant in files:
                if variant.startswith(base_name + '.dds'):
                    source_file = os.path.join(root, variant)
                    target_file = os.path.join(target_subfolder, variant)
                    
                    # Rename base .dds to .dds.0 in the target folder
                    if variant == base_name + '.dds':
                        target_file = os.path.join(target_subfolder, base_name + '.dds.0')
                    
                    shutil.copy2(source_file, target_file)
                    print(f"Copied: {source_file} -> {target_file}")
                    

def process_dds_files(target_dir, tool_path):
    for root, _, files in os.walk(target_dir):
        for file in files:
            if file.endswith('.dds'):
                dds_file_path = os.path.join(root, file)
                base_name = file[:-4]  # Remove '.dds.0' to get the base name
                
                # Construct the command
                command = [tool_path, dds_file_path, '-s']
                # command = [tool_path, dds_file_path]
                try:
                    # Execute the command
                    subprocess.run(command, check=True)
                    print(f"Processed: {dds_file_path}")
                    
                    combined_file_path = os.path.join(root, base_name + '.combined.dds')
                    print(combined_file_path)
                    # Delete all .dds.x files for this base name
                    # for variant in files:
                    #     if variant.startswith(base_name + '.dds'):
                    #         variant_path = os.path.join(root, variant)
                    #         os.remove(variant_path)
                    #         print(f"Deleted: {variant_path}")
                    
                    # filename = dds_file_path.replace(".dds.0", ".dds")
                    # (base_filename, filename_ext) = os.path.splitext(filename)
                    # output_filename = base_filename + '.png'
                    # # Load DDS file using imageio
                    # dds_image = imageio.imread(filename)
                    # # Convert numpy array to PIL image
                    # image = Image.fromarray(dds_image)
                    # # Save as TGA
                    # image.save(output_filename)
                    
                except subprocess.CalledProcessError as e:
                    print(f"Error processing {dds_file_path}: {e}")
                
                command = [nvtt_export_path, combined_file_path, '-o', combined_file_path.replace('.dds', '.tga')]   
                try:
                    # Execute the command
                    subprocess.run(command, check=True)
                    print(f"Processed: {combined_file_path}")
                except subprocess.CalledProcessError as e:
                    print(f"Error processing {combined_file_path}: {e}") 
                
                print(file)   
                break


def import_dds_to_unreal(target_dir):
    import unreal
    import asset_import_utils
    tasks = []
    should_break = False
    for root, _, files in os.walk(target_dir):
        for file in files:
            file = file.lower()
            if file.endswith('.tga'):
                dds_file_path = os.path.join(root, file)
                package_name = dds_file_path.replace(target_dir, "/Game/Old").replace("\\", "/")
                package_name = package_name.replace('.tga', '')
                package_path = package_name[:package_name.rfind("/")]
                name = package_name.split("/")[-1]
                
                if unreal.EditorAssetLibrary.does_asset_exist(package_name):
                    # print(f"Asset already exists: {package_name}")
                    continue
                task = asset_import_utils.build_input_task_simple(dds_file_path, package_path, name)
                tasks.append(task)
            #     should_break = True
            #     break
            # if should_break:
            #     break
                
    asset_import_utils.execute_import_tasks(tasks)
                

# Define source and target directories
source_directory = r"D:\temp\Cryengine"
target_directory = r"D:\GameDev\UnrealEngine-release\KCD1Re\ArtRaw"
tool_path = r"D:\GameDev\UnrealEngine-release\KCD1Re\Tools\AssetConverter\DDS-Unsplitter.exe"
nvtt_export_path = r"C:\Program Files\NVIDIA Corporation\NVIDIA Texture Tools\nvtt_export.exe"

# Execute the function
# copy_dds_files_with_structure(ce_path_utils.CRY_ENGINE_OUTPUT_FOLDER_ROOT, target_directory)

# script_dir = os.path.dirname(os.path.abspath(__file__))
# converter_exe = os.path.join(script_dir, "../DDS-Unsplitter.exe")
# process_dds_files(ce_path_utils.CRY_ENGINE_OUTPUT_FOLDER_ROOT, tool_path)

import_dds_to_unreal(target_directory)