import os
from qgis.core import (
    QgsRasterLayer,
    QgsProject
)

# Set the base directory
working_dir = None # Example: "C:/Users/username/Documents/DEM_Files"
file_end = "" #Example: "_dem.tif"

if working_dir is None or working_dir == '':
    print("Please make sure to set the working_dir variable to the directory containing the DEM files.")
    exit()

def add_raster_layers(directory, file_end):
    """ Recursively add all _dem.tif files as raster layers in QGIS """
    for root, dirs, files in os.walk(directory):
        # Skip the Tar_files directory
        if 'Tar_files' in root:
            continue
        
        for file in files:
            if file.endswith(file_end):
                raster_path = os.path.join(root, file)
                layer_name = os.path.splitext(file)[0]
                raster_layer = QgsRasterLayer(raster_path, layer_name, "gdal")
                
                if raster_layer.isValid():
                    QgsProject.instance().addMapLayer(raster_layer)
                    print(f"Added: {raster_path}")
                else:
                    print(f"Failed to load: {raster_path}")

# Run the function to add raster layers
add_raster_layers(working_dir, file_end)

print("All valid raster layers have been added to QGIS.")
