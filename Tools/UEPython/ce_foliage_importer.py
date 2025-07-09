import xml.etree.ElementTree as ET
from typing import List, Dict
import os

class VegetationInstance:
    def __init__(self):
        self.position = (0.0, 0.0, 0.0)  # X, Y, Z
        self.scale = 1.0
        self.angle = 0.0
        self.brightness = 76  # Default brightness
        
    def __repr__(self):
        return f"VegetationInstance(pos={self.position}, scale={self.scale}, angle={self.angle})"

class Vegetation:
    def __init__(self):
        self.object_path = ""  # The Object attribute (CGF file path)
        self.category = ""     # The Category attribute
        self.instances = []    # List of VegetationInstance objects
        
        # Additional properties that might be useful
        self.id = 0
        self.guid = ""
        self.size = 1.0
        self.size_var = 0.25
        self.density = 10
        
    def __repr__(self):
        return f"Vegetation(object={self.object_path}, category={self.category}, instances={len(self.instances)})"

def parse_veg_file(file_path: str) -> Dict[str, List[Vegetation]]:
    """
    Parse a .veg file and return a dictionary with category as key and list of Vegetation objects as value
    
    Args:
        file_path: Path to the .veg file
        
    Returns:
        Dictionary mapping category names to lists of Vegetation objects
    """
    vegetation_map = {}
    
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        
        # Find all VegetationObject elements
        vegetation_objects = root.findall("VegetationObject")
        
        for veg_obj in vegetation_objects:
            vegetation = Vegetation()
            
            # Parse main attributes
            vegetation.object_path = veg_obj.attrib.get("Object", "")
            vegetation.category = veg_obj.attrib.get("Category", "")
            vegetation.id = int(veg_obj.attrib.get("Id", "0"))
            vegetation.guid = veg_obj.attrib.get("GUID", "")
            vegetation.size = float(veg_obj.attrib.get("Size", "1.0"))
            vegetation.size_var = float(veg_obj.attrib.get("SizeVar", "0.25"))
            vegetation.density = float(veg_obj.attrib.get("Density", "10"))
            
            # Parse instances
            instances_elem = veg_obj.find("Instances")
            if instances_elem is not None:
                for instance_elem in instances_elem.findall("Instance"):
                    instance = VegetationInstance()
                    
                    # Parse position (format: "X,Y,Z")
                    pos_str = instance_elem.attrib.get("Pos", "0,0,0")
                    pos_parts = pos_str.split(",")
                    if len(pos_parts) == 3:
                        instance.position = (
                            float(pos_parts[0].strip()),
                            float(pos_parts[1].strip()),
                            float(pos_parts[2].strip())
                        )
                    
                    # Parse other attributes
                    instance.scale = float(instance_elem.attrib.get("Scale", "1.0"))
                    instance.angle = float(instance_elem.attrib.get("Angle", "0.0"))
                    instance.brightness = int(instance_elem.attrib.get("Brightness", "76"))
                    
                    vegetation.instances.append(instance)
            
            # Add to map by category
            if vegetation.category not in vegetation_map:
                vegetation_map[vegetation.category] = []
            vegetation_map[vegetation.category].append(vegetation)
            
    except ET.ParseError as e:
        print(f"Error parsing {file_path}: {e}")
    except Exception as e:
        print(f"Unexpected error parsing {file_path}: {e}")
    
    return vegetation_map

def print_vegetation_summary(vegetation_map: Dict[str, List[Vegetation]]):
    """Print a summary of parsed vegetation data"""
    print(f"Found {len(vegetation_map)} vegetation categories:")
    
    obj_list = []
    for category, veg_list in vegetation_map.items():
        print(f"\nCategory: {category}")
        for i, veg in enumerate(veg_list):
            # print(f"  {i+1}. Object: {veg.object_path}")
            # print(f"      Instances: {len(veg.instances)}")
            # print(f"      ID: {veg.id}, Size: {veg.size}, Density: {veg.density}")
            
            # # Show first few instances as examples
            # if veg.instances:
            #     print(f"      Sample instances:")
            #     for j, instance in enumerate(veg.instances[:3]):  # Show first 3
            #         print(f"        {j+1}. Pos: {instance.position}, Scale: {instance.scale}, Angle: {instance.angle}")
            #     if len(veg.instances) > 3:
            #         print(f"        ... and {len(veg.instances) - 3} more")
            obj_list.append(veg.object_path)
    
    with open("vegetation_objects.txt", "w") as f:
        f.write("\n".join(obj_list))
        

def create_instance_static_mesh_actor(name, veg_list: List[Vegetation]):
    import unreal
    # Create a new empty Actor in the level
    actor_location = unreal.Vector(0, 0, 0)
    actor = unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.Actor, actor_location)
    actor.set_actor_label(f"VegImport_{name}")
    
    so_subsystem = unreal.get_engine_subsystem(unreal.SubobjectDataSubsystem)  
    root_sub_object = so_subsystem.k2_gather_subobject_data_for_instance(actor)[0]
    
    for veg in veg_list:
        new_handle, fail_reason = so_subsystem.add_new_subobject(unreal.AddNewSubobjectParams(
            parent_handle=root_sub_object,
            new_class=unreal.InstancedStaticMeshComponent,
        ))
        
        print(veg.object_path)
        component_name = veg.object_path.split("/")[-1]  # Use the last part of the path as name
        component_name = component_name.replace(".cgf", "")  
        so_subsystem.rename_subobject(new_handle, component_name)  # Use the last part of the path as name
        ism_component = actor.get_components_by_class(unreal.InstancedStaticMeshComponent)[-1]  # Get the last added component

        package_name = f"/Game/Old/{veg.object_path.replace('.cgf', '')}"
        if not unreal.EditorAssetLibrary.does_asset_exist(package_name):
            print(f"Asset does not exist: {package_name}")
            continue
        
        ism_component.set_editor_property("static_mesh", unreal.EditorAssetLibrary.load_asset(package_name))
        
        transforms = []
        for instance in veg.instances:
            # Create a transform for the instance
            transform = unreal.Transform(
                location=unreal.Vector(instance.position[0] * 100.0, instance.position[1] * -100.0, instance.position[2] * 100.0),  # Convert to Unreal units (cm)
                rotation=unreal.Rotator(0, 0, instance.angle * 60 * unreal.MathLibrary.random_float()),  # Assuming angle is in degrees
                scale=unreal.Vector(instance.scale, instance.scale, instance.scale)
            )
            transforms.append(transform)
        ism_component.add_instances(transforms, False)


def import_veg_into_unreal(veg_map: Dict[str, List[Vegetation]]):
    """
    Import vegetation data into Unreal Engine.
    
    Args:
        veg_map: Dictionary mapping category names to lists of Vegetation objects
    """
    for category, veg_list in veg_map.items():
        print(f"Importing category: {category}")
        create_instance_static_mesh_actor(category, veg_list)

# Example usage
if __name__ == "__main__":
    # Test with the provided file
    # test_file = r"d:\temp\rataja\data\levels\rataje\test.veg"
    test_file = r"D:\temp\ceoutput\ratajeveg.veg"
    
    if os.path.exists(test_file):
        vegetation_data = parse_veg_file(test_file)
    #     print_vegetation_summary(vegetation_data)
    # else:
    #     print(f"Test file not found: {test_file}")

        import_veg_into_unreal(vegetation_data)