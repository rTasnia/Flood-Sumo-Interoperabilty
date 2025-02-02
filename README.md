# Flood-Sumo-interoperability


## Flood Risk Zones Analysis
### Introduction

Flooding significantly impacts transportation infrastructure, yet research on how flood levels affect road networks, especially during dynamic flooding events, is limited. Smart cities hold the potential to leverage digital data on travel demand, infrastructure, and water levels to improve flood management and address social inequities (especially since vulnerable populations such as people without cars are more at risk during flooding events). However, traditional traffic simulation models miss out on key details such as terrain, landscape types, and elevation, hindering accurate assessments of infrastructure interdependencies during flooding. Past studies highlight the necessity of integrated urban planning to manage interdependencies effectively. Our research focuses on modeling the interdependencies between water and transportation infrastructures, assessing flood risks and their impacts on infrastructure. We develop an interoperable digital twin framework that combines road networks with rising water level simulations and encourages rerouting under flash floods to assess flood impacts, focusing on Hyde County, NC (rural area) and Wilmington, NC (urban area). Our findings indicate that (a) open-source tools can capture the impacts of rising sea levels in identifying submerged roads, which show up as transverse or longitudinal lane closure in traffic simulators, enabling dynamic rerouting decisions, and (b) interoperable flood and water infrastructure models can enable prompt identification of at-risk roads and mitigate flash flooding events. Our findings can help facilitate better disaster preparedness and response strategies.
. 
## Contributors

| Name       | Affiliation       | Email               |
|------------|-------------------|---------------------|
| Rifa Tasnia  | North Carolina Agricultural and Technical State University | tasnia1642@gmail.com |
| Venktesh Pandey | North Carolina Agricultural and Technical State University | vpandey@ncat.edu |
## License
[License](LICENSE)

## Part 1
### Instructions for download part 1:Height Above Nearest Drainage (Hand) data

Accessing the StoryMap: I started by visiting the ArcGIS StoryMap page, which provided detailed insights and resources on flood mapping using HAND data.

Setting Location: Navigate the interactive maps available on StoryMap to focus on the region of interest. By setting the location, one can view relevant data and ensure downloading the correct dataset for the specific area.

Link: https://storymaps.arcgis.com/stories/fcd5cba6104645349f59e504042bacd6

Downloading the Data: On the ASF DAAC Vertex platform, I entered my location details to search for and download HAND data in TIFF format. This data was used in my project for analyzing flood-prone areas.

Data Download link: https://asf-daac.maps.arcgis.com/apps/mapviewer/index.html?webmap=6b82a2e4ccd343d5ba73dc04d386e4ee

### Flood impact visualization
The primary script provides tools for analyzing road networks in Wilmington, North Carolina, with a focus on assessing flood risk based on elevation data. The components include:

+ Installation of Dependencies:
-- Installs necessary libraries including GDAL, rasterio, osmnx, mapclassify, folium, and matplotlib.
  
+ Loading and Plotting Road Network:
-- Loads the road network for Wilmington using OpenStreetMap data through the osmnx library.
-- Visualizes the network with nodes and edges.
-- Elevation and Flood Risk Analysis:

+ Adds elevation data to the road network nodes using the Copernicus Global 30-m DEM.
-- Classifies road segments based on node elevation into three categories:Flooded (below a threshold of 2 meters),
-- Prone (elevation between 2 and 12 meters), and Safe (above 12 meters).
-- Color-codes nodes and road segments to easily visualize flood risk.
-- Extracts specific road segments based on u, v values and their associated osmids.

+ Plots the classified nodes over the road network.
-- Integrates TIFF elevation data as a background for enhanced visualization.
-- Provides an interactive map using folium to explore flood risk classifications in a web-based format.
-- Exporting Results:

+ Saves the interactive map as an HTML file for easy sharing and exploration.

## Installation and Requirements
Run the command `pip install -r requirements.txt`.


  ### Instructions for download part 2: Network Data

  https://www.openstreetmap.org/#map=10/35.3560/-76.1874&layers=TG

### Road Network Analysis and Flood Risk-Based Travel Demand Modeling

## Overview

