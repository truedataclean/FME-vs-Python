import geopandas as gpd
import os

# Set the path to the folder containing shapefiles
folder_path = "C:\\Temp\\Topo\\TopoBDE00-pre-reblocker\\"

# Read all shapefiles in the folder
shapefiles = [gpd.read_file(os.path.join(folder_path, file)) for file in os.listdir(folder_path) if file.endswith('.shp')]

# Set the path to the second shapefile
shapefile_path_2 = "C:\\Temp\\Topo\\lds-nz-150k-tile-index-SHP\\nz-150k-tile-index.shp"

# Read the second shapefile
shapefile_2 = gpd.read_file(shapefile_path_2)

# Add a 1-meter buffer to shapefile_2
shapefile_2['geometry'] = shapefile_2.geometry.buffer(1)

# Process each shapefile in the folder
for shapefile_path in os.listdir(folder_path):
    if shapefile_path.endswith('.shp'):
        shapefile = gpd.read_file(os.path.join(folder_path, shapefile_path))
        
        # Print the fields in the shapefile
        print(shapefile_path)

        # Compare geometries and filter out touched geometries
        touched_geometries = shapefile[shapefile.geometry.apply(lambda geom1: any(geom1.overlaps(geom2) or geom1.touches(geom2) for geom2 in shapefile_2.geometry))]

        # Save the results to a new shapefile with a name derived from the input file name
        input_file_name = os.path.basename(shapefile_path).replace('.shp', '')
        output_path = f"C:\\Temp\\Topo\\outs\\{input_file_name}_f.shp"
        touched_geometries.to_file(output_path)


