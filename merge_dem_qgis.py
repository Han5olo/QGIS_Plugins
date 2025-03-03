import os
import glob
from qgis.core import QgsProject, QgsRasterLayer
from qgis import processing

# Set the base directory (same as script location)
base_dir = os.path.dirname(os.path.abspath(__file__))

# Get all _dem.tif files (excluding 'Tar_files' directory)
dem_files = []
for root, dirs, files in os.walk(base_dir):
    if "Tar_files" in root:
        continue  # Skip Tar_files
    for file in files:
        if file.endswith("_dem.tif"):
            dem_files.append(os.path.join(root, file))

# Ensure we have files to merge
if len(dem_files) < 2:
    print("Not enough DEM files found to merge.")
else:
    output_merged = os.path.join(base_dir, "merged_dem.tif")

    # Run GDAL merge
    processing.run("gdal:merge", {
        'INPUT': dem_files,
        'PCT': False,
        'SEPARATE': False,
        'NODATA_INPUT': None,
        'NODATA_OUTPUT': None,
        'OPTIONS': '',
        'DATA_TYPE': 0,
        'OUTPUT': output_merged
    })

    # Load the merged raster into QGIS
    merged_layer = QgsRasterLayer(output_merged, "Merged DEM", "gdal")
    if merged_layer.isValid():
        QgsProject.instance().addMapLayer(merged_layer)
        print(f"Merged DEM added: {output_merged}")
    else:
        print(f"Failed to load merged DEM: {output_merged}")

print("Raster merging complete.")
