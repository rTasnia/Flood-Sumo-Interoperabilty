# Flood-Sumo-interoperability


The goal of this project is to automate the integration of flood information in traffic simulation models (towards digital twin interoperability of the flood and transport network). 

## Downloaded and Used HAND Data for Flood Risk Analysis
To use HAND data for my flood risk analysis, I followed these steps:

Accessing the StoryMap
We started by visiting the ArcGIS StoryMap page, which provided detailed insights and resources on flood mapping using HAND data.
Link: ArcGIS StoryMap.

Setting Location
We navigated the interactive maps available in the StoryMap to focus on my region of interest. By setting the location, I was able to view relevant data and ensure that I was downloading the correct dataset for my specific area.

Locating the Download Link
We searched for sections in the StoryMap that referenced HAND data or provided external links to download GIS datasets. Where direct links were not available, I visited the ASF DAAC platform, which hosts various geospatial data, including HAND:
Link: ASF DAAC Vertex.

Downloading the Data
On the ASF DAAC Vertex platform, I entered my location details to search for and download HAND data in TIFF format. This data was used in my project for analyzing flood-prone areas.

## Flood impact visualization
The primary script provides tools for analyzing road networks in Wilmington, North Carolina, with a focus on assessing flood risk based on elevation data. The components include:

+ Installation of Dependencies:
-- Installs necessary libraries including GDAL, rasterio, osmnx, mapclassify, folium, and matplotlib.
  

+ Loading and Plotting Road Network:
-- Loads the road network for Wilmington using OpenStreetMap data through the osmnx library.
-- Visualizes the network with nodes and edges.
-- Elevation and Flood Risk Analysis:

+ Adds elevation data to the road network nodes using the Copernicus Global 30-m DEM.
-- Classifies road segments based on node elevation into three categories:Flooded (below a threshold of 2 meters),
Prone (elevation between 2 and 12 meters), and
Safe (above 12 meters).
Color-codes nodes and road segments to easily visualize flood risk.
Extracts specific road segments based on u, v values and their associated osmids.

+ Plots the classified nodes over the road network.
-- Integrates TIFF elevation data as a background for enhanced visualization.
-- Provides an interactive map using folium to explore flood risk classifications in a web-based format.
-- Exporting Results:

+ Saves the interactive map as an HTML file for easy sharing and exploration.

## Export flooded OSM ids in SUMO
The second set of scripts export the flooded OSM ids as CSVs, which are then read into SUMO traffic simulator for modeling appropriate lane closures.
