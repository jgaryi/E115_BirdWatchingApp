
# Import libraries
import ee
import folium
import geemap
import matplotlib.pyplot as plt

# Initialize the Earth Engine API
ee.Authenticate()
ee.Initialize(project = "class2-449500")

# Load the protected area geometry
yanachaga_chemillen_geometry = ee.FeatureCollection("projects/e115-jgarciayi/assets/YanachagaChemillen").geometry().dissolve(maxError=1)

# Load the previous location of birds
andigena_points = ee.FeatureCollection("projects/e115-jgarciayi/assets/CoordinatesAndigenaOnlyNP")
aulacorhynchus_points = ee.FeatureCollection("projects/e115-jgarciayi/assets/CoordinatesAulacorhynchusOnlyNP")
doliornis_points = ee.FeatureCollection("projects/e115-jgarciayi/assets/CoordinatesDoliornisOnlyNP")
gallinago_points = ee.FeatureCollection("projects/e115-jgarciayi/assets/CoordinatesGallinagoOnlyNP")
hapalopsittaca_points = ee.FeatureCollection("projects/e115-jgarciayi/assets/CoordinatesHapalopsittacaOnlyNP")
pionus_points = ee.FeatureCollection("projects/e115-jgarciayi/assets/CoordinatesPionusTumultuosusOnlyNP")
pipile_points = ee.FeatureCollection("projects/e115-jgarciayi/assets/CoordinatesPipileCumanensisOnlyNP")
rupicola_points = ee.FeatureCollection("projects/e115-jgarciayi/assets/CoordinatesRupicolaPeruvianusOnlyNP")

# Load the Hansen Global Forest Change dataset
forest_change_image = ee.Image("UMD/hansen/global_forest_change_2023_v1_11").select(['lossyear']).clip(yanachaga_chemillen_geometry)

# Load the ESA WorldCover dataset (2021) correctly
landcover = ee.ImageCollection("ESA/WorldCover/v100").first().select("Map").clip(yanachaga_chemillen_geometry)

# Define visualization parameters
landcover_vis = {
    'min': 10,
    'max': 100,
    'palette': ['006400', 'ffbb22', 'ffff4c', 'f096ff', 'fa0000', 'b4b4b4', 'f0f0f0']
}

# Define the years of interest
years_of_interest = list(range(2001, 2024))

# Function to calculate deforested area per year
def calc_deforestation(year):
    loss_year_mask = forest_change_image.eq(year - 2000).selfMask()
    pixel_area_image = loss_year_mask.multiply(ee.Image.pixelArea())
    area_stats = pixel_area_image.reduceRegion(
        reducer=ee.Reducer.sum(),
        geometry=yanachaga_chemillen_geometry,
        scale=200,
        maxPixels=1e14
    )
    return ee.Number(area_stats.get("lossyear")).multiply(0.0001).getInfo()  # Convert to hectares

# Compute deforestation area per year
deforestation_areas = [calc_deforestation(year) for year in years_of_interest]

# Compute cumulative deforestation
cumulative_deforestation = [sum(deforestation_areas[:i+1]) for i in range(len(deforestation_areas))]

# Graph 1: Annual deforestation (hectares per year)
plt.figure(figsize=(10, 5))
plt.plot(years_of_interest, deforestation_areas, marker='o', linestyle='-', color='green', label="Annual Deforestation (ha)")
plt.xlabel("Year")
plt.ylabel("Deforestation Area (hectares)")
plt.title("Annual Deforestation Over the Years inside the National Park")

# Set x-ticks to display all years
plt.xticks(years_of_interest, rotation=45)

# Remove both horizontal and vertical gridlines
plt.grid(False)

# Legend
plt.legend()
plt.show()

# Graph 2: Cumulative deforestation (hectares)
plt.figure(figsize=(10, 5))
plt.plot(years_of_interest, cumulative_deforestation, marker='s', linestyle='--', color='b', label="Cumulative Deforestation (ha)")
plt.xlabel("Year")
plt.ylabel("Cumulative Deforestation Area (hectares)")
plt.title("Cumulative Deforestation Over the Years inside the National Park")

# Set x-ticks to display all years
plt.xticks(years_of_interest, rotation=45)

# Remove both horizontal and vertical gridlines
plt.grid(False)

# Legend
plt.legend()
plt.show()

# Visualize results using geemap
Map = geemap.Map()
Map.centerObject(yanachaga_chemillen_geometry, 10)

# Add layers to the map
Map.addLayer(yanachaga_chemillen_geometry, {'color': 'white'}, 'Yanachaga Chemillen National Park')
Map.addLayer(rupicola_points, {"color": "blue"}, "Previous Rupicola peruvianus Locations")

# Add deforestation layer to the map
Map.addLayer(forest_change_image, {'bands': ['lossyear'], 'palette': ['red']}, 'Forest Loss')

# Display the map
Map