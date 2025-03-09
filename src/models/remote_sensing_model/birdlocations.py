
# Import libraries
import ee
import folium
import geemap

# Initialize the Earth Engine API
ee.Authenticate(force=True)
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

# Dictionary to connect bird names to layers
bird_layers = {
    "Andigena hypoglauca": andigena_points,
    "Aulacorhynchus coeruleicinctis": aulacorhynchus_points,
    "Doliornis sclateri": doliornis_points,
    "Gallinago jamesoni": gallinago_points,
    "Hapalopsittaca melanotis": hapalopsittaca_points,
    "Pionus tumultuosus": pionus_points,
    "Pipile cumanensis": pipile_points,
    "Rupicola peruvianus": rupicola_points
}

# Ask the user for the bird name
bird_name = input("Enter the bird species name (e.g., Andigena hypoglauca): ")

# Visualize results using geemap
Map = geemap.Map()
Map.centerObject(yanachaga_chemillen_geometry, 10)

# Add the protected area to the map
Map.addLayer(yanachaga_chemillen_geometry, {'color': 'white'}, 'Yanachaga Chemillen National Park')

# Add the selected bird's layer if it exists
if bird_name in bird_layers:
    Map.addLayer(bird_layers[bird_name], {"color": "red"}, f"Previous {bird_name} Locations")
    print(f"Displaying {bird_name} locations.")
else:
    print("Aulacorhynchus coeruleicinctis")

# Display the map
Map