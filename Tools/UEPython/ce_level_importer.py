import os
import xml.etree.ElementTree as ET

CRY_ENGINE_OUTPUT_FOLDER_ROOT = "D:/temp/rataja"
LEVEL_ROOT_FOLDER = "data/levels"  # Removed leading slash for consistency
LEVEL_LAYERS_FOLDER = "layers"
LEVEL_EDITOR_XML = "level.editor_xml"
PREFAB_ROOT_FOLDER = 'prefabs'

LEVEL_NAME = "rataje"

LAYER_WHITELIST = [
    "Rataje",
]

class StaticMesh:
    def __init__(self):
        self.name = None
        self.pos = None
        self.rotate = None
        self.scale = None
        self.mesh_path = None
        
    def init_from_brush_xml(self, xml_node):
        self.name = xml_node.get("Name") if "Name" in xml_node.attrib else None
        self.pos = xml_node.get("Pos") if "Pos" in xml_node.attrib else "0.0,0.0,0.0"
        self.rotate = xml_node.get("Rotate") if "Rotate" in xml_node.attrib else "0.0,0.0,0.0,0.0"
        self.scale = xml_node.get("Scale") if "Scale" in xml_node.attrib else "1.0,1.0,1.0"
        self.mesh_path = xml_node.get("Prefab") if "Prefab" in xml_node.attrib else None
        
    def init_from_geo_xml(self, xml_node):
        self.name = xml_node.get("Name") if "Name" in xml_node.attrib else None
        self.pos = xml_node.get("Pos") if "Pos" in xml_node.attrib else "0.0,0.0,0.0"
        self.rotate = xml_node.get("Rotate") if "Rotate" in xml_node.attrib else "0.0,0.0,0.0,0.0"
        self.scale = xml_node.get("Scale") if "Scale" in xml_node.attrib else "1.0,1.0,1.0"
        self.mesh_path = xml_node.get("Geometry") if "Geometry" in xml_node.attrib else None
        
        
class PrefabActor:
    def __init__(self):
        self.name = None
        self.pos = None
        self.rotate = None
        self.scale = None
        self.prefab_name = None
        
    def init_from_brush_xml(self, xml_node):
        self.name = xml_node.get("Name") if "Name" in xml_node.attrib else None
        self.pos = xml_node.get("Pos") if "Pos" in xml_node.attrib else "0.0,0.0,0.0"
        self.rotate = xml_node.get("Rotate") if "Rotate" in xml_node.attrib else "0.0,0.0,0.0,0.0"
        self.scale = xml_node.get("Scale") if "Scale" in xml_node.attrib else "1.0,1.0,1.0"
        self.prefab_name = xml_node.get("PrefabName") if "PrefabName" in xml_node.attrib else None


class Layer:
    def __init__(self, name):
        self.name = name
        self.prefab_actors = []
        self.static_meshes = []
        self.child_layers = []
        
    def init_from_xml(self, xml_node):
        # self.name = xml_node.get("Name") if "Name" in xml_node.attrib else None
        self.prefab_actors = []
        self.static_meshes = []
        self.child_layers = []

        # Iterate through child objects
        objects_node = xml_node.find(".//LayerObjects")
        if objects_node is not None:
            for obj_node in objects_node.findall("Object"):
                obj_type = obj_node.get("Type")
                if obj_type == "Prefab":
                    prefab_actor = PrefabActor()
                    prefab_actor.init_from_brush_xml(obj_node)
                    self.prefab_actors.append(prefab_actor)
                elif obj_type == "GeomEntity":
                    static_mesh = StaticMesh()
                    static_mesh.init_from_geo_xml(obj_node)
                    self.static_meshes.append(static_mesh)
                elif obj_type == "Brush":
                    static_mesh = StaticMesh()
                    static_mesh.init_from_brush_xml(obj_node)
                    self.static_meshes.append(static_mesh)
        
        child_layers_node = xml_node.find(".//ChildLayers")
        layers_node = child_layers_node.findall("Layer") if child_layers_node is not None else None
        if layers_node is not None:
            for layer_node in layers_node:
                fullname = layer_node.get("FullName")
                name = layer_node.get("Name")
                
                layer_xml_path = os.path.join(CRY_ENGINE_OUTPUT_FOLDER_ROOT, LEVEL_ROOT_FOLDER, LEVEL_NAME, LEVEL_LAYERS_FOLDER, f"{fullname}.lyr")
                if os.path.exists(layer_xml_path):
                    tree = ET.parse(layer_xml_path)
                    root = tree.getroot()
                    layer = Layer(name)
                    layer.init_from_xml(root)
                    self.child_layers.append(layer)
                else:
                    print(f"Layer file not found: {layer_xml_path}")
                    
        print(f"Layer: {self.name}")
        print(f"Prefab Actors: {[actor.name for actor in self.prefab_actors]}")
    
    def get_mesh_paths(self):
        mesh_paths = set()
        for static_mesh in self.static_meshes:
            if static_mesh.mesh_path:
                mesh_paths.add(static_mesh.mesh_path)
                
        for child_layer in self.child_layers:
            child_mesh_paths = child_layer.get_mesh_paths()
            mesh_paths.update(child_mesh_paths)    
        
        return mesh_paths
    
    def get_prefab_paths(self):
        prefab_actor_paths = set()
        for prefab_actor in self.prefab_actors:
            if prefab_actor.prefab_name:
                prefab_actor_paths.add(prefab_actor.prefab_name)
                
        for child_layer in self.child_layers:
            child_prefab_actor_paths = child_layer.get_prefab_paths()
            prefab_actor_paths.update(child_prefab_actor_paths)    
        
        return prefab_actor_paths
    

