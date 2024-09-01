# C2SMARTER-Project.

The goal of this project is to automate the integration of flood information in traffic simulation models (towards digital twin interoperability of the flood and transport network). 

## Flood impact visualization
The primary script provides tools for analyzing road networks in Wilmington, North Carolina, with a focus on assessing flood risk based on elevation data. The components include:

+ Installation of Dependencies:
-- Installs necessary libraries including GDAL, rasterio, osmnx, mapclassify, folium, and matplotlib.

+ Loading and Plotting Road Network:
-- Loads the road network for Wilmington using OpenStreetMap data through the osmnx library.
-- Visualizes the network with nodes and edges.
-- Elevation and Flood Risk Analysis:

+ Adds elevation data to the road network nodes using a USGS raster file.
-- Classifies nodes based on their elevation into three categories: flooded, prone, and safe.
-- Assigns colors to nodes based on their flood risk status.
-- Visualization:

+ Plots the classified nodes over the road network.
-- Integrates TIFF elevation data as a background for enhanced visualization.
-- Provides an interactive map using folium to explore the flood risk classification in a web-based format.
-- Exporting Results:

+ Saves the interactive map as an HTML file for easy sharing and exploration.

## Export flooded OSM ids in SUMO
The second set of scripts export the flooded OSM ids as CSVs, which are then read into SUMO traffic simulator for modeling appropriate lane closures.
