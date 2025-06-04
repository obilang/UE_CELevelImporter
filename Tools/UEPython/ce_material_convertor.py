import os
import xml.etree.ElementTree as ET
from collections import defaultdict
import ce_path_utils
from typing import List

class Texture:
    def __init__(self):
        self.Filter = None
        self.IsTileU = None
        self.Map = None
        self.IsTileV = None
        self.File = None
        self.TileU = 1.0
        self.TileV = 1.0

    def __repr__(self):
        return f"Texture(Map={self.Map}, File={self.File})"

class Material:
    def __init__(self, name) -> None:
        self.name = name
        # Material attributes
        self.Emittance = None
        self.VoxelCoverage = None
        self.FurAmount = None
        self.Emissive = None
        self.CloakAmount = None
        self.Opacity = None
        self.StringGenMask = None
        self.GlowAmount = None
        self.vertModifType = None
        self.MtlFlags = None
        self.Shininess = None
        self.Diffuse = None
        self.HeatAmountScaled = None
        self.Shader = None
        self.CustomSortPriority = None
        self.MatTemplate = None
        self.SurfaceType = None
        self.Specular = None
        self.AlphaTest = None
        self.GenMask = None
        self.LayerAct = None
        # PublicParams attributes
        self.WeaponBloodColor = None
        self.WeaponQualityZone2 = None
        self.MaskSaturation3 = None
        self.FresnelPower = None
        self.FresnelScale = None
        self.DirOverlayX = None
        self.DecalFalloff = None
        self.DetailDiffuseScale = None
        self.RandomValueOffset = None
        self.BlendLayer2Specular = None
        self.ColorizingHue = None
        self.SelfShadowStrength = None
        self.WeaponBloodSpecular = None
        self.ObmDisplacement = None
        self.AmbientMultiplier = None
        self.MaskBrightness2 = None
        self.RandomValueScale = None
        self.WeaponQualityZone0 = None
        self.TessellationFactorMin = None
        self.WeaponQualityZone5 = None
        self.FresnelBias = None
        self.BlendMaskTiling = None
        self.WeaponBloodBlendFactor = None
        self.ColorizingSaturation = None
        self.WeaponBloodBlendFalloff = None
        self.OverlayDetailR = None
        self.OverlayDetailG = None
        self.BackFaceBrightnessMult = None
        self.HeightBias = None
        self.DirOverlayThresholdMin = None
        self.WeaponBloodGloss = None
        self.BlendFactor = None
        self.MaskBrightness3 = None
        self.DecalAlphaMult = None
        self.OverlayTiling = None
        self.GlossFromDiffuseOffset = None
        self.DirOverlayTilingU = None
        self.SubsurfaceScatteringAmount = None
        self.EmittanceMapGamma = None
        self.SndUVsTileV = None
        self.IndirectColor = None
        self.SSSIndex = None
        self.WeaponQualityZone6 = None
        self.WeaponBloodTexScale = None
        self.WeaponQualityZone4 = None
        self.MaskSaturation1 = None
        self.GlossFromDiffuseContrast = None
        self.MaskHue2 = None
        self.DirOverlayThresholdMax = None
        self.ColorizingBrightness = None
        self.GlossFromDiffuseBrightness = None
        self.MaskBrightness1 = None
        self.MaskHue1 = None
        self.GlossFromDiffuseAmount = None
        self.BlendLayer2Tiling = None
        self.DirOverlayTilingV = None
        self.WeaponQualityZone7 = None
        self.SndUVsTileU = None
        self.WeaponRustBlendFalloff = None
        self.TessellationFaceCull = None
        self.BlendFalloff = None
        self.DirOverlayZ = None
        self.MaskSaturation2 = None
        self.WeaponQualityZone1 = None
        self.NumTexParts = None
        self.WeaponRustTexScale = None
        self.DetailGlossScale = None
        self.DirOverlayBumpScale = None
        self.TessellationFactor = None
        self.DecalDiffuseOpacity = None
        self.DebugUVScale = None
        self.PomDisplacement = None
        self.TessellationFactorMax = None
        self.WeaponQualityZone3 = None
        self.WeaponRustBlendFactor = None
        self.WeaponRustBlend = None
        self.MaskHue3 = None
        self.OverlayDetailB = None
        self.DirOverlayY = None
        self.DetailBumpScale = None
        # Textures
        self.textures = []
        
    def get_enabled_switches(self):
        enabled_switches = self.StringGenMask.split('%') if self.StringGenMask else []
        if len(enabled_switches) > 1:
            enabled_switches.remove('')  # Remove empty strings
        return enabled_switches

    def __repr__(self):
        return f"Material(name={self.name}, textures={self.textures})"