class Prefab:
    def __init__(self):
        self.name = None
        self.library = None
        self.static_meshes = []
        
    def init_from_xml(self, xml_node):
        self.name = xml_node.get("Name") if "Name" in xml_node.attrib else None
        self.library = xml_node.get("Library") if "Library" in xml_node.attrib else None
        self.static_meshes = []

        # Iterate through child objects
        objects_node = xml_node.find("Objects")
        if objects_node is not None:
            for obj_node in objects_node.findall("Object"):
                obj_type = obj_node.get("Type")
                if obj_type == "GeomEntity":
                    static_mesh = StaticMesh()
                    static_mesh.init_from_geo_xml(obj_node)
                    self.static_meshes.append(static_mesh)
                elif obj_type == "Brush":
                    static_mesh = StaticMesh()
                    static_mesh.init_from_brush_xml(obj_node)
                    self.static_meshes.append(static_mesh)
    
    def get_prefab_name(self):
        return f"{self.library}.{self.name}" if self.library else self.name
    
    def get_mesh_paths(self):
        mesh_paths = set()
        for static_mesh in self.static_meshes:
            if static_mesh.mesh_path:
                mesh_paths.add(static_mesh.mesh_path)
        return mesh_paths
    

class Level:
    def __init__(self):
        self.name = None
        self.prefabs = {}
        self.layers = []
    
    def get_all_mesh_paths(self):
        all_mesh_paths = set()
        all_mesh_paths = set()
        for layer in self.layers:
            layer_mesh_paths = layer.get_mesh_paths()
            all_mesh_paths.update(layer_mesh_paths)
            all_prefab_paths = layer.get_prefab_paths()
            
        for prefab in self.prefabs.values():
            if prefab in all_prefab_paths:
                prefab_mesh_paths = prefab.get_mesh_paths()
                all_mesh_paths.update(prefab_mesh_paths)
        return all_mesh_paths


def parse_prefabs_library(prefabs_library_node):
    prefabs = []
    libraries = []

    # Parse LevelLibrary for prefabs
    level_library_node = prefabs_library_node.find("LevelLibrary")
    if level_library_node is not None:
        for prefab_node in level_library_node.findall("Prefab"):
            prefab = Prefab()
            prefab.init_from_xml(prefab_node)
            prefabs.append(prefab)

    # Parse Library names
    for library_node in prefabs_library_node.findall("Library"):
        library_name = library_node.get("Name")
        if library_name:
            libraries.append(library_name)

    for library_name in libraries:
        library_path = os.path.join(CRY_ENGINE_OUTPUT_FOLDER_ROOT, PREFAB_ROOT_FOLDER, f"{library_name.lower()}.xml")
        if os.path.exists(library_path):
            tree = ET.parse(library_path)
            root = tree.getroot()
            for prefab_node in root.findall("Prefab"):
                prefab = Prefab()
                prefab.init_from_xml(prefab_node)
                prefabs.append(prefab)
        
    prefab_dict = {}        
    for prefab in prefabs:
        prefab_dict[prefab.get_prefab_name()] = prefab
        
    return prefab_dict