This repository contains scripts and datasets used for extracting road network data, modeling travel demand, and generating TNTP trip and network files with adjustments based on flood risk. The analysis integrates multiple geospatial and transportation modeling tools, including OSM2GMNS, GRID2DEMAND, and TNTP file generation scripts.

## Road Network Data Extraction and Analysis

+ Extracts road network data using osm2gmns.
+ Processes link, node, and POI datasets and converts them into GeoDataFrames.
+ Calculates road attributes (lanes, type, speed, travel time, width).
+ Integrates elevation data from a DEM to compute road grades.
+ Saves processed data in UTF-8 encoded CSV files.

## Automated Grid-Based Travel Demand Modeling and Zone Analysis

+ Uses GRID2DEMAND (version 0.3.9) for transportation demand modeling.
+ Generates Traffic Analysis Zones (TAZs) based on network partitioning.
+ Synchronizes geometries between nodes, POIs, and zones for consistency.
+ Computes POI trip rates, production, and attraction estimates per node.
+ Generates a zone-to-zone distance matrix and applies a gravity model.
+ Outputs demand tables and zone distance matrices as CSV files.
+ Implements Haversine formula to find the closest node to a zone centroid.

## Automated TNTP Trip and Network File Generation with Flood Risk Adjustments
### TNTP File Generation

File name: `Generate Trips, net file.ipynb`.

+ Generates TNTP format trip and network files based on demand and flood risk.
+ Adjusts demand using a reduction factor and writes the adjusted demand in TNTP format.
+ Modifies network file capacity based on flood risk factors.
+ Handles multiple parameter combinations for batch processing.
+ Outputs files with unique names based on parameters for easy scenario analysis.

### Export flooded OSM ids in SUMO
The second set of scripts export the flooded OSM ids as CSVs, which are then read into SUMO traffic simulator for modeling appropriate lane closures.


## Part 2
## SUMO Simulation with Flooded Lanes
The Python script is designed to simulate vehicle rerouting in SUMO (Simulation of Urban MObility) by closing specific lanes based on flood risks. The script reads a CSV file containing OSM (OpenStreetMap) IDs of road segments that are at risk of flooding, closes those lanes during the simulation, and reroutes vehicles to available adjacent lanes.

### Features:
- Dynamic Lane Closure: Lanes corresponding to flooded OSM IDs are closed after a specified number of steps.
- Vehicle Rerouting: Vehicles on closed lanes are rerouted to adjacent lanes (if available).
- Trip Information Parsing: Trip data before and after lane closures is collected and saved into CSV files for further analysis.
- Error Handling: The script checks for the presence of necessary files (SUMO configuration and CSV) and handles potential errors gracefully.

### Usage:
- Ensure that the SUMO_HOME environment variable is set correctly.
- Modify the script to specify the correct path to your SUMO configuration file and the CSV file containing the OSM IDs of flooded lanes.
- Run the script either in GUI mode or in command-line mode using the --nogui option.
### Requirements:
- SUMO: The script interacts with SUMO through TraCI (Traffic Control Interface). Ensure SUMO is installed and properly configured.
- CSV Data: A CSV file containing OSM IDs is required to specify which lanes should be closed during the simulation.
- Python Libraries: The script uses pandas for data processing, and optparse, sumolib, traci for SUMO interaction.

### How It Works:
- The simulation starts with normal traffic flow.
- After a specified number of steps (e.g., 1000), lanes corresponding to OSM IDs in the CSV file are closed.
- Vehicles on closed lanes are rerouted to adjacent lanes where possible.
- Trip data before and after lane closure is collected and saved for analysis.

### Output:
- tripinfo_before_closure.csv: Contains trip information before lanes are closed.
- tripinfo_AFTER_flood.csv: Contains trip information after the lanes are closed.
- tripinfo.xml: Raw trip data generated by SUMO.
- vehStatistic.xml: Detailed vehicle statistics generated by SUMO.


### Acknowledgments
We acknowledge the support provided by the Connected Communities for Smart Mobility Towards Accessible & Resilient Transportation for Equitably Reducing Congestion (C2SMARTER) Center. This work was supported under Award #69A3551747124, with New York University as the lead institution and North Carolina A&T State University as the project lead.