def parse_mtl_file(file_path) -> List[Material]:
    import xml.etree.ElementTree as ET
    materials = []
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        sub_node = root.find(".//SubMaterials")
        if sub_node is None:
            print(f"SubMaterials not found in {file_path}")
            return materials

        for material_elem in sub_node.findall("Material"):
            mat = Material(material_elem.attrib.get("Name", "").replace(".", "_"))
            # Set Material attributes
            for k, v in material_elem.attrib.items():
                if hasattr(mat, k):
                    setattr(mat, k, v)
            # Parse <Textures>
            textures_elem = material_elem.find("Textures")
            if textures_elem is not None:
                for tex_elem in textures_elem.findall("Texture"):
                    tex = Texture()
                    for k, v in tex_elem.attrib.items():
                        if hasattr(tex, k):
                            setattr(tex, k, v)
                    texmod_elem = tex_elem.find("TexMod")
                    if texmod_elem is not None:
                        tex.TileU = float(texmod_elem.attrib.get("TileU", 1.0))
                        tex.TileV = float(texmod_elem.attrib.get("TileV", 1.0))
                    mat.textures.append(tex)
            # Parse <PublicParams>
            public_params_elem = material_elem.find("PublicParams")
            if public_params_elem is not None:
                for k, v in public_params_elem.attrib.items():
                    if hasattr(mat, k):
                        setattr(mat, k, v)
            materials.append(mat)
    except ET.ParseError as e:
        print(f"Error parsing {file_path}: {e}")
    return materials

def collect_unique_attributes(directory):
    # Dictionary to store unique attributes for each element type
    unique_attributes = defaultdict(set)

    # Recursively iterate through all files in the directory and subdirectories
    for root_dir, _, files in os.walk(directory):
        for filename in files:
            if filename.endswith(".mtl"):
                file_path = os.path.join(root_dir, filename)
                print(file_path)
                try:
                    # Parse the XML file
                    tree = ET.parse(file_path)
                    root = tree.getroot()

                    # Collect attributes for each element type
                    sub_node = root.find(".//SubMaterials")
                    if sub_node is None:
                        print(f"SubMaterials not found in {file_path}")
                        continue
                    for material in sub_node.findall("Material"):
                        shader_type = material.attrib.get("Shader")
                        if shader_type != "Illum":
                            print(f"ShaderType{shader_type} is not Illum in {file_path}")
                            continue
                        
                        unique_attributes["Material"].update(material.attrib.keys())

                        for child in material:
                            unique_attributes[child.tag].update(child.attrib.keys())

                            for subchild in child:
                                unique_attributes[subchild.tag].update(subchild.attrib.keys())

                except ET.ParseError as e:
                    print(f"Error parsing {file_path}: {e}")

    return unique_attributes

# # Get the results and print them
# unique_attributes = collect_unique_attributes(ce_path_utils.CRY_ENGINE_OUTPUT_FOLDER_ROOT)
# print(unique_attributes)
# for element_type, attributes in unique_attributes.items():
#     print(f"{element_type}: {', '.join(attributes)}")


def find_material_by_name(materials, name):
    for mat in materials:
        if mat.name == name:
            return mat
    return None

def find_texture_by_path(mat_data, texture_name, is_gloss=False):
    texture_path = None
    for tex in mat_data.textures:
        if tex.Map == texture_name:
            texture_path = tex.File
            break
    
    if not texture_path:
        print(f"Texture {texture_name} not found in material {mat_data.name}")
        return None
    
    texture_path = texture_path.replace('.tif', '')
    texture_path = texture_path.replace('.dds', '')
    texture_path = f"/Game/Old/{texture_path}"
    
    if is_gloss:
        texture_path += "_glossmap"
    
    import unreal
    if unreal.EditorAssetLibrary.does_asset_exist(texture_path):
        return unreal.EditorAssetLibrary.load_asset(texture_path)
    else: 
        unreal.log_warning(f"Texture asset not found: {texture_path}")
        return None
    
def get_texture_tiling(mat_data, texture_name):
    for tex in mat_data.textures:
        if tex.Map == texture_name:
            return (tex.TileU, tex.TileV)
    return (1.0, 1.0)  # Default tiling if not found

def str_to_vec3(s):
    parts = s.split(',')
    if len(parts) == 3:
        return [float(part.strip()) for part in parts]
    return [0.0, 0.0, 0.0]  # Default if parsing fails

def create_material_instance(material_data: Material, target_path, mesh_name):
    import unreal
    PARENT_MATERIAL_PATH = "/Game/Materials/CE/M_CE_Illum"
    parent_material = unreal.EditorAssetLibrary.load_asset(PARENT_MATERIAL_PATH)
    
    target_package_name = f"{target_path}/mtl_{mesh_name}_{material_data.name}"
    material_instance = None
    if unreal.EditorAssetLibrary.does_asset_exist(target_package_name):
        unreal.EditorAssetLibrary.delete_asset(target_package_name)
        # material_instance = unreal.EditorAssetLibrary.load_asset(target_package_name)
    # Create the material instance
    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()

    factory = unreal.MaterialInstanceConstantFactoryNew()

    material_instance = asset_tools.create_asset(
        asset_name=f"mtl_{mesh_name}_{material_data.name}",
        package_path=target_path,
        asset_class=unreal.MaterialInstanceConstant,
        factory=factory
    )
    
    if material_instance:
        material_instance.set_editor_property("parent", parent_material)
        # set material properties
        mat_edit_lib = unreal.MaterialEditingLibrary
        diffuse_tex = find_texture_by_path(material_data, "Diffuse")
        if diffuse_tex:
            mat_edit_lib.set_material_instance_texture_parameter_value(material_instance, "Diffuse", diffuse_tex)
        bump_tex = find_texture_by_path(material_data, "Bumpmap")
        if bump_tex:
            mat_edit_lib.set_material_instance_texture_parameter_value(material_instance, "Bumpmap", bump_tex)
        gloss_tex = find_texture_by_path(material_data, "Bumpmap", is_gloss=True)
        if gloss_tex:
            mat_edit_lib.set_material_instance_texture_parameter_value(material_instance, "Bumpmap Gloss", gloss_tex)
        specular_tex = find_texture_by_path(material_data, "Specular")
        if specular_tex:
            mat_edit_lib.set_material_instance_texture_parameter_value(material_instance, "Specular", specular_tex)
            
        if material_data.Diffuse:
            mat_edit_lib.set_material_instance_vector_parameter_value(
                material_instance, "MatDiffuse", str_to_vec3(material_data.Diffuse))
        if material_data.Specular:
            mat_edit_lib.set_material_instance_vector_parameter_value(
                material_instance, "MatSpecular", str_to_vec3(material_data.Specular))

        enabled_switches = material_data.get_enabled_switches()
        if "BLENDLAYER" in enabled_switches:
            mat_edit_lib.set_material_instance_static_switch_parameter_value(
                material_instance, "BLENDLAYER", True)
            if material_data.BlendFactor:
                mat_edit_lib.set_material_instance_scalar_parameter_value(
                    material_instance, "BlendFactor", float(material_data.BlendFactor))
            if material_data.BlendMaskTiling:
                mat_edit_lib.set_material_instance_scalar_parameter_value(
                    material_instance, "BlendMaskTiling", float(material_data.BlendMaskTiling))
            if material_data.BlendFalloff:
                mat_edit_lib.set_material_instance_scalar_parameter_value(
                    material_instance, "BlendFalloff", float(material_data.BlendFalloff))
            if material_data.BlendLayer2Tiling:
                mat_edit_lib.set_material_instance_scalar_parameter_value(
                    material_instance, "BlendLayer2Tiling", float(material_data.BlendLayer2Tiling))
            if material_data.BlendLayer2Specular:
                mat_edit_lib.set_material_instance_scalar_parameter_value(
                    material_instance, "BlendLayer2Specular", float(material_data.BlendLayer2Specular))
            custom_tex = find_texture_by_path(material_data, "Custom")
            if custom_tex:
                mat_edit_lib.set_material_instance_texture_parameter_value(
                    material_instance, "Custom", custom_tex)
            custom_1_tex = find_texture_by_path(material_data, "[1] Custom")
            if custom_1_tex:
                mat_edit_lib.set_material_instance_texture_parameter_value(
                    material_instance, "[1] Custom", custom_1_tex)
            custom_1_gloss_tex = find_texture_by_path(material_data, "[1] Custom", is_gloss=True)
            if custom_1_gloss_tex:
                mat_edit_lib.set_material_instance_texture_parameter_value(
                    material_instance, "[1] Custom Gloss", custom_1_gloss_tex)
            opacity_tex = find_texture_by_path(material_data, "Opacity")
            if opacity_tex:
                mat_edit_lib.set_material_instance_texture_parameter_value(
                    material_instance, "Opacity", opacity_tex)
        
        if "DETAIL_MAPPING" in enabled_switches:
            mat_edit_lib.set_material_instance_static_switch_parameter_value(
                material_instance, "DETAIL_MAPPING", True)
            detail_tex = find_texture_by_path(material_data, "Detail")
            if detail_tex:
                mat_edit_lib.set_material_instance_texture_parameter_value(
                    material_instance, "Detail", detail_tex)
        
        if "DETAIL_ATLAS" in enabled_switches:
            mat_edit_lib.set_material_instance_static_switch_parameter_value(
                material_instance, "DETAIL_ATLAS", True)
            mat_edit_lib.set_material_instance_static_switch_parameter_value(
                material_instance, "DETAIL_MAPPING", True)
            detail_atlas_tex = find_texture_by_path(material_data, "Detail")
            mat_edit_lib.set_material_instance_texture_parameter_value(
                material_instance, "DetailMask", detail_atlas_tex)
        
        if "DETAIL_ATLAS" in enabled_switches or "DETAIL_MAPPING" in enabled_switches:
            if material_data.DetailDiffuseScale:
                mat_edit_lib.set_material_instance_scalar_parameter_value(
                    material_instance, "DetailDiffuseScale", float(material_data.DetailDiffuseScale))
            if material_data.DetailGlossScale:
                mat_edit_lib.set_material_instance_scalar_parameter_value(
                    material_instance, "DetailGlossScale", float(material_data.DetailGlossScale))
            if material_data.DetailBumpScale:
                mat_edit_lib.set_material_instance_scalar_parameter_value(
                    material_instance, "DetailBumpScale", float(material_data.DetailBumpScale))
            tile_u, tile_v = get_texture_tiling(material_data, "Detail")
            mat_edit_lib.set_material_instance_scalar_parameter_value(
                material_instance, "Detail Tile U", float(tile_u))
            mat_edit_lib.set_material_instance_scalar_parameter_value(
                material_instance, "Detail Tile V", float(tile_v))
            
        if "USE_FIRST_UV_DETMAP" in enabled_switches:
            mat_edit_lib.set_material_instance_static_switch_parameter_value(
                material_instance, "USE_FIRST_UV_DETMAP", True)
        
        if "SNDUVS" in enabled_switches:
            mat_edit_lib.set_material_instance_static_switch_parameter_value(
                material_instance, "SNDUVS", True)
            snd_uvs_tex = find_texture_by_path(material_data, "[1] Diffuse")
            if snd_uvs_tex:
                mat_edit_lib.set_material_instance_texture_parameter_value(
                    material_instance, "[1] Diffuse", snd_uvs_tex)
            if material_data.SndUVsTileU:
                mat_edit_lib.set_material_instance_scalar_parameter_value(
                    material_instance, "SndUVsTileU", float(material_data.SndUVsTileU))
            if material_data.SndUVsTileV:
                mat_edit_lib.set_material_instance_scalar_parameter_value(
                    material_instance, "SndUVsTileV", float(material_data.SndUVsTileV))
            
            
        unreal.EditorAssetLibrary.save_loaded_asset(material_instance)
        return material_instance
    
    return None