def parse_level():
    level = Level()
    level.name = LEVEL_NAME
    # Extract and parse the PrefabsLibrary contents
    file_path = os.path.join(CRY_ENGINE_OUTPUT_FOLDER_ROOT, LEVEL_ROOT_FOLDER, LEVEL_NAME, LEVEL_EDITOR_XML)
    if os.path.exists(file_path):
        tree = ET.parse(file_path)
        root = tree.getroot()
        prefabs_library_node = root.find("PrefabsLibrary")
        if prefabs_library_node is not None:
            level.prefabs = parse_prefabs_library(prefabs_library_node)
            
            # # Print all prefab names
            # for prefab in level.prefabs.keys():
            #     print(prefab)
    
        else:
            print("No <PrefabsLibrary> element found in the XML.")
            
        layers = []
        # Properly locate ChildLayers nodes under ObjectLayers -> RootLayer
        object_layers_node = root.find(".//ObjectLayers")
        if object_layers_node is not None:
            root_layer_nodes = object_layers_node.findall("RootLayer")
            # if root_layer_node is not None:
            #     child_layers_node = root_layer_node.find("ChildLayers")
            #     if child_layers_node is not None:
            for layer_node in root_layer_nodes:
                fullname = layer_node.get("FullName")
                name = layer_node.get("Name")
                
                if name not in LAYER_WHITELIST:
                    print(f"Layer {name} not in whitelist, skipping.")
                    continue
                
                layer_xml_path = os.path.join(CRY_ENGINE_OUTPUT_FOLDER_ROOT, LEVEL_ROOT_FOLDER, LEVEL_NAME, LEVEL_LAYERS_FOLDER, f"{fullname}.lyr")
                if os.path.exists(layer_xml_path):
                    tree = ET.parse(layer_xml_path)
                    root = tree.getroot()
                    layer = Layer(name)
                    layer.init_from_xml(root)
                    layers.append(layer)
                else:
                    print(f"Layer file not found: {layer_xml_path}")
        level.layers = layers
    else:
        print(f"File not found: {file_path}")
    return level


import unreal
editor_level_lib = unreal.EditorLevelLibrary()
level_editor_sub = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
editor_asset_sub = unreal.get_editor_subsystem(unreal.EditorAssetSubsystem)
data_layer_sub = unreal.get_editor_subsystem(unreal.DataLayerEditorSubsystem)

PLACE_HOLDER_SM= "/Engine/BasicShapes/Cube"
place_holder_sm_obj = unreal.EditorAssetLibrary.load_asset(PLACE_HOLDER_SM)

PREFAB_PACKAGE_PATH = "/Game/Old/prefabs"
INPUT_PACKAGE_ROOT = "/Game/Old"

import math

def quaternion_to_euler(quaternion):
    """
    Converts a quaternion (x, y, z, w) to Euler angles (pitch, yaw, roll) in degrees.
    """
    x, y, z, w = quaternion

    # Roll (X-axis rotation)
    sinr_cosp = 2 * (w * x + y * z)
    cosr_cosp = 1 - 2 * (x * x + y * y)
    roll = math.atan2(sinr_cosp, cosr_cosp)

    # Pitch (Y-axis rotation)
    sinp = 2 * (w * y - z * x)
    if abs(sinp) >= 1:
        pitch = math.copysign(math.pi / 2, sinp)  # Use 90 degrees if out of range
    else:
        pitch = math.asin(sinp)

    # Yaw (Z-axis rotation)
    siny_cosp = 2 * (w * z + x * y)
    cosy_cosp = 1 - 2 * (y * y + z * z)
    yaw = math.atan2(siny_cosp, cosy_cosp)

    # Convert radians to degrees
    roll = math.degrees(roll)
    pitch = math.degrees(pitch)
    yaw = math.degrees(yaw)

    return pitch, yaw, roll

def convert_cryengine_to_unreal_rotation(cryengine_rotate):
    """
    Converts CryEngine quaternion rotation to Unreal Engine rotator.
    Assumes the input quaternion is in (w, x, y, z) order.
    
    For example, a CryEngine rotation "0.90630782,0.42261824,0,0"
    represents a 50° rotation about the X axis and should produce
    an Unreal rotator of (Pitch: 50.0, Yaw: 0.0, Roll: 0.0).
    """
    # Parse the quaternion string into floats (expected order: w, x, y, z)
    input_quat = [float(coord) for coord in cryengine_rotate.split(",")]
    
    # Reorder to (x, y, z, w) for our conversion formulas
    q = [input_quat[1], input_quat[2], input_quat[3], input_quat[0]]
    # Compute Euler angles using the standard conversion:
    # This returns (pitch, yaw, roll) where roll is rotation about X-axis.
    computed_pitch, computed_yaw, computed_roll = quaternion_to_euler(q)
    # Remap to Unreal's Rotator:
    # Unreal expects (Pitch, Yaw, Roll), but we want the CryEngine X-rotation
    # (computed as roll) to map to Unreal's Pitch.
    unreal_pitch = computed_roll     # X-axis rotation becomes Pitch
    unreal_yaw   = -1.0*computed_pitch        # Y-axis rotation remains Yaw
    unreal_roll  = -1.0*computed_yaw  # Z-axis rotation becomes Roll
    
    return unreal_pitch, unreal_yaw, unreal_roll