def create_and_assign_mat_to_mesh(mesh_data):
    import unreal
    static_mesh = unreal.EditorAssetLibrary.load_asset(mesh_data.package_name)
    
    mesh_path = str(mesh_data.package_path)
    name = str(mesh_data.asset_name)
    source_folder = os.path.join(ce_path_utils.CRY_ENGINE_OUTPUT_FOLDER_ROOT, mesh_path.replace('/Game/Old/', ''))
    if os.path.exists(source_folder):
        for mat_slot in static_mesh.static_materials:
            mat_slot_name = str(mat_slot.material_slot_name)
            
            parts = []
            if '_mtl__' in mat_slot_name:
                parts = mat_slot_name.split('_mtl__')
            elif '_mtl_' in mat_slot_name:
                parts = mat_slot_name.split('_mtl_')
            
            if len(parts) != 2:
                unreal.log_warning(f"Material slot name {mat_slot_name} does not match expected format, skipping.")
                continue
            
            mtl_file = parts[0]
            mat_name = parts[1]
        
            target_mat = os.path.join(source_folder, mtl_file + ".mtl")
            materials = None
            if os.path.exists(target_mat):
                materials = parse_mtl_file(target_mat)
            
                mat_data = find_material_by_name(materials, mat_name)
                if mat_data:
                    if mat_data.Shader != "Illum":
                        unreal.log_warning(f"Material {mat_data.name} is not Illum, skipping.")
                        continue
                    material_instance = create_material_instance(mat_data, mesh_path, mesh_data.asset_name)
                    if material_instance:
                        mat_slot.material_interface = material_instance
                        static_mesh.set_material(static_mesh.get_material_index(mat_slot.material_slot_name), material_instance)
            else:
                unreal.log_warning(f"Material file not found: {target_mat}")
        unreal.EditorAssetLibrary.save_loaded_asset(static_mesh)
    

def create_and_assign_mat_to_selected_meshes():
    import unreal
    editor_util_lib = unreal.EditorUtilityLibrary
    selected_assets = editor_util_lib.get_selected_asset_data()
    
    with unreal.ScopedSlowTask(len(selected_assets), "Importing Materials..") as slow_task:
        # display the dialog
        slow_task.make_dialog(True)
        
        for selected_asset in selected_assets:
            if slow_task.should_cancel():
                break
            slow_task.enter_progress_frame(1, "Importing Materials For {}".format(selected_asset.asset_name))
            create_and_assign_mat_to_mesh(selected_asset)


if __name__ == "__main__":
    create_and_assign_mat_to_selected_meshes()