def recreate_level_in_unreal(level_data):
    with unreal.ScopedSlowTask(len(level_data.layers), "Importing Layers...") as slow_task:
        # display the dialog
        slow_task.make_dialog(True)
        for layer in level_data.layers:
            if slow_task.should_cancel():
                break
            slow_task.enter_progress_frame(1, "Importing Layer {}".format(layer.name))
            recreate_layer_in_unreal(layer)

def recreate_layer_in_unreal(layer, parent_layer=None):
    data_layer_instance = data_layer_sub.get_data_layer_from_label(layer.name)
    if not data_layer_instance:
        data_layer_create_param = unreal.DataLayerCreationParameters()
        data_layer_create_param.data_layer_asset = None
        data_layer_create_param.is_private = True
        
        data_layer_instance = data_layer_sub.create_data_layer_instance(data_layer_create_param)
        result = unreal.PythonFunctionLibrary().set_data_layer_short_name(data_layer_instance, layer.name)
    
    if parent_layer:
        data_layer_sub.set_parent_data_layer(data_layer_instance, parent_layer)
    
    spawned_actors = []
    # Iterate through prefab actors and static meshes
    for prefab_actor in layer.prefab_actors:
        prefab_actor = spawn_prefab_actor(prefab_actor)
        spawned_actors.append(prefab_actor)
        
    for static_mesh in layer.static_meshes:
        static_mesh_actor = spawn_static_mesh(static_mesh)
        spawned_actors.append(static_mesh_actor)
        
    result = data_layer_sub.add_actors_to_data_layer(spawned_actors, data_layer_instance)
        
    for layer in layer.child_layers:
        recreate_layer_in_unreal(layer, data_layer_instance)
        
def spawn_actor_common(actor, actor_class):
    pos_str = actor.pos
    pos = [float(coord)*100.0 for coord in pos_str.split(",")]
    rotate = convert_cryengine_to_unreal_rotation(actor.rotate)
    scale_str = actor.scale
    scale = [float(coord) for coord in scale_str.split(",")]
    
    mesh_actor = editor_level_lib.spawn_actor_from_class(actor_class, unreal.Vector(pos[0], -1.0*pos[1], pos[2]))
    mesh_actor.set_actor_rotation(unreal.Rotator(rotate[0], rotate[1], rotate[2]), False)
    mesh_actor.set_actor_scale3d(unreal.Vector(scale[0], scale[1], scale[2]))
    
    return mesh_actor
        
def spawn_static_mesh(static_mesh):
    mesh_actor = spawn_actor_common(static_mesh, unreal.StaticMeshActor)
    mesh_actor.set_actor_label(static_mesh.name)
    mesh_component = mesh_actor.get_component_by_class(unreal.StaticMeshComponent)
    mesh_package_path = INPUT_PACKAGE_ROOT + '/' + static_mesh.mesh_path.replace('.cgf', '')
    if editor_asset_sub.does_asset_exist(mesh_package_path):
        static_mesh_obj = editor_asset_sub.load_asset(mesh_package_path)
        mesh_component.set_static_mesh(static_mesh_obj)
    else:
        mesh_component.set_static_mesh(place_holder_sm_obj)
        
    return mesh_actor
    
def spawn_prefab_actor(prefab_actor):
    prefab_path = prefab_actor.prefab_name.replace('.', '/')
    prefab_path = PREFAB_PACKAGE_PATH + "/" + prefab_path
    
    level_instance_actor = spawn_actor_common(prefab_actor, unreal.LevelInstance)
    world_asset = unreal.EditorAssetLibrary.load_asset(prefab_path)
    level_instance_actor.set_editor_property("world_asset", world_asset)
    level_instance_actor.set_actor_label(prefab_actor.name)
    
    return level_instance_actor

def generated_all_prefabs(level_data: Level):
    for prefab in level_data.prefabs.values():
        create_level_prefab(prefab)

def create_level_prefab(prefab: Prefab):
    print(prefab.get_prefab_name())
    new_level_path = prefab.get_prefab_name().replace('.', '/')
    new_level_path = PREFAB_PACKAGE_PATH + "/" + new_level_path
    print(new_level_path)
    level_editor_sub.new_level(new_level_path, False)
    for static_mesh in prefab.static_meshes:
        spawn_static_mesh(static_mesh)
    level_editor_sub.save_current_level()

if __name__ == "__main__":
    level_data = parse_level()
    # generated_all_prefabs(level_data)
    recreate_level_in_unreal(level_data)
    
    # all_mesh_paths = level_data.get_all_mesh_paths()
    # print(all_mesh_paths)
    # for mesh_path in all_mesh_paths:
    #     print(mesh_path